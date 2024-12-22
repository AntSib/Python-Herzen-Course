# Лабораторная работа № 4. Задачи.
## Комплект 1: Алгоритмы на Python. Начало.
### Задача 1.1 
Написать функцию two_sum, которая возвращает кортеж из двух индексов элементов списка lst, таких что сумма элементов по этим индексам равна переменной target. 
Элемент по индексу может быть выбран лишь единожды, значения в списке могут повторяться.
Если в списке встречается больше, чем два индекса, подходящих под условие вернуть наименьшие из всех.
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

two_sum_f.py
Код программы:
```python
lst = [i for i in range(1, 16)]
target = 7


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
    
    print("No matching pair found")
    return None


if __name__ == "__main__":
    res = two_sum(lst, target)
    print(res)
```

Результат работы программы:
```python
(0, 5)
```

Анализ:
Сложность данного алгоритма O(n^2), так как программа имеет два вложенных цикла.
Если в списке нет таких чисел, которые в сумме давали бы нужно число, программа выведет об этом сообщение.

### Задача 1.2
Усовершенствуйте предыдущую задачу 1.1, добавив функцию two_sum_hashed(lst, target) так, чтобы сложность алгоритма была ниже: O(n) или O(n · log(n)).

two_sum_fast_f.py
Код программы:
```python
lst = [i for i in range(1, 16)]
target = 7


def two_sum_fast(lst: list, target: int) -> tuple:
    """
    Return a tuple of two indices whose corresponding elements in the given list add up to the target.

    :param lst: a list of integers
    :param target: an integer
    :return: a tuple of two indices or None if no matching pair is found
    """
    for item in lst:                # O(n)
        if target - item in lst:
            a = lst.index(item)
            b = lst.index(target - item)

            if b > a:               # Check if b is after a, this also prevents duplicates
                return (a, b)

    print("No matching pair found")
    return None


if __name__ == "__main__":
    res = two_sum_fast(lst, target)
    print(res)
```

Результат работы программы:
```python
(0, 5)
```

Анализ:
Сложность данного алгоритма O(n), так как программа имеет только один цикл.
Если в списке нет таких чисел, которые в сумме давали бы нужно число, программа выведет об этом сообщение.


Задание 1.3
совершенствуйте предыдущую задачу 1.2, добавив функцию  которая возвращает все наборы индексов, удовлетворяющих условию суммы target. 
Пример использования:
```python
st = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 8
result = two_sum_hashed_all(lst, target)
print(result)
```
Результат:
```python
[(0,6), (1,5), (2,4)]
```

two_sum_fast_all_f.py
Код программы:
```python
lst = [i for i in range(1, 101)]
target = 10


def two_sum_hashed_all(lst: list, target: int) -> list:
    """
    Return a list of tuples, each containing two indices whose corresponding elements
    in the given list add up to the target.

    :param lst: a list of integers
    :param target: an integer
    :return: a list of tuples of two indices or None if no matching pairs are found
    """
    found = []

    for item in lst:                    # O(n)
        if target - item in lst:
            a = lst.index(item)
            b = lst.index(target - item)

            if b > a:                   # Check if b is after a, this also prevents duplicates
                found.append((a, b))    # Saving indices

    if found:
        return found

    print("No matching pair found")
    return None


if __name__ == "__main__":
    res = two_sum_hashed_all(lst, target)
    print(res)
```

Результат работы программы:
```python
[(0, 8), (1, 7), (2, 6), (3, 5)]
```

Анализ:
Сложность данного алгоритма O(n), так как для нахождения всех пар чисел программе нужно пройти по списку только один раз.

Тестирование программ:

