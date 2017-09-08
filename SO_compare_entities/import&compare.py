from spreadsheet import SpreadsheetConnector
from suzy.ans import get_entities


def print_all(q_entities, ans_entities):
    # Printing the entities
    print '\033[1m' + 'Question entities :' + '\033[0m',
    print q_entities
    print '\033[1m' + 'Answer entities :' + '\033[0m',
    print ans_entities

    common = list(ans_entities.intersection(q_entities))
    print common
    print '\033[1m' + str(float(len(common)) / len(q_entities) * 100) + '%' + '\033[0m'


if __name__ == '__main__':
    # This only executes when file is executed rather than imported
    row = 2
    connector = SpreadsheetConnector('./SO_compare_entities/AnswerEvaluation.json')

    while True:
        q_entities = set()

        # Entities is in the 3rd column
        for en in connector.import_sheet(row, "Answer Evaluation", columns=[3])[0].split('\n'):
            q_entities.add(en.lower())

        # Bot answer is in the 4th column
        bot_ans = connector.import_sheet(row, "Answer Evaluation", columns=[4])[0]
        if bot_ans == '':
            break
        row += 1

        ans_entities = get_entities(bot_ans)
        print_all(q_entities, ans_entities)
