from time import sleep

from commons.data.entity import Extractor, comparator, reducer
from commons.spreadsheet.basic import SpreadsheetConnector
from commons.suzy.ans import get_entities

# This only executes when file is executed rather than imported
row = 34
connector = SpreadsheetConnector('./SO_compare_entities/AnswerEvaluation.json')
extractor = Extractor()

while True:
    q_en = []

    print '\033[1m' + 'Row No :' + '\033[0m',
    print row

    while True:
        try:
            # Entities is in the 3rd column
            for en in connector.import_row(row, "Answer Evaluation", sheet_no=1, columns=[3])[0].split('\n'):
                q_en.append(en)

            # Bot ans is in the 4th column
            bot_ans = connector.import_row(row, "Answer Evaluation", sheet_no=1, columns=[4])[0]
            print '\033[1m' + 'Bot ans imported' + '\033[0m'

            if bot_ans == '':
                break
        except IndexError:
            print '$'
            sleep(1)
            continue
        break

    # Not compulsory in future based on correctness (question entities reduction)
    q_entities = []
    for q in reducer(q_en):
        q_entities.append(q)

    print '\033[1m' + 'Question entities :' + '\033[0m',
    print q_entities

    ans_entities = list(reducer(list(get_entities(extractor, bot_ans))))

    print '\033[1m' + 'Answer entities :' + '\033[0m',
    print ans_entities

    # Finding the common entities from the bot answer and the question
    common = comparator(list(q_entities), list(ans_entities))
    rank = str(float(len(common)) / len(q_entities) * 100) + '%'
    print common
    print '\033[1m' + rank + '\033[0m'

    while True:

        try:
            # Exporting the rank to the spreadsheet
            connector.export_row("Answer Evaluation", row, sheetNo=1, column_data=[rank], column_index=[7])
        except IndexError:
            print'#'
            sleep(1)
            continue
        break

    row += 1
    # if row == 3:
    #     break
