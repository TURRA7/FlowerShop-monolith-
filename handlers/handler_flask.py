from flask import Flask, render_template, request, \
    redirect, url_for, flash
from flask_limiter import Limiter
from flask.views import View
from flask_login import login_user, login_required, logout_user
from flask_wtf.csrf import CSRFProtect
from flask_sslify import SSLify

import os
import pytz
from datetime import datetime
from typing import Union, Type
from werkzeug.utils import secure_filename

from pagination_create.paginate_flask import WorkingWithPagination
from cute_form.form_create import DeleteItemsForm, AdminLoginForm, \
    AddItemForm, AddArticleForm, DeleteArticleForm
from database_create.FDataBase import DeleteItems, UserAdmin, Item, Article, db
from authorization.auth import check_auth, login_manager
from toolkits.toolkit import CheckingText, CheckingNumber
from content_flask import cont_error, cont_info

import logging
from logging.handlers import RotatingFileHandler


# Создание экземпляра приложения
app = Flask(__name__)
app.config.from_pyfile('config.py')
# Инициализация базы данных
db.init_app(app)
# Создание экземпляра класса лимитера
limiter = Limiter(app)
# Инициализация всех запросов Flask-приложению через HTTPS
sslify = SSLify(app)
# Инициализация логин менеджера
login_manager.init_app(app)
# Инициализация csrf токена
csrf = CSRFProtect(app)
# Создание логгера
logger = logging.getLogger('log_handlers.log')
logger.setLevel(logging.DEBUG)
# Создание обработчика консоли и установка уровеня отладки
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Создание форматтера
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Добавить форматтер в ch
ch.setFormatter(formatter)
# Добавлении ротации логов
file_handler = RotatingFileHandler('log_handlers.log',
                                   maxBytes=1024*1024,
                                   backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# Добавить ch в логгер, создание ротации
logger.addHandler(ch)
logger.addHandler(file_handler)


@login_manager.user_loader
def load_user(user_id):
    '''
    Обработчик используется для загрузки объекта пользователя на основе
    идентификатора пользователя, который обычно хранится в сессии.
    '''
    limiter.logger.info('Входящий запрос: %s %s', request.method, request.path)
    return UserAdmin.query.get(int(user_id))


class WorkingWithHandlers(View):
    '''
    Базовый (родительский) класс, для работы с обработчиками.
    '''

    init_every_request = False
    decorators = [limiter.limit("100 per minute")]
    methods = ["GET", "POST", "PUT", "DELETE"]

    def __init__(self):
        pass

    def dispatch_request(self):
        pass


class HandlersItem(WorkingWithHandlers):
    '''
    Класс обрабатывает страницы каталога, а так же новостей.
    '''

    def __init__(self, name_page: str, number: int, amount_item: int,
                 table_db: Union[Type[Item], Type[Article]],
                 name_id: str, method_pag: str):
        '''
        :param name_page: Название страницы.
        :param number: Категория товаров (в каталоге).
        :param amount_item: Количество айтемов на странице.
        :param table_db: Таблица (её название).
        :param name_id: Тип айтема на странице (товар/новость).
        :param method_pag: метод, при котором передаётся либо пагинация,
        либо айтемы.
        :param html_path: Название шаблона html(полный путь).
        '''
        super().__init__()
        self.name_page = name_page
        self.number = number
        self.amount_item = amount_item
        self.table_db = table_db
        self.name_id = name_id
        self.method_pag = method_pag
        if self.method_pag == "catalog":
            self.html_path = f"catalog/{self.name_page}.html"
        if self.method_pag == "news":
            self.html_path = f"news/{self.name_page}.html"

    def dispatch_request(self):
        """
        Метод реализует обработичик и через пагинацию,
        выводит товары на страницу.
        """

        logger.info('Входящий запрос: %s выполнен!', self.name_page)
        pag = WorkingWithPagination(self.amount_item, self.table_db)

        if self.method_pag == "news":
            delete_form = DeleteArticleForm()
        elif self.method_pag == "catalog":
            delete_form = DeleteItemsForm()
        else:
            delete_form = DeleteItemsForm()

        delete_item = DeleteItems(self.name_id, self.table_db,
                                  self.name_page, delete_form)
        delete_item.delete_items()

        if self.method_pag == "news":
            products = pag.news("news").items
            pagination = pag.news("pagination")
            total_pages = pag.news("news").pages
        elif self.method_pag == "catalog":
            products = pag.catalog("products", self.number).items
            pagination = pag.catalog("pagination", self.number)
            total_pages = pag.catalog("products", self.number).pages

        return render_template(self.html_path,
                               form=delete_form,
                               products=products,
                               pagination=pagination,
                               total_pages=total_pages,
                               check_total=check_auth())


class HomePage(WorkingWithHandlers):
    '''
    Класс обрабатывает простые страницы без доп. функционала.
    '''

    def __init__(self, html_path):
        '''
        :param html_path: Название шаблона html(полный путь).
        '''
        super().__init__()
        self.html_path = html_path

    def dispatch_request(self):
        """
        Метод реализует обработичик главной страницы.
        """

        logger.info('Входящий запрос: %s выполнен!', self.html_path)
        return render_template(self.html_path,
                               check_total=check_auth())


class AdminLogin(WorkingWithHandlers):
    '''
    Класс обрабатывает страницу авторизации админов.
    '''

    def __init__(self, name_page: str, name_db: Type[UserAdmin],
                 redirect_menu: str):
        '''
        :param name_page: Название страницы.
        :param name_db: Название таблицы.
        :param redirect_menu: Название страницы для редиректа.
        '''
        super().__init__()
        self.name_page = name_page
        self.name_db = name_db
        self.redirect_menu = redirect_menu

    def dispatch_request(self):
        """
        Метод сверяет введённые данные с данными в базе,
        при успешной проверке, авторизирует пользователя.
        """

        limiter.logger.info('Входящий запрос: %s %s',
                            request.method, request.path)
        form = AdminLoginForm()

        if form.validate_on_submit():
            username = form.login.data
            password = form.password.data

            user = db.session.execute(
                db.select(self.name_db).filter_by(
                    username=username)).scalar_one()

            if user and user.password == password:
                login_user(user)
                return redirect(url_for(self.redirect_menu))
            else:
                flash(cont_error[7], 'error_user')

        return render_template(f'admin/{self.name_page}.html', form=form)


class Logout(WorkingWithHandlers):
    '''
    Класс обрабатывает выход из админ панели.
    '''

    decorators = [login_required]

    def __init__(self, redirect_name: str):
        '''
        :param redirect_name: Название страницы для редиректа,
        после выхода из профиля.
        '''
        super().__init__()
        self.redirect_name = redirect_name

    def dispatch_request(self):
        """
        Метод обрабатывает выход из админ панели.
        """

        limiter.logger.info('Входящий запрос: %s %s',
                            request.method, request.path)
        logout_user()
        return redirect(url_for(self.redirect_name))


class AdminMenu(WorkingWithHandlers):
    '''
    Класс обрабатывает страницу админ меню.
    '''

    decorators = [login_required]

    def __init__(self, name_page: str):
        '''
        :param name_page: Название страницы админ меню.
        '''
        super().__init__()
        self.name_page = name_page

    def dispatch_request(self):
        """
        Метод реализует обработичик админ меню.
        """

        limiter.logger.info('Входящий запрос: %s %s',
                            request.method, request.path)
        return render_template(f'admin/{self.name_page}.html',
                               check_total=check_auth())


class AdminPanel(WorkingWithHandlers):
    '''
    Класс для обработки формы добавления товара в базу данных.
    '''

    decorators = [login_required]

    def __init__(self, name_page: str):
        '''
        :param name_page: Название страницы админ панели.
        '''
        super().__init__()
        self.name_page = name_page

    def dispatch_request(self):
        """
        Метод:
        1. проверяет метод запроса и валидацию формы.
        2. Получает данные из формы проверяет их и проверяет наличие имени фото
        3. Сохраняет фото в папку uploads и сохраняет айтем в базу данных
        4. Выводит сообщение об успешном добавлении, в противном случае,
        на каждом этапе выводит сообщение об ошибке.
        """

        limiter.logger.info('Входящий запрос: %s %s',
                            request.method, request.path)
        form = AddItemForm()

        if request.method == 'POST':
            logger.info("Проверка метода запроса |AddItemForm| успешно!")
            if form.validate_on_submit():
                logger.info("Проверка валидации |AddItemForm| успешно!")
                name = request.form['name']
                description = request.form['description']
                price = request.form['price']
                category = request.form['category']
                photo = request.files['photo']

                if photo:
                    logger.info("Файл |AddItemForm| получен!")
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                            filename))
                    logger.info("Файл |AddItemForm| сохранён в папку!")
                else:
                    logger.info("TypeError %s",
                                "Имя файла или путь не найдены!| AddItemForm|")
                    filename = None

                check_name = CheckingText(
                    name, 'error_panel', cont_error[5])
                check_description = CheckingText(
                    description, 'error_panel', cont_error[2])
                check_latin = CheckingText(
                    description, 'error_panel', cont_error[4])
                check_category = CheckingNumber(
                    category, 'error_panel', cont_error[6])

                total = [
                    check_name.check_length(min_length=3, max_length=15),
                    check_description.check_length(min_length=3,
                                                   max_length=1000),
                    check_latin.check_latin(),
                    check_category.check_category()]

                if all(total) and filename is not None:
                    logger.info("Все проверки |AddItemForm| пройденвы!")
                    try:
                        new_item = Item(name=name,
                                        description=description,
                                        price=price,
                                        category=category,
                                        photo=filename)
                        db.session.add(new_item)
                        db.session.commit()
                        logger.info(
                            "Айтем добавлен в базу данных!|AddItemForm|")
                        flash(cont_info[1], category='success_panel')
                    except Exception as ex:
                        logger.error(
                            "Exception %s %s",
                            "Проблема с добавлением файла!|AddItemForm|",
                            ex)
                else:
                    logger.error(
                        "Exception %s", "Проверки не пройдены!|AddItemForm| ")
                    flash(cont_info[2], category='error_panel')
                return redirect(url_for(self.name_page))
        return render_template(f'admin/{self.name_page}.html',
                               check_total=check_auth(), form=form)


