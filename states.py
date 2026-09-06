from __future__ import annotations

import time
from typing import Any


class SessionStore:
    """Short-lived, expiring conversational state for Telegram input flows."""

    def __init__(self, ttl_seconds: int = 600) -> None:
        self._sessions: dict[int, dict[str, Any]] = {}
        self._ttl_seconds = max(60, ttl_seconds)

    def set(self, user_id: int, flow: str, **data: Any) -> None:
        self._sessions[user_id] = {
            "flow": flow,
            "_expires_at": time.monotonic() + self._ttl_seconds,
            **data,
        }

    def get(self, user_id: int) -> dict[str, Any] | None:
        session = self._sessions.get(user_id)
        if not session:
            return None
        if float(session.get("_expires_at", 0)) <= time.monotonic():
            self._sessions.pop(user_id, None)
            return None
        return {key: value for key, value in session.items() if key != "_expires_at"}

    def pop(self, user_id: int) -> dict[str, Any] | None:
        session = self._sessions.pop(user_id, None)
        if not session or float(session.get("_expires_at", 0)) <= time.monotonic():
            return None
        return {key: value for key, value in session.items() if key != "_expires_at"}

    def clear(self, user_id: int) -> None:
        self._sessions.pop(user_id, None)
