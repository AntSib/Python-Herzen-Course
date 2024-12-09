### Лабораторная работа 6. Тестирование unittest + pytest
Задача 1. Анализ мест в коде с исключительными ситуациями
Проанализировать ситуации работы с файлом, в которых может возникнуть исключение и реализовать обработку этих исключительных ситуаций с помощью базового инструментария.

BatchCalculatorContextManager.py
```python
import os
from time import perf_counter
from calc.calculator_with_tolerance import calculate


class BatchCalculatorContextManager(object):
    def __init__(self, file_name):
        """
        Initializes the BatchCalculatorContextManager with the given file name.

        :param file_name: The name of the file to be opened and processed.
        """
        self.filename = file_name
    
    def __enter__(self):
        """
        Entering the context manager. Setting up timer and opening the file.
        If file does not exist or is not accessible, raises an exception.

        :return: The opened file.
        """
        if not os.path.exists(self.filename):                                   # Exceptions if file does not exist or is not accessible
            raise FileNotFoundError(f"File {self.filename} does not exist.")
        if not os.access(self.filename, os.R_OK):
            raise PermissionError(f"Cannot open {self.filename}. Permission denied.")
    
        self.start_time = perf_counter()

        try:
            self.read_file = open(self.filename, 'r')
        except Exception as err:
            raise RuntimeError(f"Unexpected error while opening file: {err}")   # Unexpected error
        
        return self.read_file
            

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exiting the context manager. Closes the file and prints the execution time.

        :param exc_type: The type of exception.
        :param exc_value: The value of exception.
        :param traceback: The traceback of exception.
        """
        if hasattr(self, 'read_file') and self.read_file: 
            self.read_file.close()
        else:
            raise TypeError("File is not opened.")

        self.end_time = perf_counter()
        self.execution_time = self.end_time - self.start_time
        print(f"Execution time: {self.execution_time:.6f} seconds")


def generate_input_from_file(iterable: list) -> str:
    """
    Iterates over a list of strings, processes each string, and yields
    a formatted prompt if valid.

    Each item in the iterable is expected to be a string that contains
    a prompt separated by colons and commas. The function extracts the
    last segment after the last colon, splits it by commas, and checks
    if the resulting list has at least three elements. If so, the list
    is joined with spaces and yielded.

    :param iterable: A list of strings to be processed.
    :yield: A string containing a space-joined prompt if valid.
    """
    for item in iterable:
        try:
            # 'INFO"__main__:+,1,2,3,0.001' -> ['+', '1', '2', '3', '0.001']
            calculation_info = item.strip('\n').split(':')[-1]
            prompt = calculation_info.split('=')[0].split(',')

            if len(prompt) >= 3:                    # check if prompt has at least 3 elements, otherwise skip it and check next
                yield ' '.join(prompt)

        except (IndexError, ValueError):
            print(f"Prompt with invalid format skipped: {prompt=}")


def calc_with_manager(filename: str) -> None:
    """
    Reads a file with managed context, and prints the result of
    calculation or an error message if an exception occurs.

    :param filename: The name of the file to be read.
    """
    with BatchCalculatorContextManager(filename) as file:
        for expression in generate_input_from_file(file):
            try:
                print(f"Task: {expression}")
                result = calculate(expression)
                print(f"Result: {result}", end='\n\n')

            except Exception as err:
                print(f"Unexpected error: {err}")


if __name__ == "__main__":
    calc_with_manager('calc_log.log')
```

Анализ:
Исключения проверяются:
При открытии файла: FileNotFoundError, PermissionError, RuntimeError.
При обработке строк: IndexError, ValueError.
При выполнении вычислений: общий обработчик для неожиданных ошибок.

