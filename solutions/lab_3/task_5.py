def mean(values):
    if not values: return 0.0
    return sum(values) / len(values)

def minimum(values):
    if not values: return 0
    m = values[0]
    for t in values:
        if t < m: m = t
    return m

def maximum(values):
    if not values: return 0
    m = -values[0]
    for y in values:
        if y > m: m = y
    return m

def classify(score):
    if score >= 91: return 'Отлично'
    elif score >= 75: return 'Хорошо'
    elif score >= 60: return 'Удовлетворительно'
    else: return 'Неудовлетворительно'

def student_summary(name, results):
    if not results:
        return {
            "name": name,
            "min": 0,
            "max": 0,
            "avg": 0.0,
            "category": "Нет оценок"
        }
    sr = mean(results)
    return {
        "name": name,
        "min": minimum(results),
        "max": maximum(results),
        "avg": sr,
        "category": classify(sr)
    }

def group_summary(students):
    s = [student_summary(name, res) for name, res in students.items()]
    if not s:
        return {"group_avg": 0.0, "categories_count": {}}
    total = sum(sm["avg"] for sm in s) / len(s)
    cat_count = {}
    for st in s:
        cat = st["category"]
        cat_count[cat] = cat_count.get(cat, 0) + 1
    return {
        "group_avg": round(total, 2),
        "categories_count": cat_count
    }


def find_top_students(students):
    if not students:
        return None
    ss = [student_summary(name, res) for name, res in students.items()]
    max_avg = max(s["avg"] for s in ss)
    top_students = [s["name"] for s in ss if s["avg"] == max_avg]
    return top_students


def format_report(student_data, group_data):
    report = []
    report.append('Итоговый отчет')
    report.append('-' * 50)
    report.append(f"Общий средний результат группы: {group_data['group_avg']}")

    top = find_top_students(student_data)
    report.append(f'Лидер(ы) группы: {', '.join(top)}')

    report.append('\nРаспределение по категориям:')
    for cat, count in group_data['categories_count'].items():
        report.append(f'  - {cat}: {count} чел.')
    report.append('-' * 50)
    return '\n'.join(report)

students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}
gr = group_summary(students)
print(format_report(students, gr))

# Тест с обычным набором данных
print("\nТест №1")
test_group = {
    "Анна":[80, 90],  # ср: 85.0
    "Борис": [60, 70]  # ср: 65.0
}
stats = group_summary(test_group)
tops = find_top_students(test_group)
print(stats, tops)

assert tops == ["Анна"]
assert stats["group_avg"] == 75.0


# Тест 2 с одним студентом
print("\nТест №2")
test_s = {"Дарья": [92, 96, 94]}  # ср: 94.0
stats = group_summary(test_s)
tops = find_top_students(test_s)

assert tops == ["Дарья"]
assert stats["group_avg"] == 94.0
print(stats, tops)


# Тест 3 с несколькими лидерами
print('\nТест №3')
leaders = {
    "Алексей": [80, 90],  # Ср: 85.0
    "Мария":[85, 85],    # Ср: 85.0
    "Олег": [60, 60]      # Ср: 60.0
}
tops = find_top_students(leaders)

assert "Алексей" in tops
assert "Мария" in tops
assert len(tops) == 2
print(tops, group_summary(leaders))


# Тест №4 с пустой группой
print('\nТест №4')
test_empty = {}
stats = group_summary(test_empty)
tops = find_top_students(test_empty)

assert tops is None
assert stats["group_avg"] == 0.0
print(stats, tops)


# Тест №5 со студентом без результатов (пустой список)
print('\nТест №5')
test = {"Игорь": []}
summary = student_summary("Игорь", test["Игорь"])

assert summary["avg"] == 0.0
assert summary["category"] == "Нет оценок"
print(test, summary)


# Тест №6 с граничными значениями категорий
assert classify(91.0) == "Отлично"
assert classify(89.9) == "Хорошо"
assert classify(75.0) == "Хорошо"
assert classify(74.9) == "Удовлетворительно"
assert classify(60.0) == "Удовлетворительно"
assert classify(59.9) == "Неудовлетворительно"

print("\nВсе тесты пройдены")
