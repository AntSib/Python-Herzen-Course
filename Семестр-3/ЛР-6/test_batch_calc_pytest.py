import pytest
from unittest.mock import mock_open, patch
from BatchCalculatorContextManager import calc_with_manager, BatchCalculatorContextManager, generate_input_from_file
from calc.calculator_with_tolerance import calculate, convert_precision
import statistics


# Mock data for tests
@pytest.fixture
def mock_valid_file_content():
    return """INFO__main__:+,1,2,3,0.001
INFO__main__:-,5,2,1
INFO__main__:*,5,3,0.01
INFO__main__:/,5,2,0.01
INFO__main__:^,4,2,1
INFO__main__:%,13,3,0.01
INFO__main__:mean,1,2,3,4,10.00001
INFO__main__:var,5,3,7,10,4,7,2,0.00001
INFO__main__:dev,5,3,7,10,4,7,2,0.00001
INFO__main__:med,5,3,7,10,4,7,2,0.00001
INFO__main__:q3-q1,5,3,7,10,4,7,2,0.00001"""


@pytest.fixture
def parsed_file_content():
    return [
        "+ 1 2 3 0.001",
        "- 5 2 1", 
        "* 5 3 0.01", 
        "/ 5 2 0.01",
        "^ 4 2 1",
        "% 13 3 0.01",
        "mean 1 2 3 4 10.00001",
        "var 5 3 7 10 4 7 2 0.00001",
        "dev 5 3 7 10 4 7 2 0.00001",
        "med 5 3 7 10 4 7 2 0.00001",
        "q3-q1 5 3 7 10 4 7 2 0.00001"
    ]


@pytest.fixture
def mock_invalid_file_content():
    return "INFO__main__:invalid_format"


def test_context_manager_valid_file(mock_valid_file_content):
    with patch('builtins.open', mock_open(read_data=mock_valid_file_content)), \
         patch('os.path.exists', return_value=True), \
         patch('os.access', return_value=True):
        with BatchCalculatorContextManager('test.log') as file:
            assert file.read() == mock_valid_file_content


def test_context_manager_file_not_found():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            with BatchCalculatorContextManager('non_existent.log'):
                pass


def test_context_manager_permission_error():
    with patch('os.path.exists', return_value=True), \
         patch('os.access', return_value=False):
        with pytest.raises(PermissionError):
            with BatchCalculatorContextManager('test.log'):
                pass


def test_generate_input_from_file_valid_data(mock_valid_file_content, parsed_file_content):
    mock_file = mock_valid_file_content.splitlines()
    results = list(generate_input_from_file(mock_file))
    assert results == parsed_file_content


def test_generate_input_from_file_invalid_data(mock_invalid_file_content):
    mock_file = mock_invalid_file_content.splitlines()
    results = list(generate_input_from_file(mock_file))
    assert results == []


def test_setup_logger_file_not_found():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            calc_with_manager('non_existent.log')


def test_setup_logger_permission_error():
    with patch('os.path.exists', return_value=True), \
         patch('os.access', return_value=False):
        with pytest.raises(PermissionError):
            calc_with_manager('test.log')


def test_empty_prompt():
    with pytest.raises(ValueError):
        calculate("")


def test_convert_precision_valid():
    assert convert_precision(0.001) == 3
    assert convert_precision(0.000001) == 6
    assert convert_precision(0.0000001) == 7


def test_convert_precision_invalid():
    with pytest.raises(ValueError):
        calculate("+ 1 2 a")


@pytest.mark.parametrize("expression, expected", [
    ("+ 1 2 3 0.001", 6),
    ("- 5 2 1", 3),
    ("* 5 3 0.01", 15),
    ("/ 5 2 0.01", 2.5),
    ("^ 4 2 1", 16),
    ("% 13 3 0.01", 1),
    ("mean 1 2 3 4 0.01", statistics.mean([1, 2, 3, 4])),
    ("var 9 1 5 0.00001", statistics.variance([9, 1, 5])),
    ("dev 1 4 2 4 0.01", statistics.stdev([1, 4, 2, 4])),
    ("med 1 2 3 4 0.01", statistics.median([1, 2, 3, 4])),
    ("q3_q1 4 7 15 18 36 40 41 0.01", 
     statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[2] - 
     statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[0])
])

def test_calculate_valid_operations(expression, expected):
    assert calculate(expression) == expected


def test_calculate_invalid_operator():
    assert calculate("unknown 1 2 3 0.01") is None


def test_calculate_invalid_numbers():
    with pytest.raises(ValueError):
        calculate("+ 1 a 3 0.01")


if __name__ == '__main__':
    pytest.main()
