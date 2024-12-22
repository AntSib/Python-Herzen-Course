import pytest
from functions.two_sum_fast_f import two_sum_fast

@pytest.mark.parametrize(
    "lst, target, expected",
    [   
        ([i for i in range(-10, 5)], -2, (4, 14)),
        ([i for i in range(1, 7)], 7, (0, 5)),
        ([i for i in range(1, 10, 2)], 12, (1, 4)),
        ([i for i in range(1, 10, 2)], 10, (0, 4)),
        ([-2, -1, 0, 1, 3, 4], 0, (1, 3)),
        ([-10**9, -2, 0, 3, 10**9], 0, (0, 4)),
        ([i for i in range(1, 7)], 20, None),
        ([1, 1, 1, 6], 7, (0, 3)),
        ([1], 2, None),
        ([], 5, None),
    ]
)
def test_two_sum_fast(lst, target, expected):
    """
    Test that two_sum_fast function returns expected tuple of two indices
    whose corresponding elements in the given list add up to the target.
    """
    assert two_sum_fast(lst, target) == expected


if __name__ == "__main__":
    pytest.main()