calculator_with_tolerance.py
```python
import logging
import math


def setup_logger(file_name: str) -> logging.Logger:
    """
    Setup a logger with INFO level and output to a file.
    If the file does not exist, it will be created.

    :param file_name: The name of the file to write the log to.

    :return: The logger object.
    """
    logger = logging.getLogger(__name__)                                # Initiation of logger
    logger.setLevel(logging.INFO)                                       # Set level to INFO. Warning and higher will be ignored

    try:
        logging.basicConfig(filename=file_name, level=logging.INFO)     # Basic setup for logger
    except FileNotFoundError:
        print(f"File {file_name} does not exist.")

        try:
            open(file_name, 'w').close()                                # create empty file if it does not exist
        except PermissionError:
            raise PermissionError(f"Cannot create non-existing file {file_name}. Permission denied.")
        else:
            logging.basicConfig(filename=backup_file, level=logging.INFO)
    
    except PermissionError:
        raise PermissionError(f"Cannot open {file_name}. Permission denied.")
    except Exception as err:
        print(f"Unexpected error: {err=}, {type(err)=}")
        raise err

    return logger


def greet() -> None:
    """Print instructions for using the calculator."""
    print("Choose one of the following operators: ", end='')
    for option in available_operators:
        print(f'"{option}"', end='  ')
    print("\nThe prompt should be in the format: <operator> <number> <number> ... <number> <tolerance>")
    print()


def prompt_parser(prompt: str) -> tuple[str, list[str], float]:
    """
    Parse a string prompt into operator, numbers, and tolerance.

    :param str prompt: The string prompt to be parsed.

    :returns: A tuple containing the operator, numbers, and tolerance.
    """
    if not prompt:
        raise ValueError("Prompt is empty")
    
    operator, *numbers, tolerance = prompt.split(' ')   # Possible mismatch leading to error

    if not tolerance or len(numbers) < 1:
        raise ValueError("Invalid prompt format")

    try:
        tolerance = float(tolerance)                    # Safely converting from string to float
    except ValueError:
        raise ValueError("Tolerance is not in numeric format")

    return operator, numbers, tolerance


def decoration_logger(calc: callable) -> callable:
    """
    Returns a wrapper function that logs the input and output of the decorated function and returns the result.
    
    :param callable func: The function to be decorated.

    :returns: The wrapper function.
    """
    def wrapper(prompt: str) -> float | int | None:
        """
        Logs the input operation and numbers, executes the decorated function, and logs the result.

        :param str operator: The operation to be performed.
        :param numbers: A tuple of list of string numbers to be used in the operation.
        :param float tolerance: The tolerance level for the operation.

        :returns: The result of the operation as a float.
        """
        logger = setup_logger(file_name='second_calc_log.log')              # Setting up logger
        operator, *numbers, tolerance = prompt_parser(prompt)               # Parsing the input
        result = calc(operator, *numbers, tolerance=tolerance)
        logger.info(f"{operator},{",".join(numbers[0])},{tolerance}={result}") # logging data
        return result
    return wrapper


def convert_precision(tolerance: float) -> int:
    """
    Converts a given tolerance to an appropriate number of decimal places.

    The returned value is the number of decimal places to round to, based on the given tolerance.

    :param float tolerance: The tolerance to convert.

    :returns: The appropriate number of decimal places to round to, as an integer.
    """
    precision = 0

    if tolerance <= 0: # protection for zero and negative cases
        print("Warning: Tolerance must be greater than zero. It will be set to absolute value.")
        tolerance = abs(tolerance)

    while tolerance < 1:
        tolerance *= 10
        precision += 1

    return precision


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


def q3_q1(*args) -> float | int:
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


available_operators = {     # Dictionary of available operators and corresponding functions
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
def calculate(action: str, *args, tolerance: float = 1e-6) -> float | int | None:
    """
    Perform a calculation based on the specified action and arguments, with a given precision tolerance.

    This function supports various operations provided in the `available_operators` dictionary, such as
    addition, subtraction, multiplication, division, exponentiation, modulus, mean, variance, standard deviation,
    median, and the difference between the third and first quartiles (Q3 - Q1).

    :param str action: Specifies the operation to perform.
    :param args: A variable representing numbers to be used in the operation.
    :param float tolerance: The precision tolerance for the result, default is 1e-6.5

    :returns: The result of the operation rounded according to the specified tolerance.
    """
    try:
        numbers = list(map(float, *args))            # Safely converting from string to float
    except ValueError:
        raise ValueError("At least one of the numbers is not numeric")
    
    if action not in available_operators:
        print(f"Unknown operator: {action}")
        return None                                 # If invalid operator is entered

    return round(                                   # Calling functions from dictionary and round the result to the specified precision
            available_operators[action](*numbers), \
            convert_precision(tolerance) if tolerance < 1 else None
        )


if __name__ == "__main__":
    greet()

    try:
        prompt = input("Enter an expression: ")
    except KeyboardInterrupt:                # If user presses Ctrl+C
        print("Input cancelled.")
        exit()
    
    print(calculate(prompt))
```
Анализ:
В программе учтены возможные исключения и их обработка:
Ошибки, связанные с файлами:
  Отсутствие файла (FileNotFoundError).
  Недостаток прав доступа (PermissionError).
