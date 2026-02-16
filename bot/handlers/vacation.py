"""Vacation info handler."""

from __future__ import annotations

import logging

from bot.api_client import MaxBotApi
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_messages
from bot.utils.keyboards import vacation_keyboard

logger = logging.getLogger(__name__)


async def handle_vacation(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str | None = None,
) -> None:
    """Show vacation information."""
    msgs = load_messages()
    state.set_state(user_id, UserState.AUTHORIZED)

    if query_id:
        await api.answer_callback(query_id)

    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("vacation_info", "Информация об отпуске."),
        inline_keyboard=vacation_keyboard(),
        parse_mode="",
    )
