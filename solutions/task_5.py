name = input('Введите ваше имя: ')
exp = input('Введите название эксперимента: ')
zap = int(input('Введите количество запусков: '))
vr = float(input('Введите время одного запуска: '))
cc = input('Введите части комплексного числа: ').split()
has_runs = bool(zap)

overall_time_sec = vr * zap
overall_time_min = vr * zap / 60
coefficient = complex(float(cc[0]), float(cc[1]))
kv_module = (float(cc[0]) ** 2) + (float(cc[1]) ** 2)

print('========================================', f'ЭКСПЕРИМЕНТ: {exp}', f'Исследователь: {name}',
      f'Запуски: {zap}', f'Общее время: {overall_time_sec:.2f} c ({overall_time_min:.2f} мин)',
      f'Коэффицент: {coefficient}', f'Квадрат модуля: {kv_module:.2f}',
      f'Есть выполненные запуски: {has_runs}', '========================================', sep='\n')

print('Диагностика!', f'Исследователь: {name} ==> {type(name)}', f'Эксперимент: {exp} ==> {type(exp)}',
      f'Запуски: {zap} ==> {type(zap)}', f'Коэффицент: {coefficient} ==> {type(coefficient)}',
      f'Выполненные запуски: {has_runs} ==> {type(has_runs)}', f'Квадрат модуля: {kv_module} ==> {type(kv_module)}',
      '========================================', sep='\n')
