# Лабораторная работа № 4. Итераторы, генераторы и объектная модель Python

## Цель работы

Понять механизмы, лежащие в основе цикла `for`, научиться создавать ленивые последовательности и проектировать собственные типы, поддерживающие стандартные протоколы Python.

## Задание 1. Протокол итерации

Функция `consume`:

```python
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
```

Результаты отличаются потому, что список — это многоразовый итерируемый объект, а итератор — это одноразовый указатель состояния. При передаче списка функция iter() каждый раз создает для него абсолютно новый итератор, который начинает обход с самого первого элемента. Если же передать сам итератор, то при вызове iter() он возвращает самого себя, но его внутренний указатель после первого прохода уже находится в конце данных.

**Практическое расширение**

Функции `my_enumerate` и `my_zip`:

```python
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
```

*Вопросы:*

1. Функция iter() для итерируемого объекта должна возвращать новый объект-итератор
2. После исчерпания данных next() обязан вызывать ошибку StopIteration при каждом последующем вызове
3. Итератор обычно возвращает себя для универсальности и совместимости (разные инструменты в Python могут работать друг с другом по одинаковым правилам, без написания отдельного кода для каждого случая)

## Задание 2. Собственный итератор

Класс `StepRange`:

```python
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
```

Состояние итераторов после каждого шага:
| Шаг/Действие | it1 | it2 |
| ----------- | ----------- |----------- |
| next(it1)   | 2   |0   |
| next(it1)    | 4   |0   |
| next(it2)   | 4   |2   |
| next(it1)   | 6   |2   |

**Практическое расширение:**

```python
    def __len__(self):
        if self.step > 0 and self.start >= self.stop:
            return 0
        if self.step < 0 and self.start <= self.stop:
            return 0
        return (self.stop - self.start - 1) // self.step + 1

    def __contains__(self, value):
        if self.step > 0 and (value < self.start or value >= self.stop):
            return False
        if self.step < 0 and (value > self.start or value <= self.stop):
            return False
        return (value - self.start) % self.step == 0

    def __repr__(self):
        return f"StepRange({self.start}, {self.stop}, {self.step})"
```

При проверке через `__contains__()` (сложность О(1) выполняется всего несколько операций: проверяет границы и делится ли разница на шаг без остатка, а при проверке обходом (сложность О(N)) большого диапазона будет выполнятся несколько тысяч (а то и миллионов) операций.

*Вопросы:*

1. Состояние обхода лучше хранить в отдельном объекте, чтобы разделить неизменяемую структуру данных и процесс её обхода. Создание отдельного объекта-итератора при каждом вызове iter() позволяет запускать несколько независимых проходов по одному диапазону одновременно
2. Сломается возможность повторного обхода диапазона и логика вложенных циклов
3. `StepRange` требует константный объем памяти — \(O(1)\), независимо от общего числа элементов в последовательности поскольку класс  хранит всего три целых числа — start, stop и step

## Задание 3. Генераторы и ленивый конвейер
