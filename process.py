from pathlib import Path
from app_io import *
from factory import *
import docx
import docx.document


def process_data_input():
    p = Path('').resolve()
    # Read the input Excel file and generate the application-data objects.
    er = ExcelReader('resources\\data_input.xlsx')

    for app_entry in er.fetch_all_rows():
        ApplicationFactory.create_app_data(app_entry)
        # print(app_entry)

# for row in sheet.iter_rows(min_row=1, min_col=1, max_row=6, max_col=3):
#     for cell in row:
#         print(cell.value, end=" ")
#     print()

#########################


# answer = {
#     'a3.4' : 'AchhaiWaliApplication',
#     'a5.2' : 'DomainX'
# }
#
#
# for par in mdr.doc.paragraphs:
#     if '<<$Application_Name>>' in par.text or '<<APP_NAME>>' in par.text:
#         par.text = par.text.replace('<<$Application_Name>>', answer['a3.4'])
#     if '<<$DMN1>>' in par.text:
#         par.text = par.text.replace('<<$DMN1>>', answer['a5.2'])
#     print(par.text)


def process_applications():
    print('Processing Started.')
    mdh = MasterDocumentHandler('resources\\master_document.docx')
    for app_name, app_data in ApplicationFactory.app_cache.items():
        print(app_name + ' processing...')
        child_doc = mdh.create_child_document()
        # TODO Process the content of this file
        print('Creating document for application : ' + app_name)
        paragraphs = (p for p in child_doc.paragraphs)
        for para in paragraphs:
            tag_app_name = '<<$Application_Name>>'
            if tag_app_name in para.text or '<<APP_NAME>>' in para.text:
                question = Question.cache_tag.get(tag_app_name)
                para.text = para.text.replace(tag_app_name, app_data.get_answers(question))
            print(para.text)
            print(next(paragraphs).text)
        MasterDocumentHandler.save(app_name, child_doc)
        break

