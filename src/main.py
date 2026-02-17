"""
Главная точка входа приложения
"""
import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from src.config import settings


async def main():
    """Главная функция запуска приложения"""
    
    # Настройка логирования
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )
    logger.add(
        settings.log_file,
        level=settings.log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    logger.info("🚀 Запуск Telegram бота для интеграции с Assyst")
    logger.info(f"Версия: {settings.telegram_bot_username}")
    logger.info(f"Режим отладки: {settings.app_debug}")
    
    try:
        # TODO: Инициализация базы данных
        logger.info("📊 Инициализация базы данных...")
        
        # TODO: Инициализация Redis
        logger.info("🔴 Подключение к Redis...")
        
        # TODO: Запуск Telegram бота
        logger.info("🤖 Запуск Telegram бота...")
        
        # TODO: Запуск FastAPI для webhook
        logger.info(f"🌐 Запуск webhook сервера на {settings.app_host}:{settings.app_port}")
        
        logger.success("✅ Приложение успешно запущено!")
        
        # Держим приложение работающим
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        logger.info("⚠️ Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise
    finally:
        logger.info("🛑 Остановка приложения...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Приложение остановлено")