Ошибки ввода:
  Некорректный формат строки: недостаток аргументов, не числовые значения.
  Недопустимый оператор.


Задание 2. Модульное тестирование с unittest

test_batch_calc_unittest.py
```python
import unittest
from unittest.mock import mock_open, patch
from BatchCalculatorContextManager import calc_with_manager, BatchCalculatorContextManager, generate_input_from_file
from calc.calculator_with_tolerance import calculate, convert_precision
import os
import statistics


class TestBatchCalculatorContextManager(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Mock data (aka default data for tests)
        self.valid_file_content =  "INFO__main__:+,1,2,3,0.001\n \
                                    INFO__main__:-,5,2,1\n \
                                    INFO__main__:*,5,3,0.01\n \
                                    INFO__main__:/,5,2,0.01\n \
                                    INFO__main__:^,4,2,1\n \
                                    INFO__main__:%,13,3,0.01\n \
                                    INFO__main__:mean,1,2,3,4,10.00001\n \
                                    INFO__main__:var,5,3,7,10,4,7,2,0.00001\n \
                                    INFO__main__:dev,5,3,7,10,4,7,2,0.00001\n \
                                    INFO__main__:med,5,3,7,10,4,7,2,0.00001\n \
                                    INFO__main__:q3-q1,5,3,7,10,4,7,2,0.00001"


        self.parsed_file_content = [
            "+ 1 2 3 0.001",
            "- 5 2 1", 
            "* 5 3 0.01", 
            "/ 5 2 0.01",
            "^ 4 2 1",
            "% 13 3 0.01",
            "mean 1 2 3 4 10.00001",
            "var 5 3 7 10 4 7 2 0.00001",
            "dev 5 3 7 10 4 7 2 0.00001",
            "med 5 3 7 10 4 7 2 0.00001",
            "q3-q1 5 3 7 10 4 7 2 0.00001"
        ]

        self.invalid_file_content = "INFO__main__:invalid_format"


    def test_context_manager_valid_file(self):
        # Setting up mocks. Here mocks are patches, which sets the return values of the functions
        with patch('builtins.open', mock_open(read_data=self.valid_file_content)), \
             patch('os.path.exists', return_value=True), \
             patch('os.access', return_value=True):
            with BatchCalculatorContextManager('test.log') as file:
                self.assertEqual(file.read(), self.valid_file_content)


    def test_context_manager_file_not_found(self):
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                with BatchCalculatorContextManager('non_existent.log'):
                    pass


    def test_context_manager_permission_error(self):
        with patch('os.path.exists', return_value=True), \
             patch('os.access', return_value=False):
            with self.assertRaises(PermissionError):
                with BatchCalculatorContextManager('test.log'):
                    pass

    
    def test_convert_precision_valid(self):
        self.assertEqual(convert_precision(0.001), 3)
        self.assertEqual(convert_precision(0.000001), 6)
        self.assertEqual(convert_precision(0.0000001), 7)

    
    def test_convert_precision_invalid(self):
        with self.assertRaises(ValueError):
            calculate("+ 1 2 a")


    def test_generate_input_from_file_valid_data(self):
        mock_file = self.valid_file_content.splitlines()
        results = list(generate_input_from_file(mock_file))
        self.assertEqual(results, self.parsed_file_content)


    def test_generate_input_from_file_invalid_data(self):
        mock_file = self.invalid_file_content.splitlines()
        results = list(generate_input_from_file(mock_file))
        self.assertEqual(results, [])
    
    
    def test_setup_logger_file_not_found(self):
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                calc_with_manager('non_existent.log')
    

    def test_setup_logger_permission_error(self):
        with patch('os.path.exists', return_value=True), \
             patch('os.access', return_value=False):
            with self.assertRaises(PermissionError):
                calc_with_manager('test.log')

    
    def test_empty_prompt(self):
        with self.assertRaises(ValueError):
            calculate("")


    def test_calculate_valid_operations(self):
        self.assertEqual(calculate("+ 1 2 3 0.001"), 6)
        self.assertEqual(calculate("- 5 2 1"), 3)
        self.assertEqual(calculate("* 5 3 0.01"), 15)
        self.assertEqual(calculate("/ 5 2 0.01"), 2.5)
        self.assertEqual(calculate("^ 4 2 1"), 16)
        self.assertEqual(calculate("% 13 3 0.01"), 1)
        self.assertEqual(calculate("mean 1 2 3 4 0.01"), statistics.mean([1, 2, 3, 4]))
        self.assertEqual(calculate("var 9 1 5 0.00001"), statistics.variance([9, 1, 5]))
        self.assertEqual(calculate("dev 1 4 2 4 0.01"), statistics.stdev([1, 4, 2, 4]))
        self.assertEqual(calculate("med 1 2 3 4 0.01"), statistics.median([1, 2, 3, 4]))
        self.assertEqual(calculate("q3_q1 4 7 15 18 36 40 41 0.01"), statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[2] - statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[0])


    def test_calculate_invalid_operator(self):
        self.assertIsNone(calculate("unknown 1 2 3 0.01"))


    def test_calculate_invalid_numbers(self):
        with self.assertRaises(ValueError):
            calculate("+ 1 a 3 0.01")


if __name__ == '__main__':
    unittest.main()
```

