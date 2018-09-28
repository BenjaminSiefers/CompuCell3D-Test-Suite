import os
from sys import platform

#Collects all .cc3d files                                  Path to Demos
demos = [os.path.join(dp, file) for dp, dn, filenames in os.walk('Demos') for file in filenames if os.path.splitext(file)[1] == '.cc3d']

#Check for OS
if platform == 'linux' or platform == 'linux2':
    for path in demos:
        os.system('C:/CompuCell3D-64bit/compucell3d.sh -i ' + path + ' -f 0 /C:"\"Users"\"ben"\"CC3DWorkspace/')
        os.system('C:/CompuCell3D-64bit/runScript.sh -i ' + path + ' -f 0 /C:"\"Users"\"ben"\"CC3DWorkspace/')
elif platform == 'win32':
    for path in demos:
        os.system('C:/CompuCell3D-64bit/compucell3d.bat -i ' + path + ' -f 0 -o /C:"\"Users"\"ben"\"CC3DWorkspace/')
        os.system('C:/CompuCell3D-64bit/runScript.bat -i ' + path + ' -f 0 -o /C:"\"Users"\"ben"\"CC3DWorkspace/')
elif platform == 'darwin':
    for path in demos:
        os.system('C:/CompuCell3D-64bit/compucell3d.command -i ' + path + ' -f 0 /C:"\"Users"\"ben"\"CC3DWorkspace/')
        os.system('C:/CompuCell3D-64bit/runScript.command -i ' + path + ' -f 0 /C:"\"Users"\"ben"\"CC3DWorkspace/')