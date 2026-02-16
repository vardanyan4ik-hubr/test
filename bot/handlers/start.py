"""Authorization / start handler."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from bot.api_client import MaxBotApi
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_messages
from bot.utils.keyboards import main_menu_keyboard, start_keyboard

logger = logging.getLogger(__name__)


async def handle_start_command(
    api: MaxBotApi, state: StateManager, chat_id: str, user_id: str
) -> None:
    """Handle /start command — show welcome message and 'Начать' button."""
    msgs = load_messages()
    state.reset(user_id)
    state.set_state(user_id, UserState.IDLE)

    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("welcome", "Добро пожаловать!"),
        inline_keyboard=start_keyboard(),
        parse_mode="",
    )
    logger.info("User %s triggered /start", user_id)


async def handle_start_callback(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str,
) -> None:
    """Handle 'Начать' button press — authorize user and show main menu."""
    msgs = load_messages()

    session = state.get(user_id)
    session.state = UserState.AUTHORIZED
    session.authorized_at = datetime.now(timezone.utc).isoformat()

    await api.answer_callback(query_id)
    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("main_menu", "Главное меню"),
        inline_keyboard=main_menu_keyboard(),
        parse_mode="",
    )
    logger.info("User %s authorized", user_id)
