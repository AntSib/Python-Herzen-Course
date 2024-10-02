def calculate(prompt: str) -> int:
    """
    Perform a calculation based on a string prompt.

    Keyword arguments:
    prompt -- The prompt to use for the calculation.
    
    The prompt should be in the format "number operator number", e.g. "1 + 2".
    The supported operators are "+", "-", "*", "/", "^", and "%".

    Returns the result of the calculation as an integer.

    If the input prompt is not valid, prints an error message and returns None.
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


def test_calc_add():
    """Test that calculate correctly handles addition."""
    assert calculate("1 + 2") == 3


def test_calc_subtr():
    """Test that calculate correctly handles subtraction."""
    assert calculate("1 - 2") == -1


def test_calc_mult():
    """Test that calculate correctly handles multiplication."""
    assert calculate("2 * 3") == 6

def test_calc_div():
    """Test that calculate correctly handles division."""
    assert calculate("6 / 3") == 2


def test_calc_pow():
    """Test that calculate correctly handles exponentiation."""
    assert calculate("2 ^ 3") == 8


def test_calc_mod():
    """Test that calculate correctly handles modulus."""
    assert calculate("4 % 2") == 0


def main() -> None:
    test_calc_add()
    test_calc_subtr()
    test_calc_mult()
    test_calc_div()
    test_calc_pow()
    test_calc_mod()

    print(calculate(input("Enter an expression: ")))


if __name__ == "__main__":
    main()
