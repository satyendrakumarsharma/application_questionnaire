from pathlib import Path
from app_io import *
from factory import *
import docx
import docx.document


p = Path('').resolve()


def configure_section_mapping():
    """Read the configuration Excel file and cache the question/answer objects."""
    section_map = ExcelReader('resources\\section_mapping.xlsx', max_col=6)
    for mapping in section_map.fetch_all_rows():
        ApplicationFactory.create_question_answer_mapping(mapping)
        # print(mapping)


def process_data_input():
    """Read the input Excel file and generate the application-data objects."""
    er = ExcelReader('resources\\data_input.xlsx')
    for app_entry in er.fetch_all_rows():
        ApplicationFactory.create_app_data(app_entry)
        # print(app_entry)

# for row in sheet.iter_rows(min_row=1, min_col=1, max_row=6, max_col=3):
#     for cell in row:
#         print(cell.value, end=" ")
#     print()


def process_applications():
    print('Processing Started.')
    mdh = MasterDocumentHandler('resources\\master_document.docx')
    for app_name, app_data in ApplicationFactory.app_cache.items():
        print('Processing [' + app_name + ']')
        child_doc = mdh.create_child_document()
        # TODO Process the content of this file
        print('Creating document for application : ' + app_name)
        paragraphs = (para for para in child_doc.paragraphs)

        for q_value, question in Question.cache_value.items():
            # TODO PERFORMANCE : Process the entire document for each question.
            if question.q_type == QuestionType.LARGE_TEXT:
                answer = app_data.get_answers(question)
                process_large_text_question(question, answer, paragraphs)

        MasterDocumentHandler.save(app_name, child_doc)
        # break


def process_large_text_question(question, answer, paragraphs):
    q_tag = question.q_tag
    for para in paragraphs:
        if q_tag in para.text:
            para.text = para.text.replace(q_tag, answer)
        print('#' + para.text)


def process_checkbox_question():
    pass


def process_radio_question():
    pass

