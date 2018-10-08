import openpyxl
import copy
from lxml.doctestcompare import etree
from docx import *
from docx.parts import *
from docx.shared import *
from docx.oxml.xmlchemy import *
from docx.text.paragraph import *
from utils import *


class ExcelReader:
    """This class helps in reading any given excel sheets."""

    def __init__(self, filename, read_only=True, max_row=None, max_col=None):
        self._workbook = openpyxl.load_workbook(filename, read_only)
        self._sheet = self._workbook.active   # TODO read only the first sheet
        self._max_row = max_row
        self._max_col = max_col

    def fetch_all_rows(self):
        row_end = (self._sheet.max_row if self._max_row is None else self._max_row) + 1
        col_end = (self._sheet.max_column if self._max_col is None else self._max_col) + 1

        # for rx in self._sheet.iter_rows(min_row=2, min_col=1, max_row=row_end, max_col=col_end - 1):
        #     print('AppName: ' + rx[0].value)

        for ri in range(2, row_end):
            row = []
            for ci in range(1, col_end):
                row.append(str(self._sheet.cell(row=ri, column=ci).value).strip())
            yield tuple(row)

    # def get_all_rows(self):
    #     """This method provides the data from excel in the form of a List of Tuples"""
    #     return self._rows


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
        self._app_doc = app_doc
        self._paragraphs = [para for para in app_doc.paragraphs]
        self._doc_slices = []    # list( DocBlockSlice )
        DocumentBlock.DocBlockSlice.create_block_slices(self._paragraphs, DocumentBlock.style_h2, self._doc_slices)

    def replace(self, old_val, new_val):
        """This method scans the entire document to replace the given value."""
        for para in self._paragraphs:
            if old_val in para.text:
                para.text = para.text.replace(old_val, new_val)

    def get_block_slices(self):
        return self._doc_slices

    def get_doc(self):
        return self._app_doc

    class DocBlockSlice:
        def __init__(self, paragraph_slice):
            self._paragraph_slice = paragraph_slice
            self._sub_doc_slices = []    # list( DocBlockSlice )
            # self._create_block_slices(self._paragraph_slice, DocumentBlock.style_h4, 0, len(self._paragraph_slice))
            DocumentBlock.DocBlockSlice.create_block_slices(self._paragraph_slice, DocumentBlock.style_h4, self._sub_doc_slices)

            for sds in self._sub_doc_slices:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                for ps in sds._paragraph_slice:
                    print('#' + 'H4' + '#' + ps.text)
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

        def get_sub_slices(self):
            return self._sub_doc_slices

        def contains(self, key):
            for para in self._paragraph_slice:
                if key in para.text:
                    return True
            return False

        def replace(self, old_element, new_element):
            for para in self._paragraph_slice:
                if old_element in para.text:
                    para.text = para.text.replace(old_element, new_element)

        def remove(self):
            for para in self._paragraph_slice:
                # print('REMOVING: ' + str(para.text))
                para._p.clear()
                # para.clear()
                # para.text = ''
                # p_elmt = para._element
                # p_elmt.getparent().remove(p_elmt)
                # p_elmt._p = p_elmt._element = None

        @staticmethod
        def create_block_slices(para_for_slicing, block_style, block_slices):
            para_idx = prev_idx = 0
            end_idx = len(para_for_slicing)
            para: Paragraph
            for para in para_for_slicing:
                if para_idx > end_idx:
                    break
                if para.style.name == block_style:
                    # print(para.part._element.body)
                    if prev_idx != 0:
                        block_slices.append(DocumentBlock.DocBlockSlice(para_for_slicing[prev_idx: para_idx]))
                    prev_idx = para_idx

                para_idx += 1

    # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s09.html
    # https://www.safaribooksonline.com/videos/python-for-everyday/9781788621953/9781788621953-video5_5
    # >>> https://stackoverflow.com/questions/24965042/python-docx-insertion-point