test_two_sum.py
Код программы:
```python
import pytest
from timeit import timeit
from two_sum_f import two_sum
from two_sum_fast_f import two_sum_fast
from two_sum_fast_all_f import two_sum_hashed_all


class TestTwoSums:
    def test_two_sum(self):
        """
        Test that two_sum function returns (0, 6)
        for elements in the list [1, 2, ..., 9] that add up to 8.
        """
        assert two_sum([i for i in range(1, 10)], 8) == (0, 6)
    
    def test_two_sum2(self):
        """
        Test that two_sum function returns (0, 4)
        for elements in the list [2, 3, ..., 9] that add up to 8.
        """
        assert two_sum([i for i in range(2, 10)], 8) == (0, 4)

    def test_two_sum3(self):
        """
        Test that two_sum function returns (1, 4)
        for elements in the list [1, 2, 3, 4, 6, 8, 9] that add up to 8.
        """
        assert two_sum([1, 2, 3, 4, 6, 8, 9], 8) == (1, 4)
    
    def test_two_sum_too_small(self):
        """
        Test that two_sum function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is smaller than minimum of the list.
        """
        assert two_sum([i for i in range(1, 10)], 0) == None
    
    def test_two_sum_too_big(self):
        """
        Test that two_sum function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is bigger than maximum of the list.
        """
        assert two_sum([i for i in range(1, 10)], 18) == None


class TestTwoSumsFast:
    def test_two_sum_fast(self):
        """
        Test that two_sum_fast function returns (0, 6)
        for elements in the list [1, 2, ..., 9] that add up to 8.
        """
        assert two_sum_fast([i for i in range(1, 10)], 8) == (0, 6)
    
    def test_two_sum_fast2(self):
        """
        Test that two_sum_fast function returns (0, 4)
        for elements in the list [2, 3, ..., 9] that add up to 8.
        """
        assert two_sum_fast([i for i in range(2, 10)], 8) == (0, 4)

    def test_two_sum_fast3(self):
        """
        Test that two_sum_fast function returns (1, 4)
        for elements in the list [1, 2, 3, 4, 6, 8, 9] that add up to 8.
        """
        assert two_sum_fast([1, 2, 3, 4, 6, 8, 9], 8) == (1, 4)
    
    def test_two_sum_fast_too_small(self):
        """
        Test that two_sum_fast function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is smaller than minimum of the list.
        """
        assert two_sum_fast([i for i in range(1, 10)], 0) == None
    
    def test_two_sum_fast_too_big(self):
        """
        Test that two_sum_fast function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is bigger than maximum of the list.
        """
        assert two_sum_fast([i for i in range(1, 10)], 18) == None


class TestTwoSumsFastAll:
    def test_two_sum_fast_all(self):
        """
        Test that two_sum_hashed_all function returns [(0, 5), (1, 4)]
        for elements in the list [1, 2, 3, 4, 6, 7, 8, 9] that add up to 8.
        """
        assert two_sum_hashed_all([1, 2, 3, 4, 6, 7, 8, 9], 8) == [(0, 5), (1, 4)]

    def test_two_sum_fast_all2(self):
        """
        Test that two_sum_hashed_all function returns [(0, 3)]
        for elements in the list [2, 3, 4, 6, 7, 8, 9] that add up to 8.
        """
        assert two_sum_hashed_all([2, 3, 4, 6, 7, 8, 9], 8) == [(0, 3)]

    def test_two_sum_fast_all3(self):
        """
        Test that two_sum_hashed_all function returns [(0, 8), (1, 7), (2, 6), (3, 5)]
        for elements in the list [1, 2, ..., 15] that add up to 10.
        """
        assert two_sum_hashed_all([i for i in range(1, 16)], 10) == [(0, 8), (1, 7), (2, 6), (3, 5)]

    def test_two_sum_fast_all_big_list(self):
        """
        Test that two_sum_hashed_all function returns expected list of tuples
        for a list of 100,000 elements and a target of 50.
        """
        target = 50
        test_list = [(i, target - i - 2) for i in range(target//2 - 1)]
        assert two_sum_hashed_all([i for i in range(1, 100001)], 50) == test_list
    
    def test_two_sum_fast_all_too_small(self):
        """
        Test that two_sum_hashed_all function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is smaller than the minimum of the list.
        """
        assert two_sum_hashed_all([i for i in range(1, 10)], 0) == None

    def test_two_sum_fast_all_too_big(self):
        """
        Test that two_sum_hashed_all function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is bigger than the maximum of the list.
        """
        assert two_sum_hashed_all([i for i in range(1, 10)], 18) == None


class TestTwoSumsTime:
    # Constants
    big_list = [i for i in range(1, 10001)]
    target = 50
    n_tests = 100
    to_millis = 10*6

    def time_two_sum(self):
        """
        Measure the execution time of the two_sum function
        for a list of 100,000 elements and a target of 666.
        The test is run 1000 times and the result is printed
        in milliseconds.
        """
        exec_time = timeit("two_sum(TestTwoSumsTime.big_list, TestTwoSumsTime.target)", globals=globals(), number=self.n_tests)
        print(f"Execution time of two_sum is: {exec_time * self.to_millis} milliseconds")
    
    def time_two_sum_fast(self):
        """
        Measure the execution time of the two_sum_fast function
        for a list of 100,000 elements and a target of 666.
        The test is run 1000 times and the result is printed
        in milliseconds.
        """
        exec_time = timeit("two_sum_fast(TestTwoSumsTime.big_list, TestTwoSumsTime.target)", globals=globals(), number=self.n_tests)
        print(f"Execution time of two_sum_fast is: {exec_time * self.to_millis} milliseconds")

    def time_two_sum_fast_all(self):
        """
        Measure the execution time of the two_sum_hashed_all function
        for a list of 100,000 elements and a target of 666.
        The test is run 1000 times and the result is printed
        in milliseconds.
        """
        exec_time = timeit("two_sum_hashed_all(TestTwoSumsTime.big_list, TestTwoSumsTime.target)", globals=globals(), number=self.n_tests)
        print(f"Execution time of two_sum_hashed_all is: {exec_time * self.to_millis} milliseconds")
        


if __name__ == "__main__":
    pytest.main()

    TestTwoSumsTime().time_two_sum()
    TestTwoSumsTime().time_two_sum_fast()
    TestTwoSumsTime().time_two_sum_fast_all()
```

