import openpyxl
import docx
import docx.section
import docx.shared
import docx.document


class ExcelReader:
    """This class helps in reading any given excel sheets."""

    def __init__(self, filename, read_only=True, max_row=None, max_col=None):
        self.__workbook = openpyxl.load_workbook(filename, read_only)
        self.__sheet = self.__workbook.active
        self.__max_row = max_row
        self.__max_col = max_col
        self.__rows = []

    def fetch_all_rows(self):
        row_end = (self.__sheet.max_row if self.__max_row is None else self.__max_row) + 1
        col_end = (self.__sheet.max_column if self.__max_col is None else self.__max_col) + 1

        # for rx in self.__sheet.iter_rows(min_row=2, min_col=1, max_row=row_end, max_col=col_end - 1):
        #     print('AppName: ' + rx[0].value)

        for ri in range(1, row_end):
            row = ()
            for ci in range(1, col_end):
                row += (self.__sheet.cell(row=ri, column=ci).value,)
            self.__rows.append(row)
            yield row
        # return rows

    # def get_all_rows(self):
    #     """This method provides the data from excel in the form of a List of Tuples"""
    #     return self.__rows


er = ExcelReader('S:\\DEV\\Temp\\apps.xlsx')

for app_entry in er.fetch_all_rows():
    print(app_entry)

# for row in sheet.iter_rows(min_row=1, min_col=1, max_row=6, max_col=3):
#     for cell in row:
#         print(cell.value, end=" ")
#     print()


class MasterDocumentReader:
    def __init__(self):
        self.doc = docx.Document('resources\\master_document.docx')

    def save(self):
        self.doc.save('resources\\child.docx')


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
