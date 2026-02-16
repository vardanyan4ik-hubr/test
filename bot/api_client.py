"""Async HTTP client for MAX Bot API."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import aiohttp

from bot.config import config

logger = logging.getLogger(__name__)

API_RETRY_ATTEMPTS = 3
API_RETRY_BACKOFF = 2  # seconds, multiplied each attempt


class MaxBotApi:
    """Wrapper around MAX (VK Teams) Bot API."""

    def __init__(self, token: str | None = None, base_url: str | None = None):
        self.token = token or config.token
        self.base_url = (base_url or config.api_base_url).rstrip("/")
        self._session: aiohttp.ClientSession | None = None
        self._last_event_id: int = 0

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    # -- low-level request with retry -------------------------------------------

    async def _request(
        self, method: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"{self.base_url}/{method}"
        base_params = {"token": self.token}
        if params:
            base_params.update(params)

        session = await self._get_session()
        last_exc: Exception | None = None

        for attempt in range(1, API_RETRY_ATTEMPTS + 1):
            try:
                async with session.get(url, params=base_params, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                    data = await resp.json()
                    if resp.status == 200 and data.get("ok", True):
                        return data
                    logger.warning("API %s returned %s: %s", method, resp.status, data)
                    return data
            except Exception as exc:
                last_exc = exc
                wait = API_RETRY_BACKOFF * attempt
                logger.warning(
                    "API %s attempt %d failed: %s — retrying in %ds",
                    method, attempt, exc, wait,
                )
                await asyncio.sleep(wait)

        logger.error("API %s failed after %d attempts", method, API_RETRY_ATTEMPTS)
        raise last_exc  # type: ignore[misc]

    # -- Bot API methods --------------------------------------------------------

    async def get_events(self, poll_time: int = 30) -> list[dict[str, Any]]:
        """Long-poll for new events."""
        data = await self._request(
            "events/get",
            {"lastEventId": self._last_event_id, "pollTime": poll_time},
        )
        events = data.get("events", [])
        if events:
            self._last_event_id = events[-1]["eventId"]
        return events

    async def send_text(
        self,
        chat_id: str,
        text: str,
        inline_keyboard: list[list[dict[str, str]]] | None = None,
        parse_mode: str = "MarkdownV2",
    ) -> dict[str, Any]:
        """Send a text message with optional inline keyboard."""
        params: dict[str, Any] = {
            "chatId": chat_id,
            "text": text,
        }
        if parse_mode:
            params["parseMode"] = parse_mode
        if inline_keyboard:
            params["inlineKeyboardMarkup"] = json.dumps(inline_keyboard)
        return await self._request("messages/sendText", params)

    async def edit_text(
        self,
        chat_id: str,
        msg_id: str,
        text: str,
        inline_keyboard: list[list[dict[str, str]]] | None = None,
        parse_mode: str = "MarkdownV2",
    ) -> dict[str, Any]:
        """Edit an existing message."""
        params: dict[str, Any] = {
            "chatId": chat_id,
            "msgId": msg_id,
            "text": text,
        }
        if parse_mode:
            params["parseMode"] = parse_mode
        if inline_keyboard:
            params["inlineKeyboardMarkup"] = json.dumps(inline_keyboard)
        return await self._request("messages/editText", params)

    async def answer_callback(
        self, query_id: str, text: str = "", show_alert: bool = False
    ) -> dict[str, Any]:
        """Answer a callback query."""
        params: dict[str, Any] = {"queryId": query_id}
        if text:
            params["text"] = text
        if show_alert:
            params["showAlert"] = "true"
        return await self._request("messages/answerCallbackQuery", params)

    async def get_self(self) -> dict[str, Any]:
        return await self._request("self/get")
