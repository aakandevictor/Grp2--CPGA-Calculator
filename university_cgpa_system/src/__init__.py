"""Package entry point for the FUOYE CGPA system."""

from .academic import Course, EnrolmentRecord, Semester, GRADE_TABLE, score_to_grade
from .department import Department
from .graduate import GraduateStudent
from .mixins import ResearchWorkerMixin
from .persons import Lecturer, Person, Student

__all__ = [
    "Course",
    "EnrolmentRecord",
    "Semester",
    "GRADE_TABLE",
    "score_to_grade",
    "Department",
    "GraduateStudent",
    "ResearchWorkerMixin",
    "Lecturer",
    "Person",
    "Student",
]
