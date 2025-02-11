def fib_generator(n: int) -> int:
    """
    Generate the first n Fibonacci numbers.

    Args:
        n: The number of Fibonacci numbers to generate.

    Yields:
        int: The next Fibonacci number.
    """
    a, b = 0, 1

    for i in range(n):
        yield a
        a, b = b, a + b


def plus_ten(nums_iter: object) -> int:
    """
    Given an iterator of numbers, yield each number plus 10.

    Args:
        nums_iter: An iterator of numbers.

    Yields:
        int: The next number plus 10.
    """
    for num in nums_iter:
        yield num + 10


def main():
    n = 7
    fib_numbers = fib_generator(n)
    fib_plus_ten = plus_ten(fib_generator(n))

    print("Fibonacci generator")
    for num in fib_numbers:
        print(num)

    print("Fibonacci numbers plus 10")
    for num in fib_plus_ten:
        print(num)


if __name__ == "__main__":
    main()
