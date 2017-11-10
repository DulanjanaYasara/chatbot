import requests

# Getting access tokens which are not hard coded
url = 'https://stackexchange.com/oauth/dialog'
values = {'client_id': '10291',
          'scope': 'private_info',
          'redirect_uri': 'https://stackexchange.com/oauth/login_success'}

response = requests.post(url, values)
login_url = response.url + '#log-in'

payload = {
    'email': 'dulanjanayasara1@gmail.com',
    'password': 'dyL@1994wso2'}

session_requests = requests.session()
# login_url='https://stackexchange.com/oauth/dialog?client_id=10291&redirect_uri=https%3a%2f%2fstackexchange.com%2foauth%2flogin_success&scope=private_info&response_type=token&state=&returnurl=%2foauth%2fdialog%3fclient_id%3d10291%26redirect_uri%3dhttps%253a%252f%252fstackexchange.com%252foauth%252flogin_success%26scope%3dprivate_info%26response_type%3dtoken%26state%3d#log-in'

r = session_requests.get(login_url)

s = session_requests.post(login_url, data=payload)  # ,headers=dict(referer=login_url))

print s.status_code
print r.status_code

with requests.session() as s:
    p = s.post(login_url, data=payload)

    r = s.get(login_url)
    print r.url

    print p.text
    print p.url

    # from requests import session
    #
    # payload = {
    #     'action': 'login',
    #     'email':'dulanjanayasara1@gmail.com',
    #     'password':'dyL@1994wso2'}
    #
    # with session() as c:
    #     c.post(login_url, data=payload)
    #     response = c.get('https://www.google.lk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwi4usCQlYHVAhWGwI8KHXmkB9QQFggmMAA&url=https%3A%2F%2Fstackoverflow.com%2Fusers%2Flogin&usg=AFQjCNEWShNhqqCKTEos82raEZ2nM6Iq2Q')
    #     print(response.headers)
    #     print(response.text)
