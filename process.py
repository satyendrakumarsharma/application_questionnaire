from app_io import *
from factory import *
from model import *


er = ExcelReader('S:\\DEV\\Temp\\apps.xlsx')


for app_entry in er.fetch_all_rows():
    ApplicationFactory.create_app_data(app_entry)
    # print(app_entry)

# for row in sheet.iter_rows(min_row=1, min_col=1, max_row=6, max_col=3):
#     for cell in row:
#         print(cell.value, end=" ")
#     print()

#########################


mdr = MasterDocumentReader()

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


for sec in mdr.doc.sections:
    print(sec)


print(mdr.doc.sections[0])

mdr.save()



