"""
Данный модуль предназначен для тестирования обработчиков страниц.

...
"""


def test_home_page(test_client):
    """
    Функция проверяет подключение к странице '/'.

    ...
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert "Открытка к букету" in response.data.decode('utf-8')
