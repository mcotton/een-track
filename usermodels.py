from google.appengine.ext import db


class Accounts(db.Model):
  name = db.StringProperty()
  startup = db.StringProperty()
  initialPollingState = db.StringProperty()
  startPolling = db.StringProperty()
  useable = db.StringProperty()
  remote_addr = db.StringProperty()
  ua_string = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)
  country = db.StringProperty()
  region = db.StringProperty()
  city = db.StringProperty()
  latlong = db.StringProperty()
  body = db.TextProperty()
