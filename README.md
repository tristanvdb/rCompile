rCompile: Run Compiler Tools on Remote Server
=============================================
## Installation
On both your server and client machines (assuming Ubuntu 16.04), install pip and flask
```
sudo apt-get install python-pip
sudo pip install --upgrade pip
sudo pip install flask
sudo apt-get install python-requests
```
clone this repo to each machine's local disk, assuming saved into /local-path/rCompile

## Configuration
### Setup path on both machines
 
```
export PATH=/path/to/rCompile/bin:$PATH
```

On Mac OS X, you may need to run the following command line:
```
export PYTHONPATH=/usr/local/lib/python2.7/site-packages
```

### On server side

You have to open port 5000 on your server to accept UPD/TCP traffic. Please consult your web server admins for how to do this.

Update config/server.json on the server side to set the temporary directory to store files
```
{
  "tmpdir" : "/your-server-side/tmpdir"
}
```
### On client side

Update config/client.json to use the right URL and port for the remote compilation service

```
{
  "url" : "http://your-server-name-or-ip:5000"
}
```

## Start the server

In one shell run the `rServ` command. It launches the Flask application in debug mode.

## Use on the Client
### Example 1

In another shell, do:
```
cd examples/test-1
rComp gcc test.c -o mytest
./mytest
```
In this case, we actually compile test.c on the same machine so the generated binary is valid.


## How it works

### Sequence of Events/Actions

Client side submition:
 * lookup arguments and figure if they are files in the current directory (include subdirectory but not parent directories)
 * load and package these files into JSON ; add command line
 * submit JSON to server (found in configuration: ~/.rCompile/config.json)

Server side:
 * receive JSON
 * create temporary directory and cd there
 * build files
 * launch command and capture stdout/stderr
 * capture all created/changed files (changed: not implemented yet)
 * package JSON reply: stdout/stderr and files
 * reply
 * remove tmp directory

Client side:
 * receive reply
 * write the files
 * save stdout/stderr
 * diplay stdout/stderr