Результат работы программы:
```
.Unknown operator: unknown
....Execution time: 0.000166 seconds
........
----------------------------------------------------------------------
Ran 13 tests in 0.006s

OK
```

Анализ:
Этот тестовый модуль на Python проверяет функциональность класса BatchCalculatorContextManager и калькулятора. Тесты написаны с использованием библиотеки unittest и имитируют работу с файлами, используя unittest.mock. Также импользуется patch для имитации поведения функций чтения и проверки файлов, создаёт гибкость в тестировании и исключает зависимость от реальной файловой системы.

Задание 3. Тестирование с помощью pytest

test_batch_calc_pytest.py
```python
import pytest
from unittest.mock import mock_open, patch
from BatchCalculatorContextManager import calc_with_manager, BatchCalculatorContextManager, generate_input_from_file
from calc.calculator_with_tolerance import calculate, convert_precision
import statistics


# Mock data for tests
@pytest.fixture
def mock_valid_file_content():
    return """INFO__main__:+,1,2,3,0.001
INFO__main__:-,5,2,1
INFO__main__:*,5,3,0.01
INFO__main__:/,5,2,0.01
INFO__main__:^,4,2,1
INFO__main__:%,13,3,0.01
INFO__main__:mean,1,2,3,4,10.00001
INFO__main__:var,5,3,7,10,4,7,2,0.00001
INFO__main__:dev,5,3,7,10,4,7,2,0.00001
INFO__main__:med,5,3,7,10,4,7,2,0.00001
INFO__main__:q3-q1,5,3,7,10,4,7,2,0.00001"""


@pytest.fixture
def parsed_file_content():
    return [
        "+ 1 2 3 0.001",
        "- 5 2 1", 
        "* 5 3 0.01", 
        "/ 5 2 0.01",
        "^ 4 2 1",
        "% 13 3 0.01",
        "mean 1 2 3 4 10.00001",
        "var 5 3 7 10 4 7 2 0.00001",
        "dev 5 3 7 10 4 7 2 0.00001",
        "med 5 3 7 10 4 7 2 0.00001",
        "q3-q1 5 3 7 10 4 7 2 0.00001"
    ]


@pytest.fixture
def mock_invalid_file_content():
    return "INFO__main__:invalid_format"


def test_context_manager_valid_file(mock_valid_file_content):
    with patch('builtins.open', mock_open(read_data=mock_valid_file_content)), \
         patch('os.path.exists', return_value=True), \
         patch('os.access', return_value=True):
        with BatchCalculatorContextManager('test.log') as file:
            assert file.read() == mock_valid_file_content


def test_context_manager_file_not_found():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            with BatchCalculatorContextManager('non_existent.log'):
                pass


def test_context_manager_permission_error():
    with patch('os.path.exists', return_value=True), \
         patch('os.access', return_value=False):
        with pytest.raises(PermissionError):
            with BatchCalculatorContextManager('test.log'):
                pass


def test_generate_input_from_file_valid_data(mock_valid_file_content, parsed_file_content):
    mock_file = mock_valid_file_content.splitlines()
    results = list(generate_input_from_file(mock_file))
    assert results == parsed_file_content


def test_generate_input_from_file_invalid_data(mock_invalid_file_content):
    mock_file = mock_invalid_file_content.splitlines()
    results = list(generate_input_from_file(mock_file))
    assert results == []


def test_setup_logger_file_not_found():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            calc_with_manager('non_existent.log')


def test_setup_logger_permission_error():
    with patch('os.path.exists', return_value=True), \
         patch('os.access', return_value=False):
        with pytest.raises(PermissionError):
            calc_with_manager('test.log')


def test_empty_prompt():
    with pytest.raises(ValueError):
        calculate("")


def test_convert_precision_valid():
    assert convert_precision(0.001) == 3
    assert convert_precision(0.000001) == 6
    assert convert_precision(0.0000001) == 7


def test_convert_precision_invalid():
    with pytest.raises(ValueError):
        calculate("+ 1 2 a")


@pytest.mark.parametrize("expression, expected", [
    ("+ 1 2 3 0.001", 6),
    ("- 5 2 1", 3),
    ("* 5 3 0.01", 15),
    ("/ 5 2 0.01", 2.5),
    ("^ 4 2 1", 16),
    ("% 13 3 0.01", 1),
    ("mean 1 2 3 4 0.01", statistics.mean([1, 2, 3, 4])),
    ("var 9 1 5 0.00001", statistics.variance([9, 1, 5])),
    ("dev 1 4 2 4 0.01", statistics.stdev([1, 4, 2, 4])),
    ("med 1 2 3 4 0.01", statistics.median([1, 2, 3, 4])),
    ("q3_q1 4 7 15 18 36 40 41 0.01", 
     statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[2] - 
     statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[0])
])

def test_calculate_valid_operations(expression, expected):
    assert calculate(expression) == expected


def test_calculate_invalid_operator():
    assert calculate("unknown 1 2 3 0.01") is None


def test_calculate_invalid_numbers():
    with pytest.raises(ValueError):
        calculate("+ 1 a 3 0.01")


if __name__ == '__main__':
    pytest.main()
```

Результат работы программы:
```
============================= test session starts =============================
platform win32 -- Python 3.12.5, pytest-8.3.3, pluggy-1.5.0
rootdir: C:\Users\Anton\Programms\Python\Herzen git repo\Python-Herzen-Course\ЛР-6
collected 23 items

test_batch_calc_pytest.py .......................                        [100%]

============================= 23 passed in 0.07s ==============================
```

Анализ:
Этот тестовый модуль для pytest проверяет те же аспекты работы класса BatchCalculatorContextManager и функций вычисления, что и версия на unittest, но с использованием возможностей pytest, таких как фикстуры, параметризация и более простой синтаксис тестов.
Подход с фикстурами в pytest упрощает поддержку тестов, отделяя данные от логики тестов, повышая читаемость.
