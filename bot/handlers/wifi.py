"""Wi-Fi password handler."""

from __future__ import annotations

import logging

from bot.api_client import MaxBotApi
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_messages, load_wifi
from bot.utils.keyboards import wifi_keyboard

logger = logging.getLogger(__name__)


async def handle_wifi(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    query_id: str | None = None,
) -> None:
    """Show Wi-Fi password."""
    msgs = load_messages()
    wifi = load_wifi()
    state.set_state(user_id, UserState.AUTHORIZED)

    if query_id:
        await api.answer_callback(query_id)

    if not wifi:
        await api.send_text(
            chat_id=chat_id,
            text=msgs.get("data_unavailable", "Данные недоступны."),
            inline_keyboard=wifi_keyboard(),
            parse_mode="",
        )
        return

    text = msgs.get("wifi_info", "Wi-Fi: {network_name} / {password}").format(
        network_name=wifi.get("network_name", "—"),
        password=wifi.get("password", "—"),
    )

    await api.send_text(
        chat_id=chat_id,
        text=text,
        inline_keyboard=wifi_keyboard(),
        parse_mode="",
    )
