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
#get the current time
timeStart = time.strftime("%Y-%m-%d_%H-%M")
#create a folder to store TestResults
if(not os.path.isdir("TestResult")): os.makedirs("TestResult")
#create a file to store the test, system, bit type, and time
file = open("TestResult/" + "TestResult" + timeStart + ".txt", "w")
file.write(platform.system() + " version: " + platform.version() + "  " + platform.machine() + "\n")
if(os.path.isfile("../../../CompuCell3D-64bit website.url")):
    file.write("CompuCell3D-64bit\n")
elif(os.path.isfile("../../../CompuCell3D-32bit website.url")):
    file.write("CompuCell3D-32bit\n")
file.close()

#creates a place to store used demos so that multiple instances of this program be ran
#also gets the initially used time if its been created already
if(not os.path.isfile("ProcessedDemos.txt")):
    file = open("ProcessedDemos.txt", "w")
    file.write(timeStart + "\n")
    file.close()
else:
    file = open("ProcessedDemos.txt", "r")
    timeStart = file.readline()[0:-1]
    file.close()

print("Proccessing...   This could take a VERY long time...")
#Sends the Command to Shell	and writes a clean output filels
def callInShell(arguments):
    command = ""
    for _arg in arguments:
        command += _arg + " "
    if platform != "win32":
        fileLocation = output
        try:
            commandOutput = os.popen(command, "r")
            f = open(output + tail[0:-5] + ".txt", "w")
            f.writelines(commandOutput)
            f.close()
        except os.error as e:
            print("#Error code:", e.returncode, e.output)
            f = open(output + tail[0:-5] + ".txt", "w")
            f.writelines("Error Code:" + "\n" + str(e.returncode) + "\n" + e.output)
            f.close()
    else:
        fileLocation = "Demos/Testing/TestResult/"
        try:
            commandOutput = os.popen(command, "r")
            f = open(output + tail[0:-5] + ".txt", "w")
            f.writelines(commandOutput)
            f.close()
        except os.error as e:
            print("#Error code:", e.returncode, e.output)
            f = open(output + tail[0:-5] + ".txt", "w")
            f.writelines("#Error Code:" + "\n" + str(e.returncode) + "\n" + e.output)
            f.close()
    noError = False

    #reopens it to give it a date and clean the output
    with open(fileLocation + tail[0:-5] + ".txt", "r") as infile, open(fileLocation + tail[0:-5] + "temp" + ".txt", "w") as outfile:
        buffer = []
        pastLine = False
        outfile.write(path + "\n")
        for line in infile:
            Strip = line.strip()
            if Strip == "------------------PERFORMANCE REPORT:----------------------" or Strip == "#Error code:" or pastLine:
                pastLine = True
                outfile.write("".join(buffer))
                buffer = []
                outfile.write(line)
    if(not pastLine):
        fileName = fileLocation + tail[0:-5] + ".txt"
    else:
        fileName = fileLocation + tail[0:-5] + "temp" + ".txt"

    with open(output + "TestResult" + timeStart + ".txt", "a") as testResult:
        with open(fileName) as file:
            for line in file:
                testResult.write(line)
            testResult.write("\n\n")
    testResult.close()
    file.close()
    os.remove(fileLocation + tail[0:-5] + ".txt")
    os.remove(fileLocation + tail[0:-5] + "temp" + ".txt")

#Creates a command to send the CallinShell function
def createCommand():
    if(player):
        arguments = [setup + "compucell3d" + ext, "--exitWhenDone"]
    else:
        arguments = [setup + "runScript" + ext]
    
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
    callInShell(arguments)


#move to the main directory
os.chdir("../../")

#defaults to not use the player
player = False
uniqueOuput = False
customScreenshot = False
customFrequency = False
customCoreName = False

#assign indicated args to a list
args = sys.argv
del args[0]
inputDirectory = "Demos"

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
        inputDirectory = args[args.index("-i") + 1]
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
demos = [os.path.join(dp, file) for dp, dn, filenames in os.walk(inputDirectory) for file in filenames if os.path.splitext(file)[1] == ".cc3d"]

#Checks if output director exits
output = "Demos/Testing/TestResult/"


#writes the used to demos to a file
def storeProcessedDemos(demoPath):
    with open("Demos/Testing/ProcessedDemos.txt", 'a') as processedDemos:
        processedDemos.writelines(demoPath + "\n")
    processedDemos.close()

def notInProcessedDemos(demoPath):
    with open("Demos/Testing/ProcessedDemos.txt", 'r') as processedDemos:
        for line in processedDemos:
            if demoPath + "\n" == line:
                return False
        return True

#Check for OS
if platform.system() == "Linux":
    for path in demos:
        #Gets filename
        if(notInProcessedDemos(path)):
            storeProcessedDemos(path)
            head, tail = os.path.split(path)
            ext = ".sh"
            setup = "./"
            createCommand()
elif platform.system() == "Windows":
    for path in demos:
        #Gets filename
        if(notInProcessedDemos(path)):
            storeProcessedDemos(path)
            head, tail = os.path.split(path)
            ext = ".bat"
            setup = "C:/CompuCell3D-64bit/"
            createCommand()
elif platform.system() == "Darwin":
    for path in demos:
        #Gets filename
        if(notInProcessedDemos(path)):
            storeProcessedDemos(path)
            head, tail = os.path.split(path)
            ext = ".command"
            setup = "./"
            createCommand()
