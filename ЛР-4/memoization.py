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
