FROM python:3.11.9

# Просто проверка команды
RUN echo ls

# Устанавливаем рабочую директорию
WORKDIR /app

RUN echo ls

# Устанавливаем netcat для проверки, что Postgres поднят
RUN apt-get update && apt-get install -y netcat-openbsd

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app

# Добавляем рабочую директорию в PYTHONPATH, чтобы Python видел модуль src
ENV PYTHONPATH=/app

# Ждём БД → делаем миграции → запускаем приложение
CMD ["sh", "-c", "until nc -z booking_db 5432; do echo waiting for db; sleep 1; done; alembic upgrade head; python src/main.py"]