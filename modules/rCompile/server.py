
import os
import sys
import json
import shutil

import rCompile

import flask
from flask import Flask

app = Flask(__name__)

def write_client_files(files):
	pass # TODO

def exec_client_command(command):
	return ('','') # TODO

def save_generated_and_modified_files(files):
	return dict() # TODO

@app.route('/exec', methods=['POST'])
def rCompile_exec():
	try:
		query = flask.request.get_json(force=True)
	except Exception as e:
		print e
		raise
	
	if not 'uuid' in query:
		return ( "Query needs 'uuid' field." , 400 )

	if not 'command' in query:
		return ( "Query needs 'command' field." , 400 )

	if not 'files' in query:
		return ( "Query needs 'files' field." , 400 )

	response = { 'uuid' : query['uuid'] }

	old_workdir = os.getcwd()

	workdir = '{}/{}'.format(rCompile.config['tmpdir'], query['uuid'])
	os.mkdir(workdir)
	os.chdir(workdir)

	write_client_files(query['files'])

	(stdout,stderr) = exec_client_command(query['command'])
	response.update({ 'stdout' : stdout, 'stderr' : stderr })

	response.update({ 'files' : save_generated_and_modified_files(query['files']) })

        os.chdir(old_workdir)
	shutil.rmtree(workdir)

	return ( flask.jsonify(response), 200 )

@app.route('/', methods=['GET'])
def rCompile_index():
	return flask.redirect(flask.url_for('static', filename='index.html'))

def main(argv):
	rCompile.set_config(mode='server')

	app.run(debug=True)

