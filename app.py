import config

from datetime import datetime
import pytz
import os

from flask import Flask, render_template, request, url_for, g, redirect, flash, session, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_paginate import Pagination
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from flask_wtf import FlaskForm
from wtforms import HiddenField
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_limiter import Limiter

from wtforms.validators import DataRequired, Length, NumberRange
from wtforms import StringField, PasswordField, SubmitField, \
    TextAreaField, FileField, FloatField, SelectField

from sqlalchemy import desc
from werkzeug.utils import secure_filename

import logging
from logging.handlers import RotatingFileHandler


# Подключение приложения
app = Flask(__name__)
sslify = SSLify(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config.from_object('config')


# Подклюбчение CSRF токена, для предотвращения CSRF атак
csrf = CSRFProtect(app)


# Подключение лимитера (ограниченные лимиты на запросы в период времени)
limiter = Limiter(app)


# Создание и настройка журнала
log_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
log_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
log_handler.setLevel(logging.INFO)
app.logger.addHandler(log_handler)

# Добавление обработчика журнала к объекту app.logger
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


# Подключение базы данных
db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 1024 * 1024


# Папка для загрузки файлов
UPLOAD_FOLDER = 'static/img/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Настройка Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# Таблица с админками
class UserAdmin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)


# Таблица с товарами
class Item(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(255))

    def __init__(self, name, description, price, category, photo):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.photo = photo


# Таблица с статьями
class Article(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_article = db.Column(db.String(300), nullable=False)
    text_article = db.Column(db.Text, nullable=False)
    photo_article = db.Column(db.String(255))
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name_article, text_article, photo_article, pub_date):
        self.name_article = name_article
        self.text_article = text_article
        self.photo_article = photo_article
        self.pub_date = pub_date


# Определение формы входа администратора с использованием Flask-WTF
class AdminLoginForm(FlaskForm):
    login = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


# Определение формы для удаления новостей
class DeleteItemsForm(FlaskForm):
    product_id = HiddenField(validators=[DataRequired()])
    delete_button = SubmitField('Удалить')


# Определение формы для добавления новостей
class AddArticleForm(FlaskForm):
    name_article = StringField('Название статьи', validators=[DataRequired()])
    text_article = TextAreaField('Текст статьи', validators=[DataRequired()])
    add_photo = FileField('Загрузить фото')
    submit = SubmitField('Добавить статью')


# Определение формы для добавления товаров
class AddItemForm(FlaskForm):
    name = StringField('Наименование товара',
                       validators=[DataRequired(),
                                   Length(min=3, max=15)])
    description = TextAreaField('Описание товара',
                                validators=[DataRequired(),
                                            Length(min=3)])
    price = FloatField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Категория',
                           choices=[('1', 'Категория 1'),
                                    ('2', 'Категория 2'),
                                    ('3', 'Категория 3'),
                                    ('4', 'Категория 4'),
                                    ('5', 'Категория 5'),
                                    ('6', 'Категория 6'),
                                    ('7', 'Категория 7'),
                                    ('8', 'Категория 8')],
                           coerce=int,
                           validators=[DataRequired()])
    photo = FileField('Фото товара')
    submit = SubmitField('Добавить товар')


# Определение формы для удаления статей
class DeleteArticleForm(FlaskForm):
    article_id = HiddenField(validators=[DataRequired()])
    delete_button = SubmitField('Удалить')


# Класс с методами проверки
class Checking:
    def __init__(self, text, category, message):
        self.text = text
        self.category = category
        self.message = message

    def check_admin():
        # Проверяет, аторизированн ли пользователь или нет
        if current_user.is_authenticated:
            return 'admin'
        else:
            return "no_admin"

    def check_name(self):
        # Проверяет чтобы значение было длиною от 3-х до 15-ти символов
        if not (3 < len(self.text) < 15):
            flash(self.message,
                  category=self.category)
            return False
        return True

    def check_description(self):
        # Проверяет чтобы значение было длиною от 3-х до 100-а символов
        if not (3 < len(self.text)):
            flash(self.message,
                  category=self.category)
            return False
        return True

    def check_latin(self):
        if any(c.isalpha() and c.isascii() for c in self.text):
            # Проверяет чтобы значение не содержало
            # символов из латинского(английского алфавита)
            flash(self.message,
                  category=self.category)
            return False
        return True

    def check_category(self):
        if self.text not in {'1', '2', '3', '4', '5', '6', '7', '8'}:
            flash(self.message,
                  category=self.category)
            return False
        return True


