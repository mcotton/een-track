#!/usr/bin/env python

#  Routes
#  /
#  /upload/<account_name>

#  Decorators
#  @login_required

import os
import re
import logging

from google.appengine.ext.webapp import template

import webapp2
import urllib2
import json as simplejson

import wsgiref.handlers, logging
import cgi, time, datetime

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required

from usermodels import *  # I'm storing my models in usermodels.py
from EagleEye import *

een = EagleEye()

class MainHandler(webapp2.RequestHandler):
  def get(self, resource=''):
    #Check to see if user is an admin, and display correct link
    admin = users.is_current_user_admin()
    if admin:
      admin_url = users.create_logout_url("/")
      admin_url_text = 'Logout'
    else:
      admin_url = users.create_login_url("/")
      admin_url_text = 'Login'

    template_values = {
      'admin_url': admin_url,
      'admin_url_text': admin_url_text
    }

    render_template(self, 'templates/index.html', template_values)

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
    # these headers are only when deployed
    #if not is_local():
    #  account.country = self.request.headers['X-AppEngine-Country']
    #  account.region = self.request.headers['X-AppEngine-Region']
    #  account.city = self.request.headers['X-AppEngine-City']
    #  account.latlong = self.request.headers['X-AppEngine-CityLatLong']

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
