import requests


def data_from_bot(question, answered=True):
    """Getting the answer from the bot"""
    while True:
        headers = {
            'Authorization': 'Bearer 125d1e9ed0244787a8b19f727308dc9e',
            'Content-Type': 'application/json;charset = utf-8'
        }

        params = (
            ('v', '20150910'),
            ('query', question),
            ('lang', 'en'),
            ('sessionId', '2e1b05dd-d8ba-448c-93c6-ca8289ce04c0'),
            ('timezone', '2017-08-09T14:01:19 0530'),
        )

        # Sending the request to the API.AI
        response = requests.get('https://api.api.ai/api/query', headers=headers, params=params)
        output = response.json()

        # Obtaining the HTTP status code
        http_code = output['status']['code']

        # Handling the HTTP status code
        # Client errors
        if http_code in range(400, 500):
            return output['status']['errorDetails'], False

        # Server errors
        elif http_code in range(500, 600):
            print 'E',
        else:
            # Filtering the unanswered questions
            if not output['result']['metadata'] or output['result']['metadata'][
                'intentName'] in ['Default Fallback Intent', 'default_welcome - apim', 'default_welcome - is']:
                answered = False

            # Obtaining the answer
            if 'speech' in output['result']['fulfillment']['messages'][0]:
                ans = output['result']['fulfillment']['messages'][0]['speech']
                if ans == "":
                    answered = False
            else:
                ans = ""
                answered = False

            return ans, answered