# Функция захвата id пользователя
@login_manager.user_loader
def load_user(user_id):
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    return UserAdmin.query.get(int(user_id))


# Обработчик главной страницы
@app.route('/index')
@app.route('/')
@limiter.limit("100 per minute")
def index():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    return render_template('index.html', check_total=Checking.check_admin())


# Обработчик входа в админ-панель с использованием Flask-WTF
@app.route('/admin_login', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def admin_login():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    form = AdminLoginForm()

    if form.validate_on_submit():
        username = form.login.data
        password = form.password.data

        user = UserAdmin.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('admin_menu'))
        else:
            flash('Ошибка входа. Проверьте имя пользователя и пароль.',
                  'error_user')

    return render_template('admin_login.html', form=form)


# Функция выхода из админ  панели
@app.route('/logout')
@limiter.limit("100 per minute")
@login_required
def logout():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    logout_user()
    return redirect(url_for('admin_login'))


# Обработчик админ меню с кнопками перехода
@app.route('/admin_menu', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
@login_required
def admin_menu():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    return render_template('admin_menu.html',
                           check_total=Checking.check_admin())


# Обработчик Панели с добавлением товаров
@app.route('/admin_panel', methods=['POST', 'GET'])
@limiter.limit("100 per minute")
@login_required
def admin_panel():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    form = AddItemForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            category = request.form['category']
            photo = request.files['photo']

            if photo:
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = None

            check_name = Checking(name,
                                  'error_panel',
                                  'ОШИБКА: НАЗВАНИЕ ДОЛЖНО ИМЕТЬ ОТ 3-х ДО 15 символов!')
            check_description = Checking(description,
                                         'error_panel',
                                         'ОШИБКА: ОПИСАНИЕ ДОЛЖНО СОСТОЯТЬ МИНИМУМ ИЗ 3-Х СИМВОЛОВ!')
            check_latin = Checking(description,
                                   'error_panel',
                                   'ОШИБКА: ОПИСАНИЕ ДОЛЖНО СОСТОЯТЬ ИЗ РУССКИХ СИМВОЛОВ!')
            check_category = Checking(category,
                                      'error_panel',
                                      'ОШИБКА: НУМЕРАЦИЯ КАТЕГОРИИ ОТ 1 ДО 8!')

            total = [
                check_name.check_name(),
                check_description.check_description(),
                check_latin.check_latin(),
                check_category.check_category()]

            if all(total) and filename is not None:
                try:
                    new_item = Item(name=name,
                                    description=description,
                                    price=price,
                                    category=category,
                                    photo=filename)
                    db.session.add(new_item)
                    db.session.commit()
                    flash('ТОВАР УСПЕШНО ДОБАВЛЕН!', category='success_panel')
                except Exception as ex:
                    print(ex)
            else:
                flash('НУЖНО ЗАГРУЗИТЬ ФОТО!', category='error_panel')
            return redirect(url_for('admin_panel'))
    return render_template('admin_panel.html',
                           check_total=Checking.check_admin(),
                           form=form)


# Обработчик Добавления статей
@app.route('/admin_article', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
@login_required
def admin_article():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    form = AddArticleForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name_article = request.form['name_article']
            text_article = request.form['text_article']
            photo_article = request.files['add_photo']

            utc_timezone = pytz.utc
            utc_time = datetime.now(utc_timezone)
            eet_timezone = pytz.timezone('EET')
            eet_time = utc_time.astimezone(eet_timezone)

            if photo_article:
                filename = secure_filename(photo_article.filename)
                photo_article.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                                filename))
            else:
                filename = None

            check_name_description = Checking(name_article,
                                              'error_article',
                                              'ОШИБКА: НАЗВАНИЕ ДОЛЖНО СОСТОЯТЬ МИНИМУМ ИЗ 3-Х СИМВОЛОВ!')
            check_name_latin = Checking(name_article,
                                        'error_article',
                                        'ОШИБКА: НАЗВАНИЕ ДОЛЖНО СОСТОЯТЬ ИЗ РУССКИХ СИМВОЛОВ!')
            check_text_latin = Checking(text_article,
                                        'error_article',
                                        'ОШИБКА: ОПИСАНИЕ ДОЛЖНО СОСТОЯТЬ ИЗ РУССКИХ СИМВОЛОВ!')
            check_text_description = Checking(text_article,
                                              'error_article',
                                              'ОШИБКА: ОПИСАНИЕ ДОЛЖНО СОСТОЯТЬ МИНИМУМ ИЗ 3-Х СИМВОЛОВ!')

            total = [
                check_name_description.check_description(),
                check_name_latin.check_latin(),
                check_text_latin.check_latin(),
                check_text_description.check_description()]

            if all(total) and filename is not None:
                try:
                    new_article = Article(name_article=name_article,
                                          text_article=text_article,
                                          photo_article=filename,
                                          pub_date=eet_time)
                    db.session.add(new_article)
                    db.session.commit()
                    flash('СТАТЬЯ УСПЕШНО ДОБАВЛЕНА!',
                          category='success_article')
                except Exception as ex:
                    print(ex)
            else:
                flash('НУЖНО ЗАГРУЗИТЬ ФОТО!', category='error_article')
            return redirect(url_for('admin_article'))
    return render_template('admin_article.html',
                           check_total=Checking.check_admin(),
                           form=form)


