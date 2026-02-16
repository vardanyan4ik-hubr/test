"""Company resources handler with pagination."""

from __future__ import annotations

import logging

from bot.api_client import MaxBotApi
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_messages
from bot.utils.keyboards import resources_keyboard, resources_total_pages

logger = logging.getLogger(__name__)


async def handle_resources(
    api: MaxBotApi,
    state: StateManager,
    chat_id: str,
    user_id: str,
    page: int,
    query_id: str | None = None,
) -> None:
    """Show resources page."""
    msgs = load_messages()
    total = resources_total_pages()
    page = max(1, min(page, total))

    state.set_state(user_id, UserState.RESOURCES_PAGE)
    state.set_data(user_id, "resources_page", page)

    header = msgs.get("resources_header", "Ресурсы (Стр. {page}/{total_pages})").format(
        page=page, total_pages=total
    )

    if query_id:
        await api.answer_callback(query_id)

    await api.send_text(
        chat_id=chat_id,
        text=header,
        inline_keyboard=resources_keyboard(page),
        parse_mode="",
    )
