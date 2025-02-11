lst = [i for i in range(1, 16)] # example
target = 7


def two_sum_fast(lst: list, target: int) -> tuple:
    """
    Return a tuple of two indices whose corresponding elements in the given list add up to the target.

    :param lst: a list of integers
    :param target: an integer
    :return: a tuple of two indices or None if no matching pair is found
    """
    for item in lst:                # O(n)
        if target - item in lst:
            a = lst.index(item)
            b = lst.index(target - item)

            if b > a:               # Check if b is after a, this also prevents duplicates
                return (a, b)

    print("No matching pair found")
    return None


if __name__ == "__main__":
    res = two_sum_fast(lst, target)
    print(res)
