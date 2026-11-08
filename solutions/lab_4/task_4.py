from dataclasses import dataclass

@dataclass(order=False)
class Submission:
    student_id: str
    laboratory_id: str
    attempt: int
    score: float
    comment: str = ""

    def __post_init__(self) -> None:
        if not self.student_id.strip():
            raise ValueError("Идентификатор студента не может быть пустым.")
        if not self.laboratory_id.strip():
            raise ValueError("Идентификатор лабораторной работы не может быть пустым.")
        if self.attempt <= 0:
            raise ValueError("Номер попытки должен быть положительным числом.")
        if not (0.0 <= self.score <= 100.0):
            raise ValueError("Результат должен находиться в диапазоне от 0 до 100.")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Submission):
            return False
        return (self.student_id == other.student_id and
                self.laboratory_id == other.laboratory_id and
                self.attempt == other.attempt and
                self.score == other.score and
                self.comment == other.comment)

    def __lt__(self, other: "Submission") -> bool:
        if self.attempt != other.attempt:
            return self.attempt < other.attempt
        return self.score < other.score


class Student:
    def __init__(self, student_id: str, name: str) -> None:
        self.student_id = student_id
        self.name = name
        self._submissions = []

    def validate_id(self, student_id: str) -> bool:
        return isinstance(student_id, str) and len(student_id.strip()) >= 3

    def from_full_name(self, student_id: str, full_name: str) -> "Student":
        if not self.validate_id(student_id):
            raise ValueError("Некорректный формат идентификатора.")
        return Student(student_id, full_name)

    def add_submission(self, submission: Submission) -> None:
        if submission.student_id != self.student_id:
            raise ValueError("Идентификатор студента в работе не совпадает с текущим.")
        self._submissions.append(submission)

    def submissions(self) -> list:
        return list(self._submissions)

    def sorted_submissions(self) -> list:
        return sorted(self._submissions)

    def average_score(self) -> float:
        if not self._submissions:
            return 0.0
        total = 0.0
        for sub in self._submissions:
            total += sub.score
        return total / len(self._submissions)

    def best_score(self, laboratory_id: str) -> float:
        best = 0.0
        found = False
        for sub in self._submissions:
            if sub.laboratory_id == laboratory_id:
                found = True
                if sub.score > best:
                    best = sub.score
        return best if found else 0.0

    def __len__(self) -> int:
        return len(self._submissions)

    def __iter__(self):
        return iter(self._submissions)

    def __str__(self) -> str:
        return f"Студент {self.name} (ID: {self.student_id}), средний балл: {self.average_score():.1f}"

    def __repr__(self) -> str:
        return f"Student(student_id='{self.student_id}', name='{self.name}')"


class Course:
    def __init__(self) -> None:
        self._students = {}

    def add_student(self, student: Student) -> None:
        if student.student_id in self._students:
            raise ValueError("Студент с таким идентификатором уже зарегистрирован.")
        self._students[student.student_id] = student

    def get_student(self, student_id: str) -> Student:
        if student_id not in self._students:
            raise KeyError("Студент с таким идентификатором не найден.")
        return self._students[student_id]

    def submit(self, submission: Submission) -> None:
        student = self.get_student(submission.student_id)
        student.add_submission(submission)

    def top_students(self, limit: int = 3) -> list:
        all_students = list(self._students.values())
        sorted_students = sorted(all_students, key=lambda s: s.average_score(), reverse=True)
        return sorted_students[:limit]

    def __contains__(self, student_id: str) -> bool:
        return student_id in self._students

    def __len__(self) -> int:
        return len(self._students)

    def __iter__(self):
        return iter(self._students.values())


if __name__ == "__main__":
    print("--Проверка создания посылок и инвариантов--")
    sub1 = Submission(student_id="st_101", laboratory_id="lab_1", attempt=1, score=85.0)
    sub2 = Submission(student_id="st_101", laboratory_id="lab_1", attempt=2, score=95.5)
    sub3 = Submission(student_id="st_101", laboratory_id="lab_2", attempt=1, score=70.0)
    print("Создана посылка:")
    print(" ", sub1)

    print("\n--Проверка альтернативного конструктора (через временный фабричный объект)--")
    factory = Student("st_101", "Иван Иванов")
    student = factory.from_full_name("st_101", "Иван Иванов")
    print("Инициализация через __repr__:", repr(student))

    student.add_submission(sub1)
    student.add_submission(sub2)
    student.add_submission(sub3)
    print(student)
    print(f"Всего попыток сдачи (__len__): {len(student)}")

    print("\n--Проверка защиты приватного списка и сортировки работ--")
    print(f"Длина до попытки внешнего вмешательства: {len(student._submissions)}")
    student.submissions().append("Взлом")
    print(f"Длина после попытки внешнего вмешательства: {len(student._submissions)}")

    unsorted_subs = [
        Submission("st_102", "lab_1", 2, 90.0),
        Submission("st_102", "lab_1", 1, 95.0),
        Submission("st_102", "lab_1", 1, 60.0),
    ]
    student_for_sort = Student("st_102", "Петр Петров")
    for s in unsorted_subs:
        student_for_sort.add_submission(s)

    print("Отсортированный порядок (снаружи):")
    for s in student_for_sort.sorted_submissions():
        print(f"  Попытка: {s.attempt}, Балл: {s.score}")

    print("\n--Тестирование класса Course и рейтинга лучших--")
    course = Course()
    course.add_student(student)
    course.add_student(student_for_sort)

    best_student = Student("st_103", "Анна Сидорова")
    course.add_student(best_student)
    course.submit(Submission("st_103", "lab_1", 1, 100.0))

    print("Рейтинг студентов:")
    for place, st in enumerate(course.top_students(), start=1):
        print(f"  {place} место: {st.name} со средним баллом {st.average_score():.2f}")
    # 1. Функция len() считает количество элементов
    print(len(course))  # Покажет, сколько всего студентов на курсе
    print(len(student))  # Покажет, сколько попыток сдачи сделал этот студент

    # 2. Функция iter() и цикл for позволяют перебирать элементы
    for sub in student:
        print(sub.score)  # Просто бежим по всем оценкам студента без сложных конструкций

    for st in course:
        print(st.name)  # Спокойно перебираем всех студентов на курсе

    # 3. Оператор in мгновенно ищет элемент
    if "st_101" in course:
        print("Этот студент точно учится на курсе!")
