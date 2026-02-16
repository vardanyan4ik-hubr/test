-- ==========================================
-- Инициализация базы данных для бота Михалыч
-- ==========================================

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ==========================================
-- Таблица: users (Пользователи)
-- ==========================================
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(100) PRIMARY KEY,
    employee_id VARCHAR(50),
    username VARCHAR(100) UNIQUE,
    email VARCHAR(255),
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Индексы для таблицы users
CREATE INDEX idx_users_employee_id ON users(employee_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_users_last_activity ON users(last_activity);

-- ==========================================
-- Таблица: employees (Сотрудники)
-- ==========================================
CREATE TABLE IF NOT EXISTS employees (
    employee_id VARCHAR(50) PRIMARY KEY,
    lastname VARCHAR(100) NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    middlename VARCHAR(100),
    full_name VARCHAR(255) NOT NULL,
    department VARCHAR(200),
    position VARCHAR(200),
    email VARCHAR(255),
    phone VARCHAR(50),
    office_city VARCHAR(100),
    office_building VARCHAR(200),
    office_floor VARCHAR(10),
    photo_url VARCHAR(500),
    is_manager BOOLEAN DEFAULT FALSE,
    manager_id VARCHAR(50),
    hire_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_manager FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

-- Индексы для таблицы employees
CREATE INDEX idx_employees_lastname ON employees(lastname);
CREATE INDEX idx_employees_fullname ON employees(full_name);
CREATE INDEX idx_employees_email ON employees(email);
CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_employees_manager ON employees(manager_id);
CREATE INDEX idx_employees_active ON employees(is_active);

-- Полнотекстовый поиск
CREATE INDEX idx_employees_lastname_trgm ON employees USING gin (lastname gin_trgm_ops);
CREATE INDEX idx_employees_fullname_trgm ON employees USING gin (full_name gin_trgm_ops);

-- ==========================================
-- Таблица: resources (Ресурсы компании)
-- ==========================================
CREATE TABLE IF NOT EXISTS resources (
    resource_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    url VARCHAR(500) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    icon VARCHAR(10),
    "order" INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    access_roles JSONB DEFAULT '["all"]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для таблицы resources
CREATE INDEX idx_resources_category ON resources(category);
CREATE INDEX idx_resources_active ON resources(is_active);
CREATE INDEX idx_resources_order ON resources("order");
CREATE INDEX idx_resources_access_roles ON resources USING gin (access_roles);

-- ==========================================
-- Таблица: sessions (Сессии пользователей)
-- ==========================================
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(100) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    context JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Индексы для таблицы sessions
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
CREATE INDEX idx_sessions_state ON sessions(state);

-- ==========================================
-- Таблица: audit_logs (Логи аудита)
-- ==========================================
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id VARCHAR(100) PRIMARY KEY,
    user_id VARCHAR(100),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    details JSONB DEFAULT '{}',
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для таблицы audit_logs
CREATE INDEX idx_audit_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_resource_type ON audit_logs(resource_type);

-- ==========================================
-- Таблица: wifi_networks (Wi-Fi сети)
-- ==========================================
CREATE TABLE IF NOT EXISTS wifi_networks (
    network_id VARCHAR(50) PRIMARY KEY,
    office VARCHAR(200) NOT NULL,
    ssid VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('corporate', 'guest')),
    security VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для таблицы wifi_networks
CREATE INDEX idx_wifi_office ON wifi_networks(office);
CREATE INDEX idx_wifi_type ON wifi_networks(type);
CREATE INDEX idx_wifi_active ON wifi_networks(is_active);

-- ==========================================
-- Таблица: contractors (Контрагенты)
-- ==========================================
CREATE TABLE IF NOT EXISTS contractors (
    contractor_id VARCHAR(50) PRIMARY KEY,
    legal_name VARCHAR(500) NOT NULL,
    inn VARCHAR(12) NOT NULL UNIQUE,
    kpp VARCHAR(9),
    ogrn VARCHAR(15),
    legal_address TEXT,
    cooperation JSONB DEFAULT '{}',
    status JSONB DEFAULT '{}',
    contact_person JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для таблицы contractors
CREATE INDEX idx_contractors_inn ON contractors(inn);
CREATE INDEX idx_contractors_legal_name ON contractors(legal_name);
CREATE INDEX idx_contractors_active ON contractors(is_active);

-- ==========================================
-- Таблица: vacations (Отпуска)
-- ==========================================
CREATE TABLE IF NOT EXISTS vacations (
    vacation_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled')),
    approved_by VARCHAR(50),
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_employee_vacation FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES employees(employee_id)
);

-- Индексы для таблицы vacations
CREATE INDEX idx_vacations_employee ON vacations(employee_id);
CREATE INDEX idx_vacations_year ON vacations(year);
CREATE INDEX idx_vacations_status ON vacations(status);
CREATE INDEX idx_vacations_dates ON vacations(start_date, end_date);

-- ==========================================
-- Таблица: vacation_balances (Остатки отпусков)
-- ==========================================
CREATE TABLE IF NOT EXISTS vacation_balances (
    balance_id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    total_days INTEGER NOT NULL DEFAULT 28,
    used_days INTEGER NOT NULL DEFAULT 0,
    remaining_days INTEGER NOT NULL DEFAULT 28,
    planned_days INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, year),
    CONSTRAINT fk_employee_balance FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Индексы для таблицы vacation_balances
CREATE INDEX idx_vacation_balances_employee ON vacation_balances(employee_id);
CREATE INDEX idx_vacation_balances_year ON vacation_balances(year);

-- ==========================================
-- Функции и триггеры
-- ==========================================

-- Функция для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Триггеры для обновления updated_at
CREATE TRIGGER update_employees_updated_at BEFORE UPDATE ON employees
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_resources_updated_at BEFORE UPDATE ON resources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_wifi_networks_updated_at BEFORE UPDATE ON wifi_networks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contractors_updated_at BEFORE UPDATE ON contractors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vacations_updated_at BEFORE UPDATE ON vacations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Функция для автоматической очистки истекших сессий
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS void AS $$
BEGIN
    DELETE FROM sessions WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Функция для обновления last_activity пользователя
CREATE OR REPLACE FUNCTION update_user_activity()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users 
    SET last_activity = CURRENT_TIMESTAMP 
    WHERE user_id = NEW.user_id;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Триггер для обновления активности пользователя при создании сессии
CREATE TRIGGER update_user_activity_trigger AFTER INSERT ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_user_activity();

-- ==========================================
-- Начальные данные
-- ==========================================

-- Вставка тестовых ресурсов
INSERT INTO resources (resource_id, title, url, description, category, icon, "order", is_active, access_roles) VALUES
('res_001', '🌐 Интранет', 'https://intranet.onlanta.com', 'Корпоративный портал компании', 'Основные', '🌐', 1, TRUE, '["all"]'),
('res_002', '📧 Корпоративная почта', 'https://mail.onlanta.com', 'Почтовая система компании', 'Основные', '📧', 2, TRUE, '["all"]'),
('res_003', '📊 Битрикс24', 'https://bitrix.onlanta.com', 'CRM-система и управление задачами', 'Работа', '📊', 3, TRUE, '["all"]'),
('res_004', '💰 1С Зарплата', 'https://1c.onlanta.com', 'Система учета зарплат и кадров', 'Финансы', '💰', 4, TRUE, '["all"]'),
('res_005', '📚 База знаний', 'https://kb.onlanta.com', 'Корпоративная документация и инструкции', 'Обучение', '📚', 5, TRUE, '["all"]')
ON CONFLICT (resource_id) DO NOTHING;

-- Вставка тестовых Wi-Fi сетей
INSERT INTO wifi_networks (network_id, office, ssid, password, type, security, is_active) VALUES
('wifi_001', 'Москва, БЦ "Онланта"', 'Onlanta_Corporate', 'Secure2026Pass!', 'corporate', 'WPA2-Enterprise', TRUE),
('wifi_002', 'Москва, БЦ "Онланта"', 'Onlanta_Guest', 'Guest2026!', 'guest', 'WPA2-PSK', TRUE)
ON CONFLICT (network_id) DO NOTHING;

-- ==========================================
-- Права доступа
-- ==========================================

-- Предоставление прав пользователю bot_user (если существует)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bot_user') THEN
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bot_user;
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bot_user;
        GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO bot_user;
    END IF;
END
$$;

-- ==========================================
-- Комментарии к таблицам
-- ==========================================

COMMENT ON TABLE users IS 'Пользователи бота в мессенджере MAX';
COMMENT ON TABLE employees IS 'Сотрудники компании Онланта';
COMMENT ON TABLE resources IS 'Корпоративные ресурсы компании';
COMMENT ON TABLE sessions IS 'Активные сессии пользователей';
COMMENT ON TABLE audit_logs IS 'Журнал аудита действий пользователей';
COMMENT ON TABLE wifi_networks IS 'Wi-Fi сети офисов';
COMMENT ON TABLE contractors IS 'Контрагенты компании';
COMMENT ON TABLE vacations IS 'Заявки на отпуск';
COMMENT ON TABLE vacation_balances IS 'Остатки отпускных дней сотрудников';

-- ==========================================
-- Завершение
-- ==========================================

SELECT 'Database initialization completed successfully!' as message;
