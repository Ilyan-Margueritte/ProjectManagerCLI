"""
Data models for PMCLI.
Task and Project are simple dataclasses with JSON serialization helpers.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class Task:
    title: str
    done: bool = False
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            title=data["title"],
            done=data.get("done", False),
            created_at=data.get("created_at", _now()),
        )


@dataclass
class Project:
    name: str
    status: str = "active"
    created_at: str = field(default_factory=_now)
    tasks: List[Task] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        # Migrate legacy task format (plain strings → Task dicts)
        raw_tasks = data.get("tasks", [])
        tasks = []
        for t in raw_tasks:
            if isinstance(t, str):
                tasks.append(Task(title=t))
            else:
                tasks.append(Task.from_dict(t))

        return cls(
            name=data.get("name", ""),
            status=data.get("status", "active"),
            created_at=data.get("created_at", _now()),
            tasks=tasks,
        )

    # ── Convenience helpers ──────────────────────────────────────────────────

    def find_task(self, title: str) -> Task | None:
        """Case-insensitive task lookup by title."""
        title_lower = title.lower()
        for task in self.tasks:
            if task.title.lower() == title_lower:
                return task
        return None

    def task_summary(self) -> str:
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.done)
        return f"{done}/{total}"