Результат работы программы:
```
============================= test session starts =============================
platform win32 -- Python 3.12.5, pytest-8.3.3, pluggy-1.5.0
rootdir: C:\Users\Anton\Programms\Python\Herzen git repo\Python-Herzen-Course\ЛР-4
collected 16 items
test_two_sum.py ................                                         [100%]
============================= 16 passed in 54.87s =============================

Execution time of two_sum is: 0.012390000047162175 milliseconds
Execution time of two_sum_fast is: 0.006893999889143743 milliseconds
Execution time of two_sum_hashed_all is: 2894.3197919998784 milliseconds
```

Анализ:
Функции тестируются на корректность работы для различных искомых чисел и проверяется корректность вывода при отсутствии подходящего числа.
Как следует из времени работы, функция two_sum_fast работает в два раза быстрее, чем two_sum благодаря работе в одном цикле.

### Задача 1.4
Повторите или изучите понятие мемоизации в Python. Реализуйте с помощью мемоизации и рекурсии вычисление чисел Фибоначчи сначала руками с помощью вручную добавленного к рекурсивной функции словаря с ранее вычисленными числами Фибоначчи, а затем с помощью декоратора @cache из стандартного модуля Python functools.

memoization.py
Код программы:
```python
from functools import cache, wraps
from timeit import timeit

memo = {}


def fib_test(n: int) -> int:    # function for comparison of execution time
    """
    Compute the nth Fibonacci number without memoization.

    Simple recursive function to compute the nth Fibonacci number.

    :param int n: The index of the Fibonacci number to compute.
    :returns: The nth Fibonacci number.
    """
    if n < 2:
        return n
    return fib_test(n - 1) + fib_test(n - 2)


def fib_memo_sleeve(n: int) -> int:
    """
    Compute the nth Fibonacci number using memoization.

    This function uses memoization to store previously computed Fibonacci numbers.

    :param int n: The index of the Fibonacci number to compute.
    :returns: The nth Fibonacci number.
    """
    global memo
    if n < 2:       # Base case
        return n
    if n in memo:   # Check if the number has already been computed
        return memo[n]
    memo[n] = fib_memo_sleeve(n - 1) + fib_memo_sleeve(n - 2)  # Compute the Fibonacci number

    return memo[n]


def memoize(func: callable) -> callable:
    """
    Memoize a function, by storing its results in a cache.

    This decorator will store the results of a function in a cache, so that
    subsequent calls with the same arguments will return the cached result.

    The cache is keyed by a tuple of the arguments to the function, so the
    function must be able to be called with the same arguments multiple times.

    :param callable func: The function to be memoized.
    :returns: A memoized version of the function.
    """
    cache = {}  # Cache for the results of the function
    
    @wraps(func)
    def wrapper(*args, **kwargs) -> int:
        """
        The memoized version of the function.

        This function will look up the result of the function in the cache, and
        return the cached result if it exists. If the result is not in the cache,
        it will compute the result and store it in the cache before returning it.

        :param args: The positional arguments to the function.
        :param kwargs: The keyword arguments to the function.
        :returns: The nth Fibonacci number.
        """
        key = args + tuple(sorted(kwargs.items()))

        if key not in cache:
            cache[key] = func(*args, **kwargs)       # Compute the result
        return cache[key]
        
    return wrapper


@memoize
def fib_memo(n: int) -> int:
    """
    Compute the nth Fibonacci number using memoization.

    This function uses the @memoize decorator to store previously computed Fibonacci numbers.

    :param int n: The index of the Fibonacci number to compute.
    :returns: The nth Fibonacci number.
    """
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


@cache
def fib_cached(n: int) -> int:
    """
    Compute the nth Fibonacci number using the @cache decorator.

    This function uses the @cache decorator from the functools module to store previously computed Fibonacci numbers.

    :param int n: The index of the Fibonacci number to compute.
    :returns: The nth Fibonacci number.
    """
    if n < 2:       # Base case
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)    # Compute the Fibonacci number


if __name__ == "__main__":
    to_millis = 10*6
    num = 30
    
    print(f"fib_test function: {fib_test(num)}")
    print(f"fib_memo_sleeve function: {fib_memo_sleeve(num)}")
    print(f"fib_memo function: {fib_memo(num)}")
    print(f"fib_cached function: {fib_cached(num)}")

    # globals=globals() allows the timeit function to access the fibonacci function and the variable num
    # exec_time = timeit("fib_test(num)", globals=globals(), number=10000)
    # exec_time_sleeve = timeit("fib_memo_sleeve(num)", globals=globals(), number=10000)
    # exec_time_fibonacci = timeit("fib_memo(num)", globals=globals(), number=10000)
    # exec_time_cached = timeit("fib_cached(num)", globals=globals(), number=10000)
    
    # print(f"fib_test function: {exec_time * to_millis}")
    # print(f"fib_memo_sleeve function: {exec_time_sleeve * to_millis}")
    # print(f"fib_memo function: {exec_time_fibonacci * to_millis}")
    # print(f"fib_cached function: {exec_time_cached * to_millis}")
```

