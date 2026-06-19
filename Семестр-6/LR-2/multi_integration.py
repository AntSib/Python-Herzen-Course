import concurrent.futures as c_futures
import math
import warnings
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial


def integrate(
    func: callable,
    start: float,
    end: float,
    *,
    n_iter: int = 100,
    small_value_warnining: float = 1e-20,
    **kwargs,  # noqa: ARG001
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

    Examples:
        >>> import math
        >>> abs(integrate(math.sin, 0, math.pi, n_iter=100_000) - 2) < 1e-4
        True

        >>> f = lambda x: x**2
        >>> abs(integrate(f, 0, 1, n_iter=100_000) - 1/3) < 1e-4
        True

    """
    step = (end - start) / n_iter

    if step < small_value_warnining:
        warnings.warn(
            f"Step is too small: {step}. Computation may be unstable.",
            RuntimeWarning,
            stacklevel=2,
        )

    # Trapezoid method
    cumulative = sum(func(start + (i + 1) * step) for i in range(n_iter))
    cumulative += (func(start) + func(end)) / 2
    cumulative *= step

    return cumulative


# multithreading
def multithreading_integrate(
    func: callable,
    start: float,
    end: float,
    *,
    n_iter: int = 1_000,
    n_jobs: int = 4,
    integrator: callable = integrate,
) -> float:
    """
    Numerically integrates a given function from start to end over n_iter iterations, using multithreading.

    Args:
        func: callable - The function to integrate.
        start: float - The start of the integration interval.
        end: float - The end of the integration interval.
        n_iter: int - The number of iterations to use when computing the integral.
            Defaults to 1_000.
        n_jobs: int - The number of threads to use for multithreading.
            Defaults to 4.

    Returns:
        float - The computed integral value.

    """
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        interval = (end - start) / n_jobs

        threads = {
            executor.submit(
                integrator,
                func,
                start + interval * step,
                start + interval * (step + 1),
                n_iter=n_iter // n_jobs,
            ): step
            for step in range(n_jobs)
        }

        return sum([future.result() for future in c_futures.as_completed(threads)])


def multithreading_spawn_integrate(
    func: callable,
    start: float,
    end: float,
    *,
    n_iter: int = 1_000,
    n_jobs: int = 4,
    integrator: callable = integrate,
) -> float:
    """
    Numerically integrates a given function from start to end over n_iter iterations, using multithreading and thread spawning.

    Args:
        func: callable - The function to integrate.
        start: float - The start of the integration interval.
        end: float - The end of the integration interval.
        n_iter: int - The number of iterations to use when computing the integral.
            Defaults to 1_000.
        n_jobs: int - The number of threads to use for multithreading.
            Defaults to 4.

    Returns:
        float - The computed integral value.

    """
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        interval = (end - start) / n_jobs

        spawn = partial(
            executor.submit,
            integrator,
            func,
            n_iter=n_iter // n_jobs,
        )

        threads = [
            spawn(start + interval * step, start + interval * (step + 1))
            for step in range(n_jobs)
        ]

        return sum([future.result() for future in c_futures.as_completed(threads)])


# multiprocessing
def multiprocessing_integrate(
    func: callable,
    start: float,
    end: float,
    *,
    n_iter: int = 1_000,
    n_jobs: int = 4,
    integrator: callable = integrate,
) -> float:
    """
    Numerically integrates a given function from start to end over n_iter iterations, using multiprocessing.

    Args:
        func: callable - The function to integrate.
        start: float - The start of the integration interval.
        end: float - The end of the integration interval.
        n_iter: int - The number of iterations to use when computing the integral.
            Defaults to 1_000.
        n_jobs: int - The number of processes to use for multiprocessing.
            Defaults to 4.

    Returns:
        float - The computed integral value.

    """
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        interval = (end - start) / n_jobs

        processes = {
            executor.submit(
                # executed function
                integrator,
                # arg and kwargs
                func,
                start + interval * step,
                start + interval * (step + 1),
                n_iter=n_iter // n_jobs,
            ): step
            for step in range(n_jobs)
        }

        return sum([process.result() for process in c_futures.as_completed(processes)])


def multiprocessing_spawn_integrate(
    func: callable,
    start: float,
    end: float,
    *,
    n_iter: int = 1_000,
    n_jobs: int = 4,
    integrator: callable = integrate,
) -> float:
    """
    Numerically integrates a given function from start to end over n_iter iterations, using multiprocessing with process spawning.

    Args:
        func: callable - The function to integrate.
        start: float - The start of the integration interval.
        end: float - The end of the integration interval.
        n_iter: int - The number of iterations to use when computing the integral.
            Defaults to 1_000.
        n_jobs: int - The number of processes to use for multiprocessing.
            Defaults to 4.

    Returns:
        float - The computed integral value.

    """
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        interval = (end - start) / n_jobs

        spawn = partial(
            executor.submit,
            integrator,
            func,
            n_iter=n_iter // n_jobs,
        )

        processes = [
            spawn(start + interval * step, start + interval * (step + 1))
            for step in range(n_jobs)
        ]

        return sum([process.result() for process in c_futures.as_completed(processes)])


def main() -> None:
    func = math.sin
    start = 0
    end = math.pi
    n_iter = 10_000

    print(integrate(func, start, end, n_iter=n_iter))
    mlt_thrd_integrate = multithreading_integrate(func, start, end, n_iter=n_iter)
    print(f"mlt_thrd_integrate: {mlt_thrd_integrate}")
    mlt_thrd_spawn_integrate = multithreading_spawn_integrate(
        func,
        start,
        end,
        n_iter=n_iter,
    )
    print(f"mlt_thrd_integrate: {mlt_thrd_spawn_integrate}")
    mlt_prc_integrate = multiprocessing_integrate(func, start, end, n_iter=n_iter)
    print(f"mlt_prc_integrate: {mlt_prc_integrate}")
    mlt_prc_spawn_integrate = multiprocessing_spawn_integrate(
        func,
        start,
        end,
        n_iter=n_iter,
    )
    print(f"mlt_prc_spawn_integrate: {mlt_prc_spawn_integrate}")


def run_doctests():
    import doctest

    doctest.testmod(verbose=True)


if __name__ == "__main__":
    main()
    # run_doctests()
