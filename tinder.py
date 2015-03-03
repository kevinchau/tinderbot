import requests
import json
from time import sleep
from random import randint

# Variables

FACEBOOKID = ''
FACEBOOKTOKEN = ''

# Todo: Dynamically generate these numbers:

LASTMODIFIED = 'Mon, 21 Apr 2014 04:48:31 GMT'
LASTETAG = '-1022732152'

# Facebook Auth

def facebookAuth():
  print 'Grabbing X-Auth-Token via Facebook'
  url = 'https://api.gotinder.com/auth'
  headers = {
  'app_version': '3',
  'platform': 'ios',
  'User-Agent': 'Tinder/3.0.4 (iPhone; iOS 7.1; Scale/2.00)',
  'os_version': '700001',
  'Content-Type': 'application/json; charset=utf-8',
  'Host': 'api.gotinder.com',
  'Connection': 'keep-alive',
  'Accept-Encoding': 'gzip, deflate',
  'Content-Length': '297',
  }
  payload = {
    'facebook_id': FACEBOOKID,
    'facebook_token': FACEBOOKTOKEN
  }
  a = requests.post(url, headers=headers, data=json.dumps(payload))
  return a.json()['token']


# Get Users Function

def getData():

  global LASTMODIFIED

  print 'Getting Users'
  url = 'https://api.gotinder.com/user/recs'
  headers = {
  'app_version': '3',
  'platform': 'ios',
  'User-Agent': 'Tinder/3.0.4 (iPhone; iOS 7.1; Scale/2.00)',
  'os_version': '700001',
  'Content-Type': 'application/json; charset=utf-8',
  'Host': 'api.gotinder.com',
  'Connection': 'Keep-Alive',
  'Accept-Encoding': 'gzip',
  'Content-Length': '12',
  # 'If-None-Match': LASTETAG,
  'If-Modified-Since': LASTMODIFIED,
  'X-Auth-Token': AUTHKEY
  }
  payload = {'limit':'40'}
  try:
    g = requests.post(url, headers=headers, data=json.dumps(payload))
    return g.json()
    LASTMODIFIED = g.headers['date']
  except:
    return {'status':500}


# Like Users Function

def likeUser(user_id):
  likeurl = 'https://api.gotinder.com/like' + user_id
  likeheaders = {
  'app_version': '3',
  'platform': 'ios',
  'User-Agent': 'Tinder/3.0.4 (iPhone; iOS 7.1; Scale/2.00)',
  'os_version': '700001',
  'Host': 'api.gotinder.com',
  'Connection': 'Keep-Alive',
  'Accept-Encoding': 'gzip',
  'X-Auth-Token': AUTHKEY
  }
  l = requests.get(likeurl, headers=likeheaders)

# Change Location

def changeLocation():
  locateurl = 'https://api.gotinder.com/user/ping'
  locateheaders = {
  'Host': 'api.gotinder.com',
  'User-Agent': 'Tinder/3.0.4 (iPhone; iOS 7.1; Scale/2.00)',
  'os_version': '700001',
  'platform': 'ios',
  'Content-Type': 'application/json; charset=utf-8',
  'Connection': 'Keep-Alive',
  'X-Auth-Token': AUTHKEY,
  'Proxy-Connection': 'keep-alive',
  'Authorization': 'Token token="%s"' % AUTHKEY,
  'app_version': '3',
  'Content-Length': '50',
  'Accept-Encoding': 'gzip, deflate'
  }
  location = {
  'lat': LATITUDE,
  'lon': LONGITUDE
  }
  x = requests.post(locateurl, headers=locateheaders, data=json.dumps(location))
  print x.json()
  return x.json()

# Choose City

def chooseCity(city):

  global LATITUDE
  global LONGITUDE
  global selected_city

  if city == 'sea':
    LATITUDE = 47.45055051964678
    LONGITUDE = -122.2058067215779
    selected_city = 'Seattle'

  elif city == 'nyc':
    LATITUDE = 40.76338451964678
    LONGITUDE = -73.98075047215779
    selected_city = 'Manhattan'

  elif city == 'sf':
    LATITUDE = 37.7866091964678
    LONGITUDE = -122.40961647215779
    selected_city = 'San Francico'

  elif city == 'pdx':
    LATITUDE = 45.5319331964678
    LONGITUDE = -122.69283147215779
    selected_city = 'Portland'

  else:
    LATITUDE = 47.45055051964678
    LONGITUDE = -122.2058067215779
    selected_city = 'Default to Seattle'

# Primary Function

if __name__ == "__main__":

  count = 1
  chooseCity(raw_input('Choose SEA/NYC/SF/PDX: ').lower())
  AUTHKEY = facebookAuth()
  
  while True:
   approved = changeLocation()
   sleep(10)
   if approved['status'] == 200:
    break

  print 'Authorized and Location Updated'
  print selected_city

  while True:

    users = getData()

    if users['status'] == 200:
      
      for user in users['results']:
        print count,': Liking ', user['name'], ' ', user['photos'][0]['url']
        likeUser(user['_id'])
        sleep(randint(2,10))
        count = count + 1
   
      t = randint(60,180)
      print 'Sleeping ', t, ' ', 'seconds'
      sleep(t)
      del t

    else:
      print 'Seems to be an error - Re-Authing after waiting 3000 seconds'
      sleep(3000)
      AUTHKEY = facebookAuth()
      count = 1


