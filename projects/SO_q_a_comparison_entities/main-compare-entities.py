import getDatafromSuzy
import spreadsheet
from breaknplay import entity_extraction
from extractData import find_urls
from getDatafromURL import get_data_from_url


def get_entities(bot_answer):
    # Arranging the text and urls
    text_without_url = find_urls(bot_answer)[0]
    urls = find_urls(bot_answer)[1]
    text = getDatafromSuzy.remove_default_intents(text_without_url)

    answer_entities = set()
    # Entity extraction from the text
    for entity in entity_extraction(text):
        answer_entities.add(entity.lower())
    # Entity extraction from the urls
    for url in urls:
        for entity in entity_extraction(get_data_from_url(url)):
            answer_entities.add(entity.lower())
    return answer_entities


def print_all(question_entities, answer_entities):
    # Printing the entities
    print '\033[1m' + 'Question entities :' + '\033[0m',
    print question_entities
    print '\033[1m' + 'Answer entities :' + '\033[0m',
    print answer_entities

    common = list(answer_entities.intersection(question_entities))
    print common
    print '\033[1m' + str(float(len(common)) / len(question_entities) * 100) + '%' + '\033[0m'


if __name__ == '__main__':
    # This only executes when file is executed rather than imported
    row = 2
    while True:
        q_entities = set()

        for en in spreadsheet.import_ba_e(row)[0].split('\n'):
            q_entities.add(en.lower())

        bot_ans = spreadsheet.import_ba_e(row)[1]

        if bot_ans == '':
            break
        row += 1

        ans_entities = get_entities(bot_ans)
        print_all(q_entities, ans_entities)
