import time

from commons.data.entity import Extractor, reducer
from commons.spreadsheet.basic import SpreadsheetConnector
from commons.suzy.ask import ask_suzy

"""Used to export better question entities from the SO question and the relevant suzy answers"""
# This only executes when file is executed rather than imported
row = 74
connector = SpreadsheetConnector('./SO_compare_entities/AnswerEvaluation.json')
extractor = Extractor()

while True:

    # Question is in the 2nd column
    q = connector.import_row(row, "Answer Evaluation", columns=[2])[0]
    print q

    if q == '':
        break

    # Extracting the question entities from the question
    q_entities = list(reducer(list(extractor.extract_entities(q))))

    suzy_ans = []

    while True:
        for entity in q_entities:
            try:
                print entity
                ans = ask_suzy(entity)[0]
                suzy_ans.append(ans)
            except Exception as e:
                time.sleep(2)
                continue
        break

    q_entities = '\n'.join(q_entities)
    print q_entities

    print suzy_ans
    suzy_ans = '\n'.join(suzy_ans)

    connector.export_row("Answer Evaluation", row, column_data=[q_entities], column_index=[3])
    connector.export_row("Answer Evaluation", row, column_data=[suzy_ans], column_index=[4])
    print'.'
    row += 1
