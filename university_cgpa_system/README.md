## Project Title and Overview

University Course Registration and CGPA Calculator is a Python OOP application for Federal University Oye-Ekiti (FUOYE). The system models students, lecturers, courses, enrolment records, semesters, and departments while enforcing Nigerian academic policies and computing CGPA accurately.git add .

## Team Members

| Full Name | Matric Number
| Afolabi Oluwajuwon Ayomiposi  CPE/2023/1015
| Afolayan Emmanuel Ibukunoluwa CPE/2023/1016 
| Agbotuta David Oghenekome     CPE/2023/1017
| Ajanaku Amidat Oluwadamilola  CPE/2023/1018
  Ajibade Michael Adeyemi      CPE/2023/1019
  Ajiboye Adesewa Christianah CPE/2023/1020
  Akanbi Kingsley Moyosore    CPE/2023/1021
  Akande Victor Ayomide       CPE/2023/1022
  Akintoye Isreal Olasukankanmi CPE/2023/1023
  Akinwwande Esther Taiwo       CPE/2023/1024
  Akinyemi Esther Ayomide      CPE/2023/1025
  Alabi Moses Olabode          CPE/2023/1026
  Alabi Solomon Ayomide        CPE/2023/1027
  Allison Idris Adeola         CPE/2023/1028
  Amos Timilehin Samson        CPE/2023/1029

## OOP Concepts Demonstrated

| OOP Concept | Location in Code | Which Week |
| --- | --- | --- |
| Classes & Objects | `src/persons.py`, `src/academic.py` | Week 1 |
| @property with validation | `src/persons.py`, `src/academic.py` | Week 2 |
| Custom exception hierarchy | `src/exceptions.py` | Week 2 |
| Abstract Base Class (ABC) | `src/persons.py` | Week 3 |
| Inheritance with super() | `src/graduate.py` | Week 3 |
| Multiple inheritance + MRO | `src/graduate.py`, `src/mixins.py` | Week 3 |
| __eq__, __lt__, __hash__ | `src/academic.py` | Week 4 |
| __add__ / __radd__ | `src/academic.py` | Week 4 |
| Duck typing (no isinstance) | `main.py` | Week 4 |
| @total_ordering | `src/academic.py` | Week 4 |
| UML class diagram | `uml/class_diagram.puml` | Week 5 |
| Composition vs aggregation | `src/department.py` | Week 5 |

## System Architecture

![UML Diagram](uml/class_diagram.png)

The system uses a layered design where `Person` is an abstract base for `Student` and `Lecturer`. `Department` composes `Course` objects because courses are owned by the department, while it aggregates `Student` and `Lecturer` objects because those entities can exist independently. `GraduateStudent` uses multiple inheritance and cooperative `super()` to combine student behavior with research responsibilities. `EnrolmentRecord` validates prerequisites on creation and semesters compute WGPA while enforcing credit limits.

## How to Run

```bash
git clone <repo_url>
cd university_cgpa_system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
pytest tests/ -v
```

## Sample Output

```text
============================================================
SECTION: CREATE COURSES
============================================================
CPE101 — Introduction to Computing (3 units)
MTH101 — Calculus I (4 units)
PHY101 — Physics I (3 units)
GST101 — Use of English (2 units)
CPE102 — Programming Fundamentals (3 units)
CPE201 — Data Structures (4 units)
============================================================
SECTION: CREATE DEPARTMENT
============================================================
Department CPE: Computer Engineering | Courses: 6
```

## Known Limitations

- The system uses in-memory objects and does not persist data to a database.
- Course prerequisites are validated only against completed semester records, not transfer credits.
- No graphical user interface is included; the application runs in the terminal.
- Student registration flow is simplified for demonstration purposes.

## References

- Python official documentation: https://docs.python.org/3/
- pytest documentation: https://docs.pytest.org/
- PlantUML documentation: https://plantuml.com/
