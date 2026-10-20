def projects(score, work_type, absences):
    if score < 0 or score > 100:
        return 'Неверные входные данные'
    elif absences < 0 or absences > 5:
        return 'Неверные входные данные'
    if 0 <= score <= 59 or (60 <= score <= 74 and absences > 3):
        r = 'недостаточный'
    elif (75 <= score <= 89 and absences > 3) or 60 <= score <= 74:
        r = 'удовлетворительный'
    elif (90 <= score <= 100 and absences > 3) or 75 <= score <= 89:
        r = 'хороший'
    elif 90 <= score <= 100:
        r = 'отличный'
    match work_type:
        case 'exam':
            t = 'экзаменационная работа'
        case 'project':
            t = 'проектная работа'
        case 'practice':
            t = 'практическая работа'
        case _:
            t = 'неизвестный тип работы'
    return f'Тип: {t}. Уровень: {r}'

test = [
    [0, 'exam', 2],
    [100, 'project', 6],
    [59, 'project', 0],
    [60, 'practice', 4],
    [74, 'exam', 2],
    [75, 'practice', 5],
    [89, 'project', 9],
    [90, 'classwork', 3]
]
for i in range(1, 9):
    s, w, a = test[i-1]
    print(f'Тест №{i}. {projects(s, w, a)}')
print()
print('--Практическое расширение--')
students = [
    (95, 'exam', 0),
    (82, 'project', 4),
    (77, 'practice', 1),
    (65, 'exam', 5),
    (50, 'project', 2),
    (90, 'practice', 5),
    (74, 'exam', 0),
    (88, 'classwork', 2),
    (30, 'practice', 4),
    (100, 'project', 3),
]

stats = {'отличный': 0, 'хороший': 0, 'удовлетворительный': 0, 'недостаточный': 0}

for i in range(1, 11):
    s, w, a = students[i-1]
    result = projects(s, w, a)
    print(f'Студент №{i}: {result}')
    if 'Уровень: отличный' in result:
        stats['отличный'] += 1
    elif 'Уровень: хороший' in result:
        stats['хороший'] += 1
    elif 'Уровень: удовлетворительный' in result:
        stats['удовлетворительный'] += 1
    elif 'Уровень: недостаточный' in result:
        stats['недостаточный'] += 1
print()
print('--Итоговая сводка--')
for level, count in stats.items():
    print(f'Уровень "{level}": {count} чел.')
