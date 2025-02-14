# Базовый образ с Python
FROM python:3.11-slim as builder

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-slim

# Копирование установленных пакетов из builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Установка рабочей директории
WORKDIR /app

# Копирование проекта
COPY . .

# Создание непривилегированного пользователя
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Команда запуска приложения
CMD ["gunicorn", "UMRA.wsgi:application", "--bind", "0.0.0.0:8000"]

