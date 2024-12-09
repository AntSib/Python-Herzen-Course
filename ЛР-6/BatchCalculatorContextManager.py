import os
from time import perf_counter
from calc.calculator_with_tolerance import calculate


class BatchCalculatorContextManager(object):
    def __init__(self, file_name):
        """
        Initializes the BatchCalculatorContextManager with the given file name.

        :param file_name: The name of the file to be opened and processed.
        """
        self.filename = file_name
    
    def __enter__(self):
        """
        Entering the context manager. Setting up timer and opening the file.
        If file does not exist or is not accessible, raises an exception.

        :return: The opened file.
        """
        if not os.path.exists(self.filename):                                   # Exceptions if file does not exist or is not accessible
            raise FileNotFoundError(f"File {self.filename} does not exist.")
        if not os.access(self.filename, os.R_OK):
            raise PermissionError(f"Cannot open {self.filename}. Permission denied.")
    
        self.start_time = perf_counter()

        try:
            self.read_file = open(self.filename, 'r')
        except Exception as err:
            raise RuntimeError(f"Unexpected error while opening file: {err}")   # Unexpected error
        
        return self.read_file
            

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exiting the context manager. Closes the file and prints the execution time.

        :param exc_type: The type of exception.
        :param exc_value: The value of exception.
        :param traceback: The traceback of exception.
        """
        if hasattr(self, 'read_file') and self.read_file: 
            self.read_file.close()
        else:
            raise TypeError("File is not opened.")

        self.end_time = perf_counter()
        self.execution_time = self.end_time - self.start_time
        print(f"Execution time: {self.execution_time:.6f} seconds")


def generate_input_from_file(iterable: list) -> str:
    """
    Iterates over a list of strings, processes each string, and yields
    a formatted prompt if valid.

    Each item in the iterable is expected to be a string that contains
    a prompt separated by colons and commas. The function extracts the
    last segment after the last colon, splits it by commas, and checks
    if the resulting list has at least three elements. If so, the list
    is joined with spaces and yielded.

    :param iterable: A list of strings to be processed.
    :yield: A string containing a space-joined prompt if valid.
    """
    for item in iterable:
        try:
            # 'INFO"__main__:+,1,2,3,0.001' -> ['+', '1', '2', '3', '0.001']
            calculation_info = item.strip('\n').split(':')[-1]
            prompt = calculation_info.split('=')[0].split(',')

            if len(prompt) >= 3:                    # check if prompt has at least 3 elements, otherwise skip it and check next
                yield ' '.join(prompt)

        except (IndexError, ValueError):
            print(f"Prompt with invalid format skipped: {prompt=}")


def calc_with_manager(filename: str) -> None:
    """
    Reads a file with managed context, and prints the result of
    calculation or an error message if an exception occurs.

    :param filename: The name of the file to be read.
    """
    with BatchCalculatorContextManager(filename) as file:
        for expression in generate_input_from_file(file):
            try:
                print(f"Task: {expression}")
                result = calculate(expression)
                print(f"Result: {result}", end='\n\n')

            except Exception as err:
                print(f"Unexpected error: {err}")


if __name__ == "__main__":
    calc_with_manager('calc_log.log')
