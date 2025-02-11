# Лабораторная работа №3
## Комплект 1: Работа над мини-проектом калькулятор. Функции. Тесты
### Задание 1.1 и 1.2

Модернизируйте калькулятор из задач 1.2 и 1.4 Лабораторной работы № 2. Добавьте к калькулятору такую настройку как точность вычислений, которая передаётся в виде keyword параметра tolerance со значением по умолчанию 1e−6. На основе переданного значения этого параметра извлеките с помощью вычислений порядок этого значения (например, 6 для 1e−6) в виде отдельной функции convert_precision, вызываемой из calculate. Задокументируйте convert_precision и дополните документацию к calculate в коде. Извлечённый порядок используйте для округления итогового результата в функции calculate. Покройте (напишите) дополнительными тестами convert_precision и calculate в связи с появлением tolerance с помощью пакета pytest.
___
Модернизируйте калькулятор из задачи 1.1. Добавьте переменное количество неименованных аргументов (операндов, ∗args) после параметра action и перед keyword параметром tolerance. К списку поддерживаемых действий добавьте вычисление таких величин как среднее значение (medium), дисперсия (variance), стандартное отклонение (std_deviation), медиана (median, q2, второй квартиль) и межквартильный размах (q3 - q1, разница третьего и первого квартилей). Покройте новые реализованные функции и функцию calculate дополнительными тестами.

```python
import logging
import math


logger = logging.getLogger(__name__)                            # Initiation of logger
logging.basicConfig(filename='mylog.log', level=logging.INFO)   # Basic setup for logger


def decoration_logger(func: callable) -> callable:
    """
    Returns a wrapper function that logs the input and output of the decorated function and returns the result.
    
    :param callable func: The function to be decorated.

    :returns: The wrapper function.
    """
    def wrapper(operator: str, *numbers, tolerance: float) -> float:
        """
        Logs the input operation and numbers, executes the decorated function, and logs the result.

        :param str operator: The operation to be performed.
        :param numbers: A tuple of list of string numbers to be used in the operation.
        :param float tolerance: The tolerance level for the operation.

        :returns: The result of the operation as a float.
        """
        logger.info(f"operation: {operator} numbers: {numbers}")    # logging input
        
        res = func(operator, *numbers, tolerance=tolerance)

        logger.info(f"result: {res}")                               # logging result
        return res
    return wrapper


def convert_precision(tolerance: float) -> int:
    """
    Converts a given tolerance to an appropriate number of decimal places.

    The returned value is the number of decimal places to round to, based on the given tolerance.

    :param float tolerance: The tolerance to convert.

    :returns: The appropriate number of decimal places to round to, as an integer.
    """
    counter = 0

    while tolerance < 1:
        tolerance *= 10
        counter += 1

    return counter


def summary(*args) -> int:
    """
    Return the sum of the arguments.

    :param args: The numbers to be summed.
    :returns: The sum of the arguments as an integer.
    """
    return sum(args)


def mean(*args) -> float:
    """
    Return the mean of the arguments.

    :param args: The arguments to be averaged.
    :returns: The mean of the arguments as a float.
    """
    return sum(args) / len(args)


def variance(*args) -> float:
    """
    Return the variance of the arguments.

    :param args: The arguments to be used in calculating the variance.
    :returns: The variance of the arguments as a float.
    """
    x_mean = mean(*args)
    return sum((x - x_mean) ** 2 for x in args) / (len(args) - 1)


def std_deviation(*args) -> float:
    """
    Return the standard deviation of the arguments.

    :param args: The arguments to be used in calculating the standard deviation.
    :returns: The standard deviation of the arguments as a float.
    """
    x_mean = mean(*args)

    if len(args) < 25: # for data samples with less than 25 elements it is required to divide by (n - 1)
        return math.sqrt(sum((x - x_mean) ** 2 for x in args) / (len(args) - 1))
    else:
        return math.sqrt(sum((x - x_mean) ** 2 for x in args) / len(args))


def median(*args) -> float:
    """
    Return the median of the arguments.

    :param args: The arguments to be used in calculating the median.
    :returns: The median of the arguments as a float.
    """
    data = sorted(args)
    mid = len(data) // 2
    # median of an even-sized array is the average of the two middle elements
    return (data[mid - 1] + data[mid]) / 2.0 if len(data) % 2 == 0 else data[mid]


def q3_q1(*args):
    """
    Return the difference between the third and first quartiles (Q3 - Q1).

    :param args: The numbers to be used in calculating the quartiles.
    :returns: The difference between the third and first quartiles as a float.
    """
    data = sorted(args)
    lower_half = data[:len(data) // 2]      # Data slice for first quartile

    if len(data) % 2 == 0:
        upper_half = data[len(data) // 2:]  # Data slice for third quartile
    else:
        upper_half = data[len(data) // 2 + 1:]
    
    q1 = median(*lower_half)                # Quartiles themselves
    q3 = median(*upper_half)

    return q3 - q1


awailable_operators = {     # Dictionary of available operators and corresponding functions
    '+': summary,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '^': lambda x, y: x ** y,
    '%': lambda x, y: x % y,
    'mean': mean,
    'var': variance,
    'dev': std_deviation,
    'med': median,
    'q3_q1': q3_q1
}


@decoration_logger
def calculate(action: str, *args, tolerance: float = 1e-6) -> float:
    """
    Perform a calculation based on the specified action and arguments, with a given precision tolerance.

    This function supports various operations provided in the `awailable_operators` dictionary, such as
    addition, subtraction, multiplication, division, exponentiation, modulus, mean, variance, standard deviation,
    median, and the difference between the third and first quartiles (Q3 - Q1).

    :param str action: Specifies the operation to perform.
    :param args: A variable representing numbers to be used in the operation.
    :param float tolerance: The precision tolerance for the result, default is 1e-6.5

    :returns: The result of the operation rounded according to the specified tolerance.
    """
    numbers = list(map(float, *args))   # Convertion from string to float
    
    if action in awailable_operators:
        return round(                   # Calling functions from dictionary and round the result to the specified precision
                    awailable_operators[action](*numbers), 
                    convert_precision(tolerance)
                )
    else:
        print("Invalid operator")       # If invalid operator is entered
        return None


if __name__ == "__main__":

    print("Choose your operator: ", end='')
    for option in awailable_operators:      # Print all available operators (can be moved to function)
        print(f'"{option}"', end='  ')
    print()

    prompt = input("Enter an expression: ") 
    oper, *numbers, tol = prompt.split(' ') # Parsing the input (also can be moved to function)
    tol = float(tol)
    
    print(calculate(oper, numbers, tolerance=tol))
```

