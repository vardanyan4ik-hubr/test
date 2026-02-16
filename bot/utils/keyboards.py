"""Keyboard builder helpers for MAX Bot inline keyboards."""

from __future__ import annotations

import math
from typing import Any

from bot.config import config
from bot.utils.data_loader import load_resources


def btn_callback(text: str, callback_data: str) -> dict[str, str]:
    return {"type": "callback", "text": text, "callbackData": callback_data}


def btn_url(text: str, url: str) -> dict[str, str]:
    return {"type": "url", "text": text, "url": url}


def home_button() -> list[dict[str, str]]:
    return [btn_callback("🏠 Главное меню", "menu")]


# -- Start screen ---------------------------------------------------------------

def start_keyboard() -> list[list[dict[str, str]]]:
    return [[btn_callback("Начать", "start")]]


# -- Main menu ------------------------------------------------------------------

def main_menu_keyboard() -> list[list[dict[str, str]]]:
    return [
        [btn_callback("🔍 Поиск сотрудников", "search_employees")],
        [btn_callback("📚 Ресурсы компании", "resources:1")],
        [btn_callback("🛡 Помощь СИБ", "help_sib")],
        [btn_callback("🏖 Хочу в отпуск", "vacation")],
        [btn_callback("🏋 Загрузить тренировку", "upload_training")],
        [btn_callback("🏓 Пин-понг", "ping_pong")],
        [btn_callback("📶 Показать пароль WI-FI", "wifi_password")],
        [btn_callback("👔 Руководителю", "manager_menu")],
        [btn_callback("📊 Экспресс-отчет по контрагенту", "counterparty_report")],
    ]


# -- Search results -------------------------------------------------------------

def search_result_keyboard() -> list[list[dict[str, str]]]:
    return [
        [btn_callback("🔍 Искать ещё", "search_employees")],
        home_button(),
    ]


def search_prompt_keyboard() -> list[list[dict[str, str]]]:
    return [home_button()]


# -- Resources with pagination --------------------------------------------------

def resources_keyboard(page: int) -> list[list[dict[str, str]]]:
    resources = load_resources()
    per_page = config.resources_per_page
    total_pages = max(1, math.ceil(len(resources) / per_page))
    page = max(1, min(page, total_pages))

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_resources = resources[start_idx:end_idx]

    keyboard: list[list[dict[str, str]]] = []

    for res in page_resources:
        keyboard.append([btn_url(f"🔗 {res['title']}", res["url"])])

    nav_row: list[dict[str, str]] = []
    if page > 1:
        nav_row.append(btn_callback("⬅️ Предыдущая", f"resources:{page - 1}"))
    if page < total_pages:
        nav_row.append(btn_callback("➡️ Следующая", f"resources:{page + 1}"))
    if nav_row:
        keyboard.append(nav_row)

    keyboard.append(home_button())
    return keyboard


def resources_total_pages() -> int:
    resources = load_resources()
    per_page = config.resources_per_page
    return max(1, math.ceil(len(resources) / per_page))


# -- Vacation -------------------------------------------------------------------

def vacation_keyboard() -> list[list[dict[str, str]]]:
    return [home_button()]


# -- Wi-Fi ----------------------------------------------------------------------

def wifi_keyboard() -> list[list[dict[str, str]]]:
    return [home_button()]


# -- Manager --------------------------------------------------------------------

def manager_menu_keyboard() -> list[list[dict[str, str]]]:
    return [
        [btn_callback("📋 Мои сотрудники", "manager_employees")],
        [btn_callback("📝 Заявки на согласование", "manager_approvals")],
        home_button(),
    ]


def manager_sub_keyboard() -> list[list[dict[str, str]]]:
    return [
        [btn_callback("🔙 Назад", "manager_menu")],
        home_button(),
    ]


# -- Counterparty ---------------------------------------------------------------

def counterparty_prompt_keyboard() -> list[list[dict[str, str]]]:
    return [home_button()]


def counterparty_result_keyboard() -> list[list[dict[str, str]]]:
    return [
        [btn_callback("🔄 Ввести другой ИНН", "counterparty_report")],
        home_button(),
    ]


# -- Paused section -------------------------------------------------------------

def paused_keyboard() -> list[list[dict[str, str]]]:
    return [home_button()]
