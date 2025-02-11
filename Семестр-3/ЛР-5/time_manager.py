import time


class Timer:
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.execution_time = self.end_time - self.start_time       # time in seconds
        print(f"Execution time: {self.execution_time:.6f} seconds") # format to 6 decimal places


def fib_gen(n: int) -> int:
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


def main():
    limit = 100000     # 100.000 fibonacci numbers

    with Timer() as t:
        fib_numbers = list(fib_gen(limit))

    print(f"{fib_numbers[:10]}...")

if __name__ == "__main__":
    main()
    