Результат работы программы:
```
fib_test function: 832040
fib_memo_sleeve function: 832040
fib_memo function: 832040
fib_cached function: 832040
```

Анализ:
В программе реализованы 4 функции для вычисления чисел Фибоначчи: 
функция fib_test использует классический рекурсивный метод для вычисления чисел. Она используется в качестве контрольного варианта при замере времени выполнения; 
функция fib_memo_sleeve вычисляет каждое число Фибоначчи только один раз, мемоизируя номер числа и его значение числа в словаре; 
функция fib_memo использует функцию-обёртку для мемоизации;
функция fib_cached  использует декоратор cache из встроенного модуля functools.


Тестирование программ:

test_memoization.py
Код программы:
```python
import pytest
from timeit import timeit
from memoization import fib_test, fib_memo_sleeve, fib_memo, fib_cached


class TestMemoization:
    @pytest.mark.parametrize(
        "n, expected",
        [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (7, 13),
            (8, 21),
            (11, 89),
            (12, 144)
        ]
    )
    def test_fib_memo_sleeve(self, n, expected):
        """
        Test the fib_memo_sleeve function for computing Fibonacci numbers.

        This test checks that the fib_memo_sleeve function returns the correct Fibonacci number
        for a given input 'n'. The test uses various test cases with 
        expected results.

        :param n: Index of the Fibonacci number to compute.
        :param expected: The expected Fibonacci number at index 'n'.
        """
        assert fib_memo_sleeve(n) == expected
    
    @pytest.mark.parametrize(
        "n, expected",
        [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (7, 13),
            (8, 21),
            (11, 89),
            (12, 144)
        ]
    )
    def test_fib_memo(self, n, expected):
        """
        Test the fib_memo function for computing Fibonacci numbers.

        This test checks that the fib_memo function returns the correct Fibonacci number
        for a given input 'n'. The test uses various test cases with 
        expected results.

        :param n: Index of the Fibonacci number to compute.
        :param expected: The expected Fibonacci number at index 'n'.
        """
        assert fib_memo(n) == expected
    
    @pytest.mark.parametrize(
        "n, expected",
        [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (7, 13),
            (8, 21),
            (11, 89),
            (12, 144)
        ]
    )
    def test_fib_cached(self, n, expected):
        """
        Test the fib_cached function for computing Fibonacci numbers.

        This test checks that the fib_cached function returns the correct Fibonacci number
        for a given input 'n'. The test uses various test cases with 
        expected results.

        :param n: Index of the Fibonacci number to compute.
        :param expected: The expected Fibonacci number at index 'n'.
        """
        assert fib_cached(n) == expected


class TestFuncTime:
    to_millis = 10*6
    n = 30
    n_tests = 100

    def test_fib_test(self):
        """
        Measure the execution time of the fib_test function for 50th Fibonacci number. 
        The test is run 100 of times and the result is printed in milliseconds.
        """
        exec_time = timeit("fib_test(TestFuncTime.n)", globals=globals(), number=self.n_tests)
        print(f"Execution time of fib_test is: {exec_time * self.to_millis} milliseconds")
    
    def test_fib_memo_sleeve(self):
        """
        Measure the execution time of the fib_memo_sleeve function for 50th Fibonacci number. 
        The test is run 100 of times and the result is printed in milliseconds.
        """
        exec_time = timeit("fib_memo_sleeve(TestFuncTime.n)", globals=globals(), number=self.n_tests)
        print(f"Execution time of fib_memo_sleeve is: {exec_time * self.to_millis} milliseconds")
    
    def test_fib_memo(self):
        """
        Measure the execution time of the fib_memo function for 50th Fibonacci number. 
        The test is run 100 of times and the result is printed in milliseconds.
        """
        exec_time = timeit("fib_memo(TestFuncTime.n)", globals=globals(), number=self.n_tests)
        print(f"Execution time of fib_memo is: {exec_time * self.to_millis} milliseconds")
    
    def test_fib_cached(self):
        """
        Measure the execution time of the fib_cached function for 50th Fibonacci number. 
        The test is run 100 times and the result is printed in milliseconds.
        """
        exec_time = timeit("fib_cached(TestFuncTime.n)", globals=globals(), number=self.n_tests)
        print(f"Execution time of fib_cached is: {exec_time * self.to_millis} milliseconds")


if __name__ == "__main__":
    pytest.main()

    TestFuncTime().test_fib_test()
    TestFuncTime().test_fib_memo_sleeve()
    TestFuncTime().test_fib_memo()
    TestFuncTime().test_fib_cached()
```

