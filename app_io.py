import openpyxl
import copy
from docx import Document
from utils import *


class ExcelReader:
    """This class helps in reading any given excel sheets."""

    def __init__(self, filename, read_only=True, max_row=None, max_col=None):
        self.__workbook = openpyxl.load_workbook(filename, read_only)
        self.__sheet = self.__workbook.active   # TODO read only the first sheet
        self.__max_row = max_row
        self.__max_col = max_col

    def fetch_all_rows(self):
        row_end = (self.__sheet.max_row if self.__max_row is None else self.__max_row) + 1
        col_end = (self.__sheet.max_column if self.__max_col is None else self.__max_col) + 1

        # for rx in self.__sheet.iter_rows(min_row=2, min_col=1, max_row=row_end, max_col=col_end - 1):
        #     print('AppName: ' + rx[0].value)

        for ri in range(2, row_end):
            row = []
            for ci in range(1, col_end):
                row.append(str(self.__sheet.cell(row=ri, column=ci).value).strip())
            yield tuple(row)
        # return rows

    # def get_all_rows(self):
    #     """This method provides the data from excel in the form of a List of Tuples"""
    #     return self.__rows


class MasterDocumentHandler:
    """This class handles the operations related to master document"""

    def __init__(self, master_filename):
        self.master_doc = Document(master_filename)

    def create_child_document(self):
        app_doc = copy.copy(self.master_doc)
        return app_doc

    # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s09.html
    # https://www.safaribooksonline.com/videos/python-for-everyday/9781788621953/9781788621953-video5_5

    @staticmethod
    def save(app_name, docx_doc):
        output_filename = 'output\\' + format_filename(app_name) + '.docx'
        docx_doc.save(output_filename)
        print('output file ' + output_filename + ' is created!')

