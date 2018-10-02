from pathlib import Path
from app_io import *
from app_io import DocumentBlock
from factory import *
from docx import *
from docx.document import *
from docx.enum.style import *
from docx.text import *
from docx.text.paragraph import *


p = Path('').resolve()


def configure_section_mapping():
    """Reads the configuration Excel file to generate and cache the question/answer objects."""

    section_map = ExcelReader('resources\\section_mapping.xlsx', max_col=6)
    for mapping in section_map.fetch_all_rows():
        ApplicationFactory.create_question_answer_mapping(mapping)


def process_data_input():
    """Reads the input Excel file to generate and cache the application-data objects."""
    user_input = ExcelReader('resources\\data_input.xlsx')
    for app_entry in user_input.fetch_all_rows():
        ApplicationFactory.create_app_data(app_entry)

# for row in sheet.iter_rows(min_row=1, min_col=1, max_row=6, max_col=3):
#     for cell in row:
#         print(cell.value, end=" ")
#     print()


def process_applications():
    print('Processing Started.')
    mdh = MasterDocumentHandler('resources\\master_document.docx')
    for app_name, app_data in ApplicationData.app_cache.items():
        print('Processing [' + app_name + ']')
        child_doc_block = mdh.create_child_document()
        doc_block_slices = child_doc_block.get_block_slices()
        print('Creating child document for application : ' + app_name)
        # paragraphs = (para for para in child_doc.paragraphs)

        for question in Question.cache_values():
            q_type = question.q_type
            answer = app_data.get_answers(question)
            if q_type == QuestionType.LARGE_TEXT:
                process_large_text_question(question, answer, doc_block_slices)
            elif q_type == QuestionType.CHECKBOX:
                process_checkbox_question(question, answer, doc_block_slices)
            elif q_type == QuestionType.RADIO:
                process_radio_question(question, answer, doc_block_slices)

        MasterDocumentHandler.save(app_name, child_doc_block)
        break


def process_large_text_question(question, answer, doc_block_slices):
    q_tag = question.q_tag
    for block_slice in doc_block_slices:
        block_slice.replace(q_tag, answer)


def process_checkbox_question(question, answers, doc_block_slices):
    q_tag = question.q_tag
    for ans in question.all_answer_options:
        if ans in answers:
            # process the block of this answer
            for block_slice in doc_block_slices:
                for sub_slices in block_slice.get_sub_slices():
                    if sub_slices.contains(ans.tag):
                        sub_slices.replace(ans.tag, ans.value)
        else:
            # remove the block of this answer
            for block_slice in doc_block_slices:
                for sub_slices in block_slice.get_sub_slices():
                    if sub_slices.contains(ans.tag):
                        sub_slices.remove()
    # TODO Use element tree of docx instead of slices.

    # for block_slice in doc_block_slices:
    #     if q_tag in para.text:
    #         para.text = para.text.replace(q_tag, answers)
    #     print('[C}' + para.text)


def process_radio_question(question, answer, doc_block_slices):
    q_tag = question.q_tag
    # for block_slice in doc_block_slices:
    #     if q_tag in para.text:
    #         para.text = para.text.replace(q_tag, answer)
    #     print('[R}' + para.text)
