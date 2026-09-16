from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class ChatRepository:
    """Lưu và đọc tin nhắn từ file JSON."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        project_root = Path(__file__).resolve().parent.parent
        self.file_path = Path(file_path or project_root / "data" / "messages.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        try:
            content = self.file_path.read_text(encoding="utf-8")
            data = json.loads(content or "[]")
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def _write(self, messages: list[dict[str, Any]]) -> None:
        self.file_path.write_text(
            json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def get_messages(self) -> list[dict[str, Any]]:
        return self._read()

    def add_message(self, role: str, content: str) -> dict[str, Any]:
        message = {
            "role": role,
            "content": content,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        messages = self._read()
        messages.append(message)
        self._write(messages)
        return message

    def clear_messages(self) -> None:
        self._write([])
