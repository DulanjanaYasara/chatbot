from locale import str
from time import sleep

import requests

import breaknplay
import extractData
import getDatafromSuzy
import spreadsheet

# Searching based on different tags
search_criteria = [(' ', 'wso2esb'), ('wso2esb', 'wso2;esb')]
row = 1
count_q = 0

for tag in search_criteria:
    page_number = 1

    while True:

        try:
            # Just considering only 100 questions
            if count_q > 100:
                break

            # Finding the questions with the tags through the stack overflow API with the use of access tokens and keys
            # This is considered from 01.01.2016 up to 30.08.2017
            responseQuestion = requests.get(
                "https://api.stackexchange.com/2.2/search/advanced?page=" + str(page_number) +
                "&pagesize=100&fromdate=1451606400&todate=1504051200&order=desc&sort=activity&accepted=True&nottagged="
                + tag[0] + "&tagged=" + tag[1] + "&site=stackoverflow&filter=!*e9ibzERTZv_4jPLGyBUXbiO0TCnjFLALrHd*&"
                                                 "access_token=3*MQ0YtINm2*xpbWplNVKw))&key=b500RPkbAnAO3TH6oRQVew((")

            print str(page_number) + ')',
            page_number += 1

            dataQuestion = responseQuestion.json()
            # print json.dumps(dataQuestion, sort_keys=True, indent=7)

            # Generating the accepted answer for the given question
            for value in dataQuestion['items']:

                # Extracting the question and deciding whether they have codes or blockquotes
                question, q_has_codes_errors = extractData.extractall(value['body'])

                questionIntent = extractData.extractall(value['title'])[0]
                # print('Intent>>>  ' + questionIntent + '\nQuestion>>>  ' + question)

                for answer in value['answers']:
                    if answer['is_accepted']:
                        # Extracting the answer and deciding whether they have codes or blockquotes
                        answer, a_has_codes_errors = extractData.extractall(answer['body'])
                        # print('Answer>>>  ' + answer)
                        # print('_______________________________________________________________________________________')

                        # Checking for question and answer suitability to be asked from the bot
                        suitable = not q_has_codes_errors and not a_has_codes_errors

                        # Sleeping for 1s due to throttling of data after each API.AI call
                        # botAnswer, answered = getDatafromSuzy.data_from_bot(question)
                        # sleep(1)

                        if suitable:
                            while True:
                                try:
                                    # Checking the length of the question
                                    if len(question) < 256:
                                        botAnswer, answered = getDatafromSuzy.data_from_bot(question)
                                        sleep(1)
                                        if answered:
                                            row += 1
                                            spreadsheet.exportQ_A(questionIntent, '', question, botAnswer, answer, row)
                                            count_q += 1
                                            print count_q,

                                    else:
                                        # If the question has no codes and blockquotes, then the question is broke
                                        # and given to the bot 'Break and Play'
                                        entities, bot_ans = breaknplay.breaknplay_bot(question)
                                        sleep(1)
                                        row += 1
                                        spreadsheet.exportQ_A(questionIntent, entities, question, bot_ans, answer, row)
                                        count_q += 1
                                        print count_q,

                                    break
                                except requests.ConnectionError:
                                    print '!',
                                    sleep(2)
                                except KeyError:
                                    print '#', questionIntent,
                                    botAnswer, answered = None, False
                                    break

                        break

            print ''
            if not dataQuestion['has_more']:
                break

        except KeyError:
            print 'X'
            # print dataQuestion
        except requests.ConnectionError:
            print '!',
            sleep(1)
