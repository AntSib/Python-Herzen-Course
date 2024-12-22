# Лабораторная работа № 2
## Комплект 1: Начало использования Closures, Decorators, Logging, Unittests
### Задание 1.1

Создайте простое замыкание (closure) в виде внутренней (вложенной) функции внутри обычной функции. Внутренняя функция (замыкание, closure) должна использовать переменные и аргументы обычной функции, в которую она вложена. Внутри внутренней функции (closure) распечатайте переданные аргументы в терминале. Верните вложенную функцию из обычной функции с помощью выражения return.

```python
def outerfunc(arg1: str, arg2: str):
    """
    Return a function that takes two arguments and returns a dictionary with those two arguments.

    The returned function is a closure that captures the arguments to outerfunc and uses them as the
    arguments to innerfunc.

    :param str arg1: The first argument to capture.
    :param str arg2: The second argument to capture.

    :returns: A function that takes two arguments and returns a dictionary.
    """
    def innerfunc(arg3: str, arg4: str) -> dict:
        """
        Return a dictionary with the two arguments.

        :param str arg3: The first argument.
        :param str arg4: The second argument.

        :returns: A dictionary with the arguments.
        """
        return {"arg3": arg3, "arg4": arg4}

    return innerfunc(arg1, arg2)


if __name__ == "__main__":
    print(outerfunc("Sam", "25"))
```
### Задание 1.2

Изучите на примерах в интернете, что такое closure и как их применять для создания простого декоратора (decorator) с @-синтаксисом в Python. Модернизируйте калькулятор из задачи 3.1 лабораторной работы №1.
<br>
Декорируйте вашу функцию calculate. В соответствующем декорирующем замыкании, в сlosure, то есть во внутренней функции используйте простое логирование (стандартный модуль Python logging).
<br>
Сделайте логирование внутри замыкания до вызова вашей функции calculate(operand1, operand2, action), в котором логируется информация о том какие операнды и какая арифметическая операция собираются поступить на вход функции calculate(operand1, operand2, action). Затем внутри того же closure следует сам вызов функции calculate(...). А затем, после этого вызова должно быть снова логирование, но уже с результатом выполнения вычисления, проделанного в этой функции.

```python
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='Calculator.log', level=logging.INFO)


def decorator(func: callable) -> callable:
    """
    Returns a wrapper function that logs the input and output of the decorated function and returns the result.
    
    :param callable func: The function to be decorated.

    :returns: The wrapper function.
    """
    def wrapper(prompt: str) -> int:
        """
        Logs the input and output of the decorated function and returns the result.

        :param str prompt: The string prompt to be processed by the decorated function.

        :returns: The result of the decorated function.
        """
        num1, oper, num2 = prompt.split(' ')
        
        logger.info("operand1: " + num1 + " operand2: " + num2 + " operation: " + oper) # logging input prameters
        
        res = func(prompt)

        logger.info("result: " + str(res))                                              # logging result of function
        return res
    return wrapper


@decorator
def calculate(prompt: str) -> int:
    """
    Perform a calculation based on a string prompt.

    The prompt should be in the format "number operator number", e.g. "1 + 2".
    The supported operators are "+", "-", "*", "/", "^", and "%".

    If the input prompt is not valid, prints an error message and returns None.

    Keyword arguments:
    :param str prompt: The prompt to use for the calculation.
    
    :returns: The result of the calculation as an integer.
    """
    
    num1, oper, num2 = prompt.split(' ')
    
    if num1.isdigit() and num2.isdigit() and not oper.isdigit():
        num1 = int(num1)
        num2 = int(num2)

        if oper == "+": return num1 + num2
        if oper == "-": return num1 - num2
        if oper == "*": return num1 * num2
        if oper == "/": return num1 / num2
        if oper == "^": return num1 ** num2
        if oper == "%": return num1 % num2
    else:
        print("Invalid input")


if __name__ == "__main__":
    print(calculate(input("Enter an expression: ")))



if __name__ == "__main__":
    print(calculate(input("Enter an expression: ")))
```

### Задание 1.3

Изучите основы каррирования. Каррирование в самом простом варианте - это создание специализированной функции на основе более общей функции с предустановленными параметрами для этой более общей функции.
<br>
Реализуйте каррирование на примере вычисления количества радиоактивного вещества N, оставшегося в некоторый момент времени t от радиоактивного вещества с периодом полураспада t1/2, если изначально это количество было равно N0.
<br>
Закон распада задан формулой: N=N_0*(1/2)^(t/t_(1/2) )
<br>
В качестве проставленного заранее параметра в данном примере должно быть значение периода полураспада t1/2, которое постоянно для каждого типа радиоактивного материала (радиоактивного изотопа химического элемента).
<br>
Сделайте словарь, где в качестве колючей используются строки с символами радиоактивных изотопов, а в качестве значений им сопоставлены каррированные с характерными периодами полураспада. В основном коде вашей программы организуйте цикл по этому словарю и продемонстрируйте в нём вызовы каррированных функций с распечаткой на экране сколько вещества осталось от одного и того же N0 в некоторый момент времени t в зависимости от типа изотопа.

