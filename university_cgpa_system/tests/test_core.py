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


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_student() -> Student:
    return Student(
        "Akande Victor Ayomide",
        "CPE/2023/1022",
        "Computer Engineering",
        date(2004, 2, 19),
        300,
    )


@pytest.fixture
def sample_lecturer() -> Lecturer:
    return Lecturer(
        "Soladoye Adewale Abiodun",
        "CPE/STAFF/0001",
        "Computer Engineering",
        date(1978, 5, 10),
        "LECTURER",
    )


@pytest.fixture
def course_no_prereq() -> Course:
    return Course("CPE302", "Computer Architecture", 3)


@pytest.fixture
def course_with_prereq() -> Course:
    return Course("CPE312", "Software Engineering", 3, ["CPE302"])


@pytest.fixture
def sample_semester() -> Semester:
    return Semester("2023/2024", 1)


# ── Construction Tests (valid) ───────────────────────────────────────────────

def test_student_valid_construction(sample_student: Student) -> None:
    assert sample_student.full_name == "Akande Victor Ayomide"
    assert sample_student.matric_no == "CPE/2023/1022"
    assert sample_student.level == 300
    assert sample_student.department == "Computer Engineering"


def test_lecturer_valid_construction(sample_lecturer: Lecturer) -> None:
    assert sample_lecturer.staff_id == "CPE/STAFF/0001"
    assert sample_lecturer.rank == "LECTURER"
    assert "Dept" in str(sample_lecturer)


def test_course_valid_construction(course_with_prereq: Course) -> None:
    assert course_with_prereq.course_code == "CPE312"
    assert course_with_prereq.credit_units == 3
    assert course_with_prereq.prerequisite_codes == ["CPE302"]


def test_enrolment_record_valid_construction(
    sample_student: Student, course_no_prereq: Course
) -> None:
    record = EnrolmentRecord(
        sample_student, course_no_prereq, "2023/2024 Semester 1", 70
    )
    assert record.grade == "A"
    assert record.grade_point == 5


def test_semester_valid_construction(sample_semester: Semester) -> None:
    assert len(sample_semester) == 0
    assert sample_semester.wgpa == 0.0
    assert "Semester" in str(sample_semester)


def test_department_valid_construction(
    sample_student: Student,
    sample_lecturer: Lecturer,
    course_no_prereq: Course,
) -> None:
    department = Department("CPE", "Computer Engineering")
    department.add_course(course_no_prereq)
    department.enrol_student(sample_student)
    department.add_lecturer(sample_lecturer)
    assert len(department.get_courses()) == 1
    assert sample_student in department


# ── Construction Tests (invalid) ────────────────────────────────────────────

def test_student_invalid_matric_no_raises_value_error() -> None:
    with pytest.raises(GradeError):
        Student(
            "Afolabi Oluwajuwon Ayomiposi",
            "INVALID/123",
            "Computer Engineering",
            date(2004, 3, 15),
            300,
        )


def test_student_invalid_level_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Student(
            "Afolayan Emmanuel Ibukunoluwa",
            "CPE/2023/1016",
            "Computer Engineering",
            date(2004, 7, 22),
            999,
        )


def test_lecturer_invalid_staff_id_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Lecturer(
            "Adebiyi Temitope Funmilayo",
            "CPE/001",
            "Computer Engineering",
            date(1980, 1, 1),
            "LECTURER",
        )


def test_lecturer_invalid_rank_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Lecturer(
            "Asaolu Oluwaseun Oluwole",
            "CPE/STAFF/0002",
            "Computer Engineering",
            date(1975, 3, 12),
            "INSTRUCTOR",
        )


def test_course_invalid_credit_units_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Course("CPE306", "Embedded Systems", 10)


def test_enrolment_score_out_of_range_raises_grade_error(
    sample_student: Student, course_no_prereq: Course
) -> None:
    with pytest.raises(GradeError):
        EnrolmentRecord(
            sample_student, course_no_prereq, "2023/2024 Semester 1", 120
        )


# ── Business Logic Tests ─────────────────────────────────────────────────────

