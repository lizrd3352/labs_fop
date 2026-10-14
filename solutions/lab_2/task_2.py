import copy

original = [
    ['Python', 5],
    ['Algorithms', 4],
]

alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

def changes(name):
    print(f'{name}')
    print(f'Идентификаторы внешних списков: original = {id(original)}, alias = {id(alias)}, '
          f'shallow = {id(shallow)}, deep = {id(deep)}')
    print(f'Идентификаторы первого вложенного списка: original = {id(original[0])}, alias = {id(alias[0])}, '
          f'shallow = {id(shallow[0])}, deep = {id(deep[0])}')
    print(f'Идентификаторы объекта первой оценки: original = {id(original[0][1])}, alias = {id(alias[0][1])}, '
          f'shallow = {id(shallow[0][1])}, deep = {id(deep[0][1])}')

original.append(['Databases', 5])
changes('Первое изменение')
print()
original[0][1] = 3
changes('Второе изменение')
print()
wrong_matrix = [[0] * 3] * 3
wrong_matrix[0][0] = 1
print(*wrong_matrix, sep='\n')
print()
correct_matrix = [[0] * 3 for _ in range(3)]
print(*correct_matrix, sep='\n')

print('Проверка:')
print('Идентичны ли 1 и 3 строчки в wrong_matrix:', wrong_matrix[0] is wrong_matrix[2])
print('Идентичны ли 1 и 3 строчки в correct_matrix:', correct_matrix[0] is correct_matrix[2])
