import unittest
from unittest.mock import mock_open, patch
from BatchCalculatorContextManager import calc_with_manager, BatchCalculatorContextManager, generate_input_from_file
from calc.calculator_with_tolerance import calculate, convert_precision
import os
import statistics


class TestBatchCalculatorContextManager(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Mock data (aka default data for tests)
        self.valid_file_content =  "INFO__main__:+,1,2,3,0.001\n \
                                    INFO__main__:-,5,2,1\n \
                                    INFO__main__:*,5,3,0.01\n \
                                    INFO__main__:/,5,2,0.01\n \
                                    INFO__main__:^,4,2,1\n \
                                    INFO__main__:%,13,3,0.01\n \
                                    INFO__main__:mean,1,2,3,4,10.00001\n \
                                    INFO__main__:var,5,3,7,10,4,7,2,0.00001\n \
                                    INFO__main__:dev,5,3,7,10,4,7,2,0.00001\n \
                                    INFO__main__:med,5,3,7,10,4,7,2,0.00001\n \
                                    INFO__main__:q3-q1,5,3,7,10,4,7,2,0.00001"


        self.parsed_file_content = [
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

        self.invalid_file_content = "INFO__main__:invalid_format"


    def test_context_manager_valid_file(self):
        # Setting up mocks. Here mocks are patches, which sets the return values of the functions
        with patch('builtins.open', mock_open(read_data=self.valid_file_content)), \
             patch('os.path.exists', return_value=True), \
             patch('os.access', return_value=True):
            with BatchCalculatorContextManager('test.log') as file:
                self.assertEqual(file.read(), self.valid_file_content)


    def test_context_manager_file_not_found(self):
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                with BatchCalculatorContextManager('non_existent.log'):
                    pass


    def test_context_manager_permission_error(self):
        with patch('os.path.exists', return_value=True), \
             patch('os.access', return_value=False):
            with self.assertRaises(PermissionError):
                with BatchCalculatorContextManager('test.log'):
                    pass

    
    def test_convert_precision_valid(self):
        self.assertEqual(convert_precision(0.001), 3)
        self.assertEqual(convert_precision(0.000001), 6)
        self.assertEqual(convert_precision(0.0000001), 7)

    
    def test_convert_precision_invalid(self):
        with self.assertRaises(ValueError):
            calculate("+ 1 2 a")


    def test_generate_input_from_file_valid_data(self):
        mock_file = self.valid_file_content.splitlines()
        results = list(generate_input_from_file(mock_file))
        self.assertEqual(results, self.parsed_file_content)


    def test_generate_input_from_file_invalid_data(self):
        mock_file = self.invalid_file_content.splitlines()
        results = list(generate_input_from_file(mock_file))
        self.assertEqual(results, [])
    
    
    def test_setup_logger_file_not_found(self):
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                calc_with_manager('non_existent.log')
    

    def test_setup_logger_permission_error(self):
        with patch('os.path.exists', return_value=True), \
             patch('os.access', return_value=False):
            with self.assertRaises(PermissionError):
                calc_with_manager('test.log')

    
    def test_empty_prompt(self):
        with self.assertRaises(ValueError):
            calculate("")


    def test_calculate_valid_operations(self):
        self.assertEqual(calculate("+ 1 2 3 0.001"), 6)
        self.assertEqual(calculate("- 5 2 1"), 3)
        self.assertEqual(calculate("* 5 3 0.01"), 15)
        self.assertEqual(calculate("/ 5 2 0.01"), 2.5)
        self.assertEqual(calculate("^ 4 2 1"), 16)
        self.assertEqual(calculate("% 13 3 0.01"), 1)
        self.assertEqual(calculate("mean 1 2 3 4 0.01"), statistics.mean([1, 2, 3, 4]))
        self.assertEqual(calculate("var 9 1 5 0.00001"), statistics.variance([9, 1, 5]))
        self.assertEqual(calculate("dev 1 4 2 4 0.01"), statistics.stdev([1, 4, 2, 4]))
        self.assertEqual(calculate("med 1 2 3 4 0.01"), statistics.median([1, 2, 3, 4]))
        self.assertEqual(calculate("q3_q1 4 7 15 18 36 40 41 0.01"), statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[2] - statistics.quantiles([4, 7, 15, 18, 36, 40, 41], n=4)[0])


    def test_calculate_invalid_operator(self):
        self.assertIsNone(calculate("unknown 1 2 3 0.01"))


    def test_calculate_invalid_numbers(self):
        with self.assertRaises(ValueError):
            calculate("+ 1 a 3 0.01")


if __name__ == '__main__':
    unittest.main()
