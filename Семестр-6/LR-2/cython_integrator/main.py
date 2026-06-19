from integrate import integrate


def f(x):
    return x**2 + 5 * x - 15


print(integrate(f, 0.0, 1.0))
