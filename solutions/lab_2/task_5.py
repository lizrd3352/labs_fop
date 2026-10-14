import sys
print('Часть 1')
a = []
b = [2, 10, 9, 52, 22, 67, 3, 0, 5, 48]
c = (2, 10, 9, 52, 22, 67, 3, 0, 5, 48)
d = 'helloworld'
e = 100
f = None
print(sys.getsizeof(a))
print(sys.getsizeof(b))
print(sys.getsizeof(c))
print(sys.getsizeof(d))
print(sys.getsizeof(e))
print(sys.getsizeof(f))
print()
print('Часть 2')
p = []
st = sys.getsizeof(p)
for t in range(0, 201, 2):
    p.append(t)
    now = sys.getsizeof(p)
    if now != st:
        print(f'Длина --> {len(p)}, размер --> {now}')
        st = now
print()
print('Часть 3')
import tracemalloc
tracemalloc.start()
numbers_l = list(range(100_000))
c_l, p_l = tracemalloc.get_traced_memory()
tracemalloc.stop()

tracemalloc.start()
numbers_r = range(100_000)
c_r, p_r = tracemalloc.get_traced_memory()
tracemalloc.stop()

print('numbers_l:')
print(f'Текущая память: {c_l / 1024:.2f} КБ')
print(f'Пиковая память:  {p_l / 1024:.2f} КБ')

print('numbers_r:')
print(f'Текущая память: {c_r / 1024:.2f} КБ')
print(f'Пиковая память:  {p_r / 1024:.2f} КБ')
