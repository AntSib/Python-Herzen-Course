# Лабораторная работа №2. Методы оптимизации вычисления кода с помощью потоков, процессов, Cython, отпускания GIL.

На основе [ноутбука](https://colab.research.google.com/drive/12ImNzq9aWlnS7pAuIm6jIsjq5a1ls-ud#scrollTo=Z7mFLeBTknM-) Google Colab, выполнить:

Итерация 1:
* Документацию функции;
* Написать полный и содержательный docstring;
* Использовать аннотации типов для аргументов и возвращаемых значений;
* Создать два примера для проверки правильности работы функции, размещённые непосредственно в docstring функции;
* Разработать дополнительные юнит-тесты, покрывающие хотя бы две ситуации: правильный расчёт известного интеграла и проверку устойчивости к изменению числа итераций;
* Провести оценку производительности функции с помощью модуля timeit.

Итерация 2:
* Оптимизировать функцию с помощью потоков;
* Оптимизировать функцию с помощью процессов.

---

В качестве функции для работы была выбрана функция вычисления интегралов методом трапеций.

Коды функций находятся в файле [multi_integration.py](./multi_integration.py).
В файле [test_integrate.py](./test_integrate.py) находятся pytest-тесты для данной функции.

Всё запуски происходили в Python 3.13.
В результаты замеров времени выполнений функций при разбиении интервала интегрирования на 1000 частей, каждая функция по 1000 замеров, для 4 потоков/процессов:
* integrate:                        executed in 374.1435    ms.
* multiprocessing_integrate:        executed in 170877.4022 ms.
* multiprocessing_spawn_integrate:  executed in 165889.3111 ms.
* multithreading_integrate:         executed in 1097.7007   ms.
* multithreading_spawn_integrate:   executed in 1137.7631   ms.

Как видно из результатов, использование потоков и процессов увеличивает время выполнение функций, особенно для потоков.
Замедление, в первую очередь, связано с накладными расходами для создания потоков или процессов. При многопроцессорном выполнении, накладные расходы частично компенсируются параллельностью выполнения задач, в то время как потоки выполняются последовательно из-за синхронизации, вызванной GIL (global interpreter lock).

---

Итерация 3:
* оптимизировать функцию integrate с помощью Cython;
* замерить время вычисления функции без потоков и процессов (сравнить с итерацией 1);
* замерить время вычисления с потоками и процессами (сравнить с итерациями 2 и 3 соответственно);
* использовать annotate = True получить html-файл для модуля integrate и максимально;
* оптимировать код для уменьшения взаимодействия с C-API.

---

Функция integrate() была скомпилирована для __Cython__ при помощи uv.
Для этого была создана директория cython_integrator

Результат профилирования Cython:
Не оптимизированная версия:
[file](./cy_compilation/unoptimized_integrate.html)
<iframe src="./cy_compilation/unoptimized_integrate.html" width="100%" height="500px"></iframe>
Оптимизированная версия:
[file](./cy_compilation/optimized_integrate.html)
<iframe src="./cy_compilation/optimized_integrate.html" width="100%" height="500px"></iframe>


Замеры времени выполнения функций:
* integrate:                        executed in 173.18190 ms;
* multiprocessing_integrate:        executed in 89117.61460 millis.
* multiprocessing_spawn_integrate:  executed in 129538.21670 millis.
* multithreading_integrate:         executed in 894.33080 millis.
* multithreading_spawn_integrate:   executed in 811.61030 millis.

* integrate:                        executed in 374.1435    ms.
* multiprocessing_integrate:        executed in 170877.4022 ms.
* multiprocessing_spawn_integrate:  executed in 165889.3111 ms.
* multithreading_integrate:         executed in 1097.7007   ms.
* multithreading_spawn_integrate:   executed in 1137.7631   ms.

Как видно из результатов замеров, время выполнения функции integrate с использованием Cython уменьшилось с более 2 раза. Для многопоточных функций прирост производительности есть не такой большой, что ожидаемо, так как многопоточность реализована на Python.

---

Итерация 4:

* переписать код функции integrate с использование noGIL.
* сделать замеры позволяющие оценить время выполнения кода с 2, 4, 6 потоками и сравнить
* время вычисления с помощью потоков integrate  без GIL (noGIL ) и сайтонизированной с
* временем вычисления с помощью процессов сайтонизированной версии
* оценить возможность применения примитивов синхронизации (семафор, мьютекс), дать объяснение имеет ли это смысл или нет и почему?
* python 3.14 исследовать изменяются ли значения времени вычисления , произведенные в итерации 2 (если мы используем 3.14, нужно ли нам отпускать GIL)

---

В Python 3.12+ GIL можно отключить при помощи аргумента в командной строке при запуске программы:
```bash
python -X gil=0 <file>
```
В Python 3.14 GIL также можно отключить (не отключён нативно) и начиная с этой версии работа без GIL более оптимизирована.

Замеры времени выполнения функций без GIL (для 4 потоков):
* integrate:                        executed in 233.73460 ms;
* multiprocessing_integrate:        executed in 86880.86620 ms;
* multiprocessing_spawn_integrate:  executed in 93878.07970 ms;
* multithreading_integrate:         executed in 561.28420 ms;
* multithreading_spawn_integrate:   executed in 625.67320 ms.

При сравнении времени исполнения с обычным временем выполнения noGIL выполняется быстрее примерно в ~1.6-2 раза. При этом наибольший прирост имеют процессы.



Замеры времени выполнения функций с разным количеством потоков/процессов:
* multiprocessing_integrate         executed in 60183.65070 ms with 1 work flows;
* multiprocessing_spawn_integrate   executed in 61283.24150 ms with 1 work flows;
* multithreading_integrate          executed in 389.86420   ms with 1 work flows;
* multithreading_spawn_integrate    executed in 381.31520   ms with 1 work flows;

* multiprocessing_integrate         executed in 69688.47170 ms with 2 work flows;
* multiprocessing_spawn_integrate   executed in 67375.92480 ms with 2 work flows;
* multithreading_integrate          executed in 426.67100 ms with 2 work flows;
* multithreading_spawn_integrate    executed in 417.11010 ms with 2 work flows;

* multiprocessing_integrate         executed in 82319.67720 ms with 4 work flows;
* multiprocessing_spawn_integrate   executed in 83952.44370 ms with 4 work flows;
* multithreading_integrate          executed in 661.59480 ms with 4 work flows;
* multithreading_spawn_integrate    executed in 608.19560 ms with 4 work flows;

* multiprocessing_integrate         executed in 99386.50530 ms with 6 work flows;
* multiprocessing_spawn_integrate   executed in 102820.34190 ms with 6 work flows;
* multithreading_integrate          executed in 786.75590 ms with 6 work flows;
* multithreading_spawn_integrate    executed in 830.08960 ms with 6 work flows;

Как следует из списка, время выполнения и для потоков, и для процессов растёт с повышением количества потоков/процессов. На основе этого можно сказать, что для данной реализации задачи многопоточность и многопроцессорность не приносит увеличения производительности. Дополнительно можно заметить, что функция-обёртка partial уменьшает время выполнения для потоков, но для процессов, напротив, увеличивает.


Как только функции в потоке/процессе выполнились, из их значений вычисляется интеграл и нет необходимости обмениваться какой-либо информацией между потоками/процессами. Поэтому для данной задачи использование примитивов синхронизации не имеет смысла.

