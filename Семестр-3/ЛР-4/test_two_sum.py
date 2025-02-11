import pytest
from timeit import timeit
from two_sum_f import two_sum
from two_sum_fast_f import two_sum_fast
from two_sum_fast_all_f import two_sum_hashed_all


class TestTwoSums:
    def test_two_sum(self):
        """
        Test that two_sum function returns (0, 6)
        for elements in the list [1, 2, ..., 9] that add up to 8.
        """
        assert two_sum([i for i in range(1, 10)], 8) == (0, 6)
    
    def test_two_sum2(self):
        """
        Test that two_sum function returns (0, 4)
        for elements in the list [2, 3, ..., 9] that add up to 8.
        """
        assert two_sum([i for i in range(2, 10)], 8) == (0, 4)

    def test_two_sum3(self):
        """
        Test that two_sum function returns (1, 4)
        for elements in the list [1, 2, 3, 4, 6, 8, 9] that add up to 8.
        """
        assert two_sum([1, 2, 3, 4, 6, 8, 9], 8) == (1, 4)
    
    def test_two_sum_too_small(self):
        """
        Test that two_sum function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is smaller than minimum of the list.
        """
        assert two_sum([i for i in range(1, 10)], 0) == None
    
    def test_two_sum_too_big(self):
        """
        Test that two_sum function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is bigger than maximum of the list.
        """
        assert two_sum([i for i in range(1, 10)], 18) == None


class TestTwoSumsFast:
    def test_two_sum_fast(self):
        """
        Test that two_sum_fast function returns (0, 6)
        for elements in the list [1, 2, ..., 9] that add up to 8.
        """
        assert two_sum_fast([i for i in range(1, 10)], 8) == (0, 6)
    
    def test_two_sum_fast2(self):
        """
        Test that two_sum_fast function returns (0, 4)
        for elements in the list [2, 3, ..., 9] that add up to 8.
        """
        assert two_sum_fast([i for i in range(2, 10)], 8) == (0, 4)

    def test_two_sum_fast3(self):
        """
        Test that two_sum_fast function returns (1, 4)
        for elements in the list [1, 2, 3, 4, 6, 8, 9] that add up to 8.
        """
        assert two_sum_fast([1, 2, 3, 4, 6, 8, 9], 8) == (1, 4)
    
    def test_two_sum_fast_too_small(self):
        """
        Test that two_sum_fast function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is smaller than minimum of the list.
        """
        assert two_sum_fast([i for i in range(1, 10)], 0) == None
    
    def test_two_sum_fast_too_big(self):
        """
        Test that two_sum_fast function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is bigger than maximum of the list.
        """
        assert two_sum_fast([i for i in range(1, 10)], 18) == None


class TestTwoSumsFastAll:
    def test_two_sum_fast_all(self):
        """
        Test that two_sum_hashed_all function returns [(0, 5), (1, 4)]
        for elements in the list [1, 2, 3, 4, 6, 7, 8, 9] that add up to 8.
        """
        assert two_sum_hashed_all([1, 2, 3, 4, 6, 7, 8, 9], 8) == [(0, 5), (1, 4)]

    def test_two_sum_fast_all2(self):
        """
        Test that two_sum_hashed_all function returns [(0, 3)]
        for elements in the list [2, 3, 4, 6, 7, 8, 9] that add up to 8.
        """
        assert two_sum_hashed_all([2, 3, 4, 6, 7, 8, 9], 8) == [(0, 3)]

    def test_two_sum_fast_all3(self):
        """
        Test that two_sum_hashed_all function returns [(0, 8), (1, 7), (2, 6), (3, 5)]
        for elements in the list [1, 2, ..., 15] that add up to 10.
        """
        assert two_sum_hashed_all([i for i in range(1, 16)], 10) == [(0, 8), (1, 7), (2, 6), (3, 5)]

    def test_two_sum_fast_all_big_list(self):
        """
        Test that two_sum_hashed_all function returns expected list of tuples
        for a list of 100,000 elements and a target of 50.
        """
        target = 50
        test_list = [(i, target - i - 2) for i in range(target//2 - 1)]
        assert two_sum_hashed_all([i for i in range(1, 100001)], 50) == test_list
    
    def test_two_sum_fast_all_too_small(self):
        """
        Test that two_sum_hashed_all function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is smaller than the minimum of the list.
        """
        assert two_sum_hashed_all([i for i in range(1, 10)], 0) == None

    def test_two_sum_fast_all_too_big(self):
        """
        Test that two_sum_hashed_all function returns None
        for elements in the list [1, 2, ..., 9] 
        when the target is bigger than the maximum of the list.
        """
        assert two_sum_hashed_all([i for i in range(1, 10)], 18) == None


class TestTwoSumsTime:
    # Constants
    big_list = [i for i in range(1, 10001)]
    target = 50
    n_tests = 100
    to_millis = 10*6

    def time_two_sum(self):
        """
        Measure the execution time of the two_sum function
        for a list of 100,000 elements and a target of 666.
        The test is run 1000 times and the result is printed
        in milliseconds.
        """
        exec_time = timeit("two_sum(TestTwoSumsTime.big_list, TestTwoSumsTime.target)", globals=globals(), number=self.n_tests)
        print(f"Execution time of two_sum is: {exec_time * self.to_millis} milliseconds")
    
    def time_two_sum_fast(self):
        """
        Measure the execution time of the two_sum_fast function
        for a list of 100,000 elements and a target of 666.
        The test is run 1000 times and the result is printed
        in milliseconds.
        """
        exec_time = timeit("two_sum_fast(TestTwoSumsTime.big_list, TestTwoSumsTime.target)", globals=globals(), number=self.n_tests)
        print(f"Execution time of two_sum_fast is: {exec_time * self.to_millis} milliseconds")

    def time_two_sum_fast_all(self):
        """
        Measure the execution time of the two_sum_hashed_all function
        for a list of 100,000 elements and a target of 666.
        The test is run 1000 times and the result is printed
        in milliseconds.
        """
        exec_time = timeit("two_sum_hashed_all(TestTwoSumsTime.big_list, TestTwoSumsTime.target)", globals=globals(), number=self.n_tests)
        print(f"Execution time of two_sum_hashed_all is: {exec_time * self.to_millis} milliseconds")
        


if __name__ == "__main__":
    pytest.main()

    TestTwoSumsTime().time_two_sum()
    TestTwoSumsTime().time_two_sum_fast()
    TestTwoSumsTime().time_two_sum_fast_all()
