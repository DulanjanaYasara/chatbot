from locale import str

import extract_data
import getDatafromSuzy
import mongoDBSheet
import requests

page_number = 0

mongoDBSheet.remove_data()

while True:

    try:

        page_number += 1
        print '%02d' % page_number,
        # if page_number > 2:
        #     break

        # Finding the questions with the tag wso2esb through the stack overflow API with the use of access tokens
        responseQuestion = requests.get(
            "https://api.stackexchange.com/2.2/questions?page=" + str(
                page_number) + "&pagesize=100&order=desc&sort=acti"
                               "vity&tagged=wso2esb&site=stackoverflow&filter=!9YdnSIN18&access_token=3*MQ0YtINm2*xpbWplNVKw))&key=b500RPkb"
                               "AnAO3TH6oRQVew((")

        dataQuestion = responseQuestion.json()

        # Generating the accepted answer for the given question
        for value in dataQuestion['items']:
            if value['is_answered'] and 'accepted_answer_id' in value:
                question = extract_data.extractall(value['body'])
                questionIntent = value['title']
                # print('Intent>>>  ' + questionIntent + '\nQuestion>>>  ' + question)
                acceptedAnswerID = value['accepted_answer_id']
                ids = str(acceptedAnswerID)
                try:
                    responseAnswer = requests.get(
                        'https://api.stackexchange.com/2.2/answers/' + ids + '?order=desc&sort=activity&site=stackoverfl'
                                                                             'ow&filter=!9YdnSMKKT&access_token=3*MQ0YtINm2*xpbWplNVKw))&key=b500RPkbAnAO3TH6oRQVew((')

                    dataAnswer = responseAnswer.json()
                    print '.',

                    for answer in dataAnswer['items']:
                        answer = extract_data.extractall(answer['body'])
                        # print('Answer>>>  ' + answer)
                        # print('_______________________________________________________________________________________')
                        botAnswer, write_data = getDatafromSuzy.data_from_bot(questionIntent)
                        if write_data:
                            mongoDBSheet.export_q_a(questionIntent, answer, botAnswer)

                except KeyError:
                    print 'x',
                    # print dataAnswer
        print ''
        if not dataQuestion['has_more']:
            break

    except KeyError:
        print 'X',
        # print dataQuestion
