"""Pytest suite for the FUOYE University CGPA system."""

from datetime import date

import pytest

from src import (
    Course,
    Department,
    EnrolmentRecord,
    GraduateStudent,
    Lecturer,
    Semester,
    Student,
    score_to_grade,
)
from src.exceptions import CreditLoadError, GradeError, PrerequisiteError


@pytest.fixture
def sample_student() -> Student:
    return Student(
        "Test Student",
        "CPE/2022/001",
        "Computer Engineering",
        date(2003, 1, 1),
        200,
    )


@pytest.fixture
def sample_lecturer() -> Lecturer:
    return Lecturer(
        "Test Lecturer",
        "CPE/STAFF/0001",
        "Computer Engineering",
        date(1980, 1, 1),
        "LECTURER",
    )


@pytest.fixture
def course_no_prereq() -> Course:
    return Course("CPE101", "Intro to Computing", 3)


@pytest.fixture
def course_with_prereq() -> Course:
    return Course("CPE102", "Programming Fundamentals", 3, ["CPE101"])


@pytest.fixture
def sample_semester() -> Semester:
    return Semester("2025/2026", 1)


def test_student_valid_construction(sample_student: Student) -> None:
    assert sample_student.full_name == "Test Student"
    assert sample_student.matric_no == "CPE/2022/001"
    assert sample_student.level == 200
    assert sample_student.department == "Computer Engineering"


def test_lecturer_valid_construction(sample_lecturer: Lecturer) -> None:
    assert sample_lecturer.staff_id == "CPE/STAFF/0001"
    assert sample_lecturer.rank == "LECTURER"
    assert "Dept" in str(sample_lecturer)


def test_course_valid_construction(course_with_prereq: Course) -> None:
    assert course_with_prereq.course_code == "CPE102"
    assert course_with_prereq.credit_units == 3
    assert course_with_prereq.prerequisite_codes == ["CPE101"]


def test_enrolment_record_valid_construction(sample_student: Student, course_no_prereq: Course) -> None:
    record = EnrolmentRecord(sample_student, course_no_prereq, "2025/2026 Semester 1", 70)
    assert record.grade == "A"
    assert record.grade_point == 5


def test_semester_valid_construction(sample_semester: Semester) -> None:
    assert len(sample_semester) == 0
    assert sample_semester.wgpa == 0.0
    assert "Semester" in str(sample_semester)


def test_department_valid_construction(sample_student: Student, sample_lecturer: Lecturer, course_no_prereq: Course) -> None:
    department = Department("CPE", "Computer Engineering")
    department.add_course(course_no_prereq)
    department.enrol_student(sample_student)
    department.add_lecturer(sample_lecturer)
    assert len(department.get_courses()) == 1
    assert sample_student in department


def test_student_invalid_matric_no_raises_value_error() -> None:
    with pytest.raises(GradeError):
        Student("Invalid Student", "INVALID/123", "Computer Engineering", date(2003, 1, 1), 200)


def test_student_invalid_level_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Student("Invalid Level", "CPE/2022/002", "Computer Engineering", date(2003, 1, 1), 999)


def test_lecturer_invalid_staff_id_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Lecturer("Bad Staff", "CPE/001", "Computer Engineering", date(1980, 1, 1), "LECTURER")


def test_lecturer_invalid_rank_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Lecturer("Bad Rank", "CPE/STAFF/0002", "Computer Engineering", date(1980, 1, 1), "INSTRUCTOR")


def test_course_invalid_credit_units_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Course("CPE103", "Bad Credit", 10)


def test_enrolment_score_out_of_range_raises_grade_error(sample_student: Student, course_no_prereq: Course) -> None:
    with pytest.raises(GradeError):
        EnrolmentRecord(sample_student, course_no_prereq, "2025/2026 Semester 1", 120)


def test_score_to_grade_all_boundaries() -> None:
    assert score_to_grade(70) == "A"
    assert score_to_grade(60) == "B"
    assert score_to_grade(50) == "C"
    assert score_to_grade(45) == "D"
    assert score_to_grade(40) == "E"
    assert score_to_grade(39) == "F"


def test_wgpa_computation_correct(sample_student: Student, course_no_prereq: Course) -> None:
    semester = Semester("2025/2026", 1)
    semester.add_record(EnrolmentRecord(sample_student, course_no_prereq, "2025/2026 Semester 1", 70))
    semester.add_record(EnrolmentRecord(sample_student, Course("MTH101", "Calculus", 4), "2025/2026 Semester 1", 50))
    assert semester.wgpa == pytest.approx((5 * 3 + 3 * 4) / 7, rel=1e-2)


def test_cgpa_across_multiple_semesters(sample_student: Student) -> None:
    sem1 = Semester("2025/2026", 1)
    sem1.add_record(EnrolmentRecord(sample_student, Course("CPE101", "Intro", 3), "2025/2026 Semester 1", 70))
    sample_student.add_semester(sem1)
    sem2 = Semester("2025/2026", 2)
    sem2.add_record(EnrolmentRecord(sample_student, Course("MTH101", "Calculus", 4), "2025/2026 Semester 2", 50))
    sample_student.add_semester(sem2)
    assert sample_student.compute_cgpa() == pytest.approx((5 * 3 + 3 * 4) / 7, rel=1e-2)


def test_honour_class_first_class(sample_student: Student) -> None:
    sem = Semester("2025/2026", 1)
    sem.add_record(EnrolmentRecord(sample_student, Course("CPE101", "Intro", 3), "2025/2026 Semester 1", 90))
    sem.add_record(EnrolmentRecord(sample_student, Course("CPE102", "Programming", 3), "2025/2026 Semester 1", 85))
    sample_student.add_semester(sem)
    assert sample_student.honour_class == "First Class"


