import tracemalloc
def measure(name):
    print(f'Сценарий: {name}')
    print(f' Число элементов: 100000')
    tracemalloc.start()
    if name is 'Список':
        obj = list(range(100_000))
    else:
        obj = range(100_000)
    outer_size = sys.getsizeof(obj)
    print(f' Размер внешнего объекта: {outer_size} байт')
    current, peak = tracemalloc.get_traced_memory()
    print(f' Текущая выделенная память: {current} байт')
    print(f' Пиковая выделенная память: {peak} байт')
    tracemalloc.stop()
    return peak

l = measure('Список')
al = measure('Алгоритм')

dif = l / al
print(f'Отношение пикового объема памяти: {dif}')
