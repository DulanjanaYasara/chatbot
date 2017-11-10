json = {
    "id": "5c21c20c-9405-4426-bb42-b5c08bb693e7",
    "timestamp": "2017-08-09T05:42:37.521Z",
    "lang": "en",
    "result": {
        "source": "domains",
        "resolvedQuery": "Why do message sampling processors stop probing messages?",
        "action": "smalltalk.confirmation.yes",
        "actionIncomplete": "false",
        "parameters": {},
        "contexts": [],
        "metadata": {},
        "fulfillment": {
            "speech": "Sure.",
            "messages": [
                {
                    "type": 0,
                    "speech": "Of course."
                }
            ]
        },
        "score": 1
    },
    "status": {
        "code": 200,
        "errorType": "success"
    },
    "sessionId": "2e1b05dd-d8ba-448c-93c6-ca8289ce04c0"
}

print json['result']['metadata']
if not json['result']['metadata']:
    print 'Hi'
