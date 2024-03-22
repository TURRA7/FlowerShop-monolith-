from datetime import datetime

from flask import request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from flask_login import UserMixin

import logging
from logging.handlers import RotatingFileHandler


# Создание логгера
logger = logging.getLogger('log_FDataBase.log')
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
file_handler = RotatingFileHandler('log_FDataBase.log',
                                   maxBytes=1024*1024,
                                   backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# Добавить ch в логгер, создание ротации
logger.addHandler(ch)
logger.addHandler(file_handler)


# Объявление базового(декларативного) класса
class Base(DeclarativeBase):
    """
    Базовый декларативный класс.
    Необходим для работы с метаданными таблиц.
    """

    pass


# Создание экземпляра SQLAlchemy
db = SQLAlchemy(model_class=Base)


# Таблица с админками
class UserAdmin(UserMixin, db.Model):
    """
    Класс создаёт таблицу с адмнистраторами проекта,
    дающую возможность им авторизироваться и пользоваться
    возможностями администрирования.

    :param id: Является id индификатором пользователя.
    :param username: логин пользователя.
    :param password: Пороль пользователя.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(300), nullable=False)
    password: str = db.Column(db.String(300), nullable=False)


# Таблица с товарами
class Item(UserMixin, db.Model):
    """
    Класс создаёт таблицу с товарами для каталога
    (для карточек товара).
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(255))

    def __init__(self, name: str, description: str,
                 price: int, category: int, photo: str):
        """
        :param id: Является id индификатором товара.
        :param name: название товара.
        :param description: Описание товара.
        :param price: Цена товара.
        :param category: Категория товара.
        :param photo: Название файла с расширением.
        """

        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.photo = photo


# Таблица с статьями
class Article(UserMixin, db.Model):
    """
    Класс создаёт таблицу с новостями.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(255))
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name: str, text: str,
                 photo: str, pub_date: datetime):
        """
        :param id: Является id индификатором новости.
        :param name: Заголовок новости.
        :param text: текст новости.
        :param photo: Название файла с расширением.
        :param pub_date: Дата и время загрузки новости.
        """

        self.name = name
        self.text = text
        self.photo = photo
        self.pub_date = pub_date


class DeleteItems:
    '''
    Класс для удаления айтемов из базы данных.
    '''

    def __init__(self, name_id: str, table_db: object,
                 name_page: str, delete_form: object):
        """
        :param name_id: Название категории айтема.
        :param table_db: Название таблицы, из которой будет удалён айтем.
        :param name_page: Название страницы с которой будет удалён айтем.
        :param delete_form: Объект класса DeleteItemsForm
        (формы удаления айтемов).
        """

        self.name_id = name_id
        self.table_db = table_db
        self.name_page = name_page
        self.delete_form = delete_form

    def delete_items(self):
        '''
        Метод удалаяет айтем из базы данных.
        '''

        if request.method == 'POST':
            if self.delete_form.validate_on_submit():
                item_id = request.form.get(self.name_id)
                item = self.table_db.query.get(item_id)
                if item:
                    try:
                        db.session.delete(item)
                        db.session.commit()
                        return redirect(url_for(self.name_page))
                    except Exception as ex:
                        # Запись информации об ошибках в логи.
                        logger.debug("Ошибка при удалении товара: {ex}")
                        print(ex)
            else:
                # !!! ПОСЛЕ ПРОВЕДЕНИЯ ТЕСТОВ, ДАННУЮ СТРОКУ УБРАТЬ !!!
                flash('Ошибка при удалении товара', 'error')
