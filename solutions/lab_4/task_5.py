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

class CourseEvent:
    def __init__(self, student: Student, timestamp: str) -> None:
        self._student = student
        self.timestamp = timestamp

    def get_student_id(self) -> str:
        return self._student.student_id

    def describe(self) -> str:
        raise NotImplementedError("Метод describe() должен быть реализован в наследниках.")


class SubmissionEvent(CourseEvent):
    def __init__(self, student: Student, timestamp: str, submission: Submission) -> None:
        super().__init__(student, timestamp)
        self.submission = submission

    def describe(self) -> str:
        return (f"[{self.timestamp}] {self._student.name} сдал работу "
                f"{self.submission.laboratory_id} (Попытка {self.submission.attempt}) "
                f"на {self.submission.score} баллов.")


class AttendanceEvent(CourseEvent):
    def __init__(self, student: Student, timestamp: str, lesson_topic: str, present: bool = True) -> None:
        super().__init__(student, timestamp)
        self.lesson_topic = lesson_topic
        self.present = present

    def describe(self) -> str:
        status = "присутствовал" if self.present else "отсутствовал"
        return f"[{self.timestamp}] {self._student.name} {status} на занятии по теме: '{self.lesson_topic}'."


class CommentEvent(CourseEvent):
    def __init__(self, student: Student, timestamp: str, author: str, text: str) -> None:
        super().__init__(student, timestamp)
        self.author = author
        self.text = text

    def describe(self) -> str:
        return f"[{self.timestamp}] {self.author} оставил отзыв для {self._student.name}: '{self.text}'."

class CourseJournal:
    def __init__(self) -> None:
        self._events = []

    def add_event(self, event: CourseEvent) -> None:
        self._events.append(event)
        if isinstance(event, SubmissionEvent):
            event._student.add_submission(event.submission)

    def events_for_student(self, student_id: str) -> object:
        for event in self._events:
            if event.get_student_id() == student_id:
                yield event

    def events_by_type(self, event_type: type) -> object:
        for event in self._events:
            if isinstance(event, event_type):
                yield event

    def summary(self) -> str:
        subs = 0
        attends = 0
        comments = 0
        for event in self._events:
            if isinstance(event, SubmissionEvent):
                subs += 1
            elif isinstance(event, AttendanceEvent):
                attends += 1
            elif isinstance(event, CommentEvent):
                comments += 1
        return f"Всего событий: {len(self._events)} (Сдачи: {subs}, Посещения: {attends}, Комментарии: {comments})"

    def __len__(self) -> int:
        return len(self._events)

    def __iter__(self):
        return iter(self._events)

    def __getitem__(self, item: object) -> object:
        if isinstance(item, slice):
            sliced_journal = CourseJournal()
            sliced_journal._events = self._events[item]
            return sliced_journal
        return self._events[item]

    def __str__(self) -> str:
        return f"Журнал активности курса ({len(self._events)} записей)"

    def __repr__(self) -> str:
        return f"CourseJournal(events_count={len(self._events)})"

def render_timeline(events) -> str:
    lines = []
    for event in events:
        lines.append(event.describe())
    return "\n".join(lines)

class ScoreViewIterator:
    def __init__(self, events_list: list) -> None:
        self._iterator = iter(events_list)

    def __next__(self) -> float:
        while True:
            event = next(self._iterator)
            if isinstance(event, SubmissionEvent):
                return event.submission.score
class ScoreView:
    def __init__(self, journal: CourseJournal) -> None:
        self._journal = journal

    def __iter__(self) -> ScoreViewIterator:
        return ScoreViewIterator(self._journal._events)

