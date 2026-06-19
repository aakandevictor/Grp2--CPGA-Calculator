"""Entry point demonstrating the FUOYE University Course Registration and CGPA system."""

from datetime import date

from src import (
    Course,
    Department,
    EnrolmentRecord,
    GraduateStudent,
    Lecturer,
    Semester,
    Student,
)
from src.exceptions import CreditLoadError, PrerequisiteError


def transcript_formatter(obj):
    """Duck-typed transcript formatter — no isinstance() check."""
    return obj.generate_transcript()


def main() -> None:
    print("=" * 60)
    print("SECTION: CREATE COURSES")
    print("=" * 60)
    courses = [
        Course("CPE101", "Introduction to Computing", 3),
        Course("MTH101", "Calculus I", 4),
        Course("PHY101", "Physics I", 3),
        Course("GST101", "Use of English", 2),
        Course("CPE102", "Programming Fundamentals", 3, ["CPE101"]),
        Course("CPE201", "Data Structures", 4, ["CPE102"]),
    ]
    for course in courses:
        print(course)

    print("=" * 60)
    print("SECTION: CREATE DEPARTMENT")
    print("=" * 60)
    department = Department("CPE", "Computer Engineering")
    for course in courses:
        department.add_course(course)
    print(department)

    print("=" * 60)
    print("SECTION: CREATE LECTURERS")
    print("=" * 60)
    lecturers = [
        Lecturer(
            "Amina Yusuf",
            "CPE/STAFF/0001",
            "Computer Engineering",
            date(1980, 4, 12),
            "PROFESSOR",
        ),
        Lecturer(
            "Oluwaseun Ade",
            "CPE/STAFF/0002",
            "Computer Engineering",
            date(1985, 9, 20),
            "LECTURER",
        ),
    ]
    for lecturer in lecturers:
        department.add_lecturer(lecturer)
        print(lecturer)

    print("=" * 60)
    print("SECTION: CREATE STUDENTS")
    print("=" * 60)
    students = [
        Student(
            "Chinwe Nnadi",
            "CPE/2022/001",
            "Computer Engineering",
            date(2003, 5, 11),
            200,
        ),
        Student(
            "Emeka Okafor",
            "CPE/2021/002",
            "Computer Engineering",
            date(2002, 8, 30),
            400,
        ),
        Student(
            "Bola Samuel",
            "CPE/2020/003",
            "Computer Engineering",
            date(2001, 11, 4),
            300,
        ),
    ]
    for student in students:
        department.enrol_student(student)
        print(student)

    # Graduate student with research supervision
    grad_student = GraduateStudent(
        "Halima Bello",
        "CPE/2025/004",
        "Computer Engineering",
        date(1998, 2, 14),
        level=700,
        degree_type="MSc",
    )
    department.enrol_student(grad_student)
    print(grad_student)

    print("=" * 60)
    print("SECTION: SEMESTER 1 ENROLMENT")
    print("=" * 60)
    semester1 = Semester("2023/2024", 1)
    non_prereq_courses = [c for c in courses if not c.prerequisite_codes]
    # Scores covering ALL grade boundaries: A, B, C, D, E, F
    scores = [85, 73, 61, 49, 42, 35]
    for course, score in zip(non_prereq_courses, scores):
        record = EnrolmentRecord(
            students[0], course, "2023/2024 Semester 1", score
        )
        semester1.add_record(record)
    students[0].add_semester(semester1)
    print(semester1)
    print("Contains CPE101:", "CPE101" in semester1)

    print("=" * 60)
    print("SECTION: PREREQUISITE DEMONSTRATION")
    print("=" * 60)
    # First attempt — student[1] has NOT passed CPE101 yet
    semester2 = Semester("2023/2024", 2)
    try:
        record = EnrolmentRecord(
            students[1], courses[4], "2023/2024 Semester 2", 78
        )
        semester2.add_record(record)
    except PrerequisiteError as error:
        print("Caught prerequisite error:", error)

    # Give student[1] a completed semester with CPE101 passed
    completed_semester = Semester("2022/2023", 1)
    completed_semester.add_record(
        EnrolmentRecord(
            students[1], courses[0], "2022/2023 Semester 1", 80
        )
    )
    students[1].add_semester(completed_semester)

    # Now enrol in CPE102 — prerequisite CPE101 now satisfied
    record = EnrolmentRecord(
        students[1], courses[4], "2023/2024 Semester 2", 78
    )
    semester2.add_record(record)
    students[1].add_semester(semester2)
    print("Prerequisite satisfied — enrolled in CPE102:")
    print(semester2)

    print("=" * 60)
    print("SECTION: CREDIT LOAD DEMONSTRATION")
    print("=" * 60)
    heavy_semester = Semester("2023/2024", 2)
    try:
        heavy_courses = [
            Course("HC101", "Heavy Course 1", 6),
            Course("HC102", "Heavy Course 2", 6),
            Course("HC103", "Heavy Course 3", 6),
            Course("HC104", "Heavy Course 4", 6),
            Course("HC105", "Heavy Course 5", 6),
        ]
        for c in heavy_courses:
            heavy_semester.add_record(
                EnrolmentRecord(
                    students[2], c, "2023/2024 Semester 2", 65
                )
            )
    except CreditLoadError as error:
        print("Caught maximum credit load error:", error)

    # Minimum credit load check
    small_semester = Semester("2023/2024", 1)
    small_semester.add_record(
        EnrolmentRecord(
            students[2], courses[0], "2023/2024 Semester 1", 70
        )
    )
    try:
        small_semester.validate_credit_load()
    except CreditLoadError as error:
        print("Caught minimum credit load error:", error)

    print("=" * 60)
    print("SECTION: COMPUTE AND DISPLAY CGPA")
    print("=" * 60)
    # Show transcripts for first 3 students
    for student in students[:3]:
        print(student)
        print(student.generate_transcript())
        print("-" * 60)

    print("=" * 60)
    print("SECTION: GRADUATE STUDENT RESEARCH")
    print("=" * 60)
    grad_student.supervisor = lecturers[0]
    grad_student.thesis_title = "AI for Sustainable Energy Management in Nigeria"
    grad_student.submit_abstract()
    print(grad_student.research_summary())

    print("=" * 60)
    print("SECTION: DEPARTMENT ANALYTICS")
    print("=" * 60)
    print(department.department_report())

    print("=" * 60)
    print("SECTION: DUCK TYPING DEMONSTRATION")
    print("=" * 60)

    class TranscriptSource:
        """Mock object to demonstrate duck typing."""

        def generate_transcript(self) -> str:
            return "Custom transcript from a duck-typed object."

    print("--- Student transcript via duck typing ---")
    print(transcript_formatter(students[0]))
    print("--- Mock object transcript via duck typing ---")
    print(transcript_formatter(TranscriptSource()))

    print("=" * 60)
    print("SECTION: OPERATOR OVERLOADING DEMONSTRATION")
    print("=" * 60)
    sorted_courses = sorted(courses)
    print("Courses sorted alphabetically by code:")
    for course in sorted_courses:
        print(f"  {course.course_code} — {course.title}")

    print(f"\nCourse equality (CPE101 == CPE101): {courses[0] == courses[0]}")
    print(f"Course equality (CPE101 == MTH101): {courses[0] == courses[1]}")
    print(f"Course ordering (CPE101 < MTH101):  {courses[0] < courses[1]}")
    print(f"CPE101 in semester1:                {'CPE101' in semester1}")
    print(f"CPE999 in semester1:                {'CPE999' in semester1}")

    print("=" * 60)
    print("SYSTEM DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()