def test_honour_class_second_upper(sample_student: Student) -> None:
    sem = Semester("2025/2026", 1)
    sem.add_record(EnrolmentRecord(sample_student, Course("CPE101", "Intro", 3), "2025/2026 Semester 1", 70))
    sem.add_record(EnrolmentRecord(sample_student, Course("CPE102", "Programming", 3), "2025/2026 Semester 1", 55))
    sample_student.add_semester(sem)
    assert sample_student.honour_class == "Second Class Upper"


def test_prerequisite_error_raised_when_not_passed(sample_student: Student, course_with_prereq: Course) -> None:
    with pytest.raises(PrerequisiteError):
        EnrolmentRecord(sample_student, course_with_prereq, "2025/2026 Semester 1", 80)


def test_prerequisite_passes_when_course_completed(sample_student: Student, course_with_prereq: Course) -> None:
    prereq_course = Course("CPE101", "Intro", 3)
    sem = Semester("2024/2025", 1)
    sem.add_record(EnrolmentRecord(sample_student, prereq_course, "2024/2025 Semester 1", 40))
    sample_student.add_semester(sem)
    record = EnrolmentRecord(sample_student, course_with_prereq, "2025/2026 Semester 1", 70)
    assert record.grade == "A"


def test_credit_load_error_when_exceeding_24_units(sample_student: Student) -> None:
    sem = Semester("2025/2026", 1)
    sem.add_record(EnrolmentRecord(sample_student, Course("CPE101", "Intro", 6), "2025/2026 Semester 1", 70))
    sem.add_record(EnrolmentRecord(sample_student, Course("MTH101", "Calculus", 6), "2025/2026 Semester 1", 65))
    sem.add_record(EnrolmentRecord(sample_student, Course("PHY101", "Physics", 6), "2025/2026 Semester 1", 60))
    sem.add_record(EnrolmentRecord(sample_student, Course("GST101", "Use of English", 6), "2025/2026 Semester 1", 75))
    with pytest.raises(CreditLoadError):
        sem.add_record(EnrolmentRecord(sample_student, Course("CPE201", "Data Structures", 3), "2025/2026 Semester 1", 55))


def test_course_equality_by_code() -> None:
    course1 = Course("CPE101", "Intro", 3)
    course2 = Course("CPE 101", "Intro", 3)
    assert course1 == course2


def test_course_ordering_alphabetic() -> None:
    course_a = Course("CPE101", "Intro", 3)
    course_b = Course("MAT101", "Math", 3)
    assert sorted([course_b, course_a])[0] is course_a


def test_course_hash_consistency() -> None:
    course1 = Course("CPE101", "Intro", 3)
    course2 = Course("CPE 101", "Intro", 3)
    assert hash(course1) == hash(course2)


def test_course_addition_operator() -> None:
    course1 = Course("CPE101", "Intro", 3)
    course2 = Course("MTH101", "Calculus", 4)
    assert course1 + course2 == 7
    assert sum([course1, course2], 0) == 7


def test_semester_len(sample_semester: Semester, sample_student: Student, course_no_prereq: Course) -> None:
    record = EnrolmentRecord(sample_student, course_no_prereq, "2025/2026 Semester 1", 70)
    sample_semester.add_record(record)
    assert len(sample_semester) == 1


def test_semester_contains_by_course_code(sample_semester: Semester, sample_student: Student, course_no_prereq: Course) -> None:
    sample_semester.add_record(EnrolmentRecord(sample_student, course_no_prereq, "2025/2026 Semester 1", 70))
    assert "CPE101" in sample_semester


def test_semester_iteration(sample_semester: Semester, sample_student: Student, course_no_prereq: Course) -> None:
    record = EnrolmentRecord(sample_student, course_no_prereq, "2025/2026 Semester 1", 70)
    sample_semester.add_record(record)
    assert list(iter(sample_semester)) == [record]


def test_transcript_formatter_duck_typing() -> None:
    class MockTranscript:
        def generate_transcript(self) -> str:
            return "mock transcript"

    def transcript_formatter(obj):
        return obj.generate_transcript()

    assert transcript_formatter(MockTranscript()) == "mock transcript"


def test_grade_error_has_structured_fields() -> None:
    error = GradeError(field="score", value=101, valid_range="0.0-100.0")
    assert error.field == "score"
    assert error.value == 101
    assert error.valid_range == "0.0-100.0"


def test_prerequisite_error_has_missing_list() -> None:
    error = PrerequisiteError(course_code="CPE102", missing_prerequisites=["CPE101"])
    assert error.missing_prerequisites == ["CPE101"]


def test_credit_load_error_has_unit_fields() -> None:
    error = CreditLoadError(attempted_units=25)
    assert error.attempted_units == 25
    assert error.min_units == 15
    assert error.max_units == 24


def test_graduate_student_inherits_from_both() -> None:
    grad = GraduateStudent(
        "Grad Student",
        "CPE/2025/010",
        "Computer Engineering",
        date(1998, 1, 1),
        level=700,
        degree_type="MSc",
    )
    assert isinstance(grad, Student)
    assert hasattr(grad, "research_summary")


def test_graduate_student_mro_cooperative_init() -> None:
    assert GraduateStudent.__mro__[1].__name__ == "Student"
    assert GraduateStudent.__mro__[2].__name__ == "ResearchWorkerMixin"


def test_research_worker_supervisor_validation(sample_lecturer: Lecturer) -> None:
    grad = GraduateStudent(
        "Grad Student",
        "CPE/2025/011",
        "Computer Engineering",
        date(1998, 1, 1),
        level=700,
        degree_type="MSc",
    )
    grad.supervisor = sample_lecturer
    with pytest.raises(TypeError):
        grad.supervisor = "not a lecturer"
