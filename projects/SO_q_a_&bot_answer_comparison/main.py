from locale import str

import requests

import extract_data
import get_data_suzy
import spreadsheet

rowNum = 1

for page_number in range(1, 6):

    # Finding the questions with the tag wso2esb through the stack overflow API with the use of access tokens
    responseQuestion = requests.get(
        "https://api.stackexchange.com/2.2/questions?page=" + str(
            page_number) + "&pagesize=100&order=desc&sort=activity"
                           "&tagged=wso2esb&site "
                           "=stackoverflow&filter=!9YdnSIN18")

    dataQuestion = responseQuestion.json()

    # Generating the accepted answer for the given question
    for value in dataQuestion['items']:
        if value['is_answered'] and 'accepted_answer_id' in value:
            question = extract_data.extractall(value['body'])
            questionIntent = value['title']
            print('Intent>>>  ' + questionIntent + '\nQuestion>>>  ' + question)
            acceptedAnswerID = value['accepted_answer_id']
            ids = str(acceptedAnswerID)
            responseAnswer = requests.get('https://api.stackexchange.com/2.2/answers/' + ids + '?order=desc&sort'
                                                                                               '=activity& '
                                                                                               'site=stackoverflow'
                                                                                               '&filter= '
                                                                                               '!9YdnSMKKT')
            dataAnswer = responseAnswer.json()
            for answer in dataAnswer['items']:
                rowNum += 1
                answer = extract_data.extractall(answer['body'])
                print('Answer>>>  ' + answer)
                print('_______________________________________________________________________________________')
                botAnswer = get_data_suzy.data_from_bot(questionIntent)
                spreadsheet.export_q_a(questionIntent, answer, botAnswer, rowNum)
