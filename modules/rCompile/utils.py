
import os
import stat
import json
import base64

def is_json_serializable(data):
	try:
		json.dumps(data)
	except:
		return False
	else:
		return True

def read_file_to_record(path):
	with open(path,'rb') as F:
		data = F.read()

	fdesc = { 'text' : data } if is_json_serializable(data) else { 'base64' : base64.b64encode(data) , 'exec' : (stat.S_IXUSR & os.stat(path)[stat.ST_MODE]) != 0 }

	return { path : fdesc }

def write_file_from_record(files):
	for (fpath,fdesc) in files.iteritems():
		dpath = os.path.dirname(fpath)
		if len(dpath) > 0 and not os.path.exists(dpath):
			os.makedirs(dpath)

		if 'text' in fdesc:
			data = fdesc['text']
		elif 'base64' in fdesc:
			data = base64.b64encode(fdesc['base64'])
		else:
			assert False, "Unexpected case!!!"

		with open(fpath, 'wb') as F:
			F.write(data)

		if 'exec' in fdesc and fdesc['exec']:
			st = os.stat(fpath)
			os.chmod(fpath, st.st_mode | stat.S_IEXEC)
