lst = [i for i in range(1, 16)]
target = 7


def two_sum(lst: list, target: int) -> tuple:
    """
    Return a tuple of two indices whose corresponding elements in the given list add up to the target.

    :param lst: a list of integers
    :param target: an integer
    :return: a tuple of two indices
    """
    for i in range(len(lst)):   # O(n^2)
        for j in range(i + 1, len(lst)):
            if lst[i] + lst[j] == target:
                return (i, j)
    
    print("No matching pair found")
    return None


if __name__ == "__main__":
    res = two_sum(lst, target)
    print(res)
