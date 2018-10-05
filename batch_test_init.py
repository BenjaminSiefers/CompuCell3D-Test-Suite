import os
import subprocess
from sys import platform

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
        command = ["./runScript.sh", "-i", path]
        f = open(output + tail[0:-5] + ".txt", "w")
        try:
            f = open(output + tail[0:-5] + ".txt", "w")
            f.writelines(subprocess.check_output(command))
        except subprocess.CalledProcessError as e:
            print "error code", e.returncode, e.output
            f.writelines("error code" + "\n" +  str(e.returncode) + "\n" + str(e.output))
        f.close()

elif platform == 'win32':
    if not os.path.isdir("C:/CC3DWorkspace/Shell_Output"):
        os.makedirs("C:/CC3DWorkspace/Shell_Output")
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        f = open(output + tail[0:-5] + ".txt", "w")
        try:
            f.writelines(subprocess.check_output("C:/CompuCell3D-64bit/runScript.bat -i " + path))
        except subprocess.CalledProcessError as e:
            print "error code", e.returncode, e.output
            f.writelines("error code" + "\n" + str(e.returncode) + "\n" + e.output)
        f.close()

elif platform == 'darwin':
    if not os.path.isdir(output):
        os.makedirs(output)
    for path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        #Creates a file to send the output
        f = open(output + tail[0:-5] + ".txt", "w")
        try:
            f.writelines(subprocess.check_output("./runScript.command -i " + path))
        except subprocess.CalledProcessError as e:
            print "error code", e.returncode, e.output
            f.writelines("error code" + "\n" + str(e.returncode) + "\n" + e.output)
        f.close()
