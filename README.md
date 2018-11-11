rCompile: Run Compiler Tools on Remote Server
=============================================

## Sequence of Events/Actions

Given the command:
 * rCompile identityTranslator -Wall myfile.c -std=c11 --mytooloptionforoutput outputfilename.json --some-random-args rnd0 rnd1 someconfigfile.json 
Client side submition:
 * lookup arguments and figure if they are files in the local directory (include subdirectory but not parent directories)
 * load and package these files into JSON ; add command line
 * submit JSON to server (found in configuration: ~/.rCompile/config.json)
Server side:
 * receive JSON
 * create temporary directory and cd there
 * build files
 * launch command and capture stdout/stderr
 * capture all created/changed files
 * package JSON reply: stdout/stderr and files
 * reply
 * remove tmp directory
Client side:
 * receive reply
 * write the files
 * save stdout/stderr
 * diplay stdout/stderr

