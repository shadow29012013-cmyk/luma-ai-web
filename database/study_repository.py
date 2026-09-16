from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StudyRepository:
    """Lưu thời khóa biểu và bài tập trong một file JSON đơn giản."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        root = Path(__file__).resolve().parent.parent
        self.file_path = Path(file_path or root / "data" / "study_data.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write({"schedule": [], "assignments": []})

    def _read(self) -> dict[str, list[dict[str, Any]]]:
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return {
                    "schedule": data.get("schedule", []),
                    "assignments": data.get("assignments", []),
                }
        except (OSError, json.JSONDecodeError):
            pass
        return {"schedule": [], "assignments": []}

    def _write(self, data: dict[str, list[dict[str, Any]]]) -> None:
        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def get_schedule(self) -> list[dict[str, Any]]:
        return self._read()["schedule"]

    def add_schedule(self, subject: str, day: str, start: str, room: str, lecturer: str) -> dict[str, Any]:
        data = self._read()
        item = {
            "id": datetime.now().strftime("lesson-%Y%m%d%H%M%S%f"),
            "subject": subject,
            "day": day,
            "start": start,
            "room": room,
            "lecturer": lecturer,
        }
        data["schedule"].append(item)
        self._write(data)
        return item

    def get_assignments(self) -> list[dict[str, Any]]:
        return self._read()["assignments"]

    def add_assignment(self, title: str, subject: str, due_date: str, priority: str) -> dict[str, Any]:
        data = self._read()
        item = {
            "id": datetime.now().strftime("task-%Y%m%d%H%M%S%f"),
            "title": title,
            "subject": subject,
            "due_date": due_date,
            "priority": priority,
            "completed": False,
        }
        data["assignments"].append(item)
        self._write(data)
        return item

    def set_assignment_completed(self, assignment_id: str, completed: bool) -> None:
        data = self._read()
        for item in data["assignments"]:
            if item.get("id") == assignment_id:
                item["completed"] = completed
                break
        self._write(data)
