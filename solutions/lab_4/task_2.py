class StepRangeIterator:
    def __init__(self, start: int, stop: int, step: int) -> None:
        self.current = start
        self.stop = stop
        self.step = step
    def __iter__(self) -> "StepRangeIterator":
        return self
    def __next__(self) -> int:
        if self.step > 0 and self.current >= self.stop:
            raise StopIteration
        if self.step < 0 and self.current <= self.stop:
            raise StopIteration
        result = self.current
        self.current += self.step
        return result

class StepRange:
    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("Шаг диапазона не может быть равен нулю.")
        self.start = start
        self.stop = stop
        self.step = step
    def __iter__(self) -> StepRangeIterator:
        return StepRangeIterator(self.start, self.stop, self.step)
    def __len__(self) -> int:
        if self.step > 0 and self.start >= self.stop:
            return 0
        if self.step < 0 and self.start <= self.stop:
            return 0
        return (self.stop - self.start - 1) // self.step + 1

    def __contains__(self, value: int) -> bool:
        if self.step > 0 and (value < self.start or value >= self.stop):
            return False
        if self.step < 0 and (value > self.start or value <= self.stop):
            return False
        return (value - self.start) % self.step == 0

    def __repr__(self) -> str:
        return f"StepRange({self.start}, {self.stop}, {self.step})"
if __name__ == "__main__":
    print(list(StepRange(0, 5, 1)))
    print(list(StepRange(5, 0, -1)))
    print(list(StepRange(0, 0, 1)))
    print(list(StepRange(0, 5, -1)))

    print("\n--Работа двух независимых итераторов--")
    r = StepRange(0, 10, 2)
    it1 = iter(r)
    it2 = iter(r)

    print(f"Вызов next(it1): {next(it1)}")
    print(f"Вызов next(it1): {next(it1)}")
    print(f"Вызов next(it2): {next(it2)}")
    print(f"Вызов next(it1): {next(it1)}")

    print("\n--Практическое расширение--")
    big_range = StepRange(0, 30_000_000, 3)
    print("__repr__():", big_range)
    print("__len__(): ", len(big_range))
    print("Проверка числа 29999997 через in:", 29_999_997 in big_range)
    print("Проверка числа 1000 через in:", 1000 in big_range)
