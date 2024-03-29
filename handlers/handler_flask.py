"""Модуль реализует обработчики приложения в стиле Views."""
import os
from datetime import datetime
from typing import Union, Type

import pytz

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, flash, redirect, render_template, \
    request, url_for
from flask.views import View
from flask_limiter import Limiter
from flask_login import login_required, login_user, logout_user
from flask_sslify import SSLify
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from database_create.FDataBase import DeleteItems, UserAdmin, Item, Article, db
from pagination_create.paginate_flask import WorkingWithPagination
from cute_form.form_create import DeleteItemsForm, AdminLoginForm, \
    AddItemForm, AddArticleForm, DeleteArticleForm
from authorization.auth import check_auth, login_manager
from toolkits.toolkit import CheckingText, CheckingNumber
from content_flask import cont_error, cont_info


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
                                   maxBytes=1024 * 1024,
                                   backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# Добавить ch в логгер, создание ротации
logger.addHandler(ch)
logger.addHandler(file_handler)


@login_manager.user_loader
def load_user(user_id):
    """
    Загрузка объекта пользователя на основе идентификатора.

    Функция вызывается Flask-Login для загрузки пользователя по его
    идентификатору из сеанса пользователя.

    : param user_id: Идентификатор пользователя.

    Returns:
        UserAdmin: Объект пользователя, найденный по указанному идентификатору.
    """
    limiter.logger.info('Входящий запрос: %s %s', request.method, request.path)
    return UserAdmin.query.get(int(user_id))


class WorkingWithHandlers(View):
    """
    Базовый (родительский) класс для работы с обработчиками.

    Attributes:
        init_every_request (bool): Флаг, указывающий, нужно ли инициализировать
            объект при каждом запросе. По умолчанию установлено значение False.
        decorators (list): Список декораторов, которые будут применены к методу
            `dispatch_request`. По умолчанию содержит декоратор, ограничивающий
            частоту запросов до 100 в минуту.
        methods (list): Список HTTP-методов, поддерживаемых этим обработчиком.
            По умолчанию содержит все HTTP-методы: GET, POST, PUT, DELETE.

    Methods:
        __init__(): Конструктор класса.
        dispatch_request(): Метод, который вызывается при обработке запроса.
            Подклассы должны переопределить этот метод для выполнения
            конкретной логики обработки запроса.
    """

    init_every_request = False
    decorators = [limiter.limit("100 per minute")]
    methods = ["GET", "POST", "PUT", "DELETE"]

    def __init__(self):
        pass

    def dispatch_request(self):
        pass


class HandlersItem(WorkingWithHandlers):
    """Класс обрабатывает страницы каталога, а так же новостей."""

    def __init__(self, name_page: str, number: int, amount_item: int,
                 table_db: Union[Type[Item], Type[Article]],
                 name_id: str, method_pag: str):
        """
        Инициализирует объект класса HandlersItem.

        :param name_page: Название страницы.
        :param number: Категория товаров (в каталоге).
        :param amount_item: Количество айтемов на странице.
        :param table_db: Таблица (её название).
        :param name_id: Тип айтема на странице (товар/новость).
        :param method_pag: метод, для передачи пагинация/айтемы.
        :param html_path: Название шаблона html(полный путь).
        """
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
        Метод реализует обработичик.

        Returns:
            Через пагинацию выводит товары на страницу.
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
    """
    Класс обрабатывает простые страницы без доп. функционала.

    Returns:
        обработанный html шаблон. Если пользователь
        является администратором, то добавляет доп кнопки на страницу
    """

    def __init__(self, html_path):
        """
        Инициализирует объект класса HomePage.

        :param html_path: Название шаблона html(полный путь).
        """
        super().__init__()
        self.html_path = html_path

    def dispatch_request(self):
        """Метод реализует обработичик главной страницы."""
        logger.info('Входящий запрос: %s выполнен!', self.html_path)
        return render_template(self.html_path,
                               check_total=check_auth())


class AdminLogin(WorkingWithHandlers):
    """
    Класс обрабатывает страницу авторизации админов.

    Returns:
        При успешной авторизации, перенаправляет в админ панель.
    """

    def __init__(self, name_page: str, name_db: Type[UserAdmin],
                 redirect_menu: str):
        """
        Инициализирует объект класса AdminLogin.

        :param name_page: Название страницы.
        :param name_db: Название таблицы.
        :param redirect_menu: Название страницы для редиректа.
        """
        super().__init__()
        self.name_page = name_page
        self.name_db = name_db
        self.redirect_menu = redirect_menu

    def dispatch_request(self):
        """
        Метод сверяет введённые данные с данными в базе.

        При успешной проверке, авторизирует пользователя.
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
    """
    Класс обрабатывает выход из админ панели.

    Returns:
        Удаляет пользователя из сессии.
    """

    decorators = [login_required]

    def __init__(self, redirect_name: str):
        """
        Инициализирует объект класса Logout.

        :param redirect_name: Название страницы для редиректа.
        """
        super().__init__()
        self.redirect_name = redirect_name

    def dispatch_request(self):
        """
        Удаляет пользователя из сессии.

        После удаление, производит редирект на указаную страницу.
        """
        limiter.logger.info('Входящий запрос: %s %s',
                            request.method, request.path)
        logout_user()
        return redirect(url_for(self.redirect_name))


class AdminMenu(WorkingWithHandlers):
    """
    Класс обрабатывает страницу админ меню.

    Returns:
        Обрабатывает html шаблон админ паанели.
    """

    decorators = [login_required]

    def __init__(self, name_page: str):
        """
        Инициализирует объект класса AdminMenu.

        :param name_page: Название страницы админ меню.
        """
        super().__init__()
        self.name_page = name_page

    def dispatch_request(self):
        """Метод реализует обработичик админ меню."""
        limiter.logger.info('Входящий запрос: %s %s',
                            request.method, request.path)
        return render_template(f'admin/{self.name_page}.html',
                               check_total=check_auth())


class AdminPanel(WorkingWithHandlers):
    """
    Класс для обработки формы добавления товара в базу данных.

    Returns:
        После прохождении всех проверок, добавляет айтем в базу данных.
    """

    decorators = [login_required]

    def __init__(self, name_page: str):
        """
        Инициализирует объект класса AdminPanel.

        :param name_page: Название страницы админ панели.
        """
        super().__init__()
        self.name_page = name_page

    def dispatch_request(self):
        """
        Реализует добавление айтема в базу данных.

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
    """
    Класс для обработки формы добавления новости в базу данных.

    Returns:
        После прохождении всех проверок, добавляет новость в базу данных.
    """

    decorators = [login_required]

    def __init__(self, name_page):
        """
        Инициализирует объект класса AdminArcticel.

        :param name_page: Название страницы добавления статей
        """
        super().__init__()
        self.name_page = name_page

    def dispatch_request(self):
        """
        Реализует добавление новости в базу данных.

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


@app.errorhandler(404)
@limiter.limit("100 per minute")
def page_not_found(error):
    """Реализует обработку ошибки 404."""
    logger.error('Страница не найдена: %s', request.url)
    return render_template('errors/page_not_found.html'), 404
