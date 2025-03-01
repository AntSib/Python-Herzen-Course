class BinTreeException(Exception):
    def __init__(self, message: str = ""):
        """
        Initializes the BinTreeException with an optional message.

        :param message: The exception message. Defaults to an empty string.
        """
        self.message: str = message
    
    def __str__(self):
        """
        Returns the exception message.

        :return: The exception message.
        """
        return self.message

class InvalidTreeParameters(BinTreeException):
    def __init__(self):
        """
        Initializes the InvalidTreeParameters exception with a default message for invalid tree parameters.
        """
        super().__init__("Invalid tree parameters. ")

class InvalidTreeHeight(InvalidTreeParameters):
    def __init__(self, height: int):
        """
        Initializes the InvalidTreeHeight exception with a message describing the invalid height.

        :param height: The invalid height.
        """
        super().__init__()
        self.message += f"Height must be an integer, not {type(height)}. "

class InvalidTreeRoot(InvalidTreeParameters):
    def __init__(self, root: int):
        """
        Initializes the InvalidTreeRoot exception with a message describing the invalid root.

        :param root: The invalid root.
        """
        super().__init__()
        self.message += f"Root must be an integer, not {type(root)}. "

class InvalidTreeFunctions(InvalidTreeParameters):
    def __init__(self, left_function, right_function):
        """
        Initializes the InvalidTreeFunctions exception with a message describing the invalid functions.

        :param left_function: The left leaf/branch function.
        :param right_function: The right leaf/branch function.
        """
        super().__init__()
        if not callable(left_function):
            self.message += f"Left leaf function cannot be called: left_function = {left_function} "
        if not callable(right_function):
            self.message += f"Right leaf function cannot be called: right_function = {right_function} "
