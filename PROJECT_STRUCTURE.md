# Структура проекта

```
telegram-assyst-bot/
│
├── src/                          # Исходный код приложения
│   ├── __init__.py
│   ├── main.py                   # Точка входа приложения
│   ├── config.py                 # Конфигурация приложения
│   │
│   ├── bot/                      # Модуль Telegram бота
│   │   ├── __init__.py
│   │   ├── handlers/             # Обработчики команд и сообщений
│   │   │   ├── __init__.py
│   │   │   ├── start.py          # /start, согласие на ПД
│   │   │   ├── auth.py           # Авторизация по email
│   │   │   ├── tickets.py        # Создание заявок
│   │   │   ├── my_requests.py    # /myrequests
│   │   │   └── confirmation.py   # Согласование закрытия
│   │   ├── keyboards.py          # Клавиатуры бота
│   │   ├── messages.py           # Шаблоны сообщений
│   │   ├── states.py             # Состояния FSM
│   │   └── bot.py                # Инициализация бота
│   │
│   ├── api/                      # API endpoints (webhook)
│   │   ├── __init__.py
│   │   ├── app.py                # FastAPI приложение
│   │   ├── routes/               # Маршруты API
│   │   │   ├── __init__.py
│   │   │   └── webhook.py        # /itsm-bot/webhook
│   │   └── schemas.py            # Pydantic схемы
│   │
│   ├── database/                 # Работа с базой данных
│   │   ├── __init__.py
│   │   ├── engine.py             # Подключение к БД
│   │   ├── models.py             # SQLAlchemy модели
│   │   ├── repositories/         # Репозитории для работы с данными
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # Работа с пользователями
│   │   │   ├── ticket.py         # Работа с заявками
│   │   │   ├── verification.py   # Коды подтверждения
│   │   │   └── rate_limit.py     # Ограничения
│   │   └── migrations/           # Alembic миграции
│   │
│   ├── services/                 # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── auth_service.py       # Авторизация
│   │   ├── ticket_service.py     # Создание и управление заявками
│   │   ├── email_service.py      # Отправка email
│   │   ├── apex_service.py       # Интеграция с Apex
│   │   ├── assyst_service.py     # Интеграция с Assyst
│   │   ├── rate_limit_service.py # Управление лимитами
│   │   └── notification_service.py # Уведомления
│   │
│   ├── models/                   # Модели данных (Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py               # Модель пользователя
│   │   ├── ticket.py             # Модель заявки
│   │   ├── webhook.py            # Модели webhook событий
│   │   └── enums.py              # Перечисления
│   │
│   └── utils/                    # Вспомогательные функции
│       ├── __init__.py
│       ├── validators.py         # Валидация данных
│       ├── formatters.py         # Форматирование текста
│       ├── file_handler.py       # Обработка файлов
│       ├── redis_client.py       # Redis клиент
│       └── logger.py             # Настройка логирования
│
├── tests/                        # Тесты
│   ├── __init__.py
│   ├── conftest.py               # Фикстуры pytest
│   ├── test_auth.py              # Тесты авторизации
│   ├── test_tickets.py           # Тесты заявок
│   ├── test_webhook.py           # Тесты webhook
│   └── test_validators.py        # Тесты валидации
│
├── logs/                         # Директория для логов
│   └── .gitkeep
│
├── .env.example                  # Пример файла переменных окружения
├── .gitignore                    # Игнорируемые файлы git
├── requirements.txt              # Python зависимости
├── Dockerfile                    # Docker образ
├── docker-compose.yml            # Docker Compose конфигурация
├── Makefile                      # Команды для управления проектом
├── README.md                     # Основная документация
├── TECHNICAL_SPECIFICATION.md    # Техническое задание
└── PROJECT_STRUCTURE.md          # Этот файл
```

## Описание модулей

### 1. `src/bot/` - Telegram бот

Содержит всю логику взаимодействия с пользователями через Telegram:

