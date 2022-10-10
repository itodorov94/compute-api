import csv
import openpyxl
from . import exceptions

from .config import OPERATIONS_DICT, CSV


class FileHandler:

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_extension = file_name.rsplit('.')[1]

    def load_file_content(self):
        """Returns parsed file based on file extension ready for calculation"""
        return self.load_csv_content() if self.file_extension == CSV else self.load_xlsx_content()

    def load_csv_content(self):
        """Returned the parsed CSV file as list containing all the rows"""
        loaded_content = []
        with open(self.file_name, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                self.__validate(row)
                loaded_content.append(row)
        return loaded_content

    def load_xlsx_content(self):
        """Returns parsed xlsx file as list containing all the rows"""
        loaded_content = []
        wb = openpyxl.load_workbook(self.file_name)
        sheet = wb.active
        rows = list(sheet.rows)
        rows = rows[1:]  # Remove cell names

        for row in rows:
            row_content = []
            for cell in row:
                row_content.append(cell.value)
            self.__validate(row_content)
            loaded_content.append(row_content)
        return loaded_content

    def __validate(self, row):
        """Validates file row content"""

        if len(row) != 3:
            raise exceptions.InvalidFileColumns('Row has more than 3 columns')
        if str(row[0]).isalpha() or str(row[2]).isalpha():
            raise exceptions.NotANumberException('Expected digit but received a character')
        if row[1] not in OPERATIONS_DICT:
            raise exceptions.WrongOperationException('Invalid Operator')
        if row[1] == '/' and str(row[2]) == '0':
            raise exceptions.DivisionByZeroException('Cannot have 0 as second operand due to Zero Division')

    def compute_file_content(self):
        file_content = self.load_file_content()
        result = 0
        for row in file_content:
            operand_a = row[0]
            operation = row[1]
            operand_b = row[2]
            result += OPERATIONS_DICT[operation](float(operand_a), float(operand_b))

        return result
