import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('AnswerEvaluation.json', scope)
client = gspread.authorize(creds)


def export_q_a(questionIntent, entities, question, botAnswer, answer, row):
    if row <= 1:
        print 'Error in writing'
        return

    # Find a workbook by name and open the first sheet
    sheet = client.open("Answer Evaluation").sheet1

    # Updating the cells of the spreadsheet with the required values
    sheet.update_cell(row, 1, questionIntent)
    sheet.update_cell(row, 2, question)
    sheet.update_cell(row, 3, entities)
    sheet.update_cell(row, 4, botAnswer)
    sheet.update_cell(row, 5, answer)


def import_ba_e(row):
    """Used to import the Bot answer and the entities form the Google spreadsheet"""
    if row <= 1:
        print 'Error in reading'
        return

    # Find the workbook by name and open  sheet
    sheet = client.open("Answer Evaluation").sheet1

    # Entities are in the 3rd column
    entities = sheet.cell(row, 3).value

    # Bot Answer in the 4th column
    bot_answer = sheet.cell(row, 4).value

    return entities, bot_answer
