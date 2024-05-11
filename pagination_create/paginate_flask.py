"""Модуль реализует работу с пагинацией на страницах.

Модуль содержит класс WorkingWithPagination,
который предоставляет функционал для работы с пагинацией
на страницах каталога и новостей.

Классы:
    WorkingWithPagination: Класс для работы с пагинацией.

Глобальные переменные:
    logger: Логгер для записи сообщений об ошибках и
    информации о работе пагинации.
"""
from flask import request

from sqlalchemy import desc
from flask_paginate import Pagination

from typing import Union
from ..log_mod import Logger

# Создание логгера
db_logger = Logger("log_paginate.log")
logger = db_logger.get_logger()


class WorkingWithPagination:
    """Класс отображает пагинацию на странице."""

    def __init__(self, amount_item: int, name_db: object):
        """
        Инициализирует объект класса WorkingWithPagination.

        :param amount_item: Колличество айтемов на странице.
        :param name_db: Название базы данных.
        """
        self.amount_item = amount_item
        self.name_db = name_db

    def catalog(self, category: str, num_cat: int) -> Union[Pagination, list]:
        """
        Метод отображает айтемы, через пагинацию на страницах каталога.

        Returns:
            Возвращает pagination или products в зависимости
            от переданного условия в category.
        """
        page = request.args.get('page', type=int, default=1)
        products = self.name_db.query.filter_by(
            category=num_cat).paginate(
                page=page, per_page=self.amount_item, error_out=False)
        pagination = Pagination(page=page,
                                total=products.total,
                                per_page=self.amount_item,
                                bs_version=4)

        if category == "pagination":
            return pagination
        elif category == "products":
            return products

    def news(self, category: str) -> Union[Pagination, list]:
        """
        Метод отображает айтемы, через пагинацию на страницах новостей.

        Returns:
            Возвращает pagination или news в зависимости
            от переданного условия в category.
        """
        page = request.args.get('page', type=int, default=1)
        news = self.name_db.query.order_by(
            desc(self.name_db.pub_date)).paginate(
                page=page, per_page=3, error_out=False)
        pagination = Pagination(page=page,
                                total=news.total,
                                per_page=self.amount_item,
                                bs_version=4)

        if category == "pagination":
            return pagination
        elif category == "news":
            return news
