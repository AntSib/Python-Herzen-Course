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
