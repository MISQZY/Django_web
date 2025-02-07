# Используем официальный образ Python
FROM python:3.13-slim-bullseye

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . .

# Открываем порт (если нужно)
EXPOSE 8000

# Выполняем миграции и собираем статику перед запуском
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Запуск сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]