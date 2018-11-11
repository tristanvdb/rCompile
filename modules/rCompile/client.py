#!/usr/bin/python2.7

import os
import sys
import json
import uuid
import requests

def get_config():
	config = None

	cfgfile = '{}/.rCompile/config.json'.format(os.path.expanduser("~"))
	if not os.path.exists(cfgfile):
		print "Cannot find configuration file: {}".format(cfgfile)
	else:
		try:
			with open(cfgfile) as F:
				config = json.load(F)
		except:
			print "Cannot read the configuration file."

	assert not config is None, "No configuration found..."

	return config

def detect_and_load_files(argv):
	files = dict()

	# TODO

	return files

def submit(query, config):
	response = None

	r = requests.post('{}/exec'.format(config['url']), data=json.dumps(query))

	assert r.status_code == 200

	return { 'uuid' : json.loads(r.text)['uuid'] }

def write_files(files):
	pass

def main(argv):
	config = get_config()

	query = { 'uuid' : str(uuid.uuid4()) , 'command' : argv , 'files' : detect_and_load_files(argv) }

	print ">> query: {}".format(query['uuid'])
	print ">> command: {}".format(' '.join(query['command']))
	if 'files' in query and len(query['files']) > 0:
		print ">> read files[begin]"
		for (fid,fpath) in enumerate(query['files'].keys()):
			print ">>>> IN[{}]: {}".format(fid, fpath)
		print ">> read files[end]"

	response = submit(query=query, config=config)

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

