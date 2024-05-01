"""Данный модуль содержит фикстуры, для облегчения тестирования кода."""
import pytest
from flask_login import login_user

from selenium import webdriver
from selenium.webdriver.common.by import By

from database_create.FDataBase import UserAdmin
from app import create_app


@pytest.fixture(scope="module")
def new_user():
    """Фикстура создаёт пользователя по модели UserAdmin."""
    user = UserAdmin(id=1,
                     username="jenya_1",
                     password=("sha256:600000$9YhgntcGJ2U5uYRk$"
                               "df894224d9d00ac8aaf6a8fe2d6beb312d1540661"
                               "954abb880021945d2887863"))
    return user


@pytest.fixture(scope="session")
def app():
    """
    Фикстура создаёт экземпляр приложения Flask.

    Так же происходит установка конфигурации.
    """
    app = create_app()
    app.config.update({
        "TestingConfig": True,
    })
    yield app


@pytest.fixture()
def client(app, new_user):
    """
    Создание тестового клиента.

    В контексте тестового клиента, происходит
    авторизация пользователя с помощью login_user().
    """
    with app.test_client() as client:
        login_user(new_user)
        yield client


@pytest.fixture()
def runner(app):
    """Саздание клиентского раннера."""
    return app.test_cli_runner()


@pytest.fixture(scope="class")
def driver():
    """Инициализация драйвера браузера от seleium (без авторизации)."""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def driver_auth(driver):
    """Авторизация в приложении, с помощью selenium(webdriver)."""
    driver.get('http://127.0.0.1:5000/admin_login')
    driver.implicitly_wait(2)
    driver.find_element(By.CLASS_NAME, 'input_log').send_keys("jenya_1")
    driver.find_element(By.CLASS_NAME, 'input_pass').send_keys("d7hBfdgrVlWB9")
    driver.find_element(By.CLASS_NAME, 'btn_authorization').click()
    yield driver
