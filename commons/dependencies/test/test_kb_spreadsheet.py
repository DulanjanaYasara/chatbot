import re
from time import time

import requests
from fuzzywuzzy import fuzz
from pymongo import MongoClient

from commons.dependencies.integrate import best_ans
from commons.dependencies.main import CoreNLP
from commons.dependencies.map import dictionary
from commons.spreadsheet import SpreadsheetConnector

connector = SpreadsheetConnector('./commons/dependencies/test/Q A match-637580fa4bf2.json')


def ask_kb(question):
    params = (
        ('question', question),
    )

    # Sending the request
    response = requests.get('http://10.100.4.189:5000/content', params=params)
    output = response.json()
    for out in output['answers'][:5]:
        yield out['answer']


def sentence_phrases_separation(text):
    """Used for part of sentence extraction based on punctuation delimiters.
    An additional space is added in between period and capital letter"""
    sentence_phrases = [sent for sent in
                        re.split(r'[.,!:;?*()\n]+\s+|\s+[.,!:;?*()\n]+|(->)', re.sub(r'(\.)([A-Z])', r'\1 \2', text)) if
                        sent]
    return sentence_phrases


def compare(true_ans, given_ans):
    given_ans_str = ''.join(re.findall(r'[A-Za-z0-9]', str(given_ans).lower()))
    result = 0
    sentences = sentence_phrases_separation(true_ans)
    str_regex = re.compile(r'[A-Za-z0-9]')
    for sent in sentences:
        sent_str = ''.join(re.findall(str_regex, str(sent).lower()))
        if sent_str in given_ans_str:
            result += 1
    percentage = (result / float(len(sentences))) * 100

    return percentage


def compare1(true, given):
    return fuzz.partial_ratio(true, given)


def fill_spreadsheet():
    all_spreadsheet = connector.import_column_all("Sample Questions", sheet_no=2, column_index=1)

    for index, val in enumerate(all_spreadsheet):
        if index == 0:
            continue
        if val == '':
            break
        question = val
        given_answers = list(ask_kb(question))
        print 'Question :',
        print '\033[1m', question, '\033[0m'
        print 'Answers  :'

        letter = {1: 'C', 2: 'D', 3: 'E', 4: 'F', 5: 'G'}
        for i, v in enumerate(given_answers):
            print str(i + 1), ')', v

        cell_range = 'C' + str(index + 1) + ':' + str(letter[len(given_answers)]) + str(index + 1)
        connector.export_cell_range("Sample Questions", given_answers, sheet_no=2, cell_range=cell_range)


def ask_dependency(no_qs=47):
    final_results = []

    print 'Importing spreadsheet ....   ',
    all_spreadsheet = connector.import_all("Sample Questions", sheet_no=2)
    print 'Done !!!'
    for index, val in enumerate(all_spreadsheet[1:no_qs + 1]):
        question = val[0]
        answer_list = [x for x in val[1:] if x]

        if answer_list[1] == 'Sorry, I don\'t know the answer for that.':
            print 'Skipping .... Question ', str(index + 1)
            continue

        print 'Question :',
        print '\033[1m', question, '\033[0m'
        print 'Answers  :'
        for i, v in enumerate(answer_list):
            print str(i + 1), ')', v

        print 'Answering .... Question ', str(index + 1), '     ',
        start = time()
        chosen_ans_index = find_ans(question, answer_list)[0]
        elapsed = time() - start
        print 'Time taken to generate answers :', elapsed
        print '\033[94m', 'Chosen answer index :', str(chosen_ans_index), '\033[0m'

        if chosen_ans_index == 1:
            result = 100
        else:
            chosen_answer = answer_list[chosen_ans_index - 1]
            result = compare(answer_list[0], chosen_answer)
        final_results.append(result)
        print '\033[91m', 'Percentage :', str(result), '%', '\033[0m'
        print '\033[92m', '_____________________________________________________________________________________________', '\033[0m'

    print 'Final results   :', sum(final_results) / float(len(final_results)), '%', ' out of ', len(
        final_results), ''' q's'''


def find_ans(q_text, a_text):
    dependency_parse = CoreNLP()
    ans_index = best_ans(dependency_parse, q_text, a_text)
    return ans_index


if __name__ == '__main__':
    # fill_spreadsheet()
    mongo = MongoClient()
    for x in mongo.get_database('dependencies').get_collection('frames').find():
        dictionary.update({(x['token'], x['pos']): set(x['frames'])})
    ask_dependency()
    mongo.get_database('dependencies').get_collection('frames').drop()
    for x in dictionary.keys():
        mongo.get_database('dependencies').get_collection('frames').insert(
            {'token': x[0], 'pos': x[1], 'frames': list(dictionary[x])})
