student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10
p = 7 / 10

print('Первый символ имени:', student[0])
print('Последний символ имени:', student[3])
print('Срез с именем:', student[0:student.find(' ')])
print('Срез с фамилией:', student[(student.find(' ') + 1)::])
print('Верхний регистр:', student.upper())
print('Нижний регистр:', student.lower())
print(f'Инициалы: {student[0]}.{student[student.find(' ') + 1]}.')
print('Обратный порядок:', course[-1::-1])
print('Оператор %:', '%s — %s: %d/%d (%.1f%%)' % (student, course, completed, total, p * 100))
print('Оператор .format():', '{} — {}: {}/{} ({:.1f}%)'.format(student, course, completed, total, p * 100))
print('f-строка:', f'{student} — {course}: {completed}/{total} ({p * 100}%)')

symbol = 'Я'
print(symbol)
print(ord(symbol))
print(chr(ord(symbol)))
print(symbol.encode('utf-8'))
print(len(symbol.encode('utf-8')))
# symbol[0] = 'a'
