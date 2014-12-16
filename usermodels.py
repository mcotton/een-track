from google.appengine.ext import db


class Accounts(db.Model):
  name = db.StringProperty()
  remote_addr = db.StringProperty()
  ua_string = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)
  body = db.TextProperty()
  SystemName = db.StringProperty()
  PlateNumber = db.StringProperty()
  cameraname = db.StringProperty()
  GMTDateTime = db.StringProperty()
  DateTime = db.StringProperty()
  Longitude = db.StringProperty()
  Latitude = db.StringProperty()
  CharHeight = db.StringProperty()
  CarImage = db.TextProperty()
  PlateImage = db.TextProperty()
