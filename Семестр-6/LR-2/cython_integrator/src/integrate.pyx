def integrate(
    func,
    double start,
    double end,
    int n_iter=100,
):
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
    cdef long double step = (end - start) / n_iter
    cdef long double cumulative = 0.0
    cdef int i

    for i in range(n_iter):
        cumulative += func(start + (i + 1) * step)

    cumulative += (func(start) + func(end)) / 2.0
    cumulative *= step

    return cumulative
