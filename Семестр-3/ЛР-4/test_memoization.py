import pytest
from timeit import timeit
from memoization import fib_test, fib_memo_sleeve, fib_memo, fib_cached


class TestMemoization:
    @pytest.mark.parametrize(
        "n, expected",
        [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (7, 13),
            (8, 21),
            (11, 89),
            (12, 144)
        ]
    )
    def test_fib_memo_sleeve(self, n, expected):
        """
        Test the fib_memo_sleeve function for computing Fibonacci numbers.

        This test checks that the fib_memo_sleeve function returns the correct Fibonacci number
        for a given input 'n'. The test uses various test cases with 
        expected results.

        :param n: Index of the Fibonacci number to compute.
        :param expected: The expected Fibonacci number at index 'n'.
        """
        assert fib_memo_sleeve(n) == expected
    
    @pytest.mark.parametrize(
        "n, expected",
        [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (7, 13),
            (8, 21),
            (11, 89),
            (12, 144)
        ]
    )
    def test_fib_memo(self, n, expected):
        """
        Test the fib_memo function for computing Fibonacci numbers.

        This test checks that the fib_memo function returns the correct Fibonacci number
        for a given input 'n'. The test uses various test cases with 
        expected results.

        :param n: Index of the Fibonacci number to compute.
        :param expected: The expected Fibonacci number at index 'n'.
        """
        assert fib_memo(n) == expected
    
    @pytest.mark.parametrize(
        "n, expected",
        [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (7, 13),
            (8, 21),
            (11, 89),
            (12, 144)
        ]
    )
    def test_fib_cached(self, n, expected):
        """
        Test the fib_cached function for computing Fibonacci numbers.

        This test checks that the fib_cached function returns the correct Fibonacci number
        for a given input 'n'. The test uses various test cases with 
        expected results.

        :param n: Index of the Fibonacci number to compute.
        :param expected: The expected Fibonacci number at index 'n'.
        """
        assert fib_cached(n) == expected


class TestFuncTime:
    to_millis = 10*6
    n = 30
    n_tests = 100

    def test_fib_test(self):
        """
        Measure the execution time of the fib_test function for 50th Fibonacci number. 
        The test is run 100 of times and the result is printed in milliseconds.
        """
        exec_time = timeit("fib_test(TestFuncTime.n)", globals=globals(), number=self.n_tests)
        print(f"Execution time of fib_test is: {exec_time * self.to_millis} milliseconds")
    
    def test_fib_memo_sleeve(self):
        """
        Measure the execution time of the fib_memo_sleeve function for 50th Fibonacci number. 
        The test is run 100 of times and the result is printed in milliseconds.
        """
        exec_time = timeit("fib_memo_sleeve(TestFuncTime.n)", globals=globals(), number=self.n_tests)
        print(f"Execution time of fib_memo_sleeve is: {exec_time * self.to_millis} milliseconds")
    
    def test_fib_memo(self):
        """
        Measure the execution time of the fib_memo function for 50th Fibonacci number. 
        The test is run 100 of times and the result is printed in milliseconds.
        """
        exec_time = timeit("fib_memo(TestFuncTime.n)", globals=globals(), number=self.n_tests)
        print(f"Execution time of fib_memo is: {exec_time * self.to_millis} milliseconds")
    
    def test_fib_cached(self):
        """
        Measure the execution time of the fib_cached function for 50th Fibonacci number. 
        The test is run 100 times and the result is printed in milliseconds.
        """
        exec_time = timeit("fib_cached(TestFuncTime.n)", globals=globals(), number=self.n_tests)
        print(f"Execution time of fib_cached is: {exec_time * self.to_millis} milliseconds")


if __name__ == "__main__":
    pytest.main()

    TestFuncTime().test_fib_test()
    TestFuncTime().test_fib_memo_sleeve()
    TestFuncTime().test_fib_memo()
    TestFuncTime().test_fib_cached()
