# Сайт витрина - FlowerShop

Это приложение, представляет собой сайт-витрину на цветочную и сувенирную тематику. Приложение построено на языке PYTHON с использованием фреймворка Flask.

## Структура проекта

```
.
└── FlowerShop
    ├── authorization
    |   ├── __init__.py
    |   └── auth.py
    ├── cute_form
    |   ├── __init__.py
    |   └── form_create.py
    ├── database_create
    |   ├── __init__.py
    |   └── FDataBase.py
    ├── handlers
    |   ├── static
    |   ├── templates
    |   ├── __init__.py
    |   ├── config.py
    |   └── handler_flask.py
    ├── pagination_create
    |   ├── __init__.py
    |   └── paginate_flask.py
    ├── tests
    |   ├── functional
    |   ├── unit
    |   ├── webdriver
    |   ├── __init__.py
    |   └── conftest.py
    ├── app.py
    ├── content_flask.py
    ├── hash_pass.py
    ├── README.md
    ├── requirements.txt
    └── setup.cfg
```

___

### Краткое описание структуры

* **authorization**: Модуль для работы с авторизацией.
* **cute_form**: Модуль по работе с формами Flask-wtforms.
* **database_create**: Модуль для работы с базой данных через Flask-SQLAlchemy.
* **handlers**: Модуль с обработчиками, шаблонами и статическими файлами.
* **pagination_create**: Модуль с пагинацией страниц.
* **tests**: Модуль с тестированием проекта.
* **app.py**: Исполнительный файл проекта.
* **content_flask.py**: Модуль содержит словари с текстовым контентом.
* **hash_pass.py**: Утилита для хеширования пароля.
* **README.md**: Файл описание проекта.
* **requirements.txt**: Файл с описанием зависимостей.
* **setup.cfg**: Конфигурационный файл для Flake8.

___

### Инструменты использованные в проекте

