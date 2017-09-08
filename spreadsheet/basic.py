import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SpreadsheetConnector:
    def __init__(self, json_data_file):
        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_data_file, self.scope)
        self.client = gspread.authorize(self.creds)

    def export(self, workbookName, rowIndex, sheetNo=1, *row):
        if rowIndex <= 1:
            print 'Error in writing'
            return

        # Find a workbook by name and open the first sheet
        sheet = self.client.open(workbookName).get_worksheet(sheetNo - 1)
        for i in range(len(row)):
            sheet.update_cell(rowIndex, i + 1, row[i])

    def import_sheet(self, rowIndex, workbookName, sheetNo=1, columns=list([])):
        """Used to import the Bot answer and the entities form the Google spreadsheet"""
        if rowIndex <= 1:
            print 'Error in reading'
            return

        # Find the workbook by name and open  sheet
        sheet = self.client.open(workbookName).get_worksheet(sheetNo - 1)
        ans = []
        for i in range(len(columns)):
            ans.append(sheet.cell(rowIndex, columns[i]).value)

        return ans
