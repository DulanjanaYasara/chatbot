from locale import str

import requests

import extractData

# #Getting access tokens which are not hard coded
url = 'https://stackexchange.com/oauth/dialog'
values = {'client_id': '10291',
          'scope': 'private_info',
          'redirect_uri': 'https://stackexchange.com/oauth/login_success'}

response = requests.post(url, values)
print response.url
print response.content
print response.url + '#log-in'

# Finding the questions with the tag wso2 through the stack overflow API with the use of access tokens
responseQuestion = requests.get("https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&tagged=wso2&site="
                                "stackoverflow&filter=!)5__yhx6tWY6D2(IDoAyXGJG2(hQ&access_token=ZRXAvblZd2Q2QyA12B3g9A))"
                                "&expires=86399&key=b500RPkbAnAO3TH6oRQVew((")

dataQuestion = responseQuestion.json()
# print dataQuestion

# Generating the accepted answer for the given question
for value in dataQuestion['items']:
    if value['is_answered']:
        if 'accepted_answer_id' in value:
            question = extractData.extractall(value['body'])
            print('Intent>>>  ' + value['title'] + '\nQuestion>>>  ' + question)
            acceptedAnswerID = value['accepted_answer_id']
            ids = str(acceptedAnswerID)
            responseAnswer = requests.get(
                'https://api.stackexchange.com/2.2/answers/' + ids + '?order=desc&sort=activity&'
                                                                     'site=stackoverflow&filter='
                                                                     '!9YdnSMKKT')
            dataAnswer = responseAnswer.json()
            for answer in dataAnswer['items']:
                answer = extractData.extractall(answer['body'])
                print('Answer>>>  ' + answer)
                print('_______________________________________________________________________________________')
