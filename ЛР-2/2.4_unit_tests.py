import unittest


class TestCalculate(unittest.TestCase):
    def test_calc_add(self):
        """Test that calculate correctly handles addition."""
        self.assertEqual(calculate("1 + 2"), 3)

    def test_calc_subtr(self):
        """Test that calculate correctly handles subtraction."""
        self.assertEqual(calculate("1 - 2"), -1)

    def test_calc_mult(self):
        """Test that calculate correctly handles multiplication."""
        self.assertEqual(calculate("2 * 3"), 6)

    def test_calc_div(self):
        """Test that calculate correctly handles division."""
        self.assertEqual(calculate("6 / 2"), 3)

    def test_calc_pow(self):
        """Test that calculate correctly handles exponentiation."""
        self.assertEqual(calculate("2 ^ 3"), 8)
        
    def test_calc_mod(self):
        """Test that calculate correctly handles modulus."""
        self.assertEqual(calculate("7 % 3"), 1)

    def test_invalid_input(self):
        """Test that calculate raises a ValueError when given invalid input."""
        with self.assertRaises(ValueError):
            calculate("1 +")


def calculate(prompt: str) -> int:
    """
    Perform a calculation based on a string prompt.

    The prompt should be in the format "number operator number", e.g. "1 + 2".
    The supported operators are "+", "-", "*", "/", "^", and "%".

    If the input prompt is not valid, prints an error message and returns None.

    Keyword arguments:
    :param str prompt: The prompt to use for the calculation.
    
    :returns: The result of the calculation as an integer.
    """
    num1, oper, num2 = prompt.split(' ')
    
    if num1.isdigit() and num2.isdigit() and not oper.isdigit():
        num1 = int(num1)
        num2 = int(num2)

        if oper == "+": return num1 + num2
        if oper == "-": return num1 - num2
        if oper == "*": return num1 * num2
        if oper == "/": return num1 / num2
        if oper == "^": return num1 ** num2
        if oper == "%": return num1 % num2
    else:
        print("Invalid input")


if __name__ == "__main__":
    unittest.main()
