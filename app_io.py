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

    # def get_all_rows(self):
    #     """This method provides the data from excel in the form of a List of Tuples"""
    #     return self.__rows


class MasterDocumentHandler:
    """This class handles the operations related to master document"""

    def __init__(self, master_filename):
        self.master_doc = Document(master_filename)

    def create_child_document(self):
        """This method creates and returns a copy of the master-document."""
        app_doc = copy.copy(self.master_doc)
        doc_block = DocumentBlock(app_doc)
        # return app_doc
        return doc_block

    @staticmethod
    def save(app_name, doc_block):
        output_filename = 'output\\' + format_filename(app_name) + '.docx'
        doc_block.get_doc().save(output_filename)
        print('output file ' + output_filename + ' is created!')


class DocumentBlock:
    style_h2 = 'Heading 2'
    style_h4 = 'Heading 4'

    def __init__(self, app_doc: Document):
        self.__app_doc = app_doc
        self.__paragraphs = [para for para in app_doc.paragraphs]

        self.__doc_slices = []    # list( DocBlockSlice )
        self.__create_block_slices(DocumentBlock.style_h2, 0, len(self.__paragraphs))

    def __create_block_slices(self, block_style, start_idx, end_idx):
        para_idx = start_idx
        prev_idx = 0
        for para in self.__paragraphs:
            if para_idx > end_idx:
                break
            if para.style.name == block_style:
                if prev_idx != 0:
                    self.__doc_slices.append(self.DocBlockSlice(self.__paragraphs, prev_idx, para_idx))
                prev_idx = para_idx
            para_idx += 1

    def get_block_slices(self):
        return self.__doc_slices

    def get_doc(self):
        return self.__app_doc

    class DocBlockSlice:
        def __init__(self, paragraphs, start_idx, end_idx):
            self.__start_idx = start_idx
            self.__end_idx = end_idx
            self.__paragraph_slice = paragraphs[start_idx: end_idx]

            self.__sub_doc_slices = []    # list( DocBlockSlice )
            self.__create_block_slices(paragraphs, DocumentBlock.style_h4, self.__start_idx, self.__end_idx)

            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[' + str(start_idx) + '] [' + str(end_idx) + ']')
            for ps in self.__paragraph_slice:
                print('####' + ps.text)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        def __create_block_slices(self, paragraphs, block_style, start_idx, end_idx):
            para_idx = start_idx
            prev_idx = 0
            for para in paragraphs:
                if para_idx > end_idx:
                    break
                if para.style.name == block_style:
                    if prev_idx != 0:
                        self.__sub_doc_slices.append(DocumentBlock.DocBlockSlice(paragraphs, prev_idx, para_idx))
                    prev_idx = para_idx
                para_idx += 1

        def get_sub_slices(self):
            return self.__sub_doc_slices

        def contains(self, key):
            for para in self.__paragraph_slice:
                if key in para.text:
                    return True
            return False

        def replace(self, old_element, new_element):
            for para in self.__paragraph_slice:
                if old_element in para.text:
                    para.text = para.text.replace(old_element, new_element)

        def remove(self):
            for para in self.__paragraph_slice:
                para.clear()
                para.text = ''
                # p_elmt = para.__element
                # p_elmt.getparent().remove(p_elmt)
                # p_elmt._p = p_elmt._element = None

    # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s09.html
    # https://www.safaribooksonline.com/videos/python-for-everyday/9781788621953/9781788621953-video5_5
