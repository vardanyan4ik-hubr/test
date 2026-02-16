"""Event router — dispatches incoming events to appropriate handlers."""

from __future__ import annotations

import logging
from typing import Any

from bot.api_client import MaxBotApi
from bot.handlers.counterparty import handle_counterparty_input, handle_counterparty_prompt
from bot.handlers.manager import (
    handle_manager_approvals,
    handle_manager_employees,
    handle_manager_menu,
)
from bot.handlers.menu import handle_menu
from bot.handlers.paused import handle_paused_section
from bot.handlers.resources import handle_resources
from bot.handlers.search import handle_search_input, handle_search_prompt
from bot.handlers.start import handle_start_callback, handle_start_command
from bot.handlers.vacation import handle_vacation
from bot.handlers.wifi import handle_wifi
from bot.state import StateManager, UserState
from bot.utils.data_loader import load_messages

logger = logging.getLogger(__name__)

PAUSED_CALLBACKS = {"help_sib", "upload_training", "ping_pong"}


def _extract_chat_id(event: dict[str, Any]) -> str | None:
    """Extract chat_id from various event shapes."""
    payload = event.get("payload", {})
    chat = payload.get("chat", {})
    if chat.get("chatId"):
        return chat["chatId"]
    msg = payload.get("message", payload.get("msg", {}))
    if isinstance(msg, dict):
        c = msg.get("chat", {})
        if c.get("chatId"):
            return c["chatId"]
    from_user = payload.get("from", {})
    if from_user.get("userId"):
        return from_user["userId"]
    return None


def _extract_user_id(event: dict[str, Any]) -> str | None:
    payload = event.get("payload", {})
    from_user = payload.get("from", {})
    if from_user.get("userId"):
        return from_user["userId"]
    chat = payload.get("chat", {})
    if chat.get("chatId"):
        return chat["chatId"]
    return None


class EventRouter:
    """Routes MAX Bot API events to handler functions."""

    def __init__(self, api: MaxBotApi, state: StateManager):
        self.api = api
        self.state = state

    async def handle_event(self, event: dict[str, Any]) -> None:
        event_type = event.get("type")
        logger.debug("Event: %s", event)

        if event_type == "newMessage":
            await self._on_message(event)
        elif event_type == "callbackQuery":
            await self._on_callback(event)
        else:
            logger.debug("Ignoring event type: %s", event_type)

    # -- message handler --------------------------------------------------------

    async def _on_message(self, event: dict[str, Any]) -> None:
        payload = event.get("payload", {})
        chat_id = _extract_chat_id(event)
        user_id = _extract_user_id(event)
        text = payload.get("text", "").strip()

        if not chat_id or not user_id:
            logger.warning("Cannot extract chat/user from event: %s", event)
            return

        if text.startswith("/start"):
            await handle_start_command(self.api, self.state, chat_id, user_id)
            return

        session = self.state.get(user_id)

        if session.state == UserState.SEARCH_EMPLOYEE:
            await handle_search_input(self.api, self.state, chat_id, user_id, text)
            return

        if session.state == UserState.COUNTERPARTY_REPORT:
            await handle_counterparty_input(self.api, self.state, chat_id, user_id, text)
            return

        if text.startswith("/"):
            msgs = load_messages()
            await self.api.send_text(
                chat_id=chat_id,
                text=msgs.get("unknown_command", "Неизвестная команда."),
                parse_mode="",
            )
            return

        msgs = load_messages()
        await self.api.send_text(
            chat_id=chat_id,
            text=msgs.get("unknown_command", "Воспользуйтесь меню."),
            parse_mode="",
        )

    # -- callback handler -------------------------------------------------------

    async def _on_callback(self, event: dict[str, Any]) -> None:
        payload = event.get("payload", {})
        callback_data = payload.get("callbackData", "")
        query_id = payload.get("queryId", "")
        chat_id = _extract_chat_id(event)
        user_id = _extract_user_id(event)

        if not chat_id or not user_id:
            logger.warning("Cannot extract chat/user from callback: %s", event)
            return

        if callback_data == "start":
            await handle_start_callback(
                self.api, self.state, chat_id, user_id, query_id
            )
        elif callback_data == "menu":
            await handle_menu(self.api, self.state, chat_id, user_id, query_id)
        elif callback_data == "search_employees":
            await handle_search_prompt(
                self.api, self.state, chat_id, user_id, query_id
            )
        elif callback_data.startswith("resources:"):
            page_str = callback_data.split(":", 1)[1]
            try:
                page = int(page_str)
            except ValueError:
                page = 1
            await handle_resources(
                self.api, self.state, chat_id, user_id, page, query_id
            )
        elif callback_data == "vacation":
            await handle_vacation(self.api, self.state, chat_id, user_id, query_id)
        elif callback_data == "wifi_password":
            await handle_wifi(self.api, self.state, chat_id, user_id, query_id)
        elif callback_data == "manager_menu":
            await handle_manager_menu(
                self.api, self.state, chat_id, user_id, query_id
            )
        elif callback_data == "manager_employees":
            await handle_manager_employees(
                self.api, self.state, chat_id, user_id, query_id
            )
        elif callback_data == "manager_approvals":
            await handle_manager_approvals(
                self.api, self.state, chat_id, user_id, query_id
            )
        elif callback_data == "counterparty_report":
            await handle_counterparty_prompt(
                self.api, self.state, chat_id, user_id, query_id
            )
        elif callback_data in PAUSED_CALLBACKS:
            await handle_paused_section(
                self.api, self.state, chat_id, user_id, query_id
            )
        else:
            logger.warning("Unknown callback: %s", callback_data)
            if query_id:
                await self.api.answer_callback(query_id)
