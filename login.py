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
import os
import jinja2
import webapp2
import cgi
import re


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape= True)

def valid_user(username=" "):
	user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	return username and user_re.match(username)

def valid_password(password=" "):
	password_re = re.compile(r"^.{3,20}$")
	return password and password_re.match(password)

def valid_email(email):
	email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
	return not email or email_re.match(email)
	
def escape_html(s):
    return cgi.escape(s, quote = True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a,**kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))		



class Signup(Handler):
	def get(self):		#get draws the empty form
		self.render('signup-form.html')

	def post(self):		#draws form with new error message
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get("email")
		
		have_error = False
		params = dict(username = username,
						email = email)

		if not valid_user(username):
			params['error_username'] = "That's not a valid username."
			have_error = True
		if not valid_password(password):
			params['error_password'] = "That's not a valid password."
			have_error = True
		elif password != verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True
		if not valid_email(email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render('signup-form.html',**params)
		else:
			self.redirect("/welcome?username=" + username)

class Welcome(Handler):
	def get(self):
		username = self.request.get('username')
		if valid_user(username):
			self.render('welcome.html', username = username)
		else:
			self.redirect('/signup')	

app = webapp2.WSGIApplication([('/signup', Signup),('/welcome', Welcome)], debug=True)