- **handlers/** - обработчики различных команд и сообщений
  - `start.py` - команда /start, согласие на обработку ПД
  - `auth.py` - процесс авторизации по email
  - `tickets.py` - создание новых заявок
  - `my_requests.py` - просмотр списка заявок
  - `confirmation.py` - обработка согласования закрытия

- **keyboards.py** - inline и reply клавиатуры
- **messages.py** - шаблоны текстовых сообщений
- **states.py** - состояния конечного автомата (FSM)
- **bot.py** - инициализация и запуск бота

### 2. `src/api/` - Webhook API

FastAPI приложение для приема webhook от Assyst:

- **routes/webhook.py** - endpoint `/itsm-bot/webhook`
- **schemas.py** - Pydantic схемы для валидации webhook данных

### 3. `src/database/` - База данных

SQLAlchemy модели и репозитории:

- **models.py** - ORM модели (Users, Tickets, Confirmations и т.д.)
- **repositories/** - паттерн Repository для работы с данными
- **migrations/** - миграции Alembic

### 4. `src/services/` - Бизнес-логика

Сервисы для реализации основной логики:

- **auth_service.py** - генерация кодов, проверка в Apex
- **ticket_service.py** - создание и обновление заявок
- **email_service.py** - отправка email в Assyst
- **apex_service.py** - HTTP клиент для Apex API
- **rate_limit_service.py** - проверка лимитов создания заявок
- **notification_service.py** - отправка уведомлений пользователям

### 5. `src/models/` - Модели данных

Pydantic модели для типизации:

- **user.py** - модель пользователя
- **ticket.py** - модель заявки
- **webhook.py** - модели событий от Assyst
- **enums.py** - перечисления (статусы, типы событий)

### 6. `src/utils/` - Утилиты

Вспомогательные функции:

- **validators.py** - валидация email, описания, файлов
- **formatters.py** - форматирование дат, текста
- **file_handler.py** - обработка изображений
- **redis_client.py** - кэширование и rate limiting

## Потоки данных

### Создание заявки пользователем

```
User → Bot Handler → Ticket Service → Email Service → Assyst
                        ↓
                   Database
                        ↓
                   Rate Limit Service
```

### Webhook от Assyst

```
Assyst → API Webhook → Assyst Service → Database
                            ↓
                    Notification Service → Bot → User
```

## База данных

Основные таблицы:

1. **users** - пользователи бота
2. **tickets** - заявки
3. **verification_codes** - коды подтверждения
4. **rate_limits** - лимиты пользователей
5. **confirmations** - запросы согласования закрытия

## Основные зависимости

- **python-telegram-bot** - Telegram Bot API
- **fastapi** - веб-фреймворк для webhook
- **sqlalchemy** - ORM для работы с БД
- **redis** - кэширование и rate limiting
- **aiosmtplib** - отправка email
- **httpx** - HTTP клиент для Apex API

## Команды управления

```bash
# Установка зависимостей
make install

# Запуск приложения
make run

# Запуск тестов
make test

# Линтинг кода
make lint

# Форматирование кода
make format

# Docker
make docker-up     # Запустить все сервисы
make docker-down   # Остановить все сервисы
make docker-logs   # Просмотр логов
```

## Переменные окружения

Все настройки задаются через файл `.env`:

```bash
# Скопировать пример
cp .env.example .env

# Отредактировать файл
nano .env
```

Обязательные переменные:
- `TELEGRAM_BOT_TOKEN` - токен бота от BotFather
- `DATABASE_URL` - строка подключения к PostgreSQL
- `APEX_API_URL` и `APEX_API_KEY` - доступ к Apex
- `SMTP_*` - настройки SMTP для отправки email

## Развертывание

### Development

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить БД и Redis через Docker
docker-compose up -d db redis

# Применить миграции
alembic upgrade head

# Запустить приложение
python -m src.main
```

### Production (Docker)

```bash
# Собрать и запустить все сервисы
docker-compose up -d

# Применить миграции
docker-compose exec bot alembic upgrade head

# Просмотр логов
docker-compose logs -f bot
```

## Мониторинг

Логи приложения сохраняются в:
- `stdout` - для Docker
- `logs/bot.log` - файловая система (ротация 10 МБ, хранение 30 дней)

## Безопасность

- Все секреты хранятся в `.env` (не коммитятся в git)
- HTTPS для webhook endpoint
- Валидация всех входящих данных через Pydantic
- Rate limiting через Redis
- Логирование всех действий

## Тестирование

```bash
# Запуск всех тестов
pytest

# С покрытием кода
pytest --cov=src --cov-report=html

# Только определенный модуль
pytest tests/test_auth.py -v
```

## Миграции БД

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "описание изменений"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1
```
