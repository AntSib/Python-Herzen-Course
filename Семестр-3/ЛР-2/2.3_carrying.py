def radioactive_decay(half_life: float) -> callable:
    """
    Returns a function that computes the remaining amount of a radioactive element.

    The returned function takes two arguments, the initial amount of the element and the time passed,
    and returns the remaining amount of the element after the given time.

    The half-life of the element is given as an argument to the outer function.

    :param float half_life: The half-life of the element in seconds.

    :returns: A function that takes two arguments, the initial amount of the element and the time passed,
              and returns the remaining amount of the element after the given time.
    """
    def decay(N_0: int, time: int) -> float:
        """
        Compute the remaining amount of a radioactive element after a given time.

        :param int N_0: The initial amount of the element.

        :param int time: The time passed in seconds.

        :returns: The remaining amount of the element after the given time.
        """
        return N_0 * 0.5 ** (time / half_life)
    return decay


if __name__ == "__main__":
    h_to_sec = 60 * 60
    d_to_sec = h_to_sec * 24
    y_to_sec = d_to_sec * 365

    h_time = 100 * h_to_sec
    N_0 = 1000

    rad_elements = {
        "At": 7.2 * h_to_sec, 
        "Tc": 61 * d_to_sec, 
        "Bk": 1380 * y_to_sec
    }

    decay_functions = {
        isotope: radioactive_decay(half_life) for isotope, half_life in rad_elements.items()
    }

    print("The remaining amount of radioactive elements:")
    for isotope, decay_function in decay_functions.items():
        remaining_amount = decay_function(N_0, h_time)
        print(f"{isotope}: {remaining_amount}")
