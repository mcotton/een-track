import re, urllib, logging, datetime, time
from google.appengine.api import memcache
from google.appengine.api import urlfetch
import json as simplejson
from google.appengine.ext import db
from usermodels import *  # I'm storing my models in usermodels.py

class EagleEye():

  def __init__(self):
    self.cookie = ''
    self.host = "https://apidocs.eagleeyenetworks.com"

  def login(self):
    logging.info('starting login()')
    url = self.host + "/g/aaa/authenticate"
    username = memcache.get('username')
    password = memcache.get('password')

    if not username and not password:
      logging.warning('username and password are not in memcache, pulling latest from datastore')
      c = Credentials().all().filter('active =', True).fetch(1)
      if c:
        #found a record
        for i in c:
          username = i.username
          password = i.password
      else:
        logging.error("no credentials in memcache or datastore")
        return False

    payload = {'username': username, 'password': password}

    result = urlfetch.fetch(url=url,
                            payload=simplejson.dumps(payload),
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/json'})

    if result.status_code == 200:
      url = self.host + "/g/aaa/authorize"
      payload = {'token': simplejson.loads(result.content)['token']}

      result = urlfetch.fetch(url=url,
                              payload=simplejson.dumps(payload),
                              method=urlfetch.POST,
                              headers={'Content-Type': 'application/json'})

      matches = re.search('videobank_sessionid=([\w]*);', result.headers['set-cookie'])
      self.cookie = matches.group(1)
      memcache.set('auth_token', self.cookie)
      memcache.set('full_cookie', result.headers['set-cookie'])
      logging.info('done login()')
      return simplejson.loads(result.content)


  def get_auth(self):
    token =  memcache.get('auth_token')
    if token:
      return token
    else:
      logging.info("don't have a cookie in memcache, calling login()")
      self.login()

  def handle_401(self):
    memcache.set('auth_token', None)
    logging.info('caught a 401, clearing memcache and calling login()')
    self.login()

  def get_image(self, esn, direction='prev'):
    #check if we already have a good image
    last = memcache.get(esn + '_last_image_update')
    if last:
      last = self.StoD(last)
      delta = last + datetime.timedelta(seconds=1)
      if delta > datetime.datetime.today():
        logging.info('returning image from memcache for %s' % esn)
        return memcache.get(esn + '_last_image')
      else:
        logging.info('image in memcache is %s stale.' % str(datetime.datetime.today() - last))

    token = self.get_auth()
    if token is not None:
      pattern = self.host + "/asset/%s/image.jpeg?c=%s&t=now&a=pre&A=%s"
      url = pattern % (direction, esn, token)
      result = urlfetch.fetch(url=url)

      if result.status_code == 200:
        memcache.set(esn + '_last_image_update', result.headers['x-ee-timestamp'][8:])
        memcache.set(esn + '_last_image', result.content)
        return result.content

      if result.status_code == 401:
        self.handle_401()
        self.get_image(esn)
    else:
      pass


  def get_device_list(self):
    token = self.get_auth()
    if token is not None:
      url = self.host + "/g/list/devices"
      result = urlfetch.fetch(url=url,
                              headers={'Content-Type': 'application/json',
                                       'Cookie': memcache.get('full_cookie')})
      if result.status_code == 200:
        logging.info('successfully grabbed list devices')
        return simplejson.loads(result.content)

      if result.status_code < 200:
        logging.warning('%s when getting list devices' % result.status_code)

      if result.status_code == 401:
        self.handle_401()

      return list()

    else:
      self.login()

  def make_all_not_active(self):
    c = Credentials().all().filter('active =', True)
    collection = []
    for i in c:
      i.active = False
      collection.append(i)
    db.put(collection)

  def StoD(self, date_str):
    return datetime.datetime(int(date_str[0:4]),
                             int(date_str[4:6]),
                             int(date_str[6:8]),
                             int(date_str[8:10]),
                             int(date_str[10:12]),
                             int(date_str[12:14]))
