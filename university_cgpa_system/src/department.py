"""Department model for course, student, and lecturer relationships."""

from __future__ import annotations

import re
from typing import List

from .academic import Course
from .exceptions import DepartmentError
from .persons import Lecturer, Student


class Department:
    """Represents an academic department with courses, students, and staff."""

    _CODE_PATTERN = re.compile(r"^[A-Z]{2,6}$")

    def __init__(self, dept_code: str, name: str) -> None:
        self.dept_code = dept_code
        self.name = name
        self.__courses: List[Course] = []
        self.__students: List[Student] = []
        self.__lecturers: List[Lecturer] = []

    @property
    def dept_code(self) -> str:
        return self._dept_code

    @dept_code.setter
    def dept_code(self, value: str) -> None:
        if not isinstance(value, str) or not self._CODE_PATTERN.match(value.strip()):
            raise DepartmentError(dept_code=value, detail="Invalid department code")
        self._dept_code = value.strip().upper()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise DepartmentError(dept_code=self.dept_code if hasattr(self, "_dept_code") else "", detail="Department name cannot be empty")
        self._name = value.strip()

    def add_course(self, course: Course) -> None:
        if not isinstance(course, Course):
            raise DepartmentError(self.dept_code, "course must be a Course instance")
        if course in self.__courses:
            return
        self.__courses.append(course)

    def remove_course(self, course_code: str) -> None:
        normalized = course_code.strip().upper()
        self.__courses = [course for course in self.__courses if course.course_code.upper() != normalized]

    def enrol_student(self, student: Student) -> None:
        if not isinstance(student, Student):
            raise DepartmentError(self.dept_code, "student must be a Student instance")
        if student not in self.__students:
            self.__students.append(student)

    def add_lecturer(self, lecturer: Lecturer) -> None:
        if not isinstance(lecturer, Lecturer):
            raise DepartmentError(self.dept_code, "lecturer must be a Lecturer instance")
        if lecturer not in self.__lecturers:
            self.__lecturers.append(lecturer)

    def get_courses(self) -> list[Course]:
        return list(self.__courses)

    def get_students(self) -> list[Student]:
        return list(self.__students)

    def get_lecturers(self) -> list[Lecturer]:
        return list(self.__lecturers)

    def honours_distribution(self) -> dict[str, int]:
        distribution = {
            "First Class": 0,
            "Second Class Upper": 0,
            "Second Class Lower": 0,
            "Third Class": 0,
            "Pass": 0,
            "Fail": 0,
        }
        for student in self.__students:
            if student.level == 400:
                distribution[student.honour_class] += 1
        return distribution

    def department_report(self) -> str:
        honours = self.honours_distribution()
        honours_lines = "\n".join(
            f"  {honour}: {count}" for honour, count in honours.items()
        )
        return (
            f"Department Report for {self.dept_code} - {self.name}\n"
            f"Courses: {len(self.__courses)} | Students: {len(self.__students)} | "
            f"Lecturers: {len(self.__lecturers)}\n"
            f"Honours distribution for 400-level:\n{honours_lines}"
        )

    def __str__(self) -> str:
        return f"Department {self.dept_code}: {self.name} | Courses: {len(self.__courses)}"

    def __repr__(self) -> str:
        return f"Department(dept_code={self.dept_code!r}, name={self.name!r})"

    def __len__(self) -> int:
        return len(self.__students)

    def __contains__(self, matric_no: object) -> bool:
        # Allow checking by Student instance or matric number string
        from .persons import Student as _Student

        if isinstance(matric_no, _Student):
            return any(student.matric_no.upper() == matric_no.matric_no.upper() for student in self.__students)
        if not isinstance(matric_no, str):
            return False
        normalized = matric_no.strip().upper()
        return any(student.matric_no.upper() == normalized for student in self.__students)
