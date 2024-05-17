"""Модуль определяет формы для приложения Flask.

Модуль содержит следующие классы форм:
    - AdminLoginForm: Форма входа администратора.
    - DeleteItemsForm: Форма удаления товаров.
    - DeleteArticleForm: Форма удаления новостей.
    - AddArticleForm: Форма добавления новостей.
    - AddItemForm: Форма добавления товаров.
"""

from flask_wtf import FlaskForm

from wtforms import (
    FileField, PasswordField, SelectField, StringField, 
    SubmitField, DecimalField)
from wtforms import HiddenField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileRequired, FileAllowed


class AdminLoginForm(FlaskForm):
    """Класс определяет форму входа админов."""

    login: str = StringField('Имя пользователя', validators=[DataRequired()])
    password: str = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class DeleteItemsForm(FlaskForm):
    """Класс определяет форму удаления товаров."""

    product_id: int = HiddenField(validators=[DataRequired()])
    delete_button = SubmitField('Удалить')


class DeleteArticleForm(FlaskForm):
    """Класс определяет форму удаления новостей."""

    article_id = HiddenField(validators=[DataRequired()])
    delete_button = SubmitField('Удалить')


class AddArticleForm(FlaskForm):
    """Класс определяет форму добавления новостей."""

    name_article: str = StringField('Название статьи',
                                    validators=[DataRequired(),
                                                Length(min=3)])
    text_article: str = StringField('Текст статьи',
                                    validators=[DataRequired(),
                                                Length(min=3)])
    add_photo: str = FileField('Загрузить фото', validators=[FileRequired(),
                               FileAllowed(['jpg', 'jpeg', 'png'],
                                           'Только форматы: JPG, JPEG и PNG')])
    submit = SubmitField('Добавить статью')


class AddItemForm(FlaskForm):
    """Класс определяет форму добавления товаров."""

    name: str = StringField('Наименование товара',
                            validators=[DataRequired(),
                                        Length(min=3, max=15)])
    description: str = StringField('Описание товара',
                                   validators=[DataRequired(),
                                               Length(min=3)])
    price: int = DecimalField('Цена', validators=[DataRequired(),
                                                  NumberRange(min=1)])
    category: int = SelectField('Категория',
                                choices=[('1', 'ЦВЕТЫ'),
                                         ('2', 'БУКЕТЫ'),
                                         ('3', 'КОРЗИНКИ'),
                                         ('4', 'КОМНАТНЫЕ'),
                                         ('5', 'ИСКУСТВЕННЫЕ'),
                                         ('6', 'ВЕНКИ'),
                                         ('7', 'ИГРУШКИ'),
                                         ('8', 'ФЕЙЕРВЕРКИ')],
                                coerce=int,
                                validators=[DataRequired(),
                                            NumberRange(min=1, max=8)])
    photo: str = FileField('Фото товара', validators=[FileRequired(),
                           FileAllowed(['jpg', 'jpeg', 'png'],
                                       'Только форматы: JPG, JPEG и PNG')])
    submit = SubmitField('Добавить товар')
