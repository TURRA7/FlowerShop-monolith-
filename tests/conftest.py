"""Данный модуль содержит фикстуры, для облегчения тестирования кода."""
import os
import pytest

from database_create.FDataBase import UserAdmin, Item, Article
from app import create_app


@pytest.fixture(scope='module')
def new_user():
    """Фикстура создаёт пользователя UserAdmin."""
    user = UserAdmin(username="jenya_1",
                     password="pbkdf2:sha256:600000$9YhgntcGJ2U5uYRk$df894224d9d00ac8aaf6a8fe2d6beb312d1540661954abb880021945d2887863")
    return user


@pytest.fixture(scope='module')
def new_item():
    """Фикстура создаёт товар Item."""
    item = Item("Букет ВЕСНА", "Яркий и свежий букет из разных цветов!",
                1700, 2, "flowers.jpg")
    return item


@pytest.fixture(scope='module')
def new_article():
    """Фикстура создаёт новость Article."""
    article = Article("Магазин открылся!",
                      "Мы рады приветствовать гостей...",
                      "shop.jpg",
                      "2024-01-01 00:00:00.01")
    return article


@pytest.fixture(scope='module')
def test_client():
    """Данная фикстура создаёт контекст приложения Flask."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