def test_score_to_grade_all_boundaries() -> None:
    assert score_to_grade(70) == "A"
    assert score_to_grade(60) == "B"
    assert score_to_grade(50) == "C"
    assert score_to_grade(45) == "D"
    assert score_to_grade(40) == "E"
    assert score_to_grade(39) == "F"


def test_wgpa_computation_correct(
    sample_student: Student, course_no_prereq: Course
) -> None:
    semester = Semester("2023/2024", 1)
    semester.add_record(
        EnrolmentRecord(sample_student, course_no_prereq, "2023/2024 Semester 1", 70)
    )
    semester.add_record(
        EnrolmentRecord(
            sample_student,
            Course("ABE302", "Agricultural Engineering Fundamentals", 3),
            "2023/2024 Semester 1",
            50,
        )
    )
    assert semester.wgpa == pytest.approx((5 * 3 + 3 * 3) / 6, rel=1e-2)


def test_cgpa_across_multiple_semesters(sample_student: Student) -> None:
    sem1 = Semester("2023/2024", 1)
    sem1.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE302", "Computer Architecture", 3),
            "2023/2024 Semester 1",
            70,
        )
    )
    sample_student.add_semester(sem1)
    sem2 = Semester("2023/2024", 2)
    sem2.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE306", "Microprocessors", 3),
            "2023/2024 Semester 2",
            50,
        )
    )
    sample_student.add_semester(sem2)
    assert sample_student.compute_cgpa() == pytest.approx(
        (5 * 3 + 3 * 3) / 6, rel=1e-2
    )


def test_honour_class_first_class(sample_student: Student) -> None:
    sem = Semester("2023/2024", 1)
    sem.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE302", "Computer Architecture", 3),
            "2023/2024 Semester 1",
            90,
        )
    )
    sem.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE310", "OOP with Python", 3),
            "2023/2024 Semester 1",
            85,
        )
    )
    sample_student.add_semester(sem)
    assert sample_student.honour_class == "First Class"


def test_honour_class_second_upper(sample_student: Student) -> None:
    sem = Semester("2023/2024", 1)
    sem.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE302", "Computer Architecture", 3),
            "2023/2024 Semester 1",
            70,
        )
    )
    sem.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE306", "Microprocessors", 3),
            "2023/2024 Semester 1",
            55,
        )
    )
    sample_student.add_semester(sem)
    assert sample_student.honour_class == "Second Class Upper"


def test_prerequisite_error_raised_when_not_passed(
    sample_student: Student, course_with_prereq: Course
) -> None:
    with pytest.raises(PrerequisiteError):
        EnrolmentRecord(
            sample_student, course_with_prereq, "2023/2024 Semester 1", 80
        )


def test_prerequisite_passes_when_course_completed(
    sample_student: Student, course_with_prereq: Course
) -> None:
    prereq_course = Course("CPE302", "Computer Architecture", 3)
    sem = Semester("2022/2023", 1)
    sem.add_record(
        EnrolmentRecord(
            sample_student, prereq_course, "2022/2023 Semester 1", 40
        )
    )
    sample_student.add_semester(sem)
    record = EnrolmentRecord(
        sample_student, course_with_prereq, "2023/2024 Semester 1", 70
    )
    assert record.grade == "A"


def test_credit_load_error_when_exceeding_24_units(
    sample_student: Student,
) -> None:
    sem = Semester("2023/2024", 1)
    sem.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE302", "Computer Architecture", 6),
            "2023/2024 Semester 1",
            70,
        )
    )
    sem.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE306", "Microprocessors", 6),
            "2023/2024 Semester 1",
            65,
        )
    )
    sem.add_record(
        EnrolmentRecord(
            sample_student,
            Course("ABE302", "Agricultural Engineering", 6),
            "2023/2024 Semester 1",
            60,
        )
    )
    sem.add_record(
        EnrolmentRecord(
            sample_student,
            Course("CPE310", "OOP with Python", 6),
            "2023/2024 Semester 1",
            75,
        )
    )
    with pytest.raises(CreditLoadError):
        sem.add_record(
            EnrolmentRecord(
                sample_student,
                Course("CPE312", "Software Engineering", 3),
                "2023/2024 Semester 1",
                55,
            )
        )