Отделный файл для тестирования

```python
import pytest
import statistics           # Using functionality of statistics module for testing
from calculator_with_tolerance import convert_precision, awailable_operators
from calculator_with_tolerance import summary, mean, variance, std_deviation, median, q3_q1, calculate


tolerance_default = 1e-6    # Default tolerance for tests

class TestCalculate:
    def test_summary(self):
        """Test that summary correctly handles addition."""
        assert awailable_operators["+"](*[1, 2, 3]) == 1 + 2 + 3
    
    def test_subtraction(self):
        """Test that function correctly handles subtraction."""
        assert awailable_operators["-"](3, 2) == 3 - 2
    
    def test_multiplication(self):
        """Test that function correctly handles multiplication."""
        assert awailable_operators["*"](3, 2) == 3 * 2
    
    def test_division(self):
        """Test that function correctly handles division."""
        assert awailable_operators["/"](6, 2) == 6 / 2
    
    def test_power(self):
        """Test that function correctly handles exponentiation."""
        assert awailable_operators["^"](2, 3) == 2 ** 3
    
    def test_modulus(self):
        """Test that function correctly handles modulus."""
        assert awailable_operators["%"](4, 2) == 4 % 2
    
    def test_mean(self):
        """Test that mean function works correctly."""
        stat_mean = statistics.mean([4, 7, 15, 18, 36, 40, 41])
        assert mean(*[4, 7, 15, 18, 36, 40, 41]) == stat_mean

    def test_variance(self):
        """Test that variance function works correctly."""
        stat_variance = statistics.variance([4, 7, 15, 18, 36, 40, 41])
        assert variance(*[4, 7, 15, 18, 36, 40, 41]) == stat_variance
    
    def test_std_dev(self):
        """Test that standart deviation function works correctly."""
        stat_std_dev = statistics.stdev([4, 7, 15, 18, 36, 40, 41])
        assert std_deviation(*[4, 7, 15, 18, 36, 40, 41]) == stat_std_dev
    
    def test_median(self):
        """Test that median function works correctly."""
        stat_median = statistics.median([4, 7, 15, 18, 36, 40, 41])
        assert median(*[4, 7, 15, 18, 36, 40, 41]) == stat_median
    
    def test_q3_q1(self):
        """Test that function correctly calculates difference between third and first quartiles (Q3 - Q1)."""
        stat_q3_q1 = statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[2] - statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[0]
        assert q3_q1(*[4, 7, 15, 18, 36, 40, 41]) == stat_q3_q1

    def test_calc_type(self):
        """Test that calculate returns a float."""
        assert type(calculate("var", [4, 7, 15, 18, 36, 40, 41], tolerance=tolerance_default)) == float

    def test_convert_precision(self):
        """Test that convert_precision correctly converts the precision to an appropriate number of decimal places."""
        assert convert_precision(1.0) == 0
        assert convert_precision(0.1) == 1
        assert convert_precision(0.01) == 2
        assert convert_precision(0.001) == 3
    
    def test_convert_precision_type(self):
        """Test that convert_precision returns an int."""
        assert type(convert_precision(0.001)) == int


if __name__ == "__main__":
    pytest.main()
```
