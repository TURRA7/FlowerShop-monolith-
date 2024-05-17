# Задаём базовый образ Linux + Python 3.11.5
FROM python:3.11.5-alpine3.18

# Установка системных зависимостей для psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Задаём рабочую папку
WORKDIR /app

# Копируем файлы из рабочей OS, в рабочую папку docker image
COPY .. /app

# Установка зависимостей для проекта
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска контейнера
ENTRYPOINT ["python3", "app.py"]