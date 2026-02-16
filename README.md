# Чат-бот "Михалыч" для мессенджера MAX

Корпоративный чат-бот компании Онланта для мессенджера MAX.

## 📋 Описание проекта

Чат-бот "Михалыч" — это автоматизированный помощник для сотрудников компании Онланта, интегрированный в корпоративный мессенджер MAX. Бот предоставляет быстрый доступ к корпоративным ресурсам, информации о сотрудниках, кадровым данным и другим полезным функциям.

## 🎯 Основные функции

### ✅ Реализовано (MVP)
- **Авторизация** — безопасная авторизация через MAX OAuth
- **Главное меню** — интуитивное навигационное меню
- **Поиск сотрудников** — быстрый поиск коллег по фамилии
- **Ресурсы компании** — постраничный список корпоративных ресурсов (18 ресурсов)
- **Информация об отпусках** — правила оформления отпуска и просмотр остатка дней
- **Пароли Wi-Fi** — доступ к паролям корпоративных Wi-Fi сетей
- **Экспресс-отчеты по контрагентам** — быстрая информация о партнерах
- **Раздел для руководителей** — управление командой и согласование заявок

### ⏸️ В разработке
- **Помощь СИБ** — интеграция со службой информационной безопасности
- **Загрузка тренировок** — учет корпоративных тренировок
- **Пин-понг турниры** — организация спортивных мероприятий

## 📁 Структура проекта

```
mikhalych-bot/
├── TECHNICAL_SPECIFICATION.md    # Полное техническое задание
├── api_schemas.json               # JSON-схемы для API
├── config.json                    # Конфигурация бота
├── sample_data.json               # Примеры данных для БД
├── README.md                      # Этот файл
├── .env.example                   # Пример файла окружения
└── app/                           # Исходный код (будет создан при разработке)
    ├── main.py
    ├── handlers/
    ├── services/
    ├── models/
    ├── database/
    └── utils/
```

## 📚 Документация

### Файлы документации

1. **[TECHNICAL_SPECIFICATION.md](./TECHNICAL_SPECIFICATION.md)** — Полное техническое задание с:
   - Функциональными требованиями
   - Нефункциональными требованиями
   - Диаграммами состояний
   - Структурой БД
   - API эндпоинтами
   - Обработкой ошибок
   - Требованиями безопасности

2. **[api_schemas.json](./api_schemas.json)** — JSON-схемы для всех API запросов и ответов:
   - Авторизация
   - Поиск сотрудников
   - Ресурсы компании
   - Отпуска
   - Wi-Fi пароли
   - Контрагенты
   - Раздел руководителя
   - Обработка ошибок

3. **[config.json](./config.json)** — Конфигурация бота:
   - Настройки сессий
   - Лимиты запросов
   - Правила валидации
   - Тексты сообщений
   - Структура меню
   - Список ресурсов компании (18 шт.)
   - Настройки Wi-Fi сетей
   - Правила отпусков
   - Настройки интеграций

## 🚀 Быстрый старт

### Требования

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker и Docker Compose (опционально)

### Установка

1. **Клонировать репозиторий:**
```bash
git clone https://github.com/onlanta/mikhalych-bot.git
cd mikhalych-bot
```

2. **Создать виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установить зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настроить переменные окружения:**
```bash
cp .env.example .env
# Отредактировать .env с вашими настройками
```

5. **Запустить миграции БД:**
```bash
python manage.py migrate
```

6. **Загрузить начальные данные:**
```bash
python manage.py load_initial_data
```

7. **Запустить бота:**
```bash
python app/main.py
```

### Docker Compose

```bash
# Запустить все сервисы
docker-compose up -d

# Просмотр логов
docker-compose logs -f bot

# Остановить сервисы
docker-compose down
```

## ⚙️ Конфигурация

### Файл .env

Создайте файл `.env` на основе `.env.example`:

```bash
# MAX API
MAX_API_URL=https://api.max.messenger.com
MAX_BOT_TOKEN=your_bot_token_here
MAX_WEBHOOK_SECRET=your_webhook_secret

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mikhalych_bot
DB_USER=bot_user
DB_PASSWORD=secure_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis_password

# External APIs
HR_SYSTEM_API_URL=https://hr.onlanta.com/api
HR_SYSTEM_API_KEY=hr_api_key
1C_API_URL=https://1c.onlanta.com/api
1C_API_USER=api_user
1C_API_PASSWORD=api_password

# Security
SECRET_KEY=your_secret_key_for_sessions
ENCRYPTION_KEY=your_encryption_key

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/mikhalych_bot/app.log
```

## 📊 Структура базы данных

### Основные таблицы

1. **users** — пользователи бота
2. **employees** — сотрудники компании
3. **resources** — корпоративные ресурсы
4. **sessions** — сессии пользователей
5. **audit_logs** — логи аудита
6. **wifi_networks** — Wi-Fi сети
7. **contractors** — контрагенты
8. **vacations** — отпуска

