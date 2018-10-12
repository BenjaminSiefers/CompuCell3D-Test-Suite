""" 
=================================
Batch Testing Script
=================================
This script is to be used to run all the .cc3d files in a directory.
Use this file in the command line with your 2.7.* python command.
You can use the command line args "-o  [Path To Directory]" for directing output, "-i [Path To Directory]" for directing input, and "-player" to determine if you want to use the player.
"-o" and "-i" are expected to be given directories
For "-o" the program will send your test result as well as your normal CompuCell3D data to that directory.
The default location for your output should be found in a folder in this directory.
"""
import os
import subprocess
import time
from sys import platform
import sys

#Sends the Command to Shell	and writes a clean output filels

def CallInShell(command):
    if platform != 'win32':
        f = open(output + tail[0:-5]  + ".txt", "w")
        FileLocation = output
        try:
            f.writelines(subprocess.check_output(command))
        except subprocess.CalledProcessError as e:
            print("#Error code:", e.returncode, e.output)
            f.writelines("Error Code:" + "\n" + str(e.returncode) + "\n" + e.output)
    else:
        FileLocation = "Demos/Testing/TestResult/"  
        f = open(FileLocation + tail[0:-5] + ".txt", "w")
        try:
            f.writelines(subprocess.check_output(command))
        except subprocess.CalledProcessError as e:
            print("#Error code:", e.returncode, e.output)
            f.writelines("#Error Code:" + "\n" + str(e.returncode) + "\n" + e.output)
    f.close()
    #reopens it to give it a date and clean the output
    with open(FileLocation + tail[0:-5] + ".txt") as infile, open(FileLocation + tail[0:-5] +  time.strftime("%Y-%m-%d %H-%M") + '.txt', 'w') as outfile:
       buffer = []
       PastLine = False
       for line in infile:
            if not line.strip():
                buffer.append(line)
                continue
            Strip = line.strip()
            if Strip == "------------------PERFORMANCE REPORT:----------------------" or Strip == "#Error code:" or PastLine:
                PastLine = True
                outfile.write(''.join(buffer))
                buffer = []
                outfile.write(line)
    os.remove(FileLocation + tail[0:-5] + ".txt")

os.chdir('../../')
#defaults to not use the player
player = False
UniqueOutput = False
#assign indicated args to a list
args = sys.argv
InputDirectory = 'Demos'
if "-i" in args:
    InputDirectory = args[args.index("-i") + 1]
if "-o" in args:
    UniqueOutput = True
    OutputDirectory = args[args.index("-o") + 1]
if "-player" in args:
    player = True	
#Collects all .cc3d files                                      
demos = [os.path.join(dp, file) for dp, dn, filenames in os.walk(InputDirectory) for file in filenames if os.path.splitext(file)[1] == '.cc3d']
#Checks if output director exits
output = "Demos/Testing/TestResult/"
#Check for OS
if platform == 'linux' or platform == 'linux2':
    if not os.path.isdir(output): os.makedirs(output)
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output

        if(player):
            command = ["./compucell3d.command", "-i", path, "--exitWhenDone"]
        else:
            command = ["./runScript.command", "-i", ]
            
        if (UniqueOutput):
            command.append("-o")
            command.append(OutputDirectory)
        CallInShell(command)	
elif platform == 'win32':
    
    if not os.path.isdir(output):
        os.makedirs(output)
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        if(player):
            command = ["C:/CompuCell3D-64bit/compucell3d.bat", "-i", path, "--exitWhenDone" ]
        else:
            command = ["C:/CompuCell3D-64bit/runScript.bat", "-i", path]
        
        if (player):
            command.append("--exitWhenDone")
        if (UniqueOutput):
            command.append("-o")
            command.append(OutputDirectory)
        CallInShell(command)
else:
    if not os.path.isdir(output):
        os.makedirs(output)
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        if(player):
            command = ["./compucell3d.command", "-i", path, "--exitWhenDone"]
        else:
            command = ["./runScript.command", "-i", ]
			
        if (player):
            command.append("--exitWhenDone")
        if (UniqueOutput):
            command.append("-o")
            command.append(OutputDirectory)
        CallInShell(command)
