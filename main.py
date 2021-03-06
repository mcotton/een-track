#!/usr/bin/env python

#  Routes
#  /
#  /upload/<account_name>

import os
import re
import logging

import sys
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup

from google.appengine.ext.webapp import template

import webapp2
import json as simplejson

import wsgiref.handlers, logging
import cgi, time, datetime

from google.appengine.ext.webapp.util import run_wsgi_app

from usermodels import *  # I'm storing my models in usermodels.py
from EagleEye import *

een = EagleEye()

class MainHandler(webapp2.RequestHandler):
  def get(self, resource=''):

    accounts = Accounts().all().fetch(10)    

    template_values = {
      'accounts': accounts
    }

    render_template(self, 'templates/list.html', template_values)

class UploadHandler(webapp2.RequestHandler):
  def get(self, resource=''):
    template_values = {
        'error_code': 'ERR0005'
    }
    render_template(self, 'templates/viper.html', template_values)
    
  def post(self, resource='not supplied'):
    account = Accounts()
    account.name = resource
    account.ua_string = self.request.headers['User-Agent']
    account.remote_addr = self.request.remote_addr
    account.body = self.request.body

    soup = BeautifulSoup(self.request.body)

    try:
      account.SystemName = str(soup.find('systemname').string)
      account.PlateNumber = str(soup.find('platenumber').string)
      account.cameraname = str(soup.find('cameraname').string)
      account.GMTDateTime = str(soup.find('gmtdatetime').string)
      account.DateTime = str(soup.find('datetime').string)
      account.Longitude = str(soup.find('longitude').string)
      account.Latitude = str(soup.find('latitude').string)
      account.CharHeight = str(soup.find('charheight').string)
      account.CarImage = str(soup.find('carimage').string)
      account.PlateImage = str(soup.find('plateimage').string)
    except AttributeError, TypeError:
      logging.info('XML parse error:', self.request.body)
      pass

    account.put()
    template_values = {
        'error_code': 'ERR0000'
    }
    render_template(self, 'templates/viper.html', template_values)


def is_local():
  # Turns on debugging error messages if on local env
  return os.environ["SERVER_NAME"] in ("localhost")

def render_template(call_from, template_name, template_values=dict()):
  # Makes rendering templates easier.
  path = os.path.join(os.path.dirname(__file__), template_name)
  call_from.response.out.write(template.render(path, template_values))

def render_json(self, data):
  self.response.headers['Content-Type'] = 'application/json'
  self.response.out.write(simplejson.dumps(data))



app = webapp2.WSGIApplication([('/', MainHandler),
                              ('/upload/([^/]+)?', UploadHandler)],
                              debug = is_local())
