"""Manager menu handler."""

from __future__ import annotations

import logging

from bot.api_client import MaxBotApi
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_messages
from bot.utils.keyboards import manager_menu_keyboard, manager_sub_keyboard

logger = logging.getLogger(__name__)


async def handle_manager_menu(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str | None = None,
) -> None:
    """Show manager sub-menu."""
    msgs = load_messages()
    state.set_state(user_id, UserState.AUTHORIZED)

    if query_id:
        await api.answer_callback(query_id)

    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("manager_menu", "Раздел для руководителей"),
        inline_keyboard=manager_menu_keyboard(),
        parse_mode="",
    )


async def handle_manager_employees(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str | None = None,
) -> None:
    """Show manager employees stub."""
    msgs = load_messages()

    if query_id:
        await api.answer_callback(query_id)

    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("manager_employees_stub", "Мои сотрудники (в разработке)."),
        inline_keyboard=manager_sub_keyboard(),
        parse_mode="",
    )


async def handle_manager_approvals(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str | None = None,
) -> None:
    """Show manager approvals stub."""
    msgs = load_messages()

    if query_id:
        await api.answer_callback(query_id)

    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("manager_approvals_stub", "Заявки на согласование (в разработке)."),
        inline_keyboard=manager_sub_keyboard(),
        parse_mode="",
    )
