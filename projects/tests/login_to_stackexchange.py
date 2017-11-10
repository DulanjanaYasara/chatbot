# email='dulanjanayasara1@gmail.com'
# password='dyL@1994wso2'
#
# cj=cookielib.CookieJar()
# opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# login_data=urllib.urlencode({'email':'dulanjanayasara1@gmail.com',
#                              'password':'dyL@1994wso2'})
# opener.open('https://stackexchange.com/users/login#log-in',login_data)
# resp=opener.open('https://stackexchange.com/oauth/dialog?client_id=10291&redirect_uri=https%3a%2f%2fstackexchange.com%2foauth%2flogin_success&scope=private_info&response_type=token&state=&returnurl=%2foauth%2fdialog%3fclient_id%3d10291%26redirect_uri%3dhttps%253a%252f%252fstackexchange.com%252foauth%252flogin_success%26scope%3dprivate_info%26response_type%3dtoken%26state%3d')
# print resp.read()
# print resp.url

import requests

EMAIL = 'dulanjanayasara1@gmail.com'
PASSWORD = 'dyL@1994wso2'

URL = 'http://stackexchange.com'


def main():
    # Start a session so we can have persistant cookies
    session = requests.session()

    # This is the form data that the page sends when logging in
    login_data = {
        'loginemail': EMAIL,
        'loginpswd': PASSWORD,
        'submit': 'login',
    }

    # Authenticate
    r = session.post(URL, data=login_data)

    # Try accessing a page that requires you to be logged in
    r = session.get('hhttps://stackexchange.com/users/login#log-in')


if __name__ == '__main__':
    main()





















    # client_id = '10291'
    # client_secret = '3egWossnAd9Oj))dpu21bg(('
    # redirect_uri = 'hhttps://stackexchange.com/oauth/login_success'
    #
    # scope = ['https://www.googleapis.com/auth/userinfo.email',
    #          'https://www.googleapis.com/auth/userinfo.profile']
    # oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
    #                            scope=scope)
    # authorization_url, state = oauth.authorization_url(
    #     'https://accounts.google.com/o/oauth2/auth',
    #     # access_type and approval_prompt are Google specific extra
    #     # parameters.
    #     access_type="offline", approval_prompt="force")
    #
    # >> > print 'Please go to %s and authorize access.' % authorization_url
    # >> > authorization_response = raw_input('Enter the full callback URL')

    # import requests
    # login_url='https://stackexchange.com/users/login#log-in'
    #
    # payload={
    #     'email':'dulanjanayasara1@gmail.com',
    #     'password':'dyL@1994wso2'}
    #
    # session_requests=requests.session()
    #
    # # r=session_requests.get(login_url)
    #
    # s=session_requests.post(login_url,data=payload)#,headers=dict(referer=login_url))
    #
    # print s.status_code
    # # print r.status_code
    #
    # with requests.session() as s:
    #     p=s.post(login_url,data=payload)
    #
    #     # r=s.get(login_url)
    #     # print r.url
    #
    #     print p.url
    #     print p.content
