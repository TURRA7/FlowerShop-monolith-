"""Тестирует модуль handler_flask."""
import os
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import Chrome


class TestHomePageFunctional:
    """
    Класс тестирует стартовую старницу (index).

    Methods:
        test_btn_home_page: Проверяет работоспособность кнопок button,
        а так же переход с помощью них, на другие страницы.
        test_href_home_page: Проверяет кнопки, которые появляются
        при авторизации, а именно 'МЕНЮ' и 'ВЫХОД'.
        test_hamburger_menu: Проверяет работоспособность 'бургер-меню'.
    """

    @pytest.mark.parametrize("btn_class, check_data", [
        ("btn_flowers", "Цветы"),
        ("btn_bouquets", "Букеты"),
        ("btn_baskets", "Корзинки"),
        ("btn_indoor", "Комнатные цветы"),
        ("btn_artificial", "Искуственные цветы"),
        ("btn_wreaths", "Венки"),
        ("btn_toys", "Игрушки"),
        ("btn_fireworks", "Фейерверки"),
    ])
    def test_btn_home_page(self, driver: Chrome,
                           btn_class: str, check_data: str):
        """Метод тестирует редиректы на странице(по кнопкам)|index|."""
        driver.get("http://localhost:5000")
        button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            btn_class)))
        button.click()
        assert check_data in driver.title

    def test_href_home_page(self, driver_auth):
        """Метод тестирует переходы по href ссылкам на странице|index|."""
        driver = driver_auth
        driver.find_element(By.CLASS_NAME, "btn-MENU").click()
        driver.find_element(By.CLASS_NAME, "btn-MENU").click()
        driver.find_element(By.CLASS_NAME, "btn-danger").click()
        assert "Вход в админ-панель" in driver.title

    def test_hamburger_menu(self, driver_auth):
        """Метод тестирует функциональность бургер-меню."""
        driver = driver_auth
        driver.find_element(By.CLASS_NAME, "btn-MENU").click()
        driver.find_element(By.CLASS_NAME, "menu_btn").click()
        driver.find_element(By.ID, "store_page").click()
        assert "Новости магазина!" in driver.title


class TestErrorFunctional:
    """
    Класс тестирует страницу ошибки 404.

    Methods:
        test_href_error: Проверяет переходы по href ссылкам
        на странице 404.
    """

    def test_href_error(self, driver: Chrome):
        """Метод тестирует переходы по href ссылкам на странице|error|."""
        driver.get("http://localhost:5000/page_doesn't_exist")
        driver.find_element(By.ID, "error_index").click()
        assert "Главная страница" in driver.title
        driver.back()
        driver.find_element(By.ID, "error_index#catralog").click()
        assert "Главная страница" in driver.title
        driver.back()
        driver.find_element(By.ID, "error_index#information").click()
        assert "Главная страница" in driver.title
        driver.back()


class TestAdminFunctional:
    """
    Класс тестирует панель администратора и добавление товаров.

    Methods:
        test_panel_add: Проверяет добавление товара в базу данных,
        через фыорму admin_panel.
    """

    def test_panel_add(self, driver_auth: Chrome):
        """
        Метод тестирует панель добавления товаров|admin_panel|.

        После добавления, driver переходит на страницу товара,
        проверяет его наличие и удаляет его из базы данных.
        """
        driver = driver_auth
        driver.find_element(By.CLASS_NAME, "btn_admin_item").click()

        driver.find_element(
            By.CLASS_NAME, "name_plh").send_keys("Товар номер 1")
        driver.find_element(
            By.CLASS_NAME, "desc_plh").send_keys("Тестовый товар!")
        driver.find_element(By.CLASS_NAME, "price_plh").send_keys(1000)
        dropdown = Select(driver.find_element(By.CLASS_NAME, "caregory_plh"))
        dropdown.select_by_index(1)

        file_add = driver.find_element(By.CLASS_NAME, "btn_picture")
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'photo_test/item.jpeg')
        file_add.send_keys(file_path)
        driver.find_element(By.CLASS_NAME, "btn_add").click()

        driver.find_element(By.CLASS_NAME, "btn-MENU_panel").click()
        driver.find_element(By.CLASS_NAME, "btn-MENU").click()
        driver.find_element(By.CLASS_NAME, "btn_bouquets").click()

        link_element = driver.find_element(
            By.XPATH, "/html/body/div/ul/li/div/div/div[1]")
        assert link_element is not None
        driver.find_element(By.CLASS_NAME, "delete_item").click()


class TestArticleFunctional:
    """
    Класс тестирует панель добавления новостей|admin_article|.

    Methods:
        test_article_add: Проверяет добавление новостей в базу данных,
        через фыорму admin_article.
    """

    def test_article_add(self, driver_auth: Chrome):
        """
        Метод тестирует панель добавления новостей|admin_article|.

        После добавления, driver переходит на страницу новостей,
        проверяет наличие новости и удаляет её из базы данных.
        """
        driver = driver_auth
        driver.find_element(By.CLASS_NAME, "btn_admin_article").click()

        driver.find_element(By.CLASS_NAME,
                            "placeholder_name_article").send_keys(
                                "Тестовая статья!")
        driver.find_element(By.CLASS_NAME,
                            "placeholder_text_article").send_keys(
                                "Форма протестирована с помощью Selenium!")

        file_add = driver.find_element(By.CLASS_NAME, "add_photo")
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'photo_test/store.jpg')
        file_add.send_keys(file_path)
        driver.find_element(By.CLASS_NAME, "btn_add_article").click()

        driver.find_element(By.CLASS_NAME, "menu_btn").click()
        driver.find_element(By.ID, "store_page").click()

        link_element = driver.find_element(
            By.XPATH, "/html/body/div/ul/li/div/div[1]")
        assert link_element is not None
        driver.find_element(By.CLASS_NAME, "delete_news").click()
