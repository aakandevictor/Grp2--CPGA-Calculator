"""Graduate student model with research capabilities."""

from __future__ import annotations

from datetime import date

from .mixins import ResearchWorkerMixin
from .persons import Student


class GraduateStudent(Student, ResearchWorkerMixin):
    """Represents a graduate student with research supervision."""

    _VALID_DEGREE_TYPES = {"MSc", "PhD"}

    def __init__(
        self,
        full_name: str,
        matric_no: str,
        department: str,
        date_of_birth: date,
        level: int = 700,
        degree_type: str = "MSc",
    ) -> None:
        # Use cooperative super() with the same parameter names Student expects
        super().__init__(
            full_name=full_name,
            matric_no=matric_no,
            department=department,
            date_of_birth=date_of_birth,
            level=level,
        )
        self.degree_type = degree_type

    @property
    def degree_type(self) -> str:
        return self._degree_type

    @degree_type.setter
    def degree_type(self, value: str) -> None:
        if value not in self._VALID_DEGREE_TYPES:
            raise ValueError("degree_type must be 'MSc' or 'PhD'")
        self._degree_type = value

    def __str__(self) -> str:
        return (
            f"Graduate Student: {self.full_name} | Degree: {self.degree_type} | "
            f"Matric: {self.matric_no} | Dept: {self.department} | "
            f"Research: {self.research_summary()}"
        )

    def __repr__(self) -> str:
        return (
            f"GraduateStudent(full_name={self.full_name!r}, matric_no={self.matric_no!r}, "
            f"department={self.department!r}, date_of_birth={self._date_of_birth!r}, "
            f"degree_type={self.degree_type!r})"
        )
