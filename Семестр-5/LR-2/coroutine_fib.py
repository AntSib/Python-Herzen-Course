import functools


def coroutine(func: callable) -> callable:
    """
    A decorator that primes a generator for use.

    Args:
        func (callable): A generator function.

    Returns:
        callable: A generator function that has been primed.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        next(generator)
        return generator
    return wrapper


@coroutine
def gen_fib() -> list[int]:
    """
    A generator that yields a Fibonacci sequence of a given length.

    The generator takes an integer as input and yields a list 
    of integers representing the Fibonacci sequence of that length.

    Args:
        n (int): The length of the Fibonacci sequence.

    Yields:
        list[int]: A list of integers representing the Fibonacci sequence of length n.
    """
    n = yield
    while True:
        if not isinstance(n, int) or n < 0:
            raise TypeError("Non-integer or negative value is not allowed")

        a, b = 0, 1
        fib_seq = []
        for _ in range(n):
            fib_seq.append(a)
            a, b = b, a + b

        n = yield fib_seq



if __name__ == "__main__":
    gen = gen_fib()
    print(gen.send(3))
    print(gen.send(8))
    print(gen.send(5))