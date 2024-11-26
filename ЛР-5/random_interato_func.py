import random


def random_numbers_generator(params: list) -> int:
    """
    Generate random numbers in range [min_val, max_val] quantity times.

    Args:
        params: List with parameters, where:
            params[0] - quantity of random numbers to generate
            params[1] - min value of random numbers
            params[2] - max value of random numbers

    Yields:
        int: Random number in range [min_val, max_val]

    Raises:
        ValueError: If quantity is less than or equal to 0.
        ValueError: If max is less than or equal to min.
    """
    quantity, min_val, max_val = params

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    if max_val <= min_val:
        raise ValueError("Max must be greater than min")

    for i in range(quantity):
        yield random.randint(min_val, max_val)


def main():
    func_gen = random_numbers_generator([5, 0, 3])
    
    print("random_numbers_generator function")
    for num in func_gen:
        print(num)


if __name__ == "__main__":
    main()
