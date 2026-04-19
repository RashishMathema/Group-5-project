from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


VALID_MODES = {"interview", "resume", "checklist"}


@dataclass
class ChatState:
    current_mode: Optional[str] = None

    def reset(self) -> None:
        self.current_mode = None

    def set_mode(self, mode: str) -> bool:
        normalized = mode.strip().lower()
        if normalized in VALID_MODES:
            self.current_mode = normalized
            return True
        return False
