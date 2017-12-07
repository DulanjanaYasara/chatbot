from locale import str
from pprint import pprint
from time import sleep
from commons.data.stackoverflow import extract
from commons.spreadsheet import SpreadsheetConnector
import requests


def ask_kb(question):
    params = (
        ('question', question),
    )

    # Sending the request
    response = requests.get('http://203.94.95.153/content', params=params)
    output = response.json()
    return output['answers'][0]['answer']


connector = SpreadsheetConnector('./projects/SO_Is_Answering/stackoverflow-c4d9f5fefce1.json')

# Searching based on different tags
tags = ['wso2',                     # WSO2
        'wso2-am',                  # API Manager
        'wso2as',                   # Application Server
        'wso2bam',                  # Business Activity Monitor
        'wso2bps',                  # Business Process Server
        'wso2brs',                  # Business Rules Server
        'wso2carbon',               # WSO2 Carbon
        'wso2cep',                  # Complex Event Processor
        'wso2-das',                 # Data Analytics Server
        'wso2dss',                  # Data Services Server
        'wso2elb',                  # Elastic Load Balancer
        'wso2esb',                  # Enterprise Service Bus
        'wso2es',                   # Enterprise Store
        'wso2greg',                 # Governance Registry
        'wso2is',                   # Identity Server
        'wso2ml',                   # Machine Learner
        'wso2mb',                   # Message Broker
        'wso2ss',                   # Storage Server
        'wso2ues',                  # User Engagement Server
        'wso2developerstudio',      # WSO2 Developer Studio
        'wso2-emm',                 # Enterprise Mobility Manager
        'wso2ppaas',                # WSO2 Private PaaS
        'wso2stratos',              # Private Cloud
        'wso2cloud',                # WSO2 Cloud
        'wso2msf4j']                # WSO2 Micro-services Framework for Java

# Obtaining the searching criteria
search_criteria1 = ' or '.join(['['+x+']' for x in tags])
# search_criteria2 = ' or '.join(['['+x+']' for x in tags[len(tags)/2:]])

row = 2
page_number = 1
tot_qs = []

while True:

    try:

        question_no = 0
        # Finding the questions with the tags through the Stack Exchange API with the use of access tokens and keys
        responseQuestion = requests.get(
            "https://api.stackexchange.com/2.2/search/advanced?page=" + str(page_number) +
            "&pagesize=100&order=desc&sort=activity&q=" + search_criteria1 + "&accepted=True&site=stackoverflow&filter="
            "!*e9ibzERTZv_4jPLGyBUXbiO0TCnjFLALrHd*&access_token=3*MQ0YtINm2*xpbWplNVKw))&key=b500RPkbAnAO3TH6oRQVew((")

        print 'Page no.', page_number
        page_number += 1

        dataQuestion = responseQuestion.json()

        # Generating the accepted answer for the given question
        for value in dataQuestion['items']:

            # Extracting the question
            question = extract(value['body'])
            questionIntent = extract(value['title'])

            for answer in value['answers']:
                if answer['is_accepted']:
                    # Extracting the answer
                    answer = extract(answer['body'])

                    while True:
                        try:

                            if ask_kb(questionIntent) == 'Sorry, I don\'t know the answer for that.':
                                print questionIntent
                                connector.export_row("Stackoverflow", row, sheetNo=1, column_data=[questionIntent, question], column_index=[1, 2])
                                question_no += 1
                                row += 1

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
        print 'Total no. of unanswered questions within page :', question_no
        tot_qs.append(question_no)

        if not dataQuestion['has_more']:
            break

    except KeyError:
        print 'X'
        # print dataQuestion
    except requests.ConnectionError:
        print '!',
        sleep(1)


print 'Total no. of question intents unanswered :', sum(tot_qs)
