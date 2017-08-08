import requests


def data_from_bot(question, answered=True):
    headers = {
        'Authorization': 'Bearer 9cb2320c9a5c421baa83dc9134237753',
        'Content-Type': 'application/json;charset = utf-8'
    }

    params = (
        ('v', '20150910'),
        ('query', question),
        ('lang', 'en'),
        ('sessionId', '0181c391-a8fb-4c0d-942a-cb19b704d37e'),
    )

    response = requests.get('https://api.api.ai/api/query', headers=headers, params=params)
    output = response.json()

    if output['result']['metadata']['intentName'] == 'default_fallback':
        answered = False

    return output['result']['fulfillment']['messages'][0]['speech'], answered