![Static Badge](https://img.shields.io/badge/python-3.12.2-badgeContent?style=flat&logo=Python&logoColor=yellow&label=Python&labelColor=blue&color=gray)
![Static Badge](https://img.shields.io/badge/python-2.3.7-badgeContent?style=flat&logo=Werkzeug&logoColor=yellow&label=Werkzeug&labelColor=%23f9ab00&color=%23e2683c)
![Static Badge](https://img.shields.io/badge/python-2021.3-badgeContent?style=flat&logo=Pytz&logoColor=yellow&label=Pytz&labelColor=%23182c32&color=%237eb7aa)
![Static Badge](https://img.shields.io/badge/python-3.0.0-badgeContent?style=flat&logo=Wtforms&logoColor=yellow&label=Wtforms&labelColor=%23E5E3E4&color=%235BA199)
![Static Badge](https://img.shields.io/badge/python-2.0.20-badgeContent?style=flat&logo=Sqlalchemy&logoColor=black&label=Sqlalchemy&labelColor=%23FAD074&color=%23FFA570)
![Static Badge](https://img.shields.io/badge/python-2.26.0-badgeContent?style=flat&logo=Requests&logoColor=black&label=Requests&labelColor=%23B9848C&color=%23806491)
![Static Badge](https://img.shields.io/badge/python-2.9.9-badgeContent?style=flat&logo=Psycopg2&logoColor=black&label=Psycopg2&labelColor=%23b0d3bf&color=%231a512e)
![Static Badge](https://img.shields.io/badge/python-7.2.6-badgeContent?style=flat&logo=Sphinx&logoColor=black&label=Sphinx&labelColor=%23ed983b&color=%23ce3c03)
![Static Badge](https://img.shields.io/badge/python-3.1.3-badgeContent?style=flat&logo=Jinja2&logoColor=black&label=Jinja2&labelColor=%23778FD2&color=%232A3759)
![Static Badge](https://img.shields.io/badge/python-1.3.0-badgeContent?style=flat&logo=Pytest_flask&logoColor=black&label=Pytest_flask&labelColor=%23e4d6f8&color=%23604d9e)
![Static Badge](https://img.shields.io/badge/python-8.1.1-badgeContent?style=flat&logo=Pytest&logoColor=white&label=Pytest&labelColor=%231C252C&color=%23F6F2F6)

![Static Badge](https://img.shields.io/badge/python-2.3.3-badgeContent?style=flat&logo=Flask&logoColor=%2381BECE&label=Flask&labelColor=%23cad4e0&color=gray)
![Static Badge](https://img.shields.io/badge/python-3.1.1-badgeContent?style=flat&logo=Flask-SQLAlchemy&logoColor=%2381BECE&label=Flask-SQLAlchemy&labelColor=%23cd333e&color=%2383a259)
![Static Badge](https://img.shields.io/badge/python-0.6.2-badgeContent?style=flat&logo=Flask-Login&logoColor=%2381BECE&label=Flask-Login&labelColor=%23A7D1D2&color=%23153f65)
![Static Badge](https://img.shields.io/badge/python-2023.10.24-badgeContent?style=flat&logo=Flask-paginate&logoColor=%2381BECE&label=Flask-paginate&labelColor=%23D7A3B6&color=%2354387F)
![Static Badge](https://img.shields.io/badge/python-0.1.4-badgeContent?style=flat&logo=Flask_sslify&logoColor=%2381BECE&label=Flask_sslify&labelColor=%23FEF4C0&color=%23FE8535)
![Static Badge](https://img.shields.io/badge/python-1.1.2-badgeContent?style=flat&logo=Flask_wtf&logoColor=%2381BECE&label=Flask_wtf&labelColor=%236B99C3&color=%23022E66)
![Static Badge](https://img.shields.io/badge/python-3.0.0-badgeContent?style=flat&logo=Flask_limiter&logoColor=%2381BECE&label=Flask_limiter&labelColor=%23cd9e50&color=%23feeb9e)
![Static Badge](https://img.shields.io/badge/python-2.1.0-badgeContent?style=flat&logo=Flask_Caching&logoColor=%2381BECE&label=Flask_Caching&labelColor=%23945D87&color=%23EDD1EC)

![Static Badge](https://img.shields.io/badge/python-7.0.0-badgeContent?style=flat&logo=Flake8&logoColor=%2381BECE&label=Flake8&labelColor=black&color=white)
![Static Badge](https://img.shields.io/badge/python-0.0.8-badgeContent?style=flat&logo=Flake8-annotations-complexity&logoColor=%2381BECE&label=Flake8-annotations-complexity&labelColor=%23A59CD3&color=%234B2D9F)
![Static Badge](https://img.shields.io/badge/python-24.2.6-badgeContent?style=flat&logo=Flake8_bugbear&logoColor=%2381BECE&label=Flake8_bugbear&labelColor=%23677C77&color=%23E0EFEA)
![Static Badge](https://img.shields.io/badge/python-2.3.0-badgeContent?style=flat&logo=Flake8_builtins&logoColor=%2381BECE&label=Flake8_builtins&labelColor=%23EFB9AD&color=%23BC0000)
![Static Badge](https://img.shields.io/badge/python-3.14.0-badgeContent?style=flat&logo=Flake8_comprehensions&logoColor=%2381BECE&label=Flake8_comprehensions&labelColor=%23ffef03&color=%23ca540c)
![Static Badge](https://img.shields.io/badge/python-2.1.0-badgeContent?style=flat&logo=Flake8_commas&logoColor=%2381BECE&label=Flake8_commas&labelColor=%23C9D46C&color=%23338309)
![Static Badge](https://img.shields.io/badge/python-1.7.0-badgeContent?style=flat&logo=Flake8_docstrings&logoColor=%2381BECE&label=Flake8_docstrings&labelColor=%23015366&color=%23A7D1D2)
![Static Badge](https://img.shields.io/badge/python-1.5.0-badgeContent?style=flat&logo=Flake8_eradicate&logoColor=%2381BECE&label=Flake8_eradicate&labelColor=%23CEAD6D&color=%23E1DCE0)
![Static Badge](https://img.shields.io/badge/python-0.18.2-badgeContent?style=flat&logo=Flake8_import_order&logoColor=%2381BECE&label=Flake8_import_order&labelColor=%23806491&color=%23B9848C)
![Static Badge](https://img.shields.io/badge/python-2.1.0-badgeContent?style=flat&logo=Flake8_pep3101&logoColor=%2381BECE&label=Flake8_pep3101&labelColor=%23BC2041&color=%239E8279)
![Static Badge](https://img.shields.io/badge/python-5.0.0-badgeContent?style=flat&logo=Flake8_print&logoColor=%2381BECE&label=Flake8_print&labelColor=%23F38307&color=%23D5F2ED)
![Static Badge](https://img.shields.io/badge/python-0.3.0-badgeContent?style=flat&logo=Flake8_rst_docstrings&logoColor=%2381BECE&label=Flake8_rst_docstrings&labelColor=%23DE60CA&color=%23882380)
![Static Badge](https://img.shields.io/badge/python-0.3.0-badgeContent?style=flat&logo=Flake8_string_format&logoColor=%2381BECE&label=Flake8_string_format&labelColor=%236B99C3&color=%23022E66)
![Static Badge](https://img.shields.io/badge/python-0.3.0-badgeContent?style=flat&logo=Flake8_string_format&logoColor=%2381BECE&label=Flake8_string_format&labelColor=%23dde4ea&color=%236e7478)
![Static Badge](https://img.shields.io/badge/python-0.0.6-badgeContent?style=flat&logo=Flake8_variables_names&logoColor=%2381BECE&label=Flake8_variables_names&labelColor=%23adbf8f&color=%23788e3c)
___

## Структура сайта

* Страница: index - является главной страницей сайта, на которой расположена приветственная информация, кнопки навигации по каталогу, меню, а так же информация о работе магазина.
* Страницы: flowers, bouquets, baskets, indoor, artificial, wreaths, toys, fireworks - являются страницами каталога, одинаковыми по своей структуре, но разными по наполнению. В них располагаются карточки товаров (при наличии в базе данных) с фотографией товара, названием, его описанием и ценой. Так же при переполнении страницы более чем на 12 карточек, создаются дополнительные страницы навигации с новыми карточками. У администраторов на карточках имеется кнопка удаления товара.
* Страница: store_news - Является страницей с новостями магазина, блоки новостей расположены вертикально, по 4шт. на странице. Новость состоит из фото, название новости, текста новости и даты публикации. У администраторов на карточках имеется кнопка удаления новости.
* Страница: admin_login - Это страница авторизации для администраторов сайта. Админы добавляются в базу данных в ручную. Пароль должен добавляться в БД в виде хэша, для этого в каталоге проекта есть соответствующий инструмент "hash_pass".
* Страница: admin_menu - Это страница навигации по меню администратора. Здесь вы можете выбрать необходимый раздел.
* Страница: admin_panel - Представляет собой форму, с помощью которой можно добавить товары.
* Страница: admin_article - Представляет собой форму, с помощью которой можно добавить новости.

> ВАЖНО!: для авторизации администраторов, используется ссылка: https://your-ip/admin_login

___

## Инструкция по установке

1. После скачивания репозитория, распакуйте его в удобное место и откройте через ваш IDE.
2. Установка виртуальной среды и зависимостей:
    1. Если ваш IDE - **VS CODE** или **PyCharm**9, создайте виртуальную среду и установите зависимости с помощью файла requirements.txt
    2. Если же вы пользуетесь другими IDE, откройте в корневом каталоге проекта 
    **PowerShell**, через shift+ПКМ(и выберите PowerShell).
        1. Введите команду: **python -m venv venv**
        2. После установки среды, выполните её активацию: **venv\Scripts\activate**
        3. Далее установите зависимости: **pip install -r requirements.txt**
3. В файле handlers/config.py добавьте необходимые конфигурационные данные.
4. В подключённую базу данных добавляйте администраторов.

___

## Контакты

Моя почта: **ght070707@gmail.com**

Мой телеграм: **https://t.me/chicano_712**