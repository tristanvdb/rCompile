import os
import sys
import json

import flask
from flask import Flask

app = Flask(__name__)

@app.route('/exec', methods=['POST'])
def rCompile_exec():
	try:
		query = flask.request.get_json(force=True)
	except Exception as e:
		print e
		raise
	
	if not 'uuid' in query:
		return ( "Query needs 'uuid' field." , 400 )

	return ( flask.jsonify({ 'uuid' : query['uuid'] }), 200 )

@app.route('/', methods=['GET'])
def rCompile_index():
	return flask.redirect(flask.url_for('static', filename='index.html'))

if __name__ == '__main__':
	app.run(debug=True)

