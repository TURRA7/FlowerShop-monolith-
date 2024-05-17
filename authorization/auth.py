"""Модуль отвечает за аутентификацию администраторов."""
from flask_login import LoginManager, current_user

from log_mod import Logger


login_manager = LoginManager()
login_manager.login_view = 'login'

# Создание логгера
db_logger = Logger("log_auth.log")
logger = db_logger.get_logger()


def check_auth() -> str:
    """
    Функция проверяет авторизирован ли пользователь.

    Возвращает 'admin', если пользователь авторизован,
    иначе "no_admin".
    """
    if current_user.is_authenticated:
        logger.info("Пользователь авторизирован!")
        return 'admin'
    else:
        logger.info("Пользователь не авторизирован!")
        return "no_admin"
