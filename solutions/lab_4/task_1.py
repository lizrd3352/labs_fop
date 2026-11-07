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


if __name__ == "__main__":
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

def my_enumerate(iterable, start=0):
    result = []
    counter = start
    it = iter(iterable)
    while True:
        try:
            item = next(it)
            result.append((counter, item))
            counter += 1
        except StopIteration:
            break
    return result


def my_zip(first, second):
    result = []
    it1 = iter(first)
    it2 = iter(second)
    while True:
        try:
            item1 = next(it1)
            try:
                item2 = next(it2)
            except StopIteration:
                break
            result.append((item1, item2))
        except StopIteration:
            break
    return result


class StepRangeIterator:
    def __init__(self, start, stop, step):
        self.current = start
        self.stop = stop
        self.step = step
    def __iter__(self):
        return self
    def __next__(self):
        if self.step > 0 and self.current >= self.stop:
            raise StopIteration
        if self.step < 0 and self.current <= self.stop:
            raise StopIteration
        result = self.current
        self.current += self.step
        return result

class StepRange:
    def __init__(self, start, stop, step):
        if step == 0:
            raise ValueError("Шаг диапазона не может быть равен нулю.")
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> StepRangeIterator:
        return StepRangeIterator(self.start, self.stop, self.step)



if __name__ == "__main__":
    test_list = [10, 20, 30]
    test_str = "ABC"
    test_step_range = StepRange(1, 10, 3)

    print("--my_enumerate--")
    print("список:", my_enumerate(test_list, start=1))
    print("StepRange:", my_enumerate(test_step_range))

    print("\n--my_zip--")
    print("строка и список (одинаковая длина):", my_zip(test_str, test_list))
    print("StepRange и строка (StepRange длиннее строки):", my_zip(test_step_range, "Hi"))
