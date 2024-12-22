import pytest
from hypothesis import given, strategies as st
from functions.simple_factorial import factorial

@given(st.integers(min_value=-20, max_value=-1))
def test_factorial_negative(n):
    """
    Test the factorial function for negative integer inputs.

    This test checks that the factorial function raises a ValueError when given
    a negative integer input. The test uses inputs ranging from -20 to -1.

    Args:
        n: A negative integer for which the factorial is computed.
    """
    with pytest.raises(ValueError):
        factorial(n)

@given(st.integers(min_value=0, max_value=20))
def test_factorial_properties(n):
    """
    Test properties of the factorial function for non-negative integers.

    This test checks that the factorial of a non-negative integer is always 
    greater than or equal to 1. Additionally, for integers greater than 2, 
    the factorial is greater than the integer itself. The test uses inputs 
    ranging from 0 to 20.
    
    Args:
        n: A non-negative integer for which the factorial is computed.
    """

    result = factorial(n)
    assert result >= 1
    if n > 2:
        assert result > n

@given(st.integers(min_value=0, max_value=100))
def test_factorial_correctness(n):
    """
    Test the correctness of the factorial function for non-negative integers.

    This test uses a recursive implementation of the factorial function to compare
    the results of the factorial function with a known correct implementation. The
    test uses inputs ranging from 0 to 100.

    Args:
        n: A non-negative integer for which the factorial is computed.
    """
    def recursive_factorial(m):
        return 1 if m == 0 else m * recursive_factorial(m - 1)
    
    assert factorial(n) == recursive_factorial(n)


@given(st.floats(min_value=-20, max_value=20))
def test_factorial_float(n):
    """
    Test the factorial function for floating point inputs.
    
    This test checks that the factorial function raises a ValueError when given a
    floating point input. The test uses inputs ranging from -20 to 20.

    Args:
        n: A floating point number for which the factorial is computed.
    """
    with pytest.raises(ValueError):
        factorial(n)


if __name__ == "__main__":
    pytest.main()
