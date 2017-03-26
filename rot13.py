import webapp2
import cgi
import codecs

form="""
<form method="post">
	<h1>Enter some text to ROT13:</h1>
	<br>
		<textarea rows="7" cols="60" type="text" name= "text">%s</textarea>
		<br>
		hello
		<br>
		<input type="submit">
</form>

"""
#python function to escape characters &<>"
def escape_html(s):
    return cgi.escape(s, quote = True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(form %'')

	def post(self):
		text = self.request.get('text')				#use get to get different paramaters
		rot_text = (codecs.encode(text, 'rot13'))   #encodes typed text into rot13 format
		rot_text = escape_html(rot_text)			#escapes special characters
		self.response.out.write(form %rot_text)		#writes the form again, only this time with the rot13 formatted text

		#use following lines to print out the actual request that is being sent to the browser
		#self.response.headers['Content-Type'] = 'text/plain'
		#self.response.out.write(self.request)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)