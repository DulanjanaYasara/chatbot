import requests

# answer.accepted,accepted_answer_id,is_answered,title,body

#######last_activity_date,question_id,
# response=requests.get("https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&tagged=wso2&site=stackoverflow&filter=!0W6RWJMS(vxTE2dnIazlX18V-&access_token=LzXrRsKRaNpgKjV9ia*q9A))&expires=86399&key=b500RPkbAnAO3TH6oRQVew((")

responseQ = requests.get(
    "https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&tagged=wso2&site=stackoverflow&filter=!)5__yhx6tWY6D2(IDoAyXGJG2(hQ&access_token=LzXrRsKRaNpgKjV9ia*q9A))&expires=86399&key=b500RPkbAnAO3TH6oRQVew((")

data = responseQ.json()
# print(data)


for value in data['items']:
    if value['is_answered']:
        if 'accepted_answer_id' in value:
            acceptedAnswerID = value['accepted_answer_id']
            ids = str(acceptedAnswerID)
            print(ids + '\n Intent>>>  ' + value['title'] + '\n Question>>>  ' + value['body'])

            responseA = requests.get(
                'https://api.stackexchange.com/2.2/answers/' + ids + '?order=desc&sort=activity&site=stackoverflow')
            dataA = responseA.json()
            print(dataA)

'''
 		if value['is_accepted']:
			print('Yes')
'''

# print(response.headers)
# How to get refresh tokens??

# generated result
'''
{"items":[
		{"is_answered":	"title":	"body":
		},
		{"is_answered":	"title":	"body":
		},
	],
"has_more":
"quota_max":
"quota_remaining"
}


def recursive_iter(obj):
    if isinstance(obj, dict):
        for item in obj.values():
            yield from recursive_iter(item)
    elif any(isinstance(obj, t) for t in (list, tuple)):
        for item in obj:
            yield from recursive_iter(item)
    else:
        yield obj

data = json.loads(my_json_data)
for item in recursive_iter(data):
    print(item)

'''
