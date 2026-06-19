"""Custom exception classes for the FUOYE CGPA system."""

from __future__ import annotations


class GradeError(ValueError):
    """Raised when a grade or score value is invalid."""

    def __init__(self, field: str, value: object, valid_range: str) -> None:
        self.field = field
        self.value = value
        self.valid_range = valid_range
        message = f"Grade error -- {field}={value}: valid range is {valid_range}"
        super().__init__(message)

    def __str__(self) -> str:
        return f"Grade error -- {self.field}={self.value}: valid range is {self.valid_range}"


class PrerequisiteError(ValueError):
    """Raised when a student has not satisfied course prerequisites."""

    def __init__(self, course_code: str, missing_prerequisites: list[str]) -> None:
        self.course_code = course_code
        self.missing_prerequisites = missing_prerequisites
        missing = ", ".join(missing_prerequisites)
        message = (
            f"Prerequisite error -- {course_code}: missing prerequisites "
            f"[{missing}]"
        )
        super().__init__(message)

    def __str__(self) -> str:
        missing = ", ".join(self.missing_prerequisites)
        return (
            f"Prerequisite error -- {self.course_code}: missing prerequisites "
            f"[{missing}]"
        )


class CreditLoadError(ValueError):
    """Raised when a semester credit load is outside allowed limits."""

    def __init__(
        self,
        attempted_units: int,
        min_units: int = 15,
        max_units: int = 24,
    ) -> None:
        self.attempted_units = attempted_units
        self.min_units = min_units
        self.max_units = max_units
        message = (
            f"Credit load error -- attempted_units={attempted_units}: "
            f"allowed range is {min_units}-{max_units}"
        )
        super().__init__(message)

    def __str__(self) -> str:
        return (
            f"Credit load error -- attempted_units={self.attempted_units}: "
            f"allowed range is {self.min_units}-{self.max_units}"
        )


class DepartmentError(ValueError):
    """Raised when a department-level operation fails."""

    def __init__(self, dept_code: str, detail: str) -> None:
        self.dept_code = dept_code
        self.detail = detail
        message = f"Department error -- {dept_code}: {detail}"
        super().__init__(message)

    def __str__(self) -> str:
        return f"Department error -- {self.dept_code}: {self.detail}"
