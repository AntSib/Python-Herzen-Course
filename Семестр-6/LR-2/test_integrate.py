import math

import pytest
from line_profiler import profile
from multi_integration import integrate


def profile_integrate(func, start, end, *args, **kwargs):
    """Decorator to profile a function."""
    return profile(integrate)(func, start, end, *args, **kwargs)


def test_known_integral_polynomial():
    """Correctness check: f [0, 1] x² dx = 1/3."""
    result = integrate(lambda x: x**2, 0, 1, n_iter=200_000)
    assert result == pytest.approx(1 / 3, abs=1e-5)  # noqa: S101


def test_known_itegral_inv_sqrt():
    """Correctness check: f [0, 1] 1/sqrt(x) dx = 2."""
    result = integrate(lambda x: 1 / math.sqrt(x), 0.5, 2, n_iter=200_000)
    assert result == pytest.approx(math.sqrt(2), abs=1e-5)  # noqa: S101


def test_known_integral_trigonometric():
    """Correctness check: f [0, pi] sin(x) dx = 2."""
    result = integrate(math.sin, 0, math.pi, n_iter=200_000)
    assert result == pytest.approx(2.0, abs=1e-5)  # noqa: S101


def test_stability_with_different_iterations():
    """
    Check stability with different high n_iter.

    Uses fixed seed for reproducibility.
    """
    import random  # noqa: PLC0415

    random.seed(42)

    def f(x):
        return x**2 + 5 * x - 15

    for _ in range(10):
        n1 = random.randint(500_000, 1_000_000)
        n2 = random.randint(500_000, 1_000_000)

        res1 = integrate(f, 0, 1, n_iter=n1)
        res2 = integrate(f, 0, 1, n_iter=n2)

        assert res1 == pytest.approx(res2, abs=1e-5)  # noqa: S101


def test_warning_on_small_step():
    """Check that a warning is raised for a too small step."""

    def f(x):
        return x

    with pytest.warns(RuntimeWarning):
        integrate(
            f,
            0,
            1e-10,
            n_iter=10**6,
            small_value_warnining=1e-15,
        )


if __name__ == "__main__":
    pytest.main()

    # pytest test_integrate.py
    func = math.sin
    start = 0
    end = math.pi
    n_iter = 10_000

    profile_integrate(func, start, end, n_iter=n_iter)
