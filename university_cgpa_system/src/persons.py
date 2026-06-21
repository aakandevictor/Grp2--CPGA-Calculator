filepath = '/content/Grp2--CPGA-Calculator/university_cgpa_system/src/persons.py'

content = '''"""Person-related entities for the FUOYE CGPA system."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from datetime import date
from typing import List

from .exceptions import GradeError


class Person(ABC):
    """Abstract base class representing a university person."""

    def __init__(self, full_name: str, person_id: str, date_of_birth: date) -> None:
        self._date_of_birth = date_of_birth
        self.full_name = full_name
        self._person_id = person_id

    @property
    @abstractmethod
    def full_name(self) -> str:
        raise NotImplementedError

    @full_name.setter
    @abstractmethod
    def full_name(self, value: str) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def person_id(self) -> str:
        raise NotImplementedError

    @property
    def age(self) -> int:
        today = date.today()
        years = today.year - self._date_of_birth.year
        if (today.month, today.day) < (
            self._date_of_birth.month,
            self._date_of_birth.day,
        ):
            years -= 1
        return years

    def __str__(self) -> str:
        return f"Person: {self.full_name} | ID: {self.person_id} | Age: {self.age}"

    def __repr__(self) -> str:
        return f"Person(full_name={self.full_name!r}, person_id={self.person_id!r})"


class Student(Person):
    """Concrete student class representing a university undergraduate."""

    _VALID_LEVELS = [100, 200, 300, 400, 500, 600, 700, 800]
    _MATRIC_PATTERN = re.compile(r"^[A-Z]{3,6}/\d{4}/\d{3,4}$")

    def __init__(
        self,
        full_name: str,
        matric_no: str,
        department: str,
        date_of_birth: date,
        level: int,
    ) -> None:
        super().__init__(full_name=full_name, person_id=matric_no, date_of_birth=date_of_birth)
        self.matric_no = matric_no
        self.department = department
        self.level = level
        self.__semesters: List["Semester"] = []
        self.__gpa: float = 0.0

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("full_name must be a string")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("full_name cannot be empty")
        self._full_name = cleaned

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def matric_no(self) -> str:
        return self._matric_no

    @matric_no.setter
    def matric_no(self, value: str) -> None:
        if not isinstance(value, str) or not self._MATRIC_PATTERN.match(value):
            raise GradeError(
                field="matric_no",
                value=value,
                valid_range="pattern [A-Z]{3,6}/YYYY/NNN or NNNN",
            )
        self._matric_no = value

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        if value not in self._VALID_LEVELS:
            raise ValueError(
                f"level must be one of {self._VALID_LEVELS}, got {value}"
            )
        self._level = value

    @property
    def honour_class(self) -> str:
        cgpa = self.compute_cgpa()
        if cgpa >= 4.50:
            return "First Class"
        if 3.50 <= cgpa <= 4.49:
            return "Second Class Upper"
        if 2.40 <= cgpa <= 3.49:
            return "Second Class Lower"
        if 1.50 <= cgpa <= 2.39:
            return "Third Class"
        if 1.00 <= cgpa <= 1.49:
            return "Pass"
        return "Fail"

    def add_semester(self, semester: "Semester") -> None:
        self.__semesters.append(semester)
        self.__gpa = self.compute_cgpa()

    def compute_cgpa(self) -> float:
        records = [
            record
            for semester in self.__semesters
            for record in semester.get_records()
        ]
        total_units = sum(record.course.credit_units for record in records)
        if total_units == 0:
            return 0.0
        total_points = sum(
            record.grade_point * record.course.credit_units for record
