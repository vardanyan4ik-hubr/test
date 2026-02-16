# Диаграммы состояний чат-бота "Михалыч"

## Основная диаграмма состояний

```mermaid
stateDiagram-v2
    [*] --> UNAUTHORIZED: Первый запуск
    
    UNAUTHORIZED --> AUTH_PENDING: Команда /start
    AUTH_PENDING --> AUTHORIZED: Успешная авторизация
    AUTH_PENDING --> UNAUTHORIZED: Ошибка авторизации
    
    AUTHORIZED --> MAIN_MENU: Переход в меню
    
    MAIN_MENU --> SEARCH_EMPLOYEE_INPUT: Поиск сотрудников
    MAIN_MENU --> SHOW_RESOURCES: Ресурсы компании
    MAIN_MENU --> VACATION_INFO: Хочу в отпуск
    MAIN_MENU --> WIFI_PASSWORD: Пароль Wi-Fi
    MAIN_MENU --> CONTRACTOR_REPORT_INPUT: Экспресс-отчет
    MAIN_MENU --> MANAGER_MENU: Раздел руководителя
    MAIN_MENU --> MODULE_UNAVAILABLE: Неактивный модуль
    
    SEARCH_EMPLOYEE_INPUT --> SEARCH_EMPLOYEE_RESULTS: Ввод фамилии
    SEARCH_EMPLOYEE_INPUT --> VALIDATION_ERROR: Ошибка валидации
    SEARCH_EMPLOYEE_RESULTS --> EMPLOYEE_DETAILS: Выбор сотрудника
    SEARCH_EMPLOYEE_RESULTS --> MAIN_MENU: Главное меню
    
    SHOW_RESOURCES --> RESOURCES_PAGE_NAVIGATION: Навигация по страницам
    RESOURCES_PAGE_NAVIGATION --> SHOW_RESOURCES: Смена страницы
    SHOW_RESOURCES --> MAIN_MENU: Главное меню
    
    VACATION_INFO --> VACATION_BALANCE: Остаток дней
    VACATION_INFO --> MAIN_MENU: Главное меню
    VACATION_BALANCE --> MAIN_MENU: Главное меню
    
    WIFI_PASSWORD --> MAIN_MENU: Главное меню
    
    CONTRACTOR_REPORT_INPUT --> CONTRACTOR_REPORT_RESULTS: Ввод ИНН
    CONTRACTOR_REPORT_INPUT --> VALIDATION_ERROR: Ошибка валидации
    CONTRACTOR_REPORT_RESULTS --> MAIN_MENU: Главное меню
    
    MANAGER_MENU --> SUBORDINATES_LIST: Мои сотрудники
    MANAGER_MENU --> TEAM_VACATIONS: Отпуска команды
    MANAGER_MENU --> DEPARTMENT_STATS: Статистика отдела
    MANAGER_MENU --> APPROVE_REQUESTS: Согласование заявок
    MANAGER_MENU --> MAIN_MENU: Главное меню
    
    SUBORDINATES_LIST --> SUBORDINATE_DETAILS: Детали сотрудника
    SUBORDINATE_DETAILS --> SUBORDINATES_LIST: Назад
    TEAM_VACATIONS --> MANAGER_MENU: Назад
    DEPARTMENT_STATS --> MANAGER_MENU: Назад
    APPROVE_REQUESTS --> REQUEST_DETAILS: Выбор заявки
    REQUEST_DETAILS --> APPROVE_REQUESTS: Назад
    
    SUBORDINATES_LIST --> MAIN_MENU: Главное меню
    TEAM_VACATIONS --> MAIN_MENU: Главное меню
    DEPARTMENT_STATS --> MAIN_MENU: Главное меню
    APPROVE_REQUESTS --> MAIN_MENU: Главное меню
    
    MODULE_UNAVAILABLE --> MAIN_MENU: Главное меню
    
    EMPLOYEE_DETAILS --> MAIN_MENU: Главное меню
    CONTRACTOR_REPORT_RESULTS --> MAIN_MENU: Главное меню
    
    VALIDATION_ERROR --> SEARCH_EMPLOYEE_INPUT: Повтор ввода
    VALIDATION_ERROR --> CONTRACTOR_REPORT_INPUT: Повтор ввода
    VALIDATION_ERROR --> MAIN_MENU: Главное меню
```

## Диаграмма процесса авторизации

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant Bot as Бот
    participant MAX as MAX API
    participant DB as База данных
    
    User->>Bot: /start
    Bot->>DB: Проверка авторизации
    
    alt Не авторизован
        DB-->>Bot: Пользователь не найден
        Bot->>User: Приветственное сообщение + кнопка "Начать"
        User->>Bot: Нажатие "Начать"
        Bot->>MAX: Запрос OAuth авторизации
        MAX-->>Bot: Токен доступа + данные пользователя
        Bot->>DB: Сохранение пользователя и сессии
        DB-->>Bot: Успех
        Bot->>User: Главное меню
    else Уже авторизован
        DB-->>Bot: Пользователь найден
        Bot->>User: Главное меню
    end
