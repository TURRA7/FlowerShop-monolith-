from flask_wtf import FlaskForm
from wtforms import HiddenField

from wtforms.validators import DataRequired, Length, NumberRange
from wtforms import StringField, PasswordField, SubmitField, \
    TextAreaField, FileField, FloatField, SelectField


class AdminLoginForm(FlaskForm):
    '''
    Класс определяет форму входа админов.
    '''

    login: str = StringField('Имя пользователя', validators=[DataRequired()])
    password: str = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class DeleteItemsForm(FlaskForm):
    '''
    Класс определяет форму удаления товаров.
    '''

    product_id: int = HiddenField(validators=[DataRequired()])
    delete_button = SubmitField('Удалить')


class DeleteArticleForm(FlaskForm):
    '''
    Класс определяет форму удаления новостей.
    '''
    article_id = HiddenField(validators=[DataRequired()])
    delete_button = SubmitField('Удалить')


class AddArticleForm(FlaskForm):
    '''
    Класс определяет форму добавления новостей.
    '''

    name_article: str = StringField('Название статьи',
                                    validators=[DataRequired()])
    text_article: str = TextAreaField('Текст статьи',
                                      validators=[DataRequired()])
    add_photo: str = FileField('Загрузить фото')
    submit = SubmitField('Добавить статью')


class AddItemForm(FlaskForm):
    '''
    Класс определяет форму добавления товаров.
    '''

    name: str = StringField('Наименование товара',
                            validators=[DataRequired(),
                                        Length(min=3, max=15)])
    description: str = TextAreaField('Описание товара',
                                     validators=[DataRequired(),
                                                 Length(min=3)])
    price: int = FloatField('Цена', validators=[DataRequired(),
                                                NumberRange(min=0)])
    category: int = SelectField('Категория',
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
    photo: str = FileField('Фото товара')
    submit = SubmitField('Добавить товар')
