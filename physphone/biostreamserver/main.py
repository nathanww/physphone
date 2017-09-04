#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
from google.appengine.api import memcache
from random import *
from google.appengine.ext import db

class sleepdata(db.Model):
  sleepdat = db.TextProperty(required=True)

class privacy(webapp2.RequestHandler):
    def get(self):
      self.response.out.write('''<h1>Privacy policies</h1>
<b>PhysPhone</b><br>
When you use PhysPhone, your phone measures the intensity of red light transmitted though your skin. This red light measurement is transmitted to our server, which allows you to read the data using other apps.
<br><br>
The information we collect is limited to light readings. Raw images from the camera are never collected or sent. 
<br><br>
The server keeps logs of incoming requests for use in troubleshooting and research. Data from your phone may be associated with your IP address and anonymous "stream ID", but are not associated with any identifying information or information about your health.''')

class sendStream(webapp2.RequestHandler):
    def get(self):
        try:
            trigger=self.request.get("trigger",default_value="N/A")
            rawData=self.request.get("rawdata",default_value="0")
            sample=self.request.get("sample",default_value="0")
            xacc=self.request.get("xacc",default_value="0")
            yacc=self.request.get("yacc",default_value="0")
            zacc=self.request.get("zacc",default_value="0")
            key=self.request.get("streamname",default_value="0")
            if (memcache.set(key,trigger+","+rawData+","+sample+","+xacc+","+yacc+","+zacc,time=30)):
                self.response.out.write("Ok!")
            else:
                self.response.out.write("Err")
        except Exception:
            self.response.out.write("Err")
class getStream(webapp2.RequestHandler):
    def get(self):
        try:
            foo=memcache.get(self.request.get("stream",default_value="0"))
            if foo:
                self.response.out.write("Trigger, data, sample,xacc,yacc,zacc\n"+foo)
            else:
                foo2="Trigger, data, sample,xacc,yacc,zacc\n0,0,0,0,0,0"
                self.response.out.write(foo2)            
        except Exception:
            self.response.out.write("Err")
class logSleep(webapp2.RequestHandler):
    def post(self):
        e = sleepdata(sleepdat=db.Text(str(self.request.arguments())))
        e.put()
    def get(self):
        e = sleepdata(sleepdat=self.request.get('results'))
        e.put()
        self.response.out.write(self.request.get('results'))

app = webapp2.WSGIApplication([
    ('/sendStream', sendStream),('/get', getStream),('/sleepdata', logSleep),('/privacy', privacy)
], debug=True)
