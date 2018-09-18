import openpyxl
import docx
import docx.section
import docx.shared
import docx.document
from utils import *


class ExcelReader:
    """This class helps in reading any given excel sheets."""

    def __init__(self, filename, read_only=True, max_row=None, max_col=None):
        self.__workbook = openpyxl.load_workbook(filename, read_only)
        self.__sheet = self.__workbook.active
        self.__max_row = max_row
        self.__max_col = max_col
        self.__rows = []

    def fetch_all_rows(self):
        row_end = (self.__sheet.max_row if self.__max_row is None else self.__max_row) + 1
        col_end = (self.__sheet.max_column if self.__max_col is None else self.__max_col) + 1

        # for rx in self.__sheet.iter_rows(min_row=2, min_col=1, max_row=row_end, max_col=col_end - 1):
        #     print('AppName: ' + rx[0].value)

        for ri in range(2, row_end):
            row = []
            for ci in range(1, col_end):
                row.append(str(self.__sheet.cell(row=ri, column=ci).value).strip())
            self.__rows.append(tuple(row))  # each row shall be immutable (viz. tuple)
            yield tuple(row)
        # return rows

    # def get_all_rows(self):
    #     """This method provides the data from excel in the form of a List of Tuples"""
    #     return self.__rows


class MasterDocumentReader:
    """This class handles the operations related to master document"""

    def __init__(self, master_filename):
        self.doc = docx.Document(master_filename)
        self.__app_name = ''

    def feed_application(self, app_data):
        self.__app_name = app_data.app_name
        logger.info('Creating document for application : ' + self.__app_name)
        pass

    def save(self):
        output_filename = 'output\\' + format_filename(self.__app_name) + '_child.docx'
        logger.info(output_filename + ' created!')
        self.doc.save(output_filename)

