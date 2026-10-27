def arithmetic_mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)

def normalize_name(name: str) -> str:
    if not name:
        return ''
    return ' '.join([p.strip().capitalize() for p in name.split() if p.strip()])


def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    if not student:
        return 'Ошибка'
    r_t = list(map(float, results))
    sr = sum(r_t) / len(r_t)
    return f'{prefix} для {student}: {sr:.{precision}f}'

def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    if not tags:
        return ()
    c = []
    for t in tags:
        if type(t) is not str: continue
        p = t.strip()
        if not p: continue
        if lowercase: p = p.lower()
        if p not in c: c.append(p)
    return tuple(c)

#Проверки для arithmetic_mean
assert arithmetic_mean([1.0, 2.0, 3.0]) == 2.0
assert arithmetic_mean([]) == 0.0
assert arithmetic_mean([5.5]) == 5.5

#Проверки для normalize_name
assert normalize_name("  иван   иванов  ") == "Иван Иванов"
assert normalize_name("") == ""
assert normalize_name("ANNA-MARIA") == "Anna-maria"

#Проверки для build_report
assert build_report("Анна", [4, 5, 5], precision=1) == "Результат для Анна: 4.7"
assert build_report("", [5, 5]) == "Ошибка"
assert build_report("Борис", [4, 4], precision=3, prefix="Отчет") == "Отчет для Борис: 4.000"

#Проверки для collect_tags
assert collect_tags("python", "  Python ", "git", "") == ("python", "git")
assert collect_tags("Lab1", "lab1", lowercase=False) == ("Lab1", "lab1")
assert collect_tags() == ()

print("Все проверки assert пройдены.")
print("\n- Стандартные вызовы -")

v_1 = build_report("Дарья", [5, 4, 5, 5], precision=4, prefix="Итог")
print(v_1)
v_2 = collect_tags("  Базы Данных", "базы данных", "SQL ", lowercase=True)
print("Собранные теги:", v_2)

print("\n- Распаковка аргументов * и ** -")
grades = [5, 5, 4, 3, 5]
settings = {
    "precision": 1,
    "prefix": "Промежуточная оценка"
}
tags_list = ["  Курсовая ", "КУРСОВАЯ", " диплом", "  "]
unpacked_tags = collect_tags(*tags_list, lowercase=True)
print("Распакованные теги:", unpacked_tags)

v_3 = build_report("Алексей", grades, **settings)
print(v_3)

# LEGB
course = "Основы программирования"
def university_course():
    status = 'Базовый уровень'
    def update_status():
        nonlocal status
        status = 'Продвинутый уровень'
        print(f"[Вложенная функция] Читаем глобальное имя: '{course}'")
        print(f"[Вложенная функция] Изменили внешнее имя: '{status}'")
    print(f"\n[Внешняя функция] Статус до вызова вложенной: '{status}'")
    update_status()
    print(f"[Внешняя функция] Статус после вызова вложенной: '{status}'")

university_course()
print(f"Глобальное имя course осталось неизменным: '{course}'")


def add_result(value, results=None):
    if results is None:
        results = []
    results.append(value)
    return results


def apply_to_results(operation, values):
    return [operation(val) for val in values]

def make_threshold_checker(threshold):
    def checker(value):
        return value >= threshold
    return checker

print('\n- apply_to_results -')

def double(x):
    return x * 2

s = [3, 4, 5, 2, 5, 4]
d = apply_to_results(double, s)
print(f'Именованная функция (удвоение чисел): {s}')

sl = apply_to_results(lambda x: x + 1, s)
print(f'Lambda-функция (прибавление 1): {sl}')

print("\n- make_threshold_checker -")

excellent = make_threshold_checker(4.6)
passed = make_threshold_checker(2.6)

test_score = 4

print(f"Результат {test_score} является отличным? -> {excellent(test_score)}")
print(f"Результат {test_score} сдал зачет? -> {passed(test_score)}")
