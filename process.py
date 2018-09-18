from app_io import *
from factory import *
from model import *
from multiprocessing import Pool


# Read the input Excel file and generate the application-data objects.
er = ExcelReader('resources\\DataInput.xlsx')


for app_entry in er.fetch_all_rows():
    ApplicationFactory.create_app_data(app_entry)
    # print(app_entry)

# for row in sheet.iter_rows(min_row=1, min_col=1, max_row=6, max_col=3):
#     for cell in row:
#         print(cell.value, end=" ")
#     print()

#########################


mdr = MasterDocumentReader('resources\\master_document.docx')

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
    for app_name, app_data in ApplicationFactory.app_cache.items():
        logger.info(app_name + ' processing...')
        mdr.feed_application(app_data)
        mdr.save()

    # for sec in mdr.doc.sections:
    #     print(sec)
    #     mdr.save()


# if __name__ == '__main__':
#     p = Pool(5)
#     print(p.map(process_applications, []))

process_applications()
