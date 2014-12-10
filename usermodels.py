from google.appengine.ext import db


class Accounts(db.Model):
  name = db.StringProperty()
  remote_addr = db.StringProperty()
  ua_string = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)
  country = db.StringProperty()
  region = db.StringProperty()
  city = db.StringProperty()
  latlong = db.StringProperty()
  body = db.TextProperty()
  SystemName = db.StringProperty()
  PlateNumber = db.StringProperty()
  cameraname = db.StringProperty()
  GMTDateTime = db.StringProperty()
  DateTime = db.StringProperty()
  Longitude = db.StringProperty()
  Latitude = db.StringProperty()
  CharHeight = db.StringProperty()
  CarImage = db.StringProperty()
  PlateImage = db.StringProperty()
