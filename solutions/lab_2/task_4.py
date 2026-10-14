import gc

first = []
second = []

first.append(second)
second.append(first)

print("first ссылается на second:", first[0] is second)
print("second ссылается на first:", second[0] is first)
print("Автоматический сборщик включён:", gc.isenabled())
print("Пороги поколений:", gc.get_threshold())
print("Статистика поколений:", gc.get_stats())

id_f, id_s = id(first), id(second)
print(f"Идентификаторы: first = {id_f}, second = {id_s}")
del first
del second
clt = gc.collect()
print(clt)

gc.disable()
def cr(n):
    a = []
    for i in range(n):
        b = []
        c = []
        b.append(c)
        c.append(b)
        a.append(b)
        a.append(c)
    return a

ll = cr(4)
del ll
clt2 = gc.collect()
print(clt2)
gc.enable()

print('Практическая задача')
before = gc.collect()
print("Собрано объектов до создания графа:", before)
u1 = {"name": "u1", "links": []}
u2 = {"name": "u2", "links": []}
u3 = {"name": "u3", "links": []}
u4 = {"name": "u4", "links": []}
u1["links"].append(u2)
u2["links"].append(u3)
u3["links"].append(u1)

print("Связи графа:")
print(f'{u1["name"]} -> {u1["links"]}')
print(f'{u2["name"]} -> {u2["links"]}')
print(f'{u3["name"]} -> {u3["links"]}')
print(f'{u4["name"]} -> {u4["links"]}')
del u1, u2, u3
after = gc.collect()
print("Собрано объектов после удаления цикла:", after)
print("Разница:", after - before)
print("Независимый узел доступен:", u4["name"])
