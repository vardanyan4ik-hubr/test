"""Counterparty report handler."""

from __future__ import annotations

import logging

from bot.api_client import MaxBotApi
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_messages
from bot.utils.keyboards import counterparty_prompt_keyboard, counterparty_result_keyboard
from bot.utils.validators import validate_inn

logger = logging.getLogger(__name__)


async def handle_counterparty_prompt(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str | None = None,
) -> None:
    """Show INN input prompt."""
    msgs = load_messages()
    state.set_state(user_id, UserState.COUNTERPARTY_REPORT)

    if query_id:
        await api.answer_callback(query_id)

    await api.send_text(
        chat_id=chat_id,
        text=msgs.get("counterparty_prompt", "Введите ИНН:"),
        inline_keyboard=counterparty_prompt_keyboard(),
        parse_mode="",
    )


async def handle_counterparty_input(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    text: str,
) -> None:
    """Process INN input from user."""
    msgs = load_messages()

    validation = validate_inn(text)
    if not validation.ok:
        error_msg = msgs.get(validation.error_key, "Ошибка валидации.")
        await api.send_text(
            chat_id=chat_id,
            text=error_msg,
            inline_keyboard=counterparty_prompt_keyboard(),
            parse_mode="",
        )
        return

    inn = text.strip()
    response_text = msgs.get(
        "counterparty_stub", "Отчёт по контрагенту (ИНН: {inn})"
    ).format(inn=inn)

    await api.send_text(
        chat_id=chat_id,
        text=response_text,
        inline_keyboard=counterparty_result_keyboard(),
        parse_mode="",
    )

    state.set_state(user_id, UserState.AUTHORIZED)
