# Лабораторная работа № 4. Итераторы, генераторы и объектная модель Python

## Цель работы

Понять механизмы, лежащие в основе цикла `for`, научиться создавать ленивые последовательности и проектировать собственные типы, поддерживающие стандартные протоколы Python.

## Задание 1. Протокол итерации

Функция consume:

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

