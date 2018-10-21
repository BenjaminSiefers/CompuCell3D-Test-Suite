""" 
=================================
Batch Testing Script
=================================
This script is to be used to run all the .cc3d files in a directory.
Use this file in the command line with your 2.7.* python command.
You can use the command line args "-o  [Path To Directory]" for directing output, "-i [Path To Directory]" for directing input, and "-player" to determine if you want to use the player.
"-o" and "-i" are expected to be given directories
For "-o" the program will send your test result as well as your normal CompuCell3D data to that directory.
The default location for your  test output should be found in a folder in this directory.
"""
import os
import time
import platform
import sys
time = time.strftime("%Y-%m-%d_%H-%M")
testFile = open("TestResult/" + "TestResult" + time + ".txt", "w")
testFile.close()

print("Proccessing..." + "   This could take a VERY long time...")
#Sends the Command to Shell	and writes a clean output filels
def CallInShell(arguments):
    command = ""
    for _arg in arguments:
        command += _arg + " "
    if platform != "win32":
        f = open(output + tail[0:-5]  + ".txt", "w")
        FileLocation = output
        try:
            print(command)
            f.writelines(os.popen(command, "r"))
        except os.error as e:
            print("#Error code:", e.returncode, e.output)
            f.writelines("Error Code:" + "\n" + str(e.returncode) + "\n" + e.output)
    else:
        FileLocation = "Demos/Testing/TestResult/"  
        f = open(FileLocation + tail[0:-5] + ".txt", "w")
        try:
            print(command)
            f.writelines(os.popen(command, "r"))
        except os.error as e:
            print("#Error code:", e.returncode, e.output)
            f.writelines("#Error Code:" + "\n" + str(e.returncode) + "\n" + e.output)
    noError = False
    f.close()
    #reopens it to give it a date and clean the output
    with open(FileLocation + tail[0:-5] + ".txt") as infile, open(FileLocation + tail[0:-5] +  "temp" + ".txt", "w") as outfile:
        buffer = []
        PastLine = False
        for line in infile:
            if not line.strip():
                buffer.append(line)
                continue
            Strip = line.strip()
            if Strip == "------------------PERFORMANCE REPORT:----------------------" or Strip == "#Error code:" or PastLine:
                PastLine = True
                outfile.write("".join(buffer))
                buffer = []
                outfile.write(line)
    if(not PastLine):
        tempFileLocation = os.path.join(FileLocation + tail[0:-5] +  "temp" + ".txt")
    else:
        tempFileLocation = os.path.join(FileLocation + tail[0:-5] +  "temp" + ".txt")
    
    with open("Demos/Testing/TestResult/" + "TestResult" + time + ".txt", "a") as TestResult:
        with open(tempFileLocation, "r") as tempFile:
            TestResult.write(platform.system() + " version: " + platform.version() + "  " +  platform.machine())
            for line in tempFile:
                TestResult.write(line)
    TestResult.close()
#Creates a command to send the CallinShell function
def CreateCommand():
    if(player):
        arguments = [setup + "compucell3d" + ext, "--exitWhenDone"]
    else:
        arguments = [setup + "runScript" + ext ]
    
    if(customScreenshot):
        arguments.append("-s")
        arguments.append(customScreenshotName)
    arguments.append("-i")
    arguments.append(path)
    if(customFrequency):
        arguments.append("-f")
        arguments.append(frequency)
    for _arg in args:
        arguments.append(_arg)   
    CallInShell(arguments)



os.chdir("../../")
if not os.path.isdir("Demos/Testing"): os.makedirs("Demos/Testing")
#defaults to not use the player
player = False
UniqueOutput = False
customScreenshot = False
customFrequency = False
customCoreName = False
#assign indicated args to a list
args = sys.argv
del args[0]
InputDirectory = "Demos"
#help command args for this file
for _arg in args:
    if _arg == "-h" or _arg == "--help":
        #TODO write a -testOutput handler
        print("""
        -h shows a list of commands
        -i [Path to Directory] Determines which directory gets searched for .cc3d files
        -o [Path to Directory] Specifies where vtk/screenshot files will be written 
        -testOutput [Path to Directory] Specifies where the test results file will be located
        --noOutput Instructs CC3D to not store any project output, but tests will be saved
        [No Player]
                -f [frequency]specifies How often .vtk files are to be stored.
                -c [outputFileCoreName] Allows users to specify core name for the vtk files.
        --player Uses the player if you want to have screenshots
                
        """)
        exit()
    #takes a directory as opposed to a file location
    elif _arg == "-i":
        InputDirectory = args[args.index("-i") + 1]
        #delete their locations for convenience later
        del args[args.index("-i") + 1]
        del args[args.index("-i")]
    elif _arg == "-testOutput":
        testOutputDirectory = args[args.index("-testOutput") + 1]
        #delete their locations for convenience later
        del args[args.index("-testOutput") + 1]
        del args[args.index("-testOutput")]
    #signals that the user wants to use the player and removes any --exitWhenDone commands
    elif _arg == "--player":
        player = True
        del args[args.index("--player")]
        if "--exitWhenDone" in args:
            del args[args.index("--exitWhenDone")]
    elif _arg == "-f":
        customFrequency = True
        frequency = args[args.index("-f") + 1]
        del args[args.index("-f") + 1]
        del args[args.index("-f")]
    elif _arg == "-c":
        customCoreName = True
        coreName = args[args.index("-c") + 1]
        del args[args.index("-c") + 1]
        del args[args.index("-c")]
    elif _arg == "--noOutput":
        pass
    else:
        print("Error: " + _arg + " is an unreconized argument!")
        print("Use the --help command to see a list of commands")

#Collects all .cc3d files                                      
demos = [os.path.join(dp, file) for dp, dn, filenames in os.walk(InputDirectory) for file in filenames if os.path.splitext(file)[1] == ".cc3d"]
#Checks if output director exits
output = "Demos/Testing/TestResult/"
#Check for OS
if platform.system() == "Linux":
    for _path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        ext = ".sh"
        setup = "./"
        CreateCommand()
elif platform.system() == "Windows":
    for _path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        ext = ".bat"
        setup = "C:/CompuCell3D-64bit/"
        CreateCommand()
elif platform.system() == "Darwin":
    for _path in demos:
        #Gets filename
        head, tail = os.path.split(path)
        ext = ".command"
        setup = "./"
        CreateCommand()
