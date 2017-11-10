# response=requests.get("https://stackexchange.com/oauth/dialog?client_id=10291&scope=private_info&redirect_uri=https://stackexchange.com/oauth/login_success")
# print(response.headers)
'''
import urllib
from urllib2 import urlopen
from urlparse import urlparse

def app_access_token(app_id, scope):
  resp = urlopen('https://stackexchange.com/oauth/dialog?client_id='+app_id+'&scope='+scope+'&redirect_uri=https://stackexchange.com/oauth/login_success')
  if resp.getcode() == 200:
      #url=resp.geturl()
      #return url.rsplit('#', 1)[-1]
      return (urllib.unquote(resp.geturl()))


  else:
      return None


print app_access_token('10291','private_info')


import urllib
import urllib2

url = 'https://stackexchange.com/oauth/dialog'
values = {'client_id' : '10291',
          'scope' : 'private_info',
          'redirect_uri' : 'https://stackexchange.com/oauth/login_success' }

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()

print the_page
'''
import requests

url = 'https://stackexchange.com/oauth/dialog'
values = {'client_id': '10291',
          'scope': 'private_info',
          'redirect_uri': 'https://stackexchange.com/oauth/login_success'}

response = requests.get(url, values)
response2 = requests.get(response.url)
print response2.url
print response2.history
print response2.url.rsplit('#', 1)[-1]
