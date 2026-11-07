def read_measurements(lines) -> object:
    for line in lines:
        cleaned = line.strip()
        if cleaned != "":
            yield float(cleaned)


def filter_range(values, minimum: float, maximum: float) -> object:
    for value in values:
        if minimum <= value <= maximum:
            yield value


def moving_average(values, window_size: int) -> object:
    if window_size < 1:
        raise ValueError("Размер окна должен быть не меньше 1.")
    window = []
    window_sum = 0.0
    for value in values:
        window.append(value)
        window_sum += value
        if len(window) > window_size:
            removed = window.pop(0)
            window_sum -= removed
        if len(window) == window_size:
            yield window_sum / window_size


if __name__ == "__main__":
    raw_lines = ["10.0", "", "12.5", "100.0", "11.5", "13.0", "9.5"]
    print("--Тестирование работы конвейера--")
    def make_pipeline():
        numbers = read_measurements(raw_lines)
        filtered = filter_range(numbers, 9.0, 15.0)
        pipeline = moving_average(filtered, 3)
        return pipeline
    pipeline_1 = make_pipeline()
    print("Первое значение конвейера:", next(pipeline_1))
    print("Второе значение конвейера:", next(pipeline_1))
    remaining = []
    while True:
        try:
            remaining.append(next(pipeline_1))
        except StopIteration:
            break
    print("Оставшиеся значения в списке:", remaining)
    print("\nПовторный проход по исчерпанному генератору:")
    repeated_list = []
    for item in pipeline_1:
        repeated_list.append(item)
    print("Результат повторного обхода:", repeated_list)

    print("\nНовый конвейер:")
    pipeline_2 = make_pipeline()
    full_list = []
    for item in pipeline_2:
        full_list.append(item)
    print("Результат нового конвейера целиком:", full_list)

    print("\n--Тестирование дополнительных выражений--")
    squares_of_evens = [x ** 2 for x in range(1, 21) if x % 2 == 0]
    print("Список квадратов четных чисел:", squares_of_evens)
    sample_strings = ["apple", "", "banana", "kiwi", "apple", "  "]
    lengths_set = {len(s.strip()) for s in sample_strings if s.strip() != ""}
    print("Множество длин непустых строк:", lengths_set)
    num_squares_dict = {x: x ** 2 for x in range(1, 11)}
    print("Словарь число -> квадрат:", num_squares_dict)
    large_squares_gen = (x ** 2 for x in range(1, 1_000_001))
    total_sum = 0
    for square in large_squares_gen:
        total_sum += square
    print("Сумма квадратов диапазона 1-1,000,000:", total_sum)

import tracemalloc

def take(n: int, iterable) -> object:
    iterator = iter(iterable)
    for _ in range(n):
        try:
            yield next(iterator)
        except StopIteration:
            break

def drop(n: int, iterable) -> object:
    iterator = iter(iterable)
    for _ in range(n):
        try:
            next(iterator)
        except StopIteration:
            break
    for item in iterator:
        yield item

def batch(iterable, size: int) -> object:
    if size < 1:
        raise ValueError("Размер пакета должен быть не меньше 1.")
    iterator = iter(iterable)
    while True:
        current_batch = []
        for _ in range(size):
            try:
                current_batch.append(next(iterator))
            except StopIteration:
                break
        if not current_batch:
            break
        yield current_batch

if __name__ == "__main__":
    raw_lines = ["10.0", "", "12.5", "100.0", "11.5", "13.0", "9.5"]
    numbers = read_measurements(raw_lines)
    filtered = filter_range(numbers, 9.0, 15.0)
    ma = moving_average(filtered, 3)
    pipeline = batch(drop(1, ma), size=2)
    packets = list(take(2, pipeline))
    print("\nСформированные пакеты значений:", packets)
    print("\n--tracemalloc--")
    large_input = ["12.5"] * 100000
    tracemalloc.start()

    lazy_numbers = read_measurements(large_input)
    lazy_filtered = filter_range(lazy_numbers, 9.0, 15.0)
    lazy_ma = moving_average(lazy_filtered, 3)
    lazy_batched = batch(lazy_ma, 5)
    lazy_result = list(take(2, lazy_batched))

    _, peak_lazy = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    stage1 = []
    for line in large_input:
        cleaned = line.strip()
        if cleaned != "":
            stage1.append(float(cleaned))
    stage2 = []
    for val in stage1:
        if 9.0 <= val <= 15.0:
            stage2.append(val)
    stage3 = []
    window = []
    window_sum = 0.0
    for val in stage2:
        window.append(val)
        window_sum += val
        if len(window) > 3:
            window_sum -= window.pop(0)
        if len(window) == 3:
            stage3.append(window_sum / 3)
    stage4 = []
    for i in range(0, len(stage3), 5):
        stage4.append(stage3[i:i + 5])

    eager_result = stage4[:2]

    _, peak_eager = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Пиковая память ЛЕНИВОГО конвейера: {peak_lazy} байт")
    print(f"Пиковая память ЖАДНОГО конвейера:  {peak_eager} байт")
