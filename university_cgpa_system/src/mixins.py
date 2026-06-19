"""Mixin classes for the FUOYE CGPA system."""

from __future__ import annotations

from typing import Any
from .persons import Person


class ResearchWorkerMixin(Person):
    """Provides research-related fields and behavior for graduate students."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._supervisor = None
        self._thesis_title = ""
        self._abstract_submitted = False

    @property
    def supervisor(self) -> "Lecturer" | None:
        return self._supervisor

    @supervisor.setter
    def supervisor(self, value: "Lecturer") -> None:
        from .persons import Lecturer

        if not isinstance(value, Lecturer):
            raise TypeError("supervisor must be a Lecturer")
        self._supervisor = value

    @property
    def thesis_title(self) -> str:
        return self._thesis_title

    @thesis_title.setter
    def thesis_title(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("thesis_title must be a non-empty string")
        self._thesis_title = value.strip()

    @property
    def abstract_submitted(self) -> bool:
        return self._abstract_submitted

    @abstract_submitted.setter
    def abstract_submitted(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("abstract_submitted must be a boolean")
        self._abstract_submitted = value

    def submit_abstract(self) -> None:
        if not self.thesis_title:
            raise ValueError("Cannot submit abstract without a thesis title")
        self._abstract_submitted = True

    def research_summary(self) -> str:
        supervisor_name = (
            self.supervisor.full_name if self.supervisor is not None else "No supervisor"
        )
        status = "submitted" if self.abstract_submitted else "not submitted"
        thesis = self.thesis_title or "No thesis title"
        return (
            f"Research Summary: Supervisor: {supervisor_name} | "
            f"Thesis: {thesis} | Abstract: {status}"
        )