if __name__ == "__main__":
    print("=== База данных ===")

    course = Course()
    factory = Student("", "")

    st1 = factory.from_full_name("st_101", "Иван Иванов")
    st2 = factory.from_full_name("st_102", "Петр Петров")
    st3 = factory.from_full_name("st_103", "Анна Сидорова")

    course.add_student(st1)
    course.add_student(st2)
    course.add_student(st3)

    journal = CourseJournal()

    journal.add_event(AttendanceEvent(st1, "09:00", "Введение в итераторы", present=True))
    journal.add_event(AttendanceEvent(st2, "09:02", "Введение в итераторы", present=True))
    journal.add_event(AttendanceEvent(st3, "09:05", "Введение в итераторы", present=False))

    sub1_1 = Submission(student_id="st_101", laboratory_id="lab_1", attempt=1, score=45.0)
    journal.add_event(SubmissionEvent(st1, "10:15", sub1_1))
    journal.add_event(CommentEvent(st1, "10:20", "Профессор", "Слабая оптимизация. Нужно переделать."))

    sub1_2 = Submission(student_id="st_101", laboratory_id="lab_1", attempt=2, score=95.0)
    journal.add_event(SubmissionEvent(st1, "14:00", sub1_2))

    journal.add_event(SubmissionEvent(st2, "11:30", Submission("st_102", "lab_1", 1, 80.0)))
    journal.add_event(CommentEvent(st2, "11:45", "Тьютор", "Зачтено."))

    journal.add_event(SubmissionEvent(st3, "15:10", Submission("st_103", "lab_1", 1, 75.0)))
    journal.add_event(CommentEvent(st3, "15:30", "Профессор", "Хороший отчет."))

    print(journal)
    print(journal.summary())
    print("Проверка связности: средний балл st1 пересчитан автоматически:", st1.average_score())

    print("\n=== 2. Срез журнала (первые 3 записи) ===")
    sliced = journal[0:3]
    print(render_timeline(sliced))

    print("\n=== 3. Выборка событий студента st_101 (Ленивый генератор) ===")
    print(render_timeline(journal.events_for_student("st_101")))

    print("\n=== 4. Выборка событий типа CommentEvent (Ленивый генератор) ===")
    print(render_timeline(journal.events_by_type(CommentEvent)))

    print("\n=== 5. Полная временная шкала курса (Полиморфизм) ===")
    print(render_timeline(journal))

    print("\n=== 6. Расчет статистики по оценкам через протокол ScoreView ===")
    scores_view = ScoreView(journal)

    total_score = 0.0
    count = 0
    for score in scores_view:
        total_score += score
        count += 1
    print(f"Всего извлечено оценок: {count}")
    print(f"Средний балл всех сдач на курсе: {total_score / count:.2f}")

    print("Список всех оценок при повторном обходе:", list(scores_view))

class DeadlineEvent(CourseEvent):
    def __init__(self, student: Student, timestamp: str, lab_id: str, penalty_points: float) -> None:
        super().__init__(student, timestamp)
        self.lab_id = lab_id
        self.penalty_points = penalty_points

    def describe(self) -> str:
        return f"[{self.timestamp}] ВНИМАНИЕ: Наступил дедлайн по {self.lab_id} для {self._student.name}. Штраф: {self.penalty_points} б."


class FilteredJournalViewIterator:
    def __init__(self, events_list: list, predicate) -> None:
        self._iterator = iter(events_list)
        self._predicate = predicate

    def __next__(self) -> CourseEvent:
        while True:
            event = next(self._iterator)
            if self._predicate(event):
                return event

class FilteredJournalView:
    def __init__(self, journal: CourseJournal, predicate) -> None:
        self._journal = journal
        self._predicate = predicate

    def __iter__(self) -> FilteredJournalViewIterator:
        return FilteredJournalViewIterator(self._journal._events, self._predicate)


def is_submission(event: CourseEvent) -> bool:
    return isinstance(event, SubmissionEvent)

if __name__ == "__main__":
    st1 = Student("st_101", "Иван Иванов")
    st2 = Student("st_102", "Петр Петров")

    journal = CourseJournal()

    sub_ok = Submission(student_id="st_101", laboratory_id="lab_1", attempt=1, score=85.0)
    journal.add_event(SubmissionEvent(st1, "10:15", sub_ok))

    journal.add_event(DeadlineEvent(st1, "12:00", "Лабораторная 2", penalty_points=5.0))
    journal.add_event(DeadlineEvent(st2, "12:00", "Лабораторная 2", penalty_points=10.0))

    print("=== 1. Проверка полиморфизма с новым типом DeadlineEvent ===")
    print(render_timeline(journal))

    print("\n=== 2. Ленивая фильтрация через именованную функцию (Только сдачи) ===")
    submissions_view = FilteredJournalView(journal, is_submission)
    print(render_timeline(submissions_view))

    print("\n=== 3. Ленивая фильтрация через lambda (Только дедлайны студента st_101) ===")
    lambda_view = FilteredJournalView(
        journal,
        lambda ev: isinstance(ev, DeadlineEvent) and ev.get_student_id() == "st_101"
    )
    print(render_timeline(lambda_view))

    print("\n=== 4. Проверка поддержки протокола повторного обхода ===")
    print("Первый обход lambda-представления:")
    print(render_timeline(lambda_view))
    print("Повторный обход lambda-представления:")
    print(render_timeline(lambda_view))
