import pytest
from hypothesis import given, strategies as st
from functions.simple_factorial import factorial

@given(st.integers(min_value=-20, max_value=-1))
def test_factorial_negative(n):
    with pytest.raises(ValueError):
        factorial(n)

@given(st.integers(min_value=0, max_value=20))
def test_factorial_properties(n):
    result = factorial(n)
    assert result >= 1
    if n > 2:
        assert result > n

@given(st.integers(min_value=0, max_value=100))
def test_factorial_correctness(n):
    def recursive_factorial(m):
        return 1 if m == 0 else m * recursive_factorial(m - 1)
    
    assert factorial(n) == recursive_factorial(n)


@given(st.floats(min_value=-20, max_value=20))
def test_factorial_float(n):
    with pytest.raises(ValueError):
        factorial(n)


if __name__ == "__main__":
    pytest.main()
