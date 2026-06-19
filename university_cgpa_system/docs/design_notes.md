# Design Notes

- `Person` is abstract because a generic person should not be instantiated directly; only specialized roles like `Student` and `Lecturer` are meaningful in the system.
- `Department` composes `Course` objects because in this application courses are owned by the department and managed within that academic unit.
- `Department` aggregates `Student` objects because students exist independently and may transfer between departments or belong to multiple academic contexts over time.
- `GraduateStudent` uses cooperative MRO with `super()` so both `Student` initialization and `ResearchWorkerMixin` initialization occur correctly without manual parent `__init__` calls.
- `Student.__gpa` is a private attribute because CGPA is derived from enrolment records and must never be set directly by external code.
- `EnrolmentRecord` validates prerequisites at creation time to ensure academic eligibility is enforced before a course registration is accepted.
