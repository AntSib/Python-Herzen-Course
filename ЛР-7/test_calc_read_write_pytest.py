import pytest
from calc import calculator_with_tolerance
import os
import tempfile

@pytest.fixture(scope="module")
def config_file():
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_config_file:
        temp_config_file.write("tolerance = 0.000001\noutput = output.log\n")
    yield temp_config_file.name
    os.remove(temp_config_file.name)

@pytest.fixture(scope="module")
def incorrect_config_file():
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_incorrect_config_file:
        temp_incorrect_config_file.write("dance = abc\nblah = 15\n")
    yield temp_incorrect_config_file.name
    os.remove(temp_incorrect_config_file.name)


def test_calc_load_params_valid(config_file):
    params = calculator_with_tolerance.load_params(config_file)
    assert params == {'tolerance': 1e-6, 'output': 'output.log'}

def test_calc_load_params_invalid():
    params = calculator_with_tolerance.load_params('invalid_file')
    assert params == {'tolerance': 1e-6, 'output': 'default_calc.log'}

def test_calc_load_params_corrupted(incorrect_config_file):
    params = calculator_with_tolerance.load_params(incorrect_config_file)
    assert params == {'tolerance': 1e-6, 'output': 'default_calc.log'}

def test_calc_write_result(caplog):    # caplog is required, because temporary files are buggy
    with caplog.at_level("INFO"):
        calculator_with_tolerance.calculate("+ 1 2 3 4 1")
    assert "+,1,2,3,4,1.0=10" in caplog.text

if __name__ == "__main__":
    pytest.main()
