"""Main menu handler."""

from __future__ import annotations

import logging

from bot.api_client import MaxBotApi
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_messages
from bot.utils.keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)


async def handle_menu(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str | None = None,
) -> None:
    """Show the main menu."""
    msgs = load_messages()
    state.set_state(user_id, UserState.AUTHORIZED)

    if query_id:
        await api.answer_callback(query_id)

    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("main_menu", "Главное меню"),
        inline_keyboard=main_menu_keyboard(),
        parse_mode="",
    )
