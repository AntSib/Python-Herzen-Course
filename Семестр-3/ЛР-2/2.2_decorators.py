import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)


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
        
        logger.info("operand1: " + num1 + " operand2: " + num2 + " operation: " + oper)
        # print("input log: ", num1, oper, num2)
        
        res = func(prompt)

        logger.info("result: " + str(res))
        # print("return log: ", res)
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
