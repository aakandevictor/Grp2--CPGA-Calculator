"""Academic classes for courses, enrolment records, and semesters."""

from __future__ import annotations

import re
from functools import total_ordering
from typing import TYPE_CHECKING, List

from .exceptions import CreditLoadError, GradeError, PrerequisiteError

if TYPE_CHECKING:
    from .persons import Student

GRADE_TABLE = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
GRADE_RANGES = [
    (70, "A"),
    (60, "B"),
    (50, "C"),
    (45, "D"),
    (40, "E"),
    (0, "F"),
]


def score_to_grade(score: float) -> str:
    """Convert numeric score to letter grade using the Nigerian scale."""
    for threshold, grade in GRADE_RANGES:
        if score >= threshold:
            return grade
    return "F"


@total_ordering
class Course:
    """Represents a university course with credit and prerequisites."""

    _CODE_PATTERN = re.compile(r"^[A-Z]{2,5}\s?\d{3}$")

    def __init__(
        self,
        course_code: str,
        title: str,
        credit_units: int,
        prerequisite_codes: List[str] | None = None,
    ) -> None:
        self.course_code = course_code
        self.title = title
        self.credit_units = credit_units
        self.prerequisite_codes = prerequisite_codes or []

    @property
    def course_code(self) -> str:
        return self._course_code

    @course_code.setter
    def course_code(self, value: str) -> None:
        if not isinstance(value, str) or not self._CODE_PATTERN.match(value.strip()):
            raise ValueError("course_code must match pattern AAA999 or AAA 999")
        # Normalize course code by removing whitespace and uppercasing
        normalized = re.sub(r"\s+", "", value).upper()
        self._course_code = normalized

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title must be a non-empty string")
        self._title = value.strip()

    @property
    def credit_units(self) -> int:
        return self._credit_units

    @credit_units.setter
    def credit_units(self, value: int) -> None:
        if not isinstance(value, int) or not (1 <= value <= 6):
            raise ValueError("credit_units must be an integer between 1 and 6")
        self._credit_units = value

    @property
    def prerequisite_codes(self) -> list[str]:
        return list(self._prerequisite_codes)

    @prerequisite_codes.setter
    def prerequisite_codes(self, value: List[str]) -> None:
        if not isinstance(value, list):
            raise ValueError("prerequisite_codes must be a list of course codes")
        normalized = [item.strip().upper() for item in value if isinstance(item, str) and item.strip()]
        self._prerequisite_codes = normalized

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Course):
            return NotImplemented
        return self.course_code.upper() == other.course_code.upper()

    def __lt__(self, other: Course) -> bool:
        if not isinstance(other, Course):
            return NotImplemented
        return self.course_code.upper() < other.course_code.upper()

    def __hash__(self) -> int:
        return hash(self.course_code.upper())

    def __add__(self, other: object) -> int:
        if isinstance(other, Course):
            return self.credit_units + other.credit_units
        if isinstance(other, int):
            return self.credit_units + other
        return NotImplemented

    def __radd__(self, other: object) -> int:
        if isinstance(other, int):
            return other + self.credit_units
        if isinstance(other, Course):
            return self.credit_units + other.credit_units
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.course_code} — {self.title} ({self.credit_units} units)"

    def __repr__(self) -> str:
        return (
            f"Course(course_code={self.course_code!r}, title={self.title!r}, "
            f"credit_units={self.credit_units!r}, prerequisite_codes={self.prerequisite_codes!r})"
        )


