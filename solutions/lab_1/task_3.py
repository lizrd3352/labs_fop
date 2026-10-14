x = 17
y = 5

print('Эксперимент А')
print()
print(x + y, type(x + y))
print(x - y, type(x - y))
print(x * y, type(x * y))
print(x / y, type(x / y))
print(x // y, type(x // y))
print(x % y, type(x % y))
print(x ** y, type(x ** y))

print()

print('Эксперимент В')
print()
print(2 ** 1000)

print()

print('Эксперимент С')
print()
import math
result = 0.1 + 0.2
print(result)
print(result == 0.3)
print(result - 0.3)
print(math.isclose(result, 0.3))

print()

print('Эксперимент D')
print()
i = int('42')
f = float('3.14')
s = str(2026)
b0 = bool(0)
b1 = bool(-1)
b = bool('')
bf = bool('False')
c = complex(2, -3)

print(i, type(i))
print(f, type(f))
print(s, type(s))
print(b0, type(b0))
print(b1, type(b1))
print(b, type(b))
print(bf, type(bf))
print(c, type(c))