# Обработчик странички с новостями магазина
@app.route('/store_news', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def store_news():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    page = request.args.get('page', type=int, default=1)
    news = Article.query.order_by(desc(Article.pub_date)).paginate(page=page,
                                                                   per_page=3,
                                                                   error_out=False)
    pagination = Pagination(page=page,
                            total=news.total,
                            per_page=3,
                            bs_version=4)

    delete_form = DeleteArticleForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('article_id')
            item = Article.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('store_news'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении новости', 'error')

    return render_template('store_news.html',
                           form=delete_form,
                           news=news.items,
                           pagination=pagination,
                           total_pages=news.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы с цветами (поштучно)
@app.route('/flowers', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def flowers():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    app.logger.error('Страница не найдена: %s', request.url)
    page = request.args.get('page', type=int, default=1)
    products = Item.query.filter_by(category=1).paginate(page=page,
                                                         per_page=12,
                                                         error_out=False)
    pagination = Pagination(page=page,
                            total=products.total,
                            per_page=12,
                            bs_version=4)

    delete_form = DeleteItemsForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('product_id')
            item = Item.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('flowers'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении товара', 'error')

    return render_template('flowers.html',
                           form=delete_form,
                           products=products.items,
                           pagination=pagination,
                           total_pages=products.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы с букетами
@app.route('/bouquets', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def bouquets():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    page = request.args.get('page', type=int, default=1)
    products = Item.query.filter_by(category=2).paginate(page=page,
                                                         per_page=9,
                                                         error_out=False)
    pagination = Pagination(page=page,
                            total=products.total,
                            per_page=9,
                            bs_version=4)

    delete_form = DeleteItemsForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('product_id')
            item = Item.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('bouquets'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении товара', 'error')

    return render_template('bouquets.html',
                           form=delete_form,
                           products=products.items,
                           pagination=pagination,
                           total_pages=products.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы с корзинками
@app.route('/baskets', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def baskets():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    page = request.args.get('page', type=int, default=1)
    products = Item.query.filter_by(category=3).paginate(page=page,
                                                         per_page=9,
                                                         error_out=False)
    pagination = Pagination(page=page,
                            total=products.total,
                            per_page=9,
                            bs_version=4)

    delete_form = DeleteItemsForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('product_id')
            item = Item.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('baskets'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении товара', 'error')

    return render_template('baskets.html',
                           form=delete_form,
                           products=products.items,
                           pagination=pagination,
                           total_pages=products.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы с комнатными цветами
@app.route('/indoor', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def indoor():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    page = request.args.get('page', type=int, default=1)
    products = Item.query.filter_by(category=4).paginate(page=page,
                                                         per_page=9,
                                                         error_out=False)
    pagination = Pagination(page=page,
                            total=products.total,
                            per_page=9,
                            bs_version=4)

    delete_form = DeleteItemsForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('product_id')
            item = Item.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('indoor'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении товара', 'error')

    return render_template('indoor.html',
                           form=delete_form,
                           products=products.items,
                           pagination=pagination,
                           total_pages=products.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы с искуственными цветами
@app.route('/artificial', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def artificial():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    page = request.args.get('page', type=int, default=1)
    products = Item.query.filter_by(category=5).paginate(page=page,
                                                         per_page=9,
                                                         error_out=False)
    pagination = Pagination(page=page,
                            total=products.total,
                            per_page=9,
                            bs_version=4)

    delete_form = DeleteItemsForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('product_id')
            item = Item.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('artificial'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении товара', 'error')

    return render_template('artificial.html',
                           form=delete_form,
                           products=products.items,
                           pagination=pagination,
                           total_pages=products.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы с венками
@app.route('/wreaths', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def wreaths():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    page = request.args.get('page', type=int, default=1)
    products = Item.query.filter_by(category=6).paginate(page=page,
                                                         per_page=9,
                                                         error_out=False)
    pagination = Pagination(page=page,
                            total=products.total,
                            per_page=9,
                            bs_version=4)

    delete_form = DeleteItemsForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('product_id')
            item = Item.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('wreaths'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении товара', 'error')

    return render_template('wreaths.html',
                           form=delete_form,
                           products=products.items,
                           pagination=pagination,
                           total_pages=products.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы с игрушками
@app.route('/toys', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def toys():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    page = request.args.get('page', type=int, default=1)
    products = Item.query.filter_by(category=7).paginate(page=page,
                                                         per_page=9,
                                                         error_out=False)
    pagination = Pagination(page=page,
                            total=products.total,
                            per_page=9,
                            bs_version=4)

    delete_form = DeleteItemsForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('product_id')
            item = Item.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('toys'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении товара', 'error')

    return render_template('toys.html',
                           form=delete_form,
                           products=products.items,
                           pagination=pagination,
                           total_pages=products.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы с фейерверками
@app.route('/fireworks', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def fireworks():
    app.logger.info('Входящий запрос: %s %s', request.method, request.path)
    page = request.args.get('page', type=int, default=1)
    products = Item.query.filter_by(category=8).paginate(page=page,
                                                         per_page=9,
                                                         error_out=False)
    pagination = Pagination(page=page,
                            total=products.total,
                            per_page=9,
                            bs_version=4)

    delete_form = DeleteItemsForm()

    if request.method == 'POST':
        if delete_form.validate_on_submit():
            item_id = request.form.get('product_id')
            item = Item.query.get(item_id)
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    return redirect(url_for('fireworks'))
                except Exception as ex:
                    print(ex)
        else:
            print('Ошибка при удалении товара', 'error')

    return render_template('fireworks.html',
                           form=delete_form,
                           products=products.items,
                           pagination=pagination,
                           total_pages=products.pages,
                           check_total=Checking.check_admin())


# Обработчик страницы "404"
@app.errorhandler(404)
@limiter.limit("100 per minute")
def page_not_found(error):
    app.logger.error('Страница не найдена: %s', request.url)
    return render_template('page_not_found.html'), 404


# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    db.create_all()