Результат работы программы:
```
============================= test session starts =============================
platform win32 -- Python 3.12.5, pytest-8.3.3, pluggy-1.5.0
rootdir: C:\Users\Anton\Programms\Python\Herzen git repo\Python-Herzen-Course\ЛР-4
collected 28 items

test_memoization.py ............................                         [100%]

============================= 28 passed in 11.44s =============================

Execution time of fib_test is: 586.8359160001273 milliseconds
Execution time of fib_memo_sleeve is: 0.0016859997413121164 milliseconds
Execution time of fib_memo is: 0.006624000234296545 milliseconds
Execution time of fib_cached is: 0.0025260000256821513 milliseconds
```

Анализ:
Программа проверяет корректность вычисления функций для n-ого числа последовательности.
Как следует из замеров времени работы мемоизация несопоставимо сильно увеличивает эффективность вычисления для больших чисел. Можно заметить, что fib_memo_sleeve работает быстрее остальных функций. По видимому это связано с использованием словаря значений непосредственно в самой функции, в то время как в остальных функциях мемоизация реализована через декораторы – «функции-обёртки».


## Комплект 2: Начало использования библиотечных модулей.
### Задача 2.1
Отправка почты через smtplib.

send_email.py
Код программы:
```python
import smtplib
from secrets import sender, receiver, google_app_password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_test_email(sender: str, receiver: str, password: str, subject: str, body: str) -> None:
    """
    Sends a email from the given sender to the receiver with the specified subject and body.

    :param str sender: The email address of the sender.
    :param str receiver: The email address of the receiver.
    :param str password: The password for the sender's email account.
    :param str subject: The subject of the email.
    :param str body: The body content of the email.

    :returns: None

    :raises Exception: If any error occurs during the email sending process.
    """
    port = 465

    msg = MIMEMultipart()           # Using MIMEMultipart to assemble the email
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain')) # Attaching the body to the email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', port) as server:    # Setting up the server
            server.ehlo()
            server.login(sender, password)                          # Logging in via google apps password
            server.sendmail(sender, receiver, msg.as_string())      # Sending the email
    except Exception as e:              # to catch random exceptions
        print(f"Error: {e}")


if __name__ == "__main__":
    subject = "Python test email"
    body = "This is a test email sent via Python."

    send_test_email(sender, receiver, google_app_password, subject, body)
```

