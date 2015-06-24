#!/usr/bin/env python

import flask
 
app = flask.Flask(__name__)

@app.route('/')
def index():
	return "hello World :)" 
 
@app.route('/link')
def show_link():
   try:
      with open('link.txt','r') as f:
         lines = f.readlines()
   except Exception as e:
      print e
   return flask.render_template('link.html',lines=lines)

 

