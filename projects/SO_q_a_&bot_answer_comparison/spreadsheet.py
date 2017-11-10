import gspread
from oauth2client.service_account import ServiceAccountCredentials


def export_q_a(question, accepted_answer, bot_answer, row):
    if row <= 1:
        print 'Error in writing'
        return

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = client.open("Performance Evaluation").sheet1

    # Updating the cells of the spreadsheet with the required values
    sheet.update_cell(row, 1, question)
    sheet.update_cell(row, 2, bot_answer)
    sheet.update_cell(row, 3, accepted_answer)