Результат работы программы:
![Python test email.eml](res/Python_test_email.eml)

Задание 2.2 и 2.3
Парсинг сайта погоды (wheather HTML parsing) на простом сайте wttr.in с помощью BeautifulSoup (v4).
С помощью бибилиотеки matplotlib вывести два окна с графиками температуры на сегодня и на завтра.

soup_program.py
Код программы:
```python
import matplotlib.pyplot as plt
import urllib.request
from bs4 import BeautifulSoup


# Getting data
data = urllib.request.urlopen("https://wttr.in/saint-petersburg").read().decode('utf-8')

# Parsing
soup = BeautifulSoup(data, 'html.parser')

# There is no way to get all data automatically.

# something very odd happens with finding items for temp50
# temp50 is ['0', '0', '+1', '1', '+1', '+1'], then it must be ['+1', '0', '+1', '+1', '1', '+1', '+1']
temp49 = soup.find_all('span', class_="ef049")
temp50 = soup.find_all('span', class_="ef050")
# THIS WILL NOT WORK FOR ANY OTHER DAY THAN 04.11.2024
# BECAUSE TEMPERATURES WILL HAVE DIFFERENT SPAN CLASS

temp49 = list(map(lambda x: x.string, temp49))
temp50 = list(map(lambda x: x.string, temp50))

# for today
today_morning = soup.find('span', class_="ef051").string
today_noon = temp49[0]
today_evening = temp50[0]
today_night = temp50[2]

# for tomorrow
tomorrow_morning = temp50[4]
tomorrow_noon = temp49[1]
tomorrow_evening = temp50[4]
today_night = temp50[5]

temp_today = [today_morning, today_noon, today_evening, today_night]
temp_tomorrow = [tomorrow_morning, tomorrow_noon, tomorrow_evening, today_night]

for i in range(len(temp_today)):
    temp_today[i] = int(temp_today[i])
    temp_tomorrow[i] = int(temp_tomorrow[i])


# Plotting

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
time_of_day = ['Morning', 'Noon', 'Evening', 'Night']  # Labels for the x-axis

# Bar graph for today's temperatures
axs[0].bar(range(len(temp_today)), temp_today, color='blue')    # Make 4 bars
axs[0].set_title('Temperatures Today')                          # Set title
axs[0].set_xlabel('Time Interval')                              # Set x-axis label
axs[0].set_ylabel('Temperature (°C)')                           # Set y-axis label
axs[0].set_xticks(range(len(temp_today)))                       # Set x-axis ticks (bars)
axs[0].set_xticklabels(time_of_day)                             # Set x-axis tick labels
axs[0].axhline(0, color='black', linewidth=1, linestyle='--')  # Zero line

# Bar graph for tomorrow's temperatures
axs[1].bar(range(len(temp_tomorrow)), temp_tomorrow, color='orange')
axs[1].set_title('Temperatures Tomorrow')
axs[1].set_xlabel('Time Interval')
axs[1].set_ylabel('Temperature (°C)')
axs[1].set_xticks(range(len(temp_tomorrow)))
axs[1].set_xticklabels(time_of_day)
axs[1].axhline(0, color='black', linewidth=1, linestyle='--')

# adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('weather_temperatures.png')
```

Результат работы программы:

![Гистограмма температур](res/weather_temperatures.png)