```

## Диаграмма поиска сотрудника

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant Bot as Бот
    participant DB as База данных
    participant HR as HR API
    
    User->>Bot: Поиск сотрудников
    Bot->>User: Введите фамилию
    User->>Bot: "Иванов"
    Bot->>Bot: Валидация ввода
    
    alt Валидация успешна
        Bot->>DB: Поиск по фамилии
        DB-->>Bot: Результаты поиска
        
        alt Найден 1 сотрудник
            Bot->>HR: Запрос детальной информации
            HR-->>Bot: Полные данные сотрудника
            Bot->>User: Карточка сотрудника
        else Найдено 2-10 сотрудников
            Bot->>User: Список сотрудников (кнопки)
            User->>Bot: Выбор сотрудника
            Bot->>HR: Запрос детальной информации
            HR-->>Bot: Полные данные сотрудника
            Bot->>User: Карточка сотрудника
        else Найдено более 10
            Bot->>User: Уточните запрос
        else Не найдено
            Bot->>User: Сотрудник не найден
        end
    else Ошибка валидации
        Bot->>User: Сообщение об ошибке
    end
```

## Диаграмма навигации по ресурсам

```mermaid
stateDiagram-v2
    [*] --> Page1: Ресурсы компании
    
    Page1 --> Page2: Следующая ➡️
    Page2 --> Page1: ⬅️ Предыдущая
    Page2 --> Page3: Следующая ➡️
    Page3 --> Page2: ⬅️ Предыдущая
    Page3 --> Page4: Следующая ➡️
    Page4 --> Page3: ⬅️ Предыдущая
    
    Page1 --> [*]: 🏠 Главное меню
    Page2 --> [*]: 🏠 Главное меню
    Page3 --> [*]: 🏠 Главное меню
    Page4 --> [*]: 🏠 Главное меню
    
    note right of Page1
        Страница 1/4
        Ресурсы 1-5
    end note
    
    note right of Page2
        Страница 2/4
        Ресурсы 6-10
    end note
    
    note right of Page3
        Страница 3/4
        Ресурсы 11-15
    end note
    
    note right of Page4
        Страница 4/4
        Ресурсы 16-18
    end note
```

## Диаграмма доступа к разделу руководителя

```mermaid
flowchart TD
    Start([Пользователь нажимает<br/>'Руководителю']) --> CheckAuth{Авторизован?}
    
    CheckAuth -->|Нет| AuthError[❌ Требуется авторизация]
    CheckAuth -->|Да| CheckRole{Роль = Руководитель?}
    
    CheckRole -->|Нет| AccessDenied[⛔ Доступ ограничен]
    CheckRole -->|Да| ManagerMenu[👔 Меню руководителя]
    
    ManagerMenu --> Choice{Выбор действия}
    
    Choice -->|Мои сотрудники| Subordinates[👥 Список подчиненных]
    Choice -->|Отпуска команды| Vacations[📅 Отпуска команды]
    Choice -->|Статистика| Stats[📊 Статистика отдела]
    Choice -->|Согласование| Approvals[✅ Заявки на согласование]
    
    Subordinates --> SubDetails[Детали сотрудника]
    Vacations --> VacDetails[График отпусков]
    Stats --> StatsView[Аналитика]
    Approvals --> ApprovalDetails[Детали заявки]
    
    SubDetails --> MainMenu[🏠 Главное меню]
    VacDetails --> MainMenu
    StatsView --> MainMenu
    ApprovalDetails --> MainMenu
    
    AccessDenied --> MainMenu
    AuthError --> Start
```

## Диаграмма жизненного цикла сессии

```mermaid
stateDiagram-v2
    [*] --> SessionCreated: Успешная авторизация
    
    SessionCreated --> Active: Активность пользователя
    Active --> Active: Действия пользователя
    
    Active --> Inactive: 30 минут бездействия
    Inactive --> Active: Действие пользователя
    Inactive --> Expired: Превышен timeout
    
    Active --> Expired: 8 часов с момента создания
    
    Expired --> [*]: Сессия удалена
    
    note right of SessionCreated
        Создается при авторизации
        Время жизни: 8 часов
    end note
    
    note right of Inactive
        Предупреждение о бездействии
        Timeout: 30 минут
    end note
    
    note right of Expired
        Требуется повторная авторизация
    end note
```

## Диаграмма обработки ошибок

