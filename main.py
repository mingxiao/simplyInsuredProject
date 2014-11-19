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
import MySQLdb
import jinja2
import os
from GoodRXAPICaller import GoodRXAPICaller

# Configure the Jinja2 environment.
JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),
  autoescape=True,
  extensions=['jinja2.ext.autoescape'])

_INSTANCE_NAME = 'ming-xiao-123:my-instance'

class MainHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
        #self.response.write('Hello world!')

    def post(self):
        drugName = self.request.get('drugName')
        if drugName:
            template = JINJA_ENVIRONMENT.get_template('results.html')
            coverageItemList = []
            if (os.getenv('SERVER_SOFTWARE') and
                os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
                db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='myDatabase', user='root', passwd='internal1')
            else:
                db = MySQLdb.connect(host='173.194.253.143', port=3306, db='myDatabase', user='root', passwd='internal1')
            cursor = db.cursor()
            cursor.execute('SELECT name, carrier,tier FROM formulary_items WHERE NAME = "{}";'.format(drugName))
            for row in cursor.fetchall():
                coverageItemList.append(dict([('name', row[0]),
                                 ('carrier', row[1]),
                                 ('tier', row[2])
                                 ]))
            # get goodRx suggestions
            goodRx = GoodRXAPICaller()
            candidates = goodRx.get_candidates(drugName)
            variables = {'coverageItemList': coverageItemList, 'candidates': candidates}
            self.response.write(template.render(variables))
            db.close()


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
