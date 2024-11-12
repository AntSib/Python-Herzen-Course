### Лабораторная работа № 4. Задачи.
## Комплект 1: Алгоритмы на Python. Начало.
Задача 1.1
Написать функцию two_sum, которая возвращает кортеж из двух индексов элементов списка lst, 
таких что сумма элементов по этим индексам равна переменной target. 
Элемент по индексу может быть выбран лишь единожды, значения в списке могут повторяться. 
Если в списке встречается больше чем два индекса, подходящих под условие вернуть наименьшие из всех. 
Элементы находятся в списке в произвольном порядке. 
Алгоритм на двух циклах, сложность O(n2).
Пример использования:
```python
st = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 8
result = two_sum(lst, target)
print(result)
```
Результат: 
```python
(0, 6)
```

Код программы:
two_sum_f.py
```python
lst = [i for i in range(1, 16)]
target = 8


def two_sum(lst: list, target: int) -> tuple:
    """
    Return a tuple of two indices whose corresponding elements in the given list add up to the target.

    :param lst: a list of integers
    :param target: an integer
    :return: a tuple of two indices
    """
    for i in range(len(lst)):   # O(n^2)
        for j in range(i + 1, len(lst)):
            if lst[i] + lst[j] == target:
                return (i, j)


if __name__ == "__main__":
    res = two_sum(lst, target)
    print(res)
```
