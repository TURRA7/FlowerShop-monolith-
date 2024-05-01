"""Тестирует модуль handler_flask."""
import pytest
import textwrap
from bs4 import BeautifulSoup

from flask import Flask


class TestHomePageUnit:
    """
    Класс тестирует стартовую старницу (index).

    Methods:
        test_elements: Проверяет наличие на странице заданых элементов.
    """

    @pytest.mark.parametrize("value", [
        ("Главная страница"),
        ("ВЫБЕРИТЕ КАТЕГОРИЮ"),
        ("МАГАЗИН ЦВЕТОВ В #####"),
        ("Мы дарим улыбки<br>обладателям наших цветов!"),
        ("Сделаем фото<br>перед отправкой!"),
        ("Открытка к букету<br>в подарок!"),
        ("Поздравим за вас<br>Анонимно!"),
        ("Гарантия<br>свежести"),
        ("ВЫБЕРИТЕ КАТЕГОРИЮ"),
        ("КОНТАКТНАЯ ИНФОРМАЦИЯ"),
        ("График работы:"),
        ("Без выходных с 7:30 до 20:00"),
        ("Адрес:"),
        ("город #####, ############# ##"),
        ("Доставка:"),
        ("""осуществляется по городу и<br>области, стоимость доставки не входит<br>
    в стоимость заказа, цены уточняйте<br>
    по телефону.</span><br><br>"""),
        ("Телефон:"),
        ("+7-###-###-##-##"),
        ("+7-***-***-**-**"),
        ("+7-000-000-00-00"),
        (": СОТРУДНИК_1"),
        (": СОТРУДНИК_2"),
        (": СОТРУДНИК_3"),
        ("btn_flowers"),
        ("btn_bouquets"),
        ("btn_baskets"),
        ("btn_indoor"),
        ("btn_artificial"),
        ("btn_wreaths"),
        ("btn_toys"),
        ("btn_fireworks"),
        ("btn-danger"),
        ("btn-MENU"),
        ("btn-danger"),
    ])
    def test_elements(self, client: Flask, value: str):
        """Метод проверяет наличие элементов на странице|index|."""
        response = client.get("/")
        assert response.status_code == 200
        assert value.encode("utf-8") in response.data


class TestErrorUnit:
    """
    Класс тестирует страницу ошибки 404.

    Methods:
        test_error_elements: Проверяет наличие на странице заданых элементов.
    """

    @pytest.mark.parametrize("value", [
        ("НЕТ ТАКОЙ СТРАНИЦЫ"),
        ("ТАКНОЙ СТРАНИЦЫ НЕ СУЩЕСТВУЕТ"),
        ("выберите нужный пункт"),
        ("Главная"),
        ("Каталог"),
        ("Информация"),
    ])
    def test_error_elements(self, client: Flask, value: str):
        """Метод проверяет наличие элементов на странице|404|."""
        response = client.get("http://localhost:5000/page_doesn't_exist")
        assert response.status_code == 404
        assert value.encode("utf-8") in response.data


class TestAdminUnit:
    """
    Класс тестирует панель администратора и добавление товаров.

    Methods:
        test_admin_panel_elements: Проверяет наличие на странице
        заданых элементов.
    """

    @pytest.mark.parametrize("class_element", [
        ("btn-danger_panel"),
        ("btn-MENU_panel"),
        ("box_admin"),
        ("admin_label"),
        ("admin_form"),
        ("preview"),
        ("input_container"),
        ("name_plh"),
        ("desc_plh"),
        ("price_plh"),
        ("caregory_plh"),
        ("photo_choice"),
        ("btn_picture"),
        ("btn_add"),
    ])
    def test_admin_panel_elements(self, client: Flask, class_element: str):
        """Метод проверяет наличие элементов на странице|admin_panel|."""
        response = client.get("http://localhost:5000/admin_panel")
        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')
        element = soup.find(class_=class_element)
        assert element is not None


class TestArticleUnit:
    """
    Класс тестирует панель панель добавления новостей|admin_article|.

    Methods:
        test_article_panel_elements: Проверяет наличие на странице
        заданых элементов.
    """

    @pytest.mark.parametrize("class_element", [
        ("btn-danger_article"),
        ("btn-MENU_article"),
        ("admin_add_article"),
        ("add_article"),
        ("block_preview"),
        ("preview_article"),
        ("block_placeholder_total"),
        ("placeholder_name_article"),
        ("placeholder_text_article"),
        ("add_photo"),
        ("btn_add_article"),
    ])
    def test_article_panel_elements(self, client: Flask, class_element: str):
        """Метод проверяет наличие элементов на странице|admin_article|."""
        response = client.get("http://localhost:5000/admin_article")
        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')
        element = soup.find(class_=class_element)
        assert element is not None
