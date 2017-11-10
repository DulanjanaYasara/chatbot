from locale import str
from time import sleep

import requests

import breaknplay
import extractData
import get_data_from_suzy

no_accepted_answers = 0
no_q_given_to_bot = 0

# Removing the data in the database
# mongoDBSheet.remove_data()

# Searching based on different tags
search_criteria = [(' ', 'wso2esb'), ('wso2esb', 'wso2;esb')]

for tag in search_criteria:
    page_number = 1

    while True:

        try:
            if page_number == 3:
                break

            # Finding the questions with the tags through the stack overflow API with the use of access tokens and keys
            response_question = requests.get(
                "https://api.stackexchange.com/2.2/search/advanced?page=" + str(page_number) +
                "&pagesize=100&order=desc&sort=activity&accepted=True&nottagged=" + tag[0] + "&tagged="
                + tag[
                    1] + "&site=stackoverflow&filter=!*e9ibzERTZv_4jPLGyBUXbiO0TCnjFLALrHd*&access_token=3*MQ0YtINm2*xp"
                         "bWplNVKw))&key=b500RPkbAnAO3TH6oRQVew((")

            # previous filter !-*f(6rc.(Xr5
            print '%02d' % page_number,
            page_number += 1

            data_question = response_question.json()
            # print json.dumps(dataQuestion, sort_keys=True, indent=7)

            # Generating the accepted answer for the given question
            for value in data_question['items']:

                # Counting the number of accepted answers
                no_accepted_answers += 1
                # Extracting the question and deciding whether they have codes or blockquotes
                question, q_has_codes_errors = extractData.extractall(value['body'])

                questionIntent = extractData.extractall(value['title'])[0]
                # print('Intent>>>  ' + questionIntent + '\nQuestion>>>  ' + question)

                # If the question has codes and blockquotes, then the question is broke and given to the bot
                # Break and Play
                breaknplay.breaknplay_bot(q_has_codes_errors, questionIntent, value['body'])

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
                                        botAnswer, answered = get_data_from_suzy.data_from_bot(question)
                                        has_to_summarize = False
                                    else:
                                        botAnswer, answered, has_to_summarize = "Long input", False, True
                                    # print '.',

                                    # Counting the questions given to the bot
                                    no_q_given_to_bot += 1
                                    break
                                except requests.ConnectionError:
                                    print '!',
                                    sleep(1)
                                except KeyError:
                                    print '#', questionIntent,
                                    botAnswer, answered = None, False
                                    break

                                    # Feeding question instead of the question intent
                                    # mongoDBSheet.export_q_a(question, questionIntent, answer, botAnswer, answered,
                                    #                         has_to_summarize)
                        # else:
                        #     mongoDBSheet.not_given_bot(questionIntent, question, answer)

                        break

            print ''
            if not data_question['has_more']:
                break

        except KeyError:
            print 'X'
            # print data_question
        except requests.ConnectionError:
            print '!',
            sleep(1)

            # extractData.print_all(no_accepted_answers, no_q_given_to_bot)
