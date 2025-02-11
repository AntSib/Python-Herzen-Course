def outerfunc(arg1: str, arg2: str):
    """
    Return a function that takes two arguments and returns a dictionary with those two arguments.

    The returned function is a closure that captures the arguments to outerfunc and uses them as the
    arguments to innerfunc.

    :param str arg1: The first argument to capture.
    :param str arg2: The second argument to capture.

    :returns: A function that takes two arguments and returns a dictionary.
    """
    def innerfunc(arg3: str, arg4: str) -> dict:
        """
        Return a dictionary with the two arguments.

        :param str arg3: The first argument.
        :param str arg4: The second argument.

        :returns: A dictionary with the arguments.
        """
        return {"arg3": arg3, "arg4": arg4}

    return innerfunc(arg1, arg2)


if __name__ == "__main__":
    print(outerfunc("Sam", "25"))
