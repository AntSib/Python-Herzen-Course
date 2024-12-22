import pytest
from calc import calculator_with_tolerance
import os
import tempfile

@pytest.fixture(scope="module")
def config_file():
    """Provides a temporary file name with a valid configuration of calculator
    settings. The file is automatically deleted when the test is finished.

    Yields:
        str: Path to the temporary configuration file.
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_config_file:
        temp_config_file.write("tolerance = 0.000001\noutput = output.log\n")
    yield temp_config_file.name
    os.remove(temp_config_file.name)


@pytest.fixture(scope="module")
def incorrect_config_file():
    """Provides a temporary file name with an invalid configuration of calculator
    settings. The file is automatically deleted when the test is finished.

    Yields:
        str: Path to the temporary configuration file.
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_incorrect_config_file:
        temp_incorrect_config_file.write("dance = abc\nblah = 15\n")
    yield temp_incorrect_config_file.name
    os.remove(temp_incorrect_config_file.name)


def test_calc_load_params_valid(config_file):
    """Test that the load_params function correctly loads valid parameters from a configuration file."""
    params = calculator_with_tolerance.load_params(config_file)
    assert params == {'tolerance': 1e-6, 'output': 'output.log'}


def test_calc_load_params_invalid():
    """
    Test that the load_params function correctly uses default parameters when
    the given configuration file does not exist.
    """
    params = calculator_with_tolerance.load_params('invalid_file')
    assert params == {'tolerance': 1e-6, 'output': 'default_calc.log'}


def test_calc_load_params_corrupted(incorrect_config_file):
    """
    Test that the load_params function correctly uses default parameters when
    the given configuration file contains invalid parameters.
    """
    params = calculator_with_tolerance.load_params(incorrect_config_file)
    assert params == {'tolerance': 1e-6, 'output': 'default_calc.log'}


def test_calc_write_result(caplog):    # here caplog is required, because output to files is buggy with pytest
    """
    Test that the calculate function writes the correct result to the output file.
    """
    with caplog.at_level("INFO"):
        calculator_with_tolerance.calculate("+ 1 2 3 4 1")
    assert "+,1,2,3,4,1.0=10" in caplog.text


if __name__ == "__main__":
    pytest.main()