```mermaid
flowchart TD
    Request[Запрос пользователя] --> ProcessRequest{Обработка}
    
    ProcessRequest -->|Успех| Success[✅ Успешный ответ]
    ProcessRequest -->|Ошибка| ErrorType{Тип ошибки}
    
    ErrorType -->|Валидация| ValidationError[❌ Ошибка валидации]
    ErrorType -->|Доступ| AccessError[⛔ Доступ запрещен]
    ErrorType -->|Не найдено| NotFoundError[❌ Не найдено]
    ErrorType -->|Система| SystemError[⚠️ Системная ошибка]
    
    ValidationError --> ShowError[Показать сообщение]
    AccessError --> ShowError
    NotFoundError --> ShowError
    SystemError --> ShowError
    
    ShowError --> LogError[Логирование ошибки]
    
    LogError --> Retry{Можно повторить?}
    
    Retry -->|Да| AllowRetry[Предложить повтор]
    Retry -->|Нет| ReturnToMenu[Вернуться в меню]
    
    AllowRetry --> Request
    ReturnToMenu --> MainMenu[🏠 Главное меню]
    Success --> End([Конец])
    MainMenu --> End
```

## Диаграмма аудита действий

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant Bot as Бот
    participant Service as Сервис
    participant Audit as Аудит
    participant DB as База данных
    
    User->>Bot: Действие (например, запрос пароля Wi-Fi)
    Bot->>Service: Обработка запроса
    
    Service->>Service: Проверка прав доступа
    
    alt Доступ разрешен
        Service->>DB: Получение данных
        DB-->>Service: Данные
        Service->>Audit: Запись в лог аудита
        Audit->>DB: Сохранение лога
        Service-->>Bot: Результат
        Bot-->>User: Отображение данных
    else Доступ запрещен
        Service->>Audit: Запись попытки несанкционированного доступа
        Audit->>DB: Сохранение лога
        Service-->>Bot: Ошибка доступа
        Bot-->>User: Сообщение об ошибке
    end
```

## Диаграмма получения экспресс-отчета

```mermaid
flowchart TD
    Start([Экспресс-отчет по контрагенту]) --> Input[Введите ИНН или название]
    
    Input --> UserInput{Пользователь вводит}
    
    UserInput -->|ИНН| ValidateINN[Валидация ИНН]
    UserInput -->|Название| ValidateName[Валидация названия]
    
    ValidateINN --> INNValid{ИНН валиден?}
    ValidateName --> NameValid{Название валидно?}
    
    INNValid -->|Нет| ErrorMessage[❌ Некорректный ИНН]
    NameValid -->|Нет| ErrorMessage
    
    INNValid -->|Да| SearchDB[Поиск в БД]
    NameValid -->|Да| SearchDB
    
    SearchDB --> Found{Найден?}
    
    Found -->|Нет| NotFoundMsg[❌ Контрагент не найден]
    Found -->|Да| GetDetails[Получение детальной информации]
    
    GetDetails --> External1C[Запрос к 1С]
    External1C --> BuildReport[Формирование отчета]
    
    BuildReport --> AuditLog[Запись в аудит]
    AuditLog --> ShowReport[📊 Отображение отчета]
    
    ErrorMessage --> Retry{Повторить?}
    NotFoundMsg --> Retry
    
    Retry -->|Да| Input
    Retry -->|Нет| MainMenu[🏠 Главное меню]
    
    ShowReport --> MainMenu
```

## Легенда

### Состояния
- **UNAUTHORIZED** — пользователь не авторизован
- **AUTH_PENDING** — процесс авторизации
- **AUTHORIZED** — успешная авторизация
- **MAIN_MENU** — главное меню
- **SEARCH_EMPLOYEE_INPUT** — ожидание ввода для поиска сотрудника
- **SEARCH_EMPLOYEE_RESULTS** — отображение результатов поиска
- **EMPLOYEE_DETAILS** — детальная информация о сотруднике
- **SHOW_RESOURCES** — отображение ресурсов компании
- **RESOURCES_PAGE_NAVIGATION** — навигация по страницам ресурсов
- **VACATION_INFO** — информация об отпусках
- **VACATION_BALANCE** — остаток отпускных дней
- **WIFI_PASSWORD** — отображение паролей Wi-Fi
- **CONTRACTOR_REPORT_INPUT** — ожидание ввода для отчета
- **CONTRACTOR_REPORT_RESULTS** — отображение отчета по контрагенту
- **MANAGER_MENU** — меню руководителя
- **SUBORDINATES_LIST** — список подчиненных
- **SUBORDINATE_DETAILS** — детали подчиненного
- **TEAM_VACATIONS** — отпуска команды
- **DEPARTMENT_STATS** — статистика отдела
- **APPROVE_REQUESTS** — список заявок на согласование
- **REQUEST_DETAILS** — детали заявки
- **MODULE_UNAVAILABLE** — модуль недоступен
- **VALIDATION_ERROR** — ошибка валидации

### Действия
- **Команда /start** — запуск бота
- **Нажатие кнопки** — взаимодействие с inline-кнопками
- **Ввод текста** — ввод данных пользователем
- **Переход в меню** — возврат в главное меню
- **Валидация** — проверка введенных данных
- **Запрос к API** — обращение к внешним системам

### Символы
- ✅ — успешная операция
- ❌ — ошибка
- ⚠️ — предупреждение
- ⛔ — доступ запрещен
- 🏠 — главное меню
- 👔 — раздел руководителя
- 📊 — отчеты и статистика
- 🔐 — безопасность и авторизация
