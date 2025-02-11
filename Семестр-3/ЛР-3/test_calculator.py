import pytest
import statistics           # Using functionality of statistics module for testing
from calculator_with_tolerance import convert_precision, awailable_operators
from calculator_with_tolerance import summary, mean, variance, std_deviation, median, q3_q1, calculate


tolerance_default = 1e-6    # Default tolerance for tests

class TestCalculate:
    def test_summary(self):
        """Test that summary correctly handles addition."""
        assert awailable_operators["+"](*[1, 2, 3]) == 1 + 2 + 3
    
    def test_subtraction(self):
        """Test that function correctly handles subtraction."""
        assert awailable_operators["-"](3, 2) == 3 - 2
    
    def test_multiplication(self):
        """Test that function correctly handles multiplication."""
        assert awailable_operators["*"](3, 2) == 3 * 2
    
    def test_division(self):
        """Test that function correctly handles division."""
        assert awailable_operators["/"](6, 2) == 6 / 2
    
    def test_power(self):
        """Test that function correctly handles exponentiation."""
        assert awailable_operators["^"](2, 3) == 2 ** 3
    
    def test_modulus(self):
        """Test that function correctly handles modulus."""
        assert awailable_operators["%"](4, 2) == 4 % 2
    
    def test_mean(self):
        """Test that mean function works correctly."""
        stat_mean = statistics.mean([4, 7, 15, 18, 36, 40, 41])
        assert mean(*[4, 7, 15, 18, 36, 40, 41]) == stat_mean

    def test_variance(self):
        """Test that variance function works correctly."""
        stat_variance = statistics.variance([4, 7, 15, 18, 36, 40, 41])
        assert variance(*[4, 7, 15, 18, 36, 40, 41]) == stat_variance
    
    def test_std_dev(self):
        """Test that standart deviation function works correctly."""
        stat_std_dev = statistics.stdev([4, 7, 15, 18, 36, 40, 41])
        assert std_deviation(*[4, 7, 15, 18, 36, 40, 41]) == stat_std_dev
    
    def test_median(self):
        """Test that median function works correctly."""
        stat_median = statistics.median([4, 7, 15, 18, 36, 40, 41])
        assert median(*[4, 7, 15, 18, 36, 40, 41]) == stat_median
    
    def test_q3_q1(self):
        """Test that function correctly calculates difference between third and first quartiles (Q3 - Q1)."""
        stat_q3_q1 = statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[2] - statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[0]
        assert q3_q1(*[4, 7, 15, 18, 36, 40, 41]) == stat_q3_q1

    def test_calc_type(self):
        """Test that calculate returns a float."""
        assert type(calculate("var", [4, 7, 15, 18, 36, 40, 41], tolerance=tolerance_default)) == float

    def test_convert_precision(self):
        """Test that convert_precision correctly converts the precision to an appropriate number of decimal places."""
        assert convert_precision(1.0) == 0
        assert convert_precision(0.1) == 1
        assert convert_precision(0.01) == 2
        assert convert_precision(0.001) == 3
    
    def test_convert_precision_type(self):
        """Test that convert_precision returns an int."""
        assert type(convert_precision(0.001)) == int


if __name__ == "__main__":
    pytest.main()