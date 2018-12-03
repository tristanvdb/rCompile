rCompile: Run Compiler Tools on Remote Server
=============================================
## Installation and Configuration
On both your server and client machines (assuming Ubuntu 16.04), install pip and flask
```
sudo apt-get install python-pip
sudo pip install --upgrade pip
sudo pip install flask
```

### Setup path on both machines

```
export PATH=/path/to/rCompile/bin:$PATH
```

### Start server

In one shell run the `rServ` command. It launches the Flask application in debug mode.

## Example use
### Test 1

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

