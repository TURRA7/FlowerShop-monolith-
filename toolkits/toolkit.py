from flask import flash

import logging
from logging.handlers import RotatingFileHandler


# Создание логгера
logger = logging.getLogger('log_toolkit.log')
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
file_handler = RotatingFileHandler('log_toolkit.log',
                                   maxBytes=1024*1024,
                                   backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# Добавить ch в логгер, создание ротации
logger.addHandler(ch)
logger.addHandler(file_handler)


class CheckingValue:
    """
    Класс предназначен для различных проверок
    входных значений (является родительским классом).
    """

    def __init__(self, value: object, category: str, message: str):
        """
        :param value: Входное значение.
        :param category: Категория ошибки, которую покажет flash
        :param message: Сообщение ошибки, которую покажет flash
        """

        self.value = value
        self.category = category
        self.message = message


class CheckingText(CheckingValue):
    """
    Класс предназначен для различных проверок входных значений (строковых).
    """

    def check_length(self, min_length: int, max_length: int) -> bool:
        """
        Проверяет длину значения в заданном диапазоне
        и выводит flash сообщение при несоответствии.
        """

        if not isinstance(self.value, str):
            logger.error("TypeError %s", "check_length")
            return False
        if not (min_length <= len(self.value) <= max_length):
            flash(self.message, category=self.category)
            return False
        return True

    def check_latin(self) -> bool:
        """
        Проверяет, содержит ли значение только символы латинского алфавита.
        """

        if not isinstance(self.value, str):
            logger.error("TypeError %s", "check_check_latin")
            return False
        if all(c.isalpha() and c.isascii() for c in self.value):
            flash(self.message, category=self.category)
            return False
        return True


class CheckingNumber(CheckingValue):
    """
    Класс предназначен для различных проверок входных значений (числовых).
    """

    def check_category(self) -> bool:
        """
        Проверяет значение, на соответствие одной из категорий.
        """
        '''
        if not isinstance(self.value, int):
            logger.error("TypeError %s", "check_category(isinstance)")
            return False
            '''
        if int(self.value) not in {1, 2, 3, 4, 5, 6, 7, 8}:
            logger.error("TypeError %s", "check_category(value)")
            flash(self.message,
                  category=self.category)
            return False
        return True
