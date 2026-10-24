submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]
students = set([s for s, l, o in submissions])
labs = set([l for s, l, o in submissions])
tries = {}
for s, l, o in submissions:
    if s not in tries:
        tries[s] = []
    tries[s].append([l, o])

best_res = {}
for s, l, o in submissions:
    key = (s, l)
    if key not in best_res:
        best_res[key] = o
    elif o > best_res[key]:
        best_res[key] = o

tries_lab = {}
for s, l, o in submissions:
    key = (s, l)
    if key not in tries_lab:
        tries_lab[key] = 1
    else: tries_lab[key] += 1

print('Вывод структур:')
print(students, labs, tries, best_res, tries_lab, sep='\n')
both_labs = {s for s, l, o in submissions if l == 'lab_01'} & {s for s, l, o in submissions if l == 'lab_02'}
print(f'Студенты, которые сдали обе работы: {both_labs}')
print()
# Добавление новой записи и обновление структур
new = ('liza', "lab_02", 5)
new_s, new_l, new_o = new
submissions.append(new)
students.add(new_s)
labs.add(new_l)
tries[new_s] = [new_l, new_o]
key = (new_s, new_l)
best_res[key] = new_o
tries_lab[key] = 1
print('Новый вывод структур:')
print(students, labs, tries, best_res, tries_lab, sep='\n')
print()

print('---Практическое расширение---')
zapros = ['student anna', 'best anna lab_01', 'attempts boris lab_02', 'completed lab_01', 'student ivan']
def process(query_str):
    p = query_str.split()
    command = p[0]
    if command == "student":
        student = p[1]
        if student not in tries:
            return f"Студент '{student}' не найден."
        return f"Попытки {student}: {tries[student]}"

    elif command == "best":
        student, lab = p[1], p[2]
        key = (student, lab)
        if key not in best_res:
            return f"Запись не найдена для студента '{student}' и работы '{lab}'."
        return f"Лучший результат {student} по {lab}: {best_res[key]}"

    elif command == "attempts":
        student, lab = p[1], p[2]
        key = (student, lab)
        if key not in tries_lab:
            return f"Попыток не найдено для студента '{student}' и работы '{lab}'."
        return f"Количество попыток {student} по {lab}: {tries_lab[key]}"

    elif command == "completed":
        lab = p[1]
        c_s = {s for s, l in best_res.keys() if l == lab}
        if not c_s:
            return f"Никто не сдавал работу '{lab}' или такой работы не существует."
        return f"Работу {lab} сдавали: {c_s}"

    else:
        return f"Неизвестная команда '{command}'."

print('Результаты выполнения запросов')
for q in zapros:
    print(q)
    print(process(q))
    print("-")
