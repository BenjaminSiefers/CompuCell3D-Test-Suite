import os
import subprocess
import getpass
from sys import platform

#Collects all .cc3d files                                  Path to Demos
demos = [os.path.join(dp, file) for dp, dn, filenames in os.walk('Demos') for file in filenames if os.path.splitext(file)[1] == '.cc3d']
#Checks if output director exits
if not os.path.isdir("/output"):
    os.makedirs("/output")
#Check for OS
if platform == 'linux' or platform == 'linux2':
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        f = open("output/" + tail[0:-5] + ".txt", "w")
        f.writelines(subprocess.check_output('C:/CompuCell3D-64bit/runScript.sh -i ' + path + ' -f 0 /C:"\"Users"\"' + getpass.getuser() + '"\"CC3DWorkspace/'))
elif platform == 'win32':
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        f = open("output/" + tail[0:-5] + ".txt", "w")
        f.writelines(subprocess.check_output('C:/CompuCell3D-64bit/runScript.bat -i ' + path + ' -f 0 -o /C:"\"Users"\"' + getpass.getuser() + '"\"CC3DWorkspace/'))
        f.close()
elif platform == 'darwin':
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        f = open("output/" + tail[0:-5] + ".txt", "w")
        f.writelines(subprocess.check_output('C:/CompuCell3D-64bit/runScript.command -i ' + path + ' -f 0 /C:"\"Users"\"' + getpass.getuser() + '"\"CC3DWorkspace/'))
        f.close()
		
