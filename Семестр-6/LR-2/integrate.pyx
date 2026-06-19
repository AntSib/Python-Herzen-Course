import cython


@cython.cfunc
def integrate(
    func: callable,
    start: cython.float,
    end: cython.float,
    *,
    n_iter: cython.int = 100,
    small_value_warnining: cython.double = 1e-20,
) -> float:
    """
    Numerically integrates a given function from start to end over n_iter iterations.

    Args:
        func: callable - The function to integrate.
        start: float - The start of the integration interval.
        end: float - The end of the integration interval.
        n_iter: int - The number of iterations to use when computing the integral.
            Defaults to 100.
        small_value_warnining: float - The minimum recommended step size to use when computing the integral.
            Defaults to 1e-20.

    Returns:
        float - The computed integral value.

    """
    step: cython.double = (end - start) / n_iter

    # cumulative: cython.longdouble = sum(func(start + (i + 1) * step) for i in range(n_iter))
    cumulative: cython.longdouble = 0
    for i in range(n_iter):
        cumulative += func(start + (i + 1) * step)

    cumulative += (func(start) + func(end)) / 2
    cumulative *= step

    return cumulative
