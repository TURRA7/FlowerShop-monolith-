"""
Данный модуль предназначен для тестирования моделей табллиц.

Построен модуль с помощью SQLAlchemy и имеет следующие функции:
    test_new_user - тестирование модели UserAdmin.
    test_new_item - тестирование модели Item.
    test_new_article - тестирование модели Article.
"""
from werkzeug.security import check_password_hash


def test_new_user(new_user):
    """
    Функция тестирует модель таблицы UserAdmin.

    GIVEN: Получение модели UserAdmin.
    WHEN: Когда создаётся новый пользователь.
    THEN: Проверяются данные пользователя.
    """
    assert new_user.username == "jenya_1"
    assert check_password_hash(new_user.password, "d7hBfdgrVlWB9")


def test_new_item(new_item):
    """
    Функция тестирует модель таблицы Item.

    GIVEN: Получение модели
    WHEN: Когда создаётся новый товар.
    THEN: Проверяются введеные данные.
    """
    assert isinstance(new_item.name, str)
    assert new_item.name == "Букет ВЕСНА"
    assert isinstance(new_item.description, str)
    assert new_item.description == "Яркий и свежий букет из разных цветов!"
    assert isinstance(new_item.price, (int, float))
    assert new_item.price == 1700
    assert isinstance(new_item.category, int)
    assert new_item.category in [1, 2, 3, 4, 5, 6, 7, 8]
    assert new_item.category == 2
    assert isinstance(new_item.photo, str)
    assert new_item.photo[new_item.photo.index(".") + 1:] in ['jpg',
                                                              'jpeg',
                                                              'png']
    assert new_item.photo == "flowers.jpg"


def test_new_article(new_article):
    """
    Функция тестирует модель таблицы Article.

    GIVEN: Получение модели
    WHEN: Когда создаётся новая новость.
    THEN: Проверяются введеные данные.
    """
    assert isinstance(new_article.name, str)
    assert new_article.name == "Магазин открылся!"
    assert isinstance(new_article.text, str)
    assert new_article.text == "Мы рады приветствовать гостей..."
    assert isinstance(new_article.photo, str)
    assert new_article.photo[new_article.photo.index(".") + 1:] in ['jpg',
                                                                    'jpeg',
                                                                    'png']
    assert new_article.photo == "shop.jpg"
