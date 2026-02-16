"""Entry point — starts the bot with long polling."""

from __future__ import annotations

import asyncio
import logging
import signal
import sys

from bot.api_client import MaxBotApi
from bot.config import config
from bot.router import EventRouter
from bot.state import StateManager

logger = logging.getLogger("bot")


def _setup_logging() -> None:
    level = getattr(logging, config.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


async def run_polling() -> None:
    """Main polling loop."""
    if not config.token:
        logger.error(
            "MAX_BOT_TOKEN is not set. "
            "Please set the environment variable and restart."
        )
        sys.exit(1)

    api = MaxBotApi()
    state = StateManager()
    router = EventRouter(api, state)

    stop_event = asyncio.Event()

    def _signal_handler() -> None:
        logger.info("Received shutdown signal")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _signal_handler)
        except NotImplementedError:
            pass

    info = await api.get_self()
    logger.info("Bot started: %s", info.get("nick", info.get("userId", "unknown")))

    while not stop_event.is_set():
        try:
            events = await api.get_events(poll_time=config.polling_interval)
            for event in events:
                try:
                    await router.handle_event(event)
                except Exception:
                    logger.exception("Error handling event: %s", event)
        except asyncio.CancelledError:
            break
        except Exception:
            logger.exception("Polling error, retrying in %ds", config.polling_interval)
            await asyncio.sleep(config.polling_interval)

    await api.close()
    logger.info("Bot stopped")


def main() -> None:
    _setup_logging()
    try:
        asyncio.run(run_polling())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")


if __name__ == "__main__":
    main()