class EnrolmentRecord:
    """Captures a student's registration and performance in a course."""

    def __init__(
        self,
        student: "Student",
        course: Course,
        semester_label: str,
        score: float,
    ) -> None:
        self._validate_prerequisites(student, course)
        self.student = student
        self.course = course
        self.semester_label = semester_label
        self.score = score

    @staticmethod
    def _validate_prerequisites(student: "Student", course: Course) -> None:
        missing = []
        completed_codes = {
            record.course.course_code.upper()
            for semester in student.get_semesters()
            for record in semester.get_records()
            if record.score >= 40.0
        }
        for prereq in course.prerequisite_codes:
            if prereq.upper() not in completed_codes:
                missing.append(prereq)
        if missing:
            raise PrerequisiteError(course_code=course.course_code, missing_prerequisites=missing)

    @property
    def score(self) -> float:
        return self._score

    @score.setter
    def score(self, value: float) -> None:
        if not isinstance(value, (int, float)) or not (0.0 <= float(value) <= 100.0):
            raise GradeError(field="score", value=value, valid_range="0.0-100.0")
        self._score = float(value)

    @property
    def grade(self) -> str:
        return score_to_grade(self.score)

    @property
    def grade_point(self) -> float:
        return float(GRADE_TABLE[self.grade])

    def __str__(self) -> str:
        return (
            f"{self.course.course_code} | {self.course.title} | "
            f"{self.score:.1f} | {self.grade} | {self.grade_point} | "
            f"{self.course.credit_units} units"
        )

    def __repr__(self) -> str:
        return (
            f"EnrolmentRecord(student={self.student.matric_no!r}, course={self.course.course_code!r}, "
            f"semester_label={self.semester_label!r}, score={self.score!r})"
        )


class Semester:
    """Represents one academic semester and its enrolment records."""

    def __init__(self, academic_year: str, semester_no: int) -> None:
        self.academic_year = academic_year
        self.semester_no = semester_no
        self.__records: List[EnrolmentRecord] = []

    @property
    def academic_year(self) -> str:
        return self._academic_year

    @academic_year.setter
    def academic_year(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("academic_year must be a non-empty string")
        self._academic_year = value.strip()

    @property
    def semester_no(self) -> int:
        return self._semester_no

    @semester_no.setter
    def semester_no(self, value: int) -> None:
        if value not in (1, 2):
            raise ValueError("semester_no must be 1 or 2")
        self._semester_no = value

    def _total_units(self) -> int:
        return sum(record.course.credit_units for record in self.__records)

    def add_record(self, record: EnrolmentRecord) -> None:
        current_units = self._total_units()
        if current_units + record.course.credit_units > 24:
            raise CreditLoadError(attempted_units=current_units + record.course.credit_units)
        self.__records.append(record)

    def get_records(self) -> list[EnrolmentRecord]:
        return list(self.__records)

    def validate_credit_load(self) -> None:
        total_units = self._total_units()
        if total_units < 15:
            raise CreditLoadError(attempted_units=total_units)

    @property
    def wgpa(self) -> float:
        total_units = self._total_units()
        if total_units == 0:
            return 0.0
        total_points = sum(
            record.grade_point * record.course.credit_units for record in self.__records
        )
        return round(total_points / total_units, 2)

    def __len__(self) -> int:
        return len(self.__records)

    def __contains__(self, course_code: object) -> bool:
        if not isinstance(course_code, str):
            return False
        normalized = course_code.strip().upper()
        return any(
            record.course.course_code.upper() == normalized for record in self.__records
        )

    def __iter__(self):
        return iter(self.__records)

    def __str__(self) -> str:
        return (
            f"Semester {self.semester_no} ({self.academic_year}) — "
            f"{len(self)} courses | WGPA: {self.wgpa:.2f}"
        )

    def __repr__(self) -> str:
        return (
            f"Semester(academic_year={self.academic_year!r}, "
            f"semester_no={self.semester_no!r})"
        )

    def generate_transcript_section(self) -> str:
        lines = [
            f"Semester {self.semester_no} ({self.academic_year})",
            "Course Code | Title | Score | Grade | Grade Point | Units",
            "-" * 70,
        ]
        for record in self.__records:
            lines.append(
                f"{record.course.course_code} | {record.course.title} | "
                f"{record.score:.1f} | {record.grade} | {record.grade_point} | "
                f"{record.course.credit_units}"
            )
        lines.append(f"Semester WGPA: {self.wgpa:.2f}")
        return "\n".join(lines)
