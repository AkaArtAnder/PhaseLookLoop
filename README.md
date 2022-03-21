# Model Phase Look Loop System
Модель сисетмы ФАПЧ(фазовой автоподстройки частоты) позволяющая
строить статистику по
результатам работы системы с различными параметрами.

Общее описание модели и её основные режимы представленны в `/src/resources/files`

## Сборка (Пути относительно корневого каталога)
Python 3.8
1. Настройка корректного виртуального окружения
```
$ python3 -m venv env
$ pip3 install -r requirements.txt
$ source env/bin/activate
```
2. Компиляция динамической библиотеки генератора нормального
распределения
```
(env)$ cd src/resources/generator
(env)$ python setup.py build_ext -i
(env)$ mv -f genormal.cpython* ../../libs
```
3. Запуск (из корня)
```
(env)$ python main.py
```