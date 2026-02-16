"""Bot configuration loaded from environment variables."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"


@dataclass
class BotConfig:
    token: str = field(default_factory=lambda: os.getenv("MAX_BOT_TOKEN", ""))
    api_base_url: str = field(
        default_factory=lambda: os.getenv(
            "API_BASE_URL", "https://api.max.ru/bot/v1"
        )
    )
    polling_interval: int = field(
        default_factory=lambda: int(os.getenv("POLLING_INTERVAL", "1"))
    )
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )
    max_search_results: int = 10
    resources_per_page: int = 5


config = BotConfig()
