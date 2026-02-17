"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Telegram
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    telegram_bot_username: str = Field(..., env="TELEGRAM_BOT_USERNAME")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    db_echo: bool = Field(False, env="DB_ECHO")
    
    # Redis
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    # SMTP
    smtp_host: str = Field(..., env="SMTP_HOST")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_user: str = Field(..., env="SMTP_USER")
    smtp_password: str = Field(..., env="SMTP_PASSWORD")
    smtp_from_email: str = Field(..., env="SMTP_FROM_EMAIL")
    smtp_use_tls: bool = Field(True, env="SMTP_USE_TLS")
    
    # Assyst
    assyst_inbox_email: str = Field("assyst.inbox@onlanta.ru", env="ASSYST_INBOX_EMAIL")
    assyst_webhook_secret: Optional[str] = Field(None, env="ASSYST_WEBHOOK_SECRET")
    
    # Apex API
    apex_api_url: str = Field(..., env="APEX_API_URL")
    apex_api_key: str = Field(..., env="APEX_API_KEY")
    
    # Application
    app_host: str = Field("0.0.0.0", env="APP_HOST")
    app_port: int = Field(8000, env="APP_PORT")
    app_debug: bool = Field(False, env="APP_DEBUG")
    webhook_url: str = Field(..., env="WEBHOOK_URL")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    verification_code_length: int = Field(4, env="VERIFICATION_CODE_LENGTH")
    verification_code_expiry_minutes: int = Field(5, env="VERIFICATION_CODE_EXPIRY_MINUTES")
    max_code_attempts: int = Field(3, env="MAX_CODE_ATTEMPTS")
    
    # Rate Limiting
    max_tickets_per_hour: int = Field(5, env="MAX_TICKETS_PER_HOUR")
    max_tickets_per_day: int = Field(10, env="MAX_TICKETS_PER_DAY")
    min_ticket_interval_minutes: int = Field(15, env="MIN_TICKET_INTERVAL_MINUTES")
    
    # File Upload
    max_file_size_mb: int = Field(10, env="MAX_FILE_SIZE_MB")
    max_files_count: int = Field(10, env="MAX_FILES_COUNT")
    allowed_file_extensions: str = Field("jpg,jpeg,png", env="ALLOWED_FILE_EXTENSIONS")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("logs/bot.log", env="LOG_FILE")
    
    @validator("allowed_file_extensions")
    def parse_file_extensions(cls, v):
        """Парсинг списка расширений файлов"""
        if isinstance(v, str):
            return [ext.strip().lower() for ext in v.split(",")]
        return v
    
    @property
    def max_file_size_bytes(self) -> int:
        """Максимальный размер файла в байтах"""
        return self.max_file_size_mb * 1024 * 1024
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Создание глобального экземпляра настроек
settings = Settings()
