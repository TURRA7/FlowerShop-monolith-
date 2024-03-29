"""Это главный исполняемый файл приложения.

Этот файл инициализирует приложение Flask,
настраивает маршруты и запускает приложение.
"""
from database_create.FDataBase import Article, Item, UserAdmin, db
from handlers.handler_flask import app, HomePage, \
    HandlersItem, AdminLogin, Logout, AdminMenu, AdminPanel, AdminArcticel


app.add_url_rule("/", view_func=HomePage.as_view(name='index',
                                                 html_path='index.html'))
app.add_url_rule("/flowers/",
                 view_func=HandlersItem.as_view(name="flowers",
                                                name_page="flowers",
                                                number=1, amount_item=12,
                                                table_db=Item,
                                                name_id='product_id',
                                                method_pag="catalog"))
app.add_url_rule("/bouquets/",
                 view_func=HandlersItem.as_view(name="bouquets",
                                                name_page="bouquets",
                                                number=2, amount_item=1212,
                                                table_db=Item,
                                                name_id='product_id',
                                                method_pag="catalog"))
app.add_url_rule("/baskets/",
                 view_func=HandlersItem.as_view(name="baskets",
                                                name_page="baskets",
                                                number=3, amount_item=1212,
                                                table_db=Item,
                                                name_id='product_id',
                                                method_pag="catalog"))
app.add_url_rule("/indoor/",
                 view_func=HandlersItem.as_view(name="indoor",
                                                name_page="indoor",
                                                number=4, amount_item=1212,
                                                table_db=Item,
                                                name_id='product_id',
                                                method_pag="catalog"))
app.add_url_rule("/artificial/",
                 view_func=HandlersItem.as_view(name="artificial",
                                                name_page="artificial",
                                                number=5, amount_item=1212,
                                                table_db=Item,
                                                name_id='product_id',
                                                method_pag="catalog"))
app.add_url_rule("/wreaths/",
                 view_func=HandlersItem.as_view(name="wreaths",
                                                name_page="wreaths",
                                                number=6, amount_item=1212,
                                                table_db=Item,
                                                name_id='product_id',
                                                method_pag="catalog"))
app.add_url_rule("/toys/",
                 view_func=HandlersItem.as_view(name="toys",
                                                name_page="toys",
                                                number=7, amount_item=1212,
                                                table_db=Item,
                                                name_id='product_id',
                                                method_pag="catalog"))
app.add_url_rule("/fireworks/",
                 view_func=HandlersItem.as_view(name="fireworks",
                                                name_page="fireworks",
                                                number=8, amount_item=1212,
                                                table_db=Item,
                                                name_id='product_id',
                                                method_pag="catalog"))
app.add_url_rule("/store_news/",
                 view_func=HandlersItem.as_view(name="store_news",
                                                name_page="store_news",
                                                number=None, amount_item=123,
                                                table_db=Article,
                                                name_id='article_id',
                                                method_pag="news"))
app.add_url_rule("/admin_login",
                 view_func=AdminLogin.as_view(name='admin_login',
                                              name_page='admin_login',
                                              name_db=UserAdmin,
                                              redirect_menu='admin_menu'))
app.add_url_rule("/logout",
                 view_func=Logout.as_view(name='logout',
                                          redirect_name='admin_login'))
app.add_url_rule("/admin_menu",
                 view_func=AdminMenu.as_view(name='admin_menu',
                                             name_page='admin_menu'))
app.add_url_rule("/admin_panel",
                 view_func=AdminPanel.as_view(name='admin_panel',
                                              name_page='admin_panel'))
app.add_url_rule("/admin_article",
                 view_func=AdminArcticel.as_view(name='admin_article',
                                                 name_page="admin_article"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