class AdminArcticel(WorkingWithHandlers):
    '''
    Класс для обработки формы добавления новости в базу данных.
    '''

    decorators = [login_required]

    def __init__(self, name_page):
        '''
        :param name_page: Название страницы добавления статей
        '''
        super().__init__()
        self.name_page = name_page

    def dispatch_request(self):
        """
        Метод:
        1. проверяет метод запроса и валидацию формы.
        2. Получает данные из формы проверяет их и проверяет наличие имени фото
        3. Сохраняет фото в папку uploads и сохраняет айтем в базу данных
        4. Выводит сообщение об успешном добавлении, в противном случае,
        на каждом этапе выводит сообщение об ошибке.
        """

        app.logger.info('Входящий запрос: %s %s', request.method, request.path)
        form = AddArticleForm()

        if request.method == 'POST':
            logger.info("Проверка метода запроса |AdminArcticel| успешно!")
            if form.validate_on_submit():
                logger.info("Проверка валидации |AdminArcticel| успешно!")
                name = request.form['name_article']
                text = request.form['text_article']
                photo = request.files['add_photo']

                utc_timezone = pytz.utc
                utc_time = datetime.now(utc_timezone)
                eet_time = utc_time.astimezone(pytz.timezone('EET'))

                if photo:
                    logger.info("Файл |AdminArcticel| получен!")
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                            filename))
                    logger.info("Файл |AdminArcticel| сохранён в папку!")
                else:
                    logger.info("Файл |AdminArcticel| не сохранён в папку!")
                    filename = None

                check_name_lat = CheckingText(name,
                                              'error_article', cont_error[1])
                check_name_des = CheckingText(name,
                                              'error_article', cont_error[3])
                check_text_lat = CheckingText(text,
                                              'error_article', cont_error[4])
                check_text_des = CheckingText(text,
                                              'error_article', cont_error[2])

                total = [
                    check_name_des.check_length(min_length=3, max_length=100),
                    check_name_lat.check_latin(),
                    check_text_lat.check_latin(),
                    check_text_des.check_length(min_length=3, max_length=1000)]

                if all(total) and filename is not None:
                    logger.info("Проверки |AdminArcticel| пройдены!")
                    try:
                        new_article = Article(name=name,
                                              text=text,
                                              photo=filename,
                                              pub_date=eet_time)
                        db.session.add(new_article)
                        db.session.commit()
                        flash('СТАТЬЯ УСПЕШНО ДОБАВЛЕНА!',
                              category='success_article')
                    except Exception as ex:
                        logger.error("Exception %s %s",
                                     "Проблема с добавлением файла!",
                                     ex)
                else:
                    logger.info("Проверки |AdminArcticel| не пройдены!")
                    flash('НУЖНО ЗАГРУЗИТЬ ФОТО!', category='error_article')
                return redirect(url_for(self.name_page))
        return render_template(f'admin/{self.name_page}.html',
                               check_total=check_auth(), form=form)
