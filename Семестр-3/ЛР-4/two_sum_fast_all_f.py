lst = [i for i in range(1, 101)]
target = 10


def two_sum_hashed_all(lst: list, target: int) -> list:
    """
    Return a list of tuples, each containing two indices whose corresponding elements
    in the given list add up to the target.

    :param lst: a list of integers
    :param target: an integer
    :return: a list of tuples of two indices or None if no matching pairs are found
    """
    found = []

    for item in lst:                    # O(n)
        if target - item in lst:
            a = lst.index(item)
            b = lst.index(target - item)

            if b > a:                   # Check if b is after a, this also prevents duplicates
                found.append((a, b))    # Saving indices

    if found:
        return found

    print("No matching pair found")
    return None


if __name__ == "__main__":
    res = two_sum_hashed_all(lst, target)
    print(res)
