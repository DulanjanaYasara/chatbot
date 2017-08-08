from locale import str
from time import sleep

import requests

import extractData
import getDatafromSuzy
import mongoDBSheet

page_number = 0

# Removing the data in the database
mongoDBSheet.remove_data()

while True:

    try:

        page_number += 1
        print '%02d' % page_number,
        # if page_number >2:
        #     break

        # Finding the questions with the tag wso2esb through the stack overflow API with the use of access tokens
        responseQuestion = requests.get(
            "https://api.stackexchange.com/2.2/questions?page=" + str(
                page_number) + "&pagesize=100&order=desc&sort=acti"
                               "vity&tagged=wso2esb&site=stackoverflow&filter=!*e9ibzERTZv_4jPLGyBUXbiO0TCnjFLALrHd*&access_token=3*MQ0YtINm2*xpbWplNVKw))&key=b500R"
                               "PkbAnAO3TH6oRQVew((")

        # previous filter !-*f(6rc.(Xr5
        # Next filter !*e9ibzERTZv_4jPLGyBUXbiO0TCnjFLALrHd*

        dataQuestion = responseQuestion.json()
        # print json.dumps(dataQuestion,sort_keys=True,indent=7 )

        # Generating the accepted answer for the given question
        for value in dataQuestion['items']:
            if 'accepted_answer_id' in value:
                question = extractData.extractall(value['body'])
                questionIntent = extractData.extractall(value['title'])
                # print('Intent>>>  ' + questionIntent + '\nQuestion>>>  ' + question)

                for answer in value['answers']:
                    if answer['is_accepted']:
                        answer = extractData.extractall(answer['body'])
                        # print('Answer>>>  ' + answer)
                        # print('_______________________________________________________________________________________')
                        print '.',

                        # Sleeping for 1s due to throttling of data after each API.AI call
                        botAnswer, answered = getDatafromSuzy.data_from_bot(questionIntent)
                        sleep(1)

                        # while True:
                        #     try:
                        #         botAnswer, answered = getDatafromSuzy.data_from_bot(questionIntent)
                        #     except requests.ConnectionError:
                        #         sleep(1)
                        #         continue
                        #     break

                        mongoDBSheet.export_q_a(questionIntent, answer, botAnswer, answered)

                        break

        print ''
        if not dataQuestion['has_more']:
            break

    except KeyError:
        print 'X',
        # print dataQuestion
