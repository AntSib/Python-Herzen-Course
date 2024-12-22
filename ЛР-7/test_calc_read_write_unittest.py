
    # Проверка с помощью создания контекста функций по считыванию настроек
    # калькулятора и запись в файл результатов выполнения операций

    # Используя параметризация тестов написать тесты функции two_sum

    # Используя гипотезы с помощью hypothesis протестировать вычисление факториала

import unittest
from calc import calculator_with_tolerance
import os
import tempfile


class TestCalcReadWrite(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """
        SetupClass creates 3 temporary files used for testing. One contains
        valid configuration parameters, one contains invalid configuration
        parameters, and one is empty to test writing to the output file.
        """
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_config_file:
            temp_config_file.write("tolerance = 0.000001\noutput = output.log\n")
        self.config_file = temp_config_file

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_incorrect_config_file:
            temp_incorrect_config_file.write("dance = abc\nblah = 15\n")
        self.incorrect_config_file = temp_incorrect_config_file

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_output_file:
            temp_output_file.write("")
        self.output_file = temp_output_file

    def test_calc_load_params_valid(self):
        """
        Test that the load_params function correctly loads valid parameters
        from a configuration file.
        """
        params = calculator_with_tolerance.load_params(self.config_file.name)
        self.assertEqual(params, {'tolerance': 1e-6, 'output': 'output.log'})

    def test_calc_load_params_invalid(self):
        """
        Test that the load_params function correctly uses default parameters when
        the given configuration file does not exist.
        """
        params = calculator_with_tolerance.load_params('invalid_file')
        self.assertEqual(params, {'tolerance': 1e-6, 'output': 'default_calc.log'})

    def test_calc_load_params_corrupted(self):
        """
        Test that the load_params function correctly uses default parameters when
        the given configuration file contains invalid parameters.
        """
        params = calculator_with_tolerance.load_params(self.incorrect_config_file.name)
        self.assertEqual(params, {'tolerance': 1e-6, 'output': 'default_calc.log'})
        
    def test_calc_write_result(self):
        """
        Test that the calculate function writes the correct result to the output file.
        """
        with open(self.output_file.name, 'r') as file:
            logger = calculator_with_tolerance.setup_logger(self.output_file.name)
            calculator_with_tolerance.calculate("+ 1 2 3 4 1")
            logger_output = file.readlines()[-1].split(':')[-1]
            self.assertIn("+,1,2,3,4,1.0=10\n", logger_output)
            

    @classmethod
    def tearDownClass(self):
        """
        Remove temporary files created by setUpClass and delete the references
        to them. This is necessary to avoid leaving temporary files on the
        filesystem after the tests have finished running.
        """
        os.remove(self.config_file.name)
        os.remove(self.incorrect_config_file.name)
        del self.config_file
        del self.incorrect_config_file
        del self.output_file


if __name__ == '__main__':
    unittest.main()
