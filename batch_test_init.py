import os
import subprocess
from sys import platform
#Sends the Command to Shell	
def CallInShell(command):
	if not platform == 'win32':
		f = open(output + tail[0:-5] + ".txt", "w")
		try:
			f.writelines(subprocess.check_output(command))
		except subprocess.CalledProcessError as e:
			print "error code", e.returncode, e.output
			f.writelines("error code" + "\n" + str(e.returncode) + "\n" + e.output)
	else:
		f = open("C:/CC3DWorkspace/Shell_Output/" + tail[0:-5] + ".txt", "w")
		try:
			f.writelines(subprocess.check_output(command))
		except subprocess.CalledProcessError as e:
			print "error code", e.returncode, e.output
			f.writelines("error code" + "\n" + str(e.returncode) + "\n" + e.output)
	f.close()
		
#Collects all .cc3d files                                      Path to Demos
demos = [os.path.join(dp, file) for dp, dn, filenames in os.walk('Demos') for file in filenames if os.path.splitext(file)[1] == '.cc3d']
#Checks if output director exits
output = os.path.expanduser('~') + "/CC3DWorkspace/Shell_Output/"

#Check for OS
if platform == 'linux' or platform == 'linux2':
    if not os.path.isdir(output):
        os.makedirs(output)
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        command = ["./compucell3d.sh", "--exitWhenDone", "-i", path, "--exitWhenDone"]
        CallInShell(command)
elif platform == 'win32':
    if not os.path.isdir("C:/CC3DWorkspace/Shell_Output"):
        os.makedirs("C:/CC3DWorkspace/Shell_Output")
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
		#Creates a file to send the output
        command = ["C:/CompuCell3D-64bit/compucell3d.bat", "-i", path, "--exitWhenDone" ]
        CallInShell(command)
else:
    if not os.path.isdir(output):
        os.makedirs(output)
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        command = ["./compucell3d.command", "-i", path, "--exitWhenDone"]
        CallInShell(command)
		


