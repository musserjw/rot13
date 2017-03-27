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
import cgi
#value defaults form to a value
#write_form function also needs to have month,day,year values defaulted in the definition and dictionary
form="""
<form method = "post">
	<label>
		Username 
		<input type="text" name="username" value= "%(username)s">
	</label>
	<label>
		Password 
		<input type="text" name="password1" value = %(password1)s>
	</label>
	<label>
		Password 
		<input type="text" name="password2" value= %(password2)s>
	</label>
	<br>
	<br>
	<div>%(error)s</div>
	<br>
	<br>
	<input type="submit">
</form>	
"""
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(),m) for m in months)

def valid_user(username):
	error = false
	if username:
		for n in username:
			if n = " ":
				error = true
	else:
		error = true			
		
def valid_password(password):
	error = false
	if password:
	else:
		error = true

def escape_html(s):
    return cgi.escape(s, quote = True)

class MainPage(webapp2.RequestHandler):

	def write_form(self, username="", password1="", password2=""):
		self.response.out.write(form %{"error": error,
										"username": escape_html(username),
										"password1": escape_html(password1),
										"password2": escape_html(password2)})

	def get(self):		#get draws the empty form
		self.write_form()

	def post(self):		#draws form with new error message
		username = self.request.get('username')
		password1 = self.request.get('password1')
		password2 = self.request.get('password2')

		username = valid_user(username)
		password1 = valid_password(password1)
		password2 = valid_password(password2) 

		if not (username and password1 and password2):
			self.write_form("That doesn't look valid",username, password1, password2)
		else:
			self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! That's a totally valid form!")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
], debug=True)


