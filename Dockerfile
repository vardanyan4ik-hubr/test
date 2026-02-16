# ==========================================
# Stage 1: Builder
# ==========================================
FROM python:3.11-slim as builder

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Production
# ==========================================
FROM python:3.11-slim

# Метаданные
LABEL maintainer="dev@onlanta.com"
LABEL description="Mikhalych Bot for MAX Messenger"
LABEL version="1.0.0"

# Устанавливаем системные зависимости для production
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для приложения
RUN useradd -m -u 1000 botuser && \
    mkdir -p /var/log/mikhalych_bot && \
    chown -R botuser:botuser /var/log/mikhalych_bot

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код приложения
COPY --chown=botuser:botuser . .

# Создаем директории для логов и временных файлов
RUN mkdir -p logs tmp && \
    chown -R botuser:botuser logs tmp

# Переключаемся на пользователя botuser
USER botuser

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PATH="/home/botuser/.local/bin:$PATH"

# Открываем порт
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
