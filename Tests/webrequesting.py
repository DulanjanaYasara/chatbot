import requests

# Below one generates
# accepted_answer_id,is_answered,link,question_id,title,body
# response=requests.get("https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&tagged=wso2&site=stackoverflow&filter=!.Iwe-B09iLj4z6ub6U65dTukFYGE4")

# ................
# answer.accepted,accepted_answer_id,is_answered,title,body

#######last_activity_date,question_id,
response = requests.get(
    "https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&tagged=wso2&site=stackoverflow&filter=!)5__yhx6tWY6D2(IDoAyXGJG2(hQ&access_token=LzXrRsKRaNpgKjV9ia*q9A))&expires=86399&key=b500RPkbAnAO3TH6oRQVew((")

# response=requests.get("https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&tagged=wso2&site=stackoverflow&filter=!SzU*70pO307kT-PAb2&access_token=6yveqvn2evgJp(Dz8vqDAQ))&key=b500RPkbAnAO3TH6oRQVew((")

# data=response.json()

print(response.content)
# print(response.headers)




##Gives question title and link
# https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&tagged=wso2&site=stackoverflow&filter=!bA1d_Kvv2YPQWk


# Getting access tokens
'''
def getAccessToken(request_code):
    headers = {'Content-Type' : 'application/json; charset=utf-8','X-Accept': 'application/json'}
    request_data = json.dumps({"consumer_key":"12092-2970cc0e27ce9a25cb39f1dd","code":["af0f6c9b-815b-cd1d-9864-b6d375"]})
    url = "https://www.facebook.com/v3/oauth/authorize"

    response_data = makeRequest(headers,request_data,url)
    access_code, username = response_data['access_token'],response_data['username']

    return access_code,username

def makeRequest(request_headers,request_data,request_url):
    request = urllib2.Request(request_url,request_data,request_headers)
    response = urllib2.urlopen(request)
    data = json.load(response)

    return data
'''
'''
import requests

response=requests.get("https://stackexchange.com/oauth/dialog?client_id=10291&scope=private_info&redirect_uri=https://facebook.com")

print(response.headers)
'''
'''
https://www.facebook.com/?code=U4royA6lU3cGj8*MlTg8jg))

code=U4royA6lU3cGj8*MlTg8jg))
'''
'''
import requests
url = 'https://stackexchange.com/oauth/access_token/json'
payload = {'client_id': 10291, 'client_secret': '3egWossnAd9Oj))dpu21bg((','code':'U4royA6lU3cGj8*MlTg8jg))'}

# GET
#r = requests.get(url)

# GET with params in URL
#r = requests.get(url, params=payload)

# POST with form-encoded data
#r = requests.post(url, data=payload)

# POST with JSON 
import json
r = requests.post(url, data=json.dumps(payload))

# Response, status etc
print(r.text)
print(r.status_code)
'''

# with implicit oauth 2.0 access_token=LzXrRsKRaNpgKjV9ia*q9A))&expires=86399
