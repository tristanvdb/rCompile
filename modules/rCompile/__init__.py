
import os
import sys
import json

config = None

configdir = '{}/.rCompile'.format(os.path.expanduser("~"))
if not os.path.isdir(configdir):
	configdir = os.path.realpath('{}/../../config'.format(os.path.dirname(__file__)))
assert os.path.isdir(configdir), "Could not find a valid configuration directory."

def set_config(mode):
	global config
	cfgfile = '{}/{}.json'.format(configdir, mode)
	try:
		with open(cfgfile) as F:
			config = json.load(F)
	except Exception as e:
		print "Cannot read the configuration file: {}".format(cfgfile)
		sys.exit(1)

