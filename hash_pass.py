"""
Модуль предназначен для хэширования поролей.

Для совершения процесса хэширования, введите пороль в
функцию generate_password_hash переменной password, затем
запустите интерпиртатор и в терминале получите готовый хэш. 
"""
from werkzeug.security import generate_password_hash

password = generate_password_hash("Здесь вы можете ввести ваш пороль!")

print(password)
