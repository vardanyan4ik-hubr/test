"""User state management (in-memory, ready for Redis migration)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class UserState(str, Enum):
    IDLE = "IDLE"
    AUTHORIZED = "AUTHORIZED"
    SEARCH_EMPLOYEE = "SEARCH_EMPLOYEE"
    RESOURCES_PAGE = "RESOURCES_PAGE"
    COUNTERPARTY_REPORT = "COUNTERPARTY_REPORT"


@dataclass
class UserSession:
    user_id: str
    state: UserState = UserState.IDLE
    data: dict[str, Any] = field(default_factory=dict)
    authorized_at: str | None = None


class StateManager:
    """In-memory user session store."""

    def __init__(self) -> None:
        self._sessions: dict[str, UserSession] = {}

    def get(self, user_id: str) -> UserSession:
        if user_id not in self._sessions:
            self._sessions[user_id] = UserSession(user_id=user_id)
        return self._sessions[user_id]

    def set_state(self, user_id: str, state: UserState) -> None:
        session = self.get(user_id)
        session.state = state

    def set_data(self, user_id: str, key: str, value: Any) -> None:
        session = self.get(user_id)
        session.data[key] = value

    def get_data(self, user_id: str, key: str, default: Any = None) -> Any:
        session = self.get(user_id)
        return session.data.get(key, default)

    def reset(self, user_id: str) -> None:
        if user_id in self._sessions:
            del self._sessions[user_id]
