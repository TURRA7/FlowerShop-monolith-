"""Модуль для работы с логгированием."""

import logging
from logging.handlers import RotatingFileHandler


class Logger:
    """Данные класс подключает логгирование для модулей."""

    def __init__(self, name, level=logging.DEBUG):
        """Метод инициализации параметров."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Создание обработчика консоли и установка уровня отладки
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)

        # Создание обработчика файла и установка ротации логов
        file_handler = RotatingFileHandler(name, maxBytes=1024*1024,
                                           backupCount=5)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Добавление обработчиков в логгер
        self.logger.addHandler(ch)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        """Метод получения логгера для работы."""
        return self.logger
