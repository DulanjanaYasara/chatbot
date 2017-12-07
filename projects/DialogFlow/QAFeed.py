from pprint import pprint

import requests

# TODO Replace with production developer token
__headers = {
    'Authorization': 'Bearer 634aedabde4b4c8b9b15cd9514a12d69',
    'Content-Type': 'application/json'
}

__params = (
    ('v', '20150910'),
    ('lang', 'en'),
)


def __get_all_intent_ids():
    # type: () -> list
    """Getting all intents from the DialogFlow"""

    # Sending the request to the API.AI
    response = requests.get('https://api.dialogflow.com/v1/intents', headers=__headers, params=__params)
    output = response.json()

    for x in output:
        yield x['id']


def __check_response(intent_id, response):
    # type: (str, str) -> dict

    """Used to check whether a similar response exists in the ``intent_id``
    If exists this returns the ``intent_dict`` else None"""

    # Sending the request to the API.AI
    respond = requests.get('https://api.dialogflow.com/v1/intents/' + str(intent_id), headers=__headers,
                           params=__params)
    output = respond.json()
    # pprint(output)
    for x in output['responses'][0]['messages']:

        if 'platform' in x:
            # Checking whether the Facebook platform exists
            if x['platform'] == 'facebook':
                if __compare_responses(x['speech'], response):
                    # Return intent dict
                    return output
        else:
            # If no facebook platform exists then the default is considered
            if __compare_responses(x['speech'], response):
                # Return intent dict
                return output


def __add_new_intent(question, response):
    # type: (str, str) -> None
    """Used to add a new intent to the DialogFlow"""

    # The json data to be posted to the DialogFlow
    data = {'auto': True,
            'contexts': [],
            'events': [],
            'fallbackIntent': False,
            'name': 'sem:'+ question,
            'priority': 500000,
            'responses': [{'action': '',
                           'affectedContexts': [],
                           'defaultResponsePlatforms': {'facebook': True},
                           'messages': [{'platform': 'facebook',
                                         'speech': response,
                                         'type': 0}],
                           'parameters': [],
                           'resetContexts': False,
                           'speech': []}],
            'templates': [],
            'userSays': [{'count': 0,
                          'data': [{'text': question}],
                          'isAuto': False,
                          'isTemplate': False}],
            'webhookForSlotFilling': False,
            'webhookUsed': False}

    # Posting the request to the API.AI
    output = requests.post('https://api.dialogflow.com/v1/intents/', json=data, headers=__headers, params=__params)
    # Checking for the HTTP status code
    status = output.json()['status']
    if status['code'] in range(400, 500):
        print status['errorDetails']
    else:
        print 'Done adding the new intent!'


def __update_intent(new_question, intent_dict):
    # type: (str, dict) -> None
    """Used to update the intent based on the intent_dict"""


    intent_dict['userSays'] = intent_dict['userSays'] + [{'count': 0,
                                                          'data': [{'text': new_question}],
                                                          'isAuto': False,
                                                          'isTemplate': False}]
    # Putting the request to the API.AI
    output = requests.put('https://api.dialogflow.com/v1/intents/' + intent_dict['id'], json=intent_dict,
                          headers=__headers,
                          params=__params)
    # Checking for the HTTP status code
    status = output.json()['status']
    if status['code'] in range(400, 500):
        print status['errorDetails']
    else:
        print 'Done updating the intent!'


def __compare_responses(existing_resp, new_resp):
    """Used to compare two responses"""
    # TODO compare two responses
    return True if existing_resp == new_resp else False


def feed(question, response):
    # type: (str, str) -> None
    """
    Used to feed the question and response to the DialogFlow.
    If response already exists, then create a new intent called question.
    Else the existing intent is updated with the question as UserSays.
    """

    for id in __get_all_intent_ids():
        output = __check_response(id, response)
        if output:
            __update_intent(question, output)
            break
    else:
        __add_new_intent(question, response)


def test():
    # print(list(__get_all_intent_ids()))
    # print __check_response('3f4bdbc2-2b67-4247-ae62-e0b5dcc23661', 'Doitashimashite')
    feed('Lol','YJ')

if __name__ == '__main__':
    test()
