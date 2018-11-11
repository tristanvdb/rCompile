
import os
import sys
import json

configdir = '{}/.rCompile'.format(os.path.expanduser("~"))
if not os.path.isdir(configdir):
	configdir = os.path.realpath('{}/../../config'.format(os.path.dirname(__file__)))
assert os.path.isdir(configdir), "Could not find a valid configuration directory."

def get_config(mode):

	config = None

	cfgfile = '{}/{}.json'.format(configdir, mode)
	try:
		with open(cfgfile) as F:
			config = json.load(F)
	except Exception as e:
		print "Cannot read the configuration file: {}".format(cfgfile)
		sys.exit(1)

	return config

