def factorial(n: int) -> int:
    """
    Calculates the factorial of a given positive integer n.

    :param n: an integer
    :return: the factorial of n
    :raises ValueError: if n is negative or a float
    """
    if n < 0 or isinstance(n, float):
        raise ValueError("Factorial is not defined for negative numbers or floats")
    result = 1
    for i in range(n, 1, -1):
        result *= i
    return result
