class FibonacciList:
    def __init__(self, input_list: list[int]):
        self.input_list = input_list
        self.__check_input()
        self.__index = 0
        self._fib_set = self._generate_fib_up_to(limit=max(self.input_list))

    def __iter__(self):
        return self

    def __next__(self):
        """Returns the next Fibonacci number from the input list."""
        while True:
            try:
                value: int = self.input_list[self.__index]
            except IndexError:
                raise StopIteration

            self.__index += 1

            if value in self._fib_set:
                return value
    
    def _generate_fib_up_to(self, limit: int = 0) -> set[int]:
        """Generates a set of Fibonacci numbers up to the given limit."""
        fib_set: set = {0, 1}
        a, b = 0, 1
        while a <= limit:
            a, b = b, a + b
            fib_set.add(a)
        
        return fib_set

    def __check_input(self):
        """
        Checks that the input is a list and contains only integers.

        Raises a TypeError if the input is incorrect.
        """
        if not isinstance(self.input_list, list):
            raise TypeError("Input must be a list")

        if not all(isinstance(value, int) for value in self.input_list):
            raise TypeError("Non-integer value is not allowed in list")


class FibonacciListGetItem:
    def __init__(self, input_list: list[int]):
        self.input_list = input_list
        self.__check_input()
        self._fib_set = self._generate_fib_up_to(max(input_list))
        self._filtered = [n for n in input_list if n in self._fib_set]

    def _generate_fib_up_to(self, limit: int = 0) -> set[int]:
        """Generates a set of Fibonacci numbers up to the given limit."""
        fib_set: set = {0, 1}
        a, b = 0, 1
        while a <= limit:
            a, b = b, a + b
            fib_set.add(a)
        
        return fib_set

    def __getitem__(self, index: int) -> int:
        """Provide index access to filtered Fibonacci numbers."""
        return self._filtered[index]

    def __len__(self) -> int:
        """Allow len() to be used on the object."""
        return len(self._filtered)
    
    def __check_input(self):
        """
        Checks that the input is a list and contains only integers.

        Raises a TypeError if the input is incorrect.
        """
        if not isinstance(self.input_list, list):
            raise TypeError("Input must be a list")

        if not all(isinstance(value, int) for value in self.input_list):
            raise TypeError("Non-integer value is not allowed in list")


def run_fib_next():
    print("FibonacciList class")
    nums = [1, 2, 3, 4, 5, 8, 13, 21, 34, 55, 100, 144, 200]
    fib_list = FibonacciList(nums)
    print(list(fib_list))


def run_fib_getitem():
    print("FibonacciListGetItem class")
    nums = [1, 2, 3, 4, 5, 8, 13, 21, 34, 55, 100, 144, 200]
    fib_filter = FibonacciListGetItem(nums)
    print(list(fib_filter))
    print(fib_filter[3])



if __name__ == "__main__":
    run_fib_next()
    run_fib_getitem()
    