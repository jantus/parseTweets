from flask import Flask
from flask import render_template

flaskapp = Flask(__name__)

worker_info_string = ""
statusLink = "<a href='status'>Worker Status</a>"

def create_html():
	pass

def create_header():
	pass

def create_body():
	body = "<div style='width:200px: margin-left: auto; margin-right:auto;'>hello</div>"
	return body

def create_footer():
	pass

def update_body():
	pass

def set_function(function):
	global worker_information 
	worker_information = function
	

@flaskapp.route('/')
def api_root():
	return "Welcome"+statusLink+"\n"


@flaskapp.route('/status')
def api_status():
	# do work to print status of worker
	info = worker_information()
	#return "This is a status page"+statusLink+ "\n las" + worker_info_string
	return render_template('index.html', info=info)

def run_app():
	print "running flaskapp"
	flaskapp.run(debug=True)


