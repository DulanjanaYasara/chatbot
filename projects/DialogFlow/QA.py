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

__dict_intents = {}

# N.B. When two identical question and response set is added, one response gets two User says criteria.
# This has to be avoided. But it never happens by the DialogFlow intent mapping. So it is not handled.

def __check_response(intent_id, response):
    # type: (str, str) -> dict

    """Returns the whole ``intent_dict`` given for a ``intent_id``
    """

    # Sending the request to the API.AI
    respond = requests.get('https://api.dialogflow.com/v1/intents/' + str(intent_id), headers=__headers,
                           params=__params)
    output = respond.json()
    # pprint(output)
    for x in output['responses'][0]['messages']:

        if 'platform' in x:
            # Checking whether the Facebook platform exists
            if x['platform'] == 'facebook':
                if x['speech'] == response:
                    # Return intent dict
                    return output
        else:
            # If no facebook platform exists then the default is considered
            if x['speech'] == response:
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
            'name': 'sem:' + question,
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
    output = requests.post('https://api.dialogflow.com/v1/intents/', json=data, headers=__headers,
                           params=__params).json()

    # Checking for the HTTP status code
    status = output['status']
    if status['code'] in range(400, 500):
        print status['errorDetails']
    else:
        # Adding to the intents dict the new intent
        __dict_intents[response] = output['id']
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


def feed(question, response):
    # type: (str, str) -> None
    """
    Used to feed the question and response to the DialogFlow.
    If response already exists, then create a new intent called question.
    Else the existing intent is updated with the question as UserSays.
    """
    if response in __dict_intents.keys():
        output = __check_response(__dict_intents[response], response)
        if output:
            __update_intent(question, output)
        else:
            print 'Updating the intent failed!'
    else:
        __add_new_intent(question, response)


def test():
    feed('ESB tool', 'ESB is WSO2 main tool.')
    feed('ESB','ESB is WSO2 main tool.')


if __name__ == '__main__':
    test()
