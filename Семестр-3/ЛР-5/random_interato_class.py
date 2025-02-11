import random


class RandomNumberGenerator(object):
    def __init__(self: object, lst: list) -> None:
        """
        Constructor.

        Args:
            lst: List with parameters, where:
                lst[0] - quantity of random numbers to generate
                lst[1] - min value of random numbers
                lst[2] - max value of random numbers

        Raises:
            ValueError: If quantity is less than 0.
        """
        self.index = 0
        # count, min, max = lst[0], lst[1], lst[2]
        self.count, self.min, self.max = lst
        
        if self.count <= 0:
            raise ValueError("Quantity must be greater than 0")
        if self.max <= self.min:
            raise ValueError("Max must be greater than min")
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """
        Generate next random number.

        Returns:
            int: Random number.

        Raises:
            StopIteration: If all numbers were generated.
        """
        if self.index < self.count:
            self.index += 1
            return random.randint(self.min, self.max)
        else:
            raise StopIteration


def main():
    class_gen = RandomNumberGenerator([5, 0, 3])

    print("RandomNumberGenerator class")
    for num in class_gen:
        print(num)


if __name__ == "__main__":
    main()
