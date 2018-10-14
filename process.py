from pathlib import Path
from app_io import *
from app_io import DocumentBlock
from factory import *
from utils import join_with_commas
from docx import *
from docx.document import *
from docx.enum.style import *
from docx.text import *
from docx.text.paragraph import *

p = Path('').resolve()


def configure_section_mapping():
    """Reads the configuration Excel file to generate and cache the question/answer objects."""

    section_map = ExcelReader('resources\\section_mapping.xlsx', max_col=7)
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
    for app_name, app_data in ApplicationData.app_cache_items():
        print('Processing [' + app_name + ']')
        child_doc_block = mdh.create_child_document()
        doc_block_slices = child_doc_block.get_block_slices()
        print('Creating child document for application : ' + app_name)
        # paragraphs = (para for para in child_doc.paragraphs)

        for question in Question.cache_values():
            q_type = question.q_type
            answer = app_data.get_answers(question)
            if q_type == QuestionType.LARGE_TEXT:
                process_large_text_question(question, answer, doc_block_slices, child_doc_block)

            elif q_type == QuestionType.CHECKBOX:
                process_checkbox_question(question, answer, doc_block_slices, child_doc_block)

            elif q_type == QuestionType.RADIO:
                process_radio_question(question, answer, doc_block_slices)

        apply_tag_value(const.APP_NAME_TAG, app_name, child_doc_block)

        MasterDocumentHandler.save(app_name, child_doc_block)
        break


def apply_tag_value(tag, value, doc_block: DocumentBlock):
    doc_block.replace(tag, value)


def process_large_text_question(question, answer, doc_block_slices, doc_block):
    q_tag = question.q_tag
    if question.q_default == const.DEFAULT_QUESTION_OTHER:
        # this question is a follow-up for another checkbox type of question, which was answered as 'Other'
        doc_block.replace(wrap_padding(question.q_tag), answer)
    else:
        for block_slice in doc_block_slices:
            answer = question.q_default if is_empty(answer) else answer
            block_slice.replace(q_tag, answer)


def process_checkbox_question(question, answers, doc_block_slices, doc_block):
    for ans_opt in question.all_answer_options:
        if ans_opt in answers:
            # process the block of this answer
            for block_slice in doc_block_slices:
                for sub_slices in block_slice.get_sub_slices():
                    if sub_slices.contains(ans_opt.tag):
                        sub_slices.replace(ans_opt.tag, ans_opt.value)
        else:
            # remove the unanswered block for this answer
            for block_slice in doc_block_slices:
                for sub_slices in block_slice.get_sub_slices():
                    if sub_slices.contains(ans_opt.tag):
                        sub_slices.remove()

    if question.q_default == const.DEFAULT_QUESTION_VALUE and const.DEFAULT_ANSWER_OTHER not in answers:
        ans_commas = join_with_commas(answers, lambda a: a.value)
        if 'other' in ans_commas.lower():
            ans_commas = replace_ignore(ans_commas, 'other', 'Other (' + wrap_padding(question.q_tag) + ')')
        doc_block.replace(question.q_tag, ans_commas)


def process_radio_question(question, answer, doc_block_slices):
    q_tag = question.q_tag
    is_used = answer is not None and not is_empty(answer.value) and answer.value.lower() != 'no'

    for ans_opt in question.all_answer_options:
        if '$No' in ans_opt.tag and not is_used and answer is None:
            answer = ans_opt

    print('>>>>>>>>>>>>>>>>>>>>>>>>>' + answer.tag)

    for block_slice in doc_block_slices:
        if block_slice.contains(q_tag):
            for sub_slices in block_slice.get_sub_slices():
                if is_used and sub_slices.contains(question.q_tag):
                    ans_val = answer.value if answer is not None and not is_empty(answer.value) and answer.value.lower() != 'yes' else 'Yes'
                    sub_slices.replace(q_tag, ans_val)
                elif not is_used and sub_slices.contains(answer.tag):
                    sub_slices.replace(answer.tag, 'No')
                else:
                    sub_slices.remove()
            break
