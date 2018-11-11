
import os
import sys
import json
import uuid
import requests

import rCompile

def file_is_text(data):

	# TODO

	return True

def encode_binary_data_to_string(data):
	text = ''

	# TODO

	return text

def detect_and_load_files(argv):
	args = list()
	files = dict()
	cwd = os.path.realpath(os.getcwd())
	for arg in argv:
		if os.path.isfile(arg):
			path = os.path.realpath(arg)
			if path.startswith(cwd):
				with open(path,'r') as F:
					data = F.read()

				if file_is_text(data):
					content = 'text'
				else:
					content = 'bin'
					data = encode_binary_data(data)

				path = path[len(cwd)+1:]
				files.update({ path : { 'content' : content , 'data' : data } })
			else:
				path = None
		else:
			path = None

		if path is None:
			args.append(arg)
		else:
			args.append(path)

	return (args,files)

def submit(query):
	response = requests.post('{}/exec'.format(rCompile.config['url']), data=json.dumps(query))

	assert response.status_code == 200

	response = json.loads(response.text)

	return response

def write_files(files):
	pass

def main(argv):
	rCompile.set_config(mode='client')

	(args,files) = detect_and_load_files(argv)

	query = { 'uuid' : str(uuid.uuid4()) , 'command' : args , 'files' : files }

	print ">> query: {}".format(query['uuid'])
	print ">> command: {}".format(' '.join(query['command']))
	if 'files' in query and len(query['files']) > 0:
		print ">> read files[begin]"
		for (fid,fpath) in enumerate(query['files'].keys()):
			print ">>>> IN[{}]: {}".format(fid, fpath)
		print ">> read files[end]"

	response = submit(query=query)

	assert response['uuid'] == query['uuid'], "Mismatch between the query and the response unique ID!"

	if 'stdout' in response and len(response['stdout']) > 0:
		print ">> stdout[begin] ==\n{}\n== stdout[end]".format(response['stdout'])
	if 'stderr' in response and len(response['stderr']) > 0:
		print ">> stderr[begin] ==\n{}\n== stderr[end]".format(response['stderr'])
	if 'files' in response and len(response['files']) > 0:
		print ">> write files[begin]"
		for (fid,fpath) in response['files']:
			print ">>>> OUT[{}]: {}".format(fid, fpath)
		print ">> write files[end]"
		write_files(response['files'])

