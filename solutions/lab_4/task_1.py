values = [10, 20, 30]
iterator = iter(values)

print(iterator is values)
print(iter(iterator) is iterator)
print(next(iterator))
print(next(iterator))
print(next(iterator))
# print(next(iterator))

def consume(iterable) -> list:
    result = []
    i = iter(iterable)
    while True:
        try:
            item = next(i)
            result.append(item)
        except StopIteration:
            break
    return result


print("--Проверка функции--")
print("Список:", consume([1, 2, 3]))
print("Кортеж:", consume((1, 2, 3)))
print("Строка:", consume("Hello"))
print("Объект range:", consume(range(5)))
llist = [100, 200, 300, 400]
part = iter(llist)
next(part)
next(part)
print("Частично использованный итератор (после 2 вызовов next):", consume(part))

print("\n--Сравнение повторного обхода--")
p_list = ['A', 'B', 'C']
print("Список - обход 1:", consume(p_list))
print("Список - обход 2:", consume(p_list))

p_iterator = iter(p_list)
print("Итератор - обход 1:", consume(p_iterator))
print("Итератор - обход 2:", consume(p_iterator))
