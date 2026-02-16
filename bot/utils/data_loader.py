"""Load JSON data files."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from bot.config import CONFIG_DIR, DATA_DIR

logger = logging.getLogger(__name__)

_cache: dict[str, Any] = {}


def _load_json(path: Path) -> Any:
    key = str(path)
    if key not in _cache:
        try:
            with open(path, "r", encoding="utf-8") as f:
                _cache[key] = json.load(f)
        except FileNotFoundError:
            logger.error("Data file not found: %s", path)
            return None
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON in %s: %s", path, exc)
            return None
    return _cache[key]


def load_messages() -> dict[str, str]:
    data = _load_json(CONFIG_DIR / "messages.json")
    return data if isinstance(data, dict) else {}


def load_resources() -> list[dict[str, Any]]:
    data = _load_json(DATA_DIR / "resources.json")
    return data if isinstance(data, list) else []


def load_employees() -> list[dict[str, Any]]:
    data = _load_json(DATA_DIR / "employees.json")
    return data if isinstance(data, list) else []


def load_wifi() -> dict[str, str]:
    data = _load_json(DATA_DIR / "wifi.json")
    return data if isinstance(data, dict) else {}


def clear_cache() -> None:
    _cache.clear()
