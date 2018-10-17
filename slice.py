
from docx import *
from docx.parts import *
from docx.shared import *
from docx.oxml.xmlchemy import *
from docx.text.paragraph import *
from lxml.doctestcompare import etree


class DocumentBlock:
    """This class represents the Document from 'docx' in terms of blocks."""
    style_h2 = 'Heading 2'
    style_h4 = 'Heading 4'

    def __init__(self, app_doc: Document):
        self._app_doc = app_doc
        self._paragraphs = [para for para in app_doc.paragraphs]
        self._doc_slices = []    # list( DocBlockSlice )
        DocumentBlock.DocBlockSlice.create_block_slices(self._paragraphs, DocumentBlock.style_h2, self._doc_slices)

        for sds in self._doc_slices:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            for ps in sds._paragraph_slice:
                print('#' + 'H2' + '#' + ps.text)
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    def replace(self, old_val, new_val):
        """This method scans the entire document to replace the given value."""
        for para in self._paragraphs:
            if old_val in para.text:
                para.text = para.text.replace(old_val, new_val)

    def get_block_slices(self):
        """This method provides a list of all the block-slices with style as H2"""
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
                pe = para._element
                pe.getparent().remove(pe)
                para._p.clear()

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