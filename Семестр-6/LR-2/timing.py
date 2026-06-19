from timeit import timeit

from multi_integration import (
    integrate,
    multiprocessing_integrate,
    multiprocessing_spawn_integrate,
    multithreading_integrate,
    multithreading_spawn_integrate,
)


def f(x):
    return x**2 + 5 * x - 15


if __name__ == "__main__":
    to_millis = 10**3

    functions_to_time: list = [
        integrate,
        multithreading_integrate,
        multithreading_spawn_integrate,
        multiprocessing_integrate,
        multiprocessing_spawn_integrate,
    ]

    start = 0

    # func = math.sin
    # stop = math.pi
    func = f
    stop = 4

    timeit_runs = 100

    exec_times = []

    for function_to_time in functions_to_time:
        # for n_iter in range(1_000, 5_001, 1_000):
        # for n_jobs in range(2, 7, 2):
        n_iter = 1000
        print(
            f"Running {function_to_time.__name__} with n_iter={n_iter}",
        )
        exec_times.append(
            (
                str(function_to_time.__name__),  # function name
                timeit(  # execution time
                    f"{function_to_time.__name__}(func, start, stop, n_iter=n_iter, integrator=integrate)",
                    globals=globals(),
                    number=timeit_runs,
                ),
                n_iter,  # steps for integer compiting
                # n_jobs,
            ),
        )

    # print(exec_times)

    for data in exec_times:
        print(
            f"Function {data[0]},\t executed in {data[1] * to_millis:.5f} ms",
        )
