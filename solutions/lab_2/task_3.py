import sys

data = [1, 2, 3]
print("После создания:", sys.getrefcount(data))

alias = data
print("После создания alias:", sys.getrefcount(data))

container = [data]
print("После помещения в контейнер:", sys.getrefcount(data))

del alias
print("После del alias:", sys.getrefcount(data))

container.clear()
print("После очистки контейнера:", sys.getrefcount(data))

import weakref


class Record:
    pass


record = Record()
weak_record = weakref.ref(record)

print(weak_record())
del record
print(weak_record())
print()

print("Практическая задача")
links = weakref.WeakValueDictionary()
a = Record()
b = Record()
c = Record()
links["a"] = a
links["b"] = b
links["c"] = c
del c
print(list(links))
del b
print(list(links))
