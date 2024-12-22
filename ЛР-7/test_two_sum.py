import pytest
from functions.two_sum_fast_f import two_sum_fast

@pytest.mark.parametrize(
    "lst, target, expected",
    [
        ([1, 2, 3, 4, 5, 6], 7, (0, 5)),
        ([1, 3, 5, 7, 9], 12, (1, 4)),
        ([2, 4, 6, 8], 10, (0, 3)),
        ([1, 2, 3, 4, 5, 6], 20, None),
        ([1, 1, 1, 6], 7, (0, 3)),
        ([1], 2, None),
        ([], 5, None),
    ]
)
def test_two_sum_fast(lst, target, expected):
    assert two_sum_fast(lst, target) == expected


if __name__ == "__main__":
    pytest.main()
