"""Employee search handler."""

from __future__ import annotations

import logging
from typing import Any

from bot.api_client import MaxBotApi
from bot.config import config
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_employees, load_messages
from bot.utils.keyboards import search_prompt_keyboard, search_result_keyboard
from bot.utils.validators import validate_last_name

logger = logging.getLogger(__name__)


def _format_employee(emp: dict[str, Any]) -> str:
    """Format a single employee record for display."""
    parts = [emp.get("last_name", ""), emp.get("first_name", ""), emp.get("middle_name", "")]
    full_name = " ".join(p for p in parts if p)
    lines = [f"👤 {full_name}"]
    if emp.get("email"):
        lines.append(f"📧 {emp['email']}")
    if emp.get("phone"):
        lines.append(f"📱 {emp['phone']}")
    if emp.get("department"):
        lines.append(f"🏢 {emp['department']}")
    if emp.get("position"):
        lines.append(f"💼 {emp['position']}")
    return "\n".join(lines)


def _search_employees(query: str) -> list[dict[str, Any]]:
    """Search employees by last name (case-insensitive substring match)."""
    employees = load_employees()
    if not employees:
        return []
    q = query.strip().lower()
    return [
        emp
        for emp in employees
        if q in emp.get("last_name", "").lower()
    ]


async def handle_search_prompt(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str | None = None,
) -> None:
    """Show search prompt."""
    msgs = load_messages()
    state.set_state(user_id, UserState.SEARCH_EMPLOYEE)

    if query_id:
        await api.answer_callback(query_id)

    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("search_prompt", "Введите фамилию:"),
        inline_keyboard=search_prompt_keyboard(),
        parse_mode="",
    )


async def handle_search_input(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    text: str,
) -> None:
    """Process surname input from user."""
    msgs = load_messages()

    validation = validate_last_name(text)
    if not validation.ok:
        error_msg = msgs.get(validation.error_key, "Ошибка валидации.")
        await api.send_text(
            chat_id=chat_id,
            text=error_msg,
            inline_keyboard=search_prompt_keyboard(),
            parse_mode="",
        )
        return

    query = text.strip()
    results = _search_employees(query)

    if results:
        limited = results[: config.max_search_results]
        header = msgs.get("search_found", "Найдено: {count}").format(count=len(results))
        body_parts = [header, ""]
        for i, emp in enumerate(limited):
            body_parts.append(_format_employee(emp))
            if i < len(limited) - 1:
                body_parts.append("─────────────────")
        if len(results) > config.max_search_results:
            body_parts.append(f"\n... и ещё {len(results) - config.max_search_results}")

        await api.send_text(
            chat_id=chat_id,
            text="\n".join(body_parts),
            inline_keyboard=search_result_keyboard(),
            parse_mode="",
        )
    else:
        await api.send_text(
            chat_id=chat_id,
            text=msgs.get("search_not_found", "Не найдено."),
            inline_keyboard=search_result_keyboard(),
            parse_mode="",
        )

    state.set_state(user_id, UserState.AUTHORIZED)