# ── Dunder Method Tests ──────────────────────────────────────────────────────

def test_course_equality_by_code() -> None:
    course1 = Course("CPE310", "OOP with Python", 3)
    course2 = Course("CPE 310", "OOP with Python", 3)
    assert course1 == course2


def test_course_ordering_alphabetic() -> None:
    course_a = Course("ABE302", "Agricultural Engineering", 3)
    course_b = Course("CPE302", "Computer Architecture", 3)
    assert sorted([course_b, course_a])[0] is course_a


def test_course_hash_consistency() -> None:
    course1 = Course("CPE310", "OOP with Python", 3)
    course2 = Course("CPE 310", "OOP with Python", 3)
    assert hash(course1) == hash(course2)


def test_course_addition_operator() -> None:
    course1 = Course("CPE302", "Computer Architecture", 3)
    course2 = Course("CPE306", "Microprocessors", 3)
    assert course1 + course2 == 6
    assert sum([course1, course2], 0) == 6


def test_semester_len(
    sample_semester: Semester,
    sample_student: Student,
    course_no_prereq: Course,
) -> None:
    record = EnrolmentRecord(
        sample_student, course_no_prereq, "2023/2024 Semester 1", 70
    )
    sample_semester.add_record(record)
    assert len(sample_semester) == 1


def test_semester_contains_by_course_code(
    sample_semester: Semester,
    sample_student: Student,
    course_no_prereq: Course,
) -> None:
    sample_semester.add_record(
        EnrolmentRecord(sample_student, course_no_prereq, "2023/2024 Semester 1", 70)
    )
    assert "CPE302" in sample_semester


def test_semester_iteration(
    sample_semester: Semester,
    sample_student: Student,
    course_no_prereq: Course,
) -> None:
    record = EnrolmentRecord(
        sample_student, course_no_prereq, "2023/2024 Semester 1", 70
    )
    sample_semester.add_record(record)
    assert list(iter(sample_semester)) == [record]


# ── Duck Typing Test ─────────────────────────────────────────────────────────

def test_transcript_formatter_duck_typing() -> None:
    class MockTranscript:
        def generate_transcript(self) -> str:
            return "mock transcript"

    def transcript_formatter(obj):
        return obj.generate_transcript()

    assert transcript_formatter(MockTranscript()) == "mock transcript"


# ── Exception Structure Tests ────────────────────────────────────────────────

def test_grade_error_has_structured_fields() -> None:
    error = GradeError(field="score", value=101, valid_range="0.0-100.0")
    assert error.field == "score"
    assert error.value == 101
    assert error.valid_range == "0.0-100.0"


def test_prerequisite_error_has_missing_list() -> None:
    error = PrerequisiteError(
        course_code="CPE312", missing_prerequisites=["CPE302"]
    )
    assert error.missing_prerequisites == ["CPE302"]


def test_credit_load_error_has_unit_fields() -> None:
    error = CreditLoadError(attempted_units=25)
    assert error.attempted_units == 25
    assert error.min_units == 15
    assert error.max_units == 24


# ── Graduate Student / MRO Tests ─────────────────────────────────────────────

def test_graduate_student_inherits_from_both() -> None:
    grad = GraduateStudent(
        "Amos Timilehin Samson",
        "CPE/2023/1029",
        "Computer Engineering",
        date(2000, 6, 18),
        level=700,
        degree_type="MSc",
    )
    assert isinstance(grad, Student)
    assert hasattr(grad, "research_summary")


def test_graduate_student_mro_cooperative_init() -> None:
    assert GraduateStudent.__mro__[1].__name__ == "Student"
    assert GraduateStudent.__mro__[2].__name__ == "ResearchWorkerMixin"


def test_research_worker_supervisor_validation(
    sample_lecturer: Lecturer,
) -> None:
    grad = GraduateStudent(
        "Allison Idris Adeola",
        "CPE/2023/1028",
        "Computer Engineering",
        date(2000, 7, 11),
        level=700,
        degree_type="PhD",
    )
    grad.supervisor = sample_lecturer
    with pytest.raises(TypeError):
        grad.supervisor = "not a lecturer"
