from flask_login import LoginManager, current_user

import logging
from logging.handlers import RotatingFileHandler

login_manager = LoginManager()
login_manager.login_view = 'login'


# Создание логгера
logger = logging.getLogger('log_auth.log')
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
file_handler = RotatingFileHandler('log_auth.log',
                                   maxBytes=1024*1024,
                                   backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# Добавить ch в логгер, создание ротации
logger.addHandler(ch)
logger.addHandler(file_handler)


def check_auth() -> str:
    """
    Возвращает 'admin', если пользователь авторизован, иначе "no_admin".
    """
    if current_user.is_authenticated:
        logger.info("Пользователь авторизирован!")
        return 'admin'
    else:
        logger.info("Пользователь не авторизирован!")
        return "no_admin"
