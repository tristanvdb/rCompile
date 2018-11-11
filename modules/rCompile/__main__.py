
import sys

if __name__ == '__main__' and len(sys.argv) > 1:

	if sys.argv[1] == 'client':
		import rCompile.client
		rCompile.client.main(sys.argv[2:])

	if sys.argv[1] == 'server':
		import rCompile.server
		rCompile.server.main(sys.argv[2:])

