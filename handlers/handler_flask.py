from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask.views import View

from typing import Union, Type

from pagination_create.paginate_flask import WorkingWithPagination
from cute_form.form_create import DeleteItemsForm
from database_create.FDataBase import DeleteItems, UserAdmin, Item, Article, db
from authorization.auth import check_auth, login_manager

import logging
from logging.handlers import RotatingFileHandler


# Создание экземпляра приложения
app = Flask(__name__)
app.config.from_pyfile('config.py')
# Создание экземпляра класса лимитера
# Инициализация базы данных
db.init_app(app)
limiter = Limiter(app)
# Инициализация логин менеджера
login_manager.init_app(app)

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

    :param name_page: Название страницы.
    :param number: Категория товаров (в каталоге).
    :param amount_item: Количество айтемов на странице.
    :param table_db: Таблица (её название).
    :param name_id: Тип айтема на странице (товар/новость).
    :param method_pag: метод, при котором передаётся либо пагинация,
    либо айтемы.
    :param html_path: Название шаблона html(полный путь).
    '''

    def __init__(self, name_page: str, number: int, amount_item: int,
                 table_db: Union[Type[Item], Type[Article]],
                 name_id: str, method_pag: str):
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
        """

        logger.info('Входящий запрос:{self.name_page} выполнен!')
        pag = WorkingWithPagination(self.amount_item, self.table_db)
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
    Класс обрабатывает главную страницу 'Index'.

    :param html_path: Название шаблона html(полный путь).
    '''

    def __init__(self, html_path):
        super().__init__()
        self.html_path = html_path

    def dispatch_request(self):
        """
        Метод реализует обработичик.
        """

        logger.info('Входящий запрос:{self.html_path} выполнен!')
        return render_template(self.html_path,
                               check_total=check_auth())
