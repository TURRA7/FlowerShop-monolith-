# Сайт витрина - FlowerShop

Это приложение представляет собой сайт-витрину на цветочную и сувенирную тематику. Приложение построено на языке **Python** с использованием фреймворка **Flask**.

---

### Краткое описание структуры проекта

* **authorization**: Модуль для работы с авторизацией пользователей.
* **cute_form**: Модуль для работы с формами на Flask с использованием **Flask-WTForms**.
* **database_create**: Модуль для работы с базой данных через **Flask-SQLAlchemy**.
* **handlers**: Модуль с обработчиками, шаблонами и статическими файлами.
* **pagination_create**: Модуль для создания пагинации страниц.
* **tests**: Модуль с тестами для проверки функционала проекта.
* **app.py**: Исполнительный файл проекта, запускающий приложение.
* **content_flask.py**: Модуль с контентом в виде словарей с текстами.
* **docker-compose.yaml**: Конфигурация для **Docker Compose**, позволяющая запускать несколько сервисов.
* **Dockerfile**: Конфигурация для создания контейнера с основным приложением.
* **hash_pass.py**: Утилита для хеширования паролей.
* **log_mod.py**: Модуль для логирования работы приложения.
* **Login details.txt**: Примеры данных для таблицы **UserAdmin**.
* **nginx.conf**: Конфигурация для веб-сервера **Nginx**.
* **README.md**: Файл с описанием проекта.
* **requirements.txt**: Список зависимостей, необходимых для работы проекта.
* **setup.cfg**: Конфигурационный файл для **Flake8** (инструмент для проверки стиля кода).

---

### Инструменты, использованные в проекте

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

---

### Установка и запуск проекта

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/username/FlowerShop.git
    ```

2. Перейдите в папку с проектом:

    ```bash
    cd FlowerShop
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Для запуска приложения используйте команду:

    ```bash
    python app.py
    ```

5. Откройте браузер и перейдите по адресу [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

### Логирование и тестирование

Для включения логирования выполните:

```bash
python log_mod.py