```python
def radioactive_decay(half_life: float) -> callable:
    """
    Returns a function that computes the remaining amount of a radioactive element.

    The returned function takes two arguments, the initial amount of the element and the time passed,
    and returns the remaining amount of the element after the given time.

    The half-life of the element is given as an argument to the outer function.

    :param float half_life: The half-life of the element in seconds.

    :returns: A function that takes two arguments, the initial amount of the element and the time passed,
              and returns the remaining amount of the element after the given time.
    """
    def decay(N_0: int, time: int) -> float:
        """
        Compute the remaining amount of a radioactive element after a given time.

        :param int N_0: The initial amount of the element.

        :param int time: The time passed in seconds.

        :returns: The remaining amount of the element after the given time.
        """
        return N_0 * 0.5 ** (time / half_life)
    return decay


if __name__ == "__main__":
    h_to_sec = 60 * 60          # Constant to convert hours to seconds
    d_to_sec = h_to_sec * 24    # Constant to convert days to seconds
    y_to_sec = d_to_sec * 365   # Constant to convert years to seconds

    h_time = 100 * h_to_sec     # Time passed since the start of the experiment
    N_0 = 1000                  # Initial amount of the element (lets assume it is 1000 grams)

    rad_elements = {
        "At": 7.2 * h_to_sec, 
        "Tc": 61 * d_to_sec, 
        "Bk": 1380 * y_to_sec
    }

    decay_functions = {         # Creating a dictionary of decay functions for each isotope
        isotope: radioactive_decay(half_life) for isotope, half_life in rad_elements.items()
    }

    print("The remaining amount of radioactive elements:")
    
    for isotope, decay_function in decay_functions.items():
        remaining_amount = decay_function(N_0, h_time)
        print(f"{isotope}: {remaining_amount}")
```

### Задание 1.4

Напишите unit-тесты для калькулятора из задачи 3.1 лабораторной работы № 1 используя стандартный модуль unittest библиотеки Python. Затем перепешите те же тесты с использованием пакета pytest.
<br>
Тестирование с помощью unittest

```python
import unittest


class TestCalculate(unittest.TestCase):
    def test_calc_add(self):
        """Test that calculate correctly handles addition."""
        self.assertEqual(calculate("1 + 2"), 3)

    def test_calc_subtr(self):
        """Test that calculate correctly handles subtraction."""
        self.assertEqual(calculate("1 - 2"), -1)

    def test_calc_mult(self):
        """Test that calculate correctly handles multiplication."""
        self.assertEqual(calculate("2 * 3"), 6)

    def test_calc_div(self):
        """Test that calculate correctly handles division."""
        self.assertEqual(calculate("6 / 2"), 3)

    def test_calc_pow(self):
        """Test that calculate correctly handles exponentiation."""
        self.assertEqual(calculate("2 ^ 3"), 8)
        
    def test_calc_mod(self):
        """Test that calculate correctly handles modulus."""
        self.assertEqual(calculate("7 % 3"), 1)

    def test_invalid_input(self):
        """Test that calculate raises a ValueError when given invalid input."""
        with self.assertRaises(ValueError):
            calculate("1 +")


def calculate(prompt: str) -> int:
    """
    Perform a calculation based on a string prompt.

    The prompt should be in the format "number operator number", e.g. "1 + 2".
    The supported operators are "+", "-", "*", "/", "^", and "%".

    If the input prompt is not valid, prints an error message and returns None.

    Keyword arguments:
    :param str prompt: The prompt to use for the calculation.
    
    :returns: The result of the calculation as an integer.
    """
    num1, oper, num2 = prompt.split(' ')
    
    if num1.isdigit() and num2.isdigit() and not oper.isdigit():
        num1 = int(num1)
        num2 = int(num2)

        if oper == "+": return num1 + num2
        if oper == "-": return num1 - num2
        if oper == "*": return num1 * num2
        if oper == "/": return num1 / num2
        if oper == "^": return num1 ** num2
        if oper == "%": return num1 % num2
    else:
        print("Invalid input")


if __name__ == "__main__":
    unittest.main()
```

Тестирование с помощью pytest

```python
import pytest


class TestCalculate:
    def test_calc_add(self):
        """Test that calculate correctly handles addition."""
        assert calculate("1 + 2") == 3

    def test_calc_subtr(self):
        """Test that calculate correctly handles subtraction."""
        assert calculate("1 - 2") == -1

    def test_calc_mult(self):
        """Test that calculate correctly handles multiplication."""
        assert calculate("2 * 3") == 6

    def test_calc_div(self):
        """Test that calculate correctly handles division."""
        assert calculate("6 / 2") == 3

    def test_calc_pow(self):
        """Test that calculate correctly handles exponentiation."""
        assert calculate("2 ^ 3") == 8

    def test_calc_mod(self):
        """Test that calculate correctly handles modulus."""
        assert calculate("7 % 3") == 1

    def test_invalid_input(self):
        """Test that calculate raises a ValueError when given invalid input."""
        with pytest.raises(ValueError):
            calculate("1 +")


def calculate(prompt: str) -> int:
    """
    Perform a calculation based on a string prompt.

    The prompt should be in the format "number operator number", e.g. "1 + 2".
    The supported operators are "+", "-", "*", "/", "^", and "%".

    If the input prompt is not valid, prints an error message and returns None.

    Keyword arguments:
    :param str prompt: The prompt to use for the calculation.
    
    :returns: The result of the calculation as an integer.
    """
    num1, oper, num2 = prompt.split(' ')
    
    if num1.isdigit() and num2.isdigit() and not oper.isdigit():
        num1 = int(num1)
        num2 = int(num2)

        if oper == "+": return num1 + num2
        if oper == "-": return num1 - num2
        if oper == "*": return num1 * num2
        if oper == "/": return num1 / num2
        if oper == "^": return num1 ** num2
        if oper == "%": return num1 % num2
    else:
        print("Invalid input")


if __name__ == "__main__":
    pytest.main(self)
```
