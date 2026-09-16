from __future__ import annotations

from datetime import date, datetime, timedelta

from database.study_repository import StudyRepository


class StudyBus:
    """Nghiệp vụ lịch học, bài tập, nhắc hạn và thống kê."""

    def __init__(self) -> None:
        self.repository = StudyRepository()

    def schedule(self) -> list[dict[str, str]]:
        return self.repository.get_schedule()

    def assignments(self) -> list[dict[str, str | bool]]:
        return self.repository.get_assignments()

    def add_schedule(self, subject: str, day: str, start: str, room: str, lecturer: str) -> None:
        if not subject.strip():
            raise ValueError("Tên môn học không được để trống.")
        self.repository.add_schedule(subject.strip(), day, start, room.strip(), lecturer.strip())

    def add_assignment(self, title: str, subject: str, due_date: date, priority: str) -> None:
        if not title.strip() or not subject.strip():
            raise ValueError("Tên bài tập và môn học không được để trống.")
        self.repository.add_assignment(title.strip(), subject.strip(), due_date.isoformat(), priority)

    def set_completed(self, assignment_id: str, completed: bool) -> None:
        self.repository.set_assignment_completed(assignment_id, completed)

    def due_soon(self, days: int = 7) -> list[dict[str, str | bool]]:
        today = date.today()
        limit = today + timedelta(days=days)
        return [
            item for item in self.assignments()
            if not item["completed"] and today <= datetime.fromisoformat(str(item["due_date"])).date() <= limit
        ]

    def stats(self) -> dict[str, int | float]:
        tasks = self.assignments()
        total = len(tasks)
        completed = sum(1 for task in tasks if task["completed"])
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "completion_rate": round(completed / total * 100) if total else 0,
        }
