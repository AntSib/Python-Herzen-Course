import pytest
from coroutine_fib import gen_fib


class TestFibonacciCoroutine:
    @pytest.mark.parametrize(
        "n, expected",
        [
            (3, [0, 1, 1]),
            (5, [0, 1, 1, 2, 3]),
            (9, [0, 1, 1, 2, 3, 5, 8, 13, 21])
        ]
    )
    def test_sequence(self, n, expected):
        """Test the Fibonacci generator.

        This test checks that the Fibonacci generator returns the correct Fibonacci sequence
        for a given input 'n'. The test uses various test cases with expected results.

        :param n: The length of the Fibonacci sequence to generate.
        :param expected: The expected Fibonacci sequence of length 'n'.
        """
        gen = gen_fib()
        assert gen.send(n) == expected

    def test_sequence_0(self):
        """Test that the Fibonacci generator returns an empty list when given input 0."""
        gen = gen_fib()
        assert gen.send(0) == []

    def test_negative_input(self):
        """Test that the Fibonacci generator raises a TypeError when given a negative input."""
        gen = gen_fib()
        with pytest.raises(TypeError):
            gen.send(-1)
            
    def test_float_as_input(self):
        """Test that the Fibonacci generator raises a TypeError when given a float input."""
        gen = gen_fib()
        with pytest.raises(TypeError):
            gen.send(2.5)
    
    def test_string_as_input(self):
        """Test that the Fibonacci generator raises a TypeError when given a string input."""
        gen = gen_fib()
        with pytest.raises(TypeError):
            gen.send('2')
    
    def test_none_as_input(self):
        """Test that the Fibonacci generator raises a TypeError when given None as input."""
        gen = gen_fib()
        with pytest.raises(TypeError):
            gen.send()


if __name__ == "__main__":
    pytest.main()
    