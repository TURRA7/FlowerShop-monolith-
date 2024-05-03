"""Модуль представляет собой вариации конфигурации."""
from datetime import timedelta


class Config:
    """Общие настройки для разработки и продакшена."""

    MAX_COOKIE_SIZE = 0
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'handlers/static/img/uploads'
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "..."
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 2592000
    SESSION_COOKIE_NAME = "session"
    CSRF_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_REFRESH_EACH_REQUEST = True
    EXPLAIN_TEMPLATE_LOADING = True


class DevelopmentConfig(Config):
    """Настройки для разработки."""

    SQLALCHEMY_DATABASE_URI = "..."
    DEBUG = True


class ProductionConfig(Config):
    """Настройки для продакшена."""

    CACHE_TYPE = "..."
    SECRET_KEY = "..."
    SESSION_COOKIE_NAME = "..."
    SQLALCHEMY_DATABASE_URI = "..."
    DEBUG = False


class TestingConfig(Config):
    """Настройки для тестирования."""

    SQLALCHEMY_DATABASE_URI = "..."
    DEBUG = True
    TESTING = True
