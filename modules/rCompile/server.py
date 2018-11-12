
import os
import sys
import json
import shutil
import subprocess

import rCompile

import flask
from flask import Flask

app = Flask(__name__)

def exec_client_command(command):
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()
	rc = p.returncode
	return (rc, out, err)

def save_generated_and_modified_files(workdir, files):
	res = dict()
	for (path, subdirs, files) in os.walk(workdir):
		for name in files:
			fpath = os.path.join(path, name)
			assert fpath.startswith(workdir)
			fpath = fpath[len(workdir)+1:]

			to_be_saved = not fpath in files
			if not to_be_saved:
				to_be_saved = False # TODO if file has changed

			if to_be_saved:
				res.update(rCompile.read_file_to_record(fpath))
				
	return res

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

	try:
		rCompile.write_file_from_record(query['files'])

		(rc, stdout, stderr) = exec_client_command(query['command'])
		response.update({ 'rc' : rc, 'stdout' : stdout, 'stderr' : stderr })

		response.update({ 'files' : save_generated_and_modified_files(workdir, query['files']) })
	except Exception as e:
        	os.chdir(old_workdir)
		shutil.rmtree(workdir)
		print e
		raise

        os.chdir(old_workdir)
	shutil.rmtree(workdir)

	return ( flask.jsonify(response), 200 )

@app.route('/', methods=['GET'])
def rCompile_index():
	return flask.redirect(flask.url_for('static', filename='index.html'))

def main(argv):
	rCompile.set_config(mode='server')

	app.run(debug=True)

