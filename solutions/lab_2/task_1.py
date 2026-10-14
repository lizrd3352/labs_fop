a = 10
b = a

print(a, b)
print(id(a), id(b))

a += 1

print(a, b)
print(id(a), id(b))
print()

print('Эксперимент B')
first = [10, 20]
second = first

print(first, second)
print(id(first), id(second))

second.append(30)

print(first, second)
print(id(first), id(second))

second = first.copy()
print('second == first: ', second == first)
print('second is first: ', second is first)

second.append(40)
print(first, second)
print()

print('Практическая задача')
project1 = {
    'Name': 'Основы программирования',
    'Students': ['Лиза', 'Вика'],
    'Starts': {
        'Duration (sec)': 10,
        'Amount': 2
    }
}

print('Учебный проект №1:', project1, sep='\n')
print()

project2 = project1
print('Учебный проект №2:', project2, sep='\n')
print()

project2['Name'] = 'Введение в Linux'
print('Нежелательное совместное изменение:')
print(project1['Name'], project2['Name'], sep='\n')
print()
# возвращаем обратно значение
project1['Name'] = 'Основы программирования'

import copy
project2 = copy.deepcopy(project1)
project2['Name'] = 'Алгоритмы и структуры данных'
project2['Students'] = ['Сережа', 'Рита', 'Лиза', 'Аня']

assert project1['Name'] == 'Основы программирования'
assert project1['Students'] == ['Лиза', 'Вика']

assert project2['Name'] == 'Алгоритмы и структуры данных'
assert project2['Students'] == ['Сережа', 'Рита', 'Лиза', 'Аня']

print('Учебный проект №1:', project1, sep='\n')
print()

print('Учебный проект №2:', project2, sep='\n')
print()

ob = []
for key1, value1 in project1.items():
    for key2, value2 in project2.items():
        if key1 is key2: ob.append(key1)
        if value1 is value2: ob.append(value1)

for key1, value1 in project1['Starts'].items():
    for key2, value2 in project2['Starts'].items():
        if value1 is value2: ob.append(value1)

for i in range(len(project1['Students'])):
    for j in range(len(project2['Students'])):
        if project1['Students'][i] is project2['Students'][j]:
            ob.append(project1['Students'][i])

print('Общие объекты:')
print(*ob, sep=', ')
print('Остальные объекты являются независимыми')