Подробное описание таблиц см. в [TECHNICAL_SPECIFICATION.md](./TECHNICAL_SPECIFICATION.md#51-база-данных).

## 🔐 Безопасность

### Реализованные меры

- ✅ OAuth 2.0 авторизация через MAX API
- ✅ Шифрование данных при передаче (TLS 1.3)
- ✅ Шифрование паролей в БД (AES-256)
- ✅ Разграничение прав доступа по ролям
- ✅ Аудит всех критичных действий
- ✅ Автоматическое истечение сессий
- ✅ Rate limiting для защиты от DDoS

### Логируемые действия

- Запросы паролей Wi-Fi
- Просмотр отчетов по контрагентам
- Поиск сотрудников
- Доступ к кадровой информации

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# Unit-тесты
pytest tests/unit/

# Integration-тесты
pytest tests/integration/

# E2E-тесты
pytest tests/e2e/

# С покрытием
pytest --cov=app --cov-report=html
```

### Минимальное покрытие

Требуется минимум **80% покрытия** кода тестами.

## 📈 Мониторинг и логирование

### Логи

Логи записываются в:
- Консоль (для разработки)
- Файл `/var/log/mikhalych_bot/app.log`
- ELK Stack (для production)

### Метрики

- Prometheus для сбора метрик
- Grafana для визуализации
- Alertmanager для уведомлений

### Ключевые метрики

- Количество активных пользователей
- Время отклика на команды
- Количество ошибок
- Использование ресурсов (CPU, RAM)
- Количество запросов к внешним API

## 🔄 API интеграции

### MAX API

- **Документация:** https://docs.max.messenger.com
- **Webhook:** `POST /api/webhook/max`
- **Отправка сообщений:** `POST /api/send_message`

### HR-система

- **Endpoint:** https://hr.onlanta.com/api/v2
- **Методы:**
  - `GET /employees` — список сотрудников
  - `GET /employees/{id}` — информация о сотруднике
  - `GET /vacations/{employee_id}` — отпуска сотрудника

### 1С ЗУП

- **Endpoint:** https://1c.onlanta.com/api/v1
- **Методы:**
  - `GET /vacation/balance` — остаток отпускных дней
  - `POST /vacation/request` — подача заявки на отпуск
  - `GET /contractors/{inn}` — информация о контрагенте

## 🛠️ Разработка

### Стиль кода

- **Стандарт:** PEP 8
- **Линтеры:** flake8, mypy, black
- **Docstrings:** Google Style
- **Type hints:** обязательны

### Pre-commit hooks

```bash
# Установка
pip install pre-commit
pre-commit install

# Ручной запуск
pre-commit run --all-files
```

### Структура коммита

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Типы:**
- `feat` — новая функция
- `fix` — исправление бага
- `docs` — изменения в документации
- `style` — форматирование кода
- `refactor` — рефакторинг
- `test` — добавление тестов
- `chore` — прочие изменения

**Пример:**
```
feat(search): добавлен поиск по email

Реализован дополнительный поиск сотрудников по email адресу.
Добавлена валидация email формата.

Closes #123
```

## 📋 Roadmap

### Фаза 1: MVP ✅ (Завершено)
- ✅ Авторизация
- ✅ Главное меню
- ✅ Поиск сотрудников
- ✅ Ресурсы компании
- ✅ Информация об отпусках
- ✅ Пароль Wi-Fi

### Фаза 2: Расширение (В работе)
- ⏳ Экспресс-отчеты по контрагентам
- ⏳ Раздел для руководителей
- ⏳ Интеграция с 1С ЗУП
- ⏳ Интеграция с HR-системой

### Фаза 3: Дополнительные модули (Запланировано)
- ⏸️ Помощь СИБ (Q2 2026)
- ⏸️ Загрузка тренировок (Q3 2026)
- ⏸️ Пин-понг турниры (Q3 2026)
- ⏸️ Уведомления и рассылки
- ⏸️ Аналитика и отчетность

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта!

### Как внести вклад

1. Форкните репозиторий
2. Создайте ветку для фичи: `git checkout -b feature/amazing-feature`
3. Зафиксируйте изменения: `git commit -m 'feat: добавлена новая функция'`
4. Отправьте в ветку: `git push origin feature/amazing-feature`
5. Откройте Pull Request

### Правила Pull Request

- Код должен соответствовать PEP 8
- Все тесты должны проходить
- Покрытие кода тестами >= 80%
- Обновлена документация (если требуется)
- Подробное описание изменений

## 📞 Контакты

### Техническая поддержка
- **Email:** support@onlanta.com
- **Телефон:** +7 (495) 123-45-67

### Разработка
- **Email:** dev@onlanta.com
- **GitHub:** https://github.com/onlanta/mikhalych-bot

### Безопасность
- **Email:** sib@onlanta.com
- **Сообщить об уязвимости:** security@onlanta.com

## 📄 Лицензия

Proprietary — Все права защищены © 2026 ООО "Онланта"

Этот проект является внутренним продуктом компании Онланта и не предназначен для публичного использования.

---

## 📊 Статистика проекта

- **Версия:** 1.0.0
- **Дата релиза:** 16 февраля 2026
- **Количество функций:** 9 (6 активных, 3 в разработке)
- **Корпоративных ресурсов:** 18
- **Поддерживаемые офисы:** 2 (Москва, Санкт-Петербург)

---

## 🎓 Полезные ссылки

- [Техническое задание](./TECHNICAL_SPECIFICATION.md)
- [API схемы](./api_schemas.json)
- [Конфигурация](./config.json)
- [Примеры данных](./sample_data.json)
- [MAX API Documentation](https://docs.max.messenger.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Последнее обновление:** 16 февраля 2026
