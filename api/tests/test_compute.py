"""Module with unit tests for the file computation"""

from pathlib import Path
from django.test import SimpleTestCase
from api.exceptions import DivisionByZeroException, InvalidFileColumns, NotANumberException, WrongOperationException
from api.file import FileHandler


class FileComputeTestCase(SimpleTestCase):
    """
    Class containing unit tests for the file computation
    """

    def test_valid_content_result(self):
        """
        Test valid file computed correctly
        """

        valid_csv_path = str(Path(__file__).parent) + '/resources/valid.csv'
        handler = FileHandler(valid_csv_path)
        self.assertEquals(handler.compute_file_content(), 4)

    def test_file_invalid_columns(self):
        """
        Test fail with more columns than supported
        """
        invalid_columns_path = str(Path(__file__).parent) + '/resources/invalid_columns.csv'
        handler = FileHandler(invalid_columns_path)
        with self.assertRaises(InvalidFileColumns):
            handler.compute_file_content()

    def test_file_division_by_zero(self):
        """
        Test fail with 0 division
        """

        invalid_divison_by_zero_path = str(Path(__file__).parent) + '/resources/division_by_zero.csv'
        handler = FileHandler(invalid_divison_by_zero_path)
        with self.assertRaises(DivisionByZeroException):
            handler.compute_file_content()

    def test_wrong_operation(self):
        """
        Test fail with unsuported operation provided
        """
        invalid_operation_csv_path = str(Path(__file__).parent) + '/resources/wrong_operation.csv'
        handler = FileHandler(invalid_operation_csv_path)
        with self.assertRaises(WrongOperationException):
            handler.compute_file_content()

    def test_file_no_numbers(self):
        """
        Test fail file contains chars for operands
        """
        file_no_numbers_csv_path = str(Path(__file__).parent) + '/resources/non_number.csv'
        handler = FileHandler(file_no_numbers_csv_path)
        with self.assertRaises(NotANumberException):
            handler.compute_file_content()
