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
timeStart = time.strftime("%d-%m-%Y_%H-%M")
#default output directory for test results
testOutput = "Demos/Testing/"
#keeps track which demo the program is on
demoNumber = 1;


def appendReturnCode(returnCode):
    file = open(testOutput + "ProcessedDemos" + timeStart + ".txt", "r")
    contents = "";
    i = 0
    # looks for the current demo and inserts the return value
    for line in file:
        contents += line;
        if (line[:-1] == path):
            contents += "Return Code: " + str(returnCode) + "\n"
        i += 1;
    file.close()
    file = open(testOutput + "ProcessedDemos" + timeStart + ".txt", "w")
    file.writelines(contents);
    file.close()

print("Proccessing...   This could take a VERY long time...")
#Sends the Command to Shell	and writes a clean output filels
def callInShell(arguments):
    command = ""

    for _arg in arguments:
        command += _arg + " "
    if platform != "win32":
        try:
            commandOutput = os.popen(command, "r")
            f = open(testOutput + tail[0:-5] + ".txt", "w")
            f.writelines(commandOutput)
            f.close()
        except os.error as e:
            print("#Error code:", e.returncode, e.output)
            f = open(testOutput + tail[0:-5] + ".txt", "w")
            f.writelines("Error Code:" + "\n" + str(e.returncode) + "\n" + e.output)
            f.close()
    else:
        try:
            commandOutput = os.popen(command, "r")
            f = open(testOutput + tail[0:-5] + ".txt", "w")
            f.writelines(commandOutput)
            f.close()
        except os.error as e:
            print("#Error code:", e.returncode, e.output)
            f = open(testOutput + tail[0:-5] + ".txt", "w")
            f.writelines("#Error Code:" + "\n" + str(e.returncode) + "\n" + e.output)
            f.close()

    #reopens it to give it a date and clean the output
    with open(testOutput + tail[0:-5] + ".txt", "r") as infile, open(testOutput + tail[0:-5] + "temp" + ".txt", "w") as outfile:
        buffer = []
        pastLine = False
        outfile.write(path + "\n")
        for line in infile:
            Strip = line.strip()
            if Strip == "------------------PERFORMANCE REPORT:----------------------" or pastLine:
                pastLine = True
                outfile.write("".join(buffer))
                buffer = []
                outfile.write(line)
    infile.close()
    outfile.close()
    if(not pastLine):
        fileName = testOutput + tail[0:-5] + ".txt"
    else:
        fileName = testOutput + tail[0:-5] + "temp" + ".txt"
    if(pastLine):
        appendReturnCode(0)
        with open(testOutput + "SuccessfulResults" + timeStart + ".txt", "a") as testResult:
            with open(fileName) as file:
                for line in file:
                    testResult.write(line)
                testResult.write("\n\n")
        testResult.close()
        file.close()
    else:
        appendReturnCode(1)
        if not os.path.exists(testOutput + "UnexpectedResults" + timeStart + ".txt"):
            file = open(testOutput + "UnexpectedResults" + timeStart + ".txt", "w")
            file.write("These are demos that have given an error or have ran to completion and did not provide a performance report.\n")
            file.close()
        with open(testOutput + "UnexpectedResults" + timeStart + ".txt", "a") as testResult:
            with open(fileName) as file:
                testResult.write("UNEXPECTED OUTPUT[DEMO #" + str(demoNumber) + "]: " + path + "\n")
                testResult.write("OUTPUT: \n")
                numberOfLinesInFile = 0
                linesToBeRemoved = 0
                contents = ""
                for line in file:
                    numberOfLinesInFile += 1
                    contents += line + "\n"
                    pass
                for line in contents.splitlines():
                    linesToBeRemoved+=1
                    if numberOfLinesInFile-20 <= linesToBeRemoved:
                        testResult.write(line)
                    pass
                file.close()
                testResult.write("\n\n")
                testResult.close()
    os.remove(testOutput + tail[0:-5] + ".txt")
    os.remove(testOutput + tail[0:-5] + "temp" + ".txt")

#Creates a command to send the CallinShell function
def createCommand():
    if(player):
        arguments = [setup + "compucell3d" + ext, "--exitWhenDone"]
    else:
        arguments = [setup + "runScript" + ext]

    arguments.append("-i")
    arguments.append(path)
    if(customOutput):
        arguments.append("-o")
        if(not os.path.isdir(outputDirectory + "/" + tail[0:-5] + timeStart)):
            os.makedirs(outputDirectory + "/" + tail[0:-5] + timeStart)
        arguments.append(outputDirectory + "/" + tail[0:-5] + timeStart)
    if(noOutput):
        arguments.append("--noOutput")
    for arg in args:
        arguments.append(arg)

    callInShell(arguments)





#defaults to not use the player
player = False
uniqueOuput = False
customScreenshot = False
customFrequency = False
customCoreName = False
customOutput = False
noOutput = False
#assign indicated args to a list
args = sys.argv
del args[0]
inputDirectory = "Demos"

#help command args for this file
j = 0
while j < len(args):
    if (args.count("-h") == 1 or args.count("--help") == 1) and (args[j] == "-h" or arg == "--help"):
        #TODO write a -testOutput handler
        print("""
This script tests all the .cc3d scripts in a directory and collects output
and determines whether the .cc3d files failed or ran to completion. See the 
documentation located in this directory for more details.
        -h shows a list of commands
        -i [Path to Directory] Determines which directory gets searched for .cc3d files
        -o [Path to Directory] Specifies where vtk/screenshot files will be written 
        -testOutput [Path to Directory] Specifies where the test results file will be located
        --noOutput Instructs CC3D to not store any project output, but tests will be saved
        --player Uses the player if you want to have screenshots
                
        """)
        exit(0)
    #takes a directory as opposed to a file location
    elif args.count("-i") == 1 and args[j] == "-i":
        inputDirectory = os.path.abspath(args[args.index("-i") + 1])
        #delete their locations for convenience later
        del args[args.index("-i") + 1]
        del args[args.index("-i")]

    elif args.count("-o") == 1 and args[j] == "-o":
        customOutput = True
        outputDirectory = os.path.abspath(args[args.index("-o") + 1])
        #delete their locations for convenience later
        del args[args.index("-o") + 1]
        del args[args.index("-o")]

    elif args.count("-testOutput") == 1 and args[j] == "-testOutput":
        testOutput = os.path.abspath(args[args.index("-testOutput") + 1]) + "/"
        #delete their locations for convenience later
        del args[args.index("-testOutput") + 1]
        del args[args.index("-testOutput")]

    #signals that the user wants to use the player and removes any --exitWhenDone commands
    elif args.count("--player") == 1 and args[j] == "--player":
        player = True
        del args[args.index("--player")]
        if "--exitWhenDone" in args:
            del args[args.index("--exitWhenDone")]

    #sets up the tests not to send any output to the CC3DWorkspace
    elif args.count("--noOutput") == 1 and args[j] == "--noOutput":
        noOutput = True
        del args[args.index("--noOutput")]

    else:
        print("Error: near " + args[j] + " is an invalid command or sequence!")
        print("Use the --help command to see a list of commands")
        exit(1)

#changes the working directory to the top directory
os.chdir("../../")

file = open(testOutput + "SuccessfulResults" + timeStart + ".txt", "w")
file.write(platform.system() + " version: " + platform.version() + "  " + platform.machine() + "\n")
if(os.path.isfile("../../../CompuCell3D-64bit website.url")):
    file.write("CompuCell3D-64bit\n")
elif(os.path.isfile("../../../CompuCell3D-32bit website.url")):
    file.write("CompuCell3D-32bit\n")
file.close()


#creates a place to store used demos so that multiple instances of this program be ran
#also gets the initially used time if its been created already
if(not os.path.isfile(testOutput + "ProcessedDemos" + timeStart + ".txt")):
    file = open(testOutput + "ProcessedDemos" + timeStart + ".txt", "w")
    file.write(timeStart + "\n")
    file.close()
else:
    file = open(testOutput +" ProcessedDemos" + timeStart + ".txt", "r")
    timeStart = file.readline()[0:-1]
    file.close()

#Collects all .cc3d files                                      
demos = [os.path.join(dp, file) for dp, dn, filenames in os.walk(inputDirectory) for file in filenames if os.path.splitext(file)[1] == ".cc3d"]

#writes the used to demos to a file
def storeProcessedDemos(demoPath):
    with open(testOutput + "ProcessedDemos" + timeStart + ".txt", 'a') as processedDemos:
        processedDemos.writelines(demoPath + "\n")
    processedDemos.close()

def notInProcessedDemos(demoPath):
    with open(testOutput + "ProcessedDemos" + timeStart + ".txt", 'r') as processedDemos:
        for line in processedDemos:
            if demoPath + "\n" == line:
                return False
        return True


#Check for OS
if platform.system() == "Linux":
    for path in demos:
        demoNumber += 1
        #Gets filename
        if(notInProcessedDemos(path)):
            storeProcessedDemos(path)
            head, tail = os.path.split(path)
            ext = ".sh"
            setup = "./"
            createCommand()
elif platform.system() == "Windows":
    for path in demos:
        demoNumber += 1
        #Gets filename
        if(notInProcessedDemos(path)):
            storeProcessedDemos(path)
            head, tail = os.path.split(path)
            ext = ".bat"
            setup = os.getcwd() + "/"
            createCommand()
elif platform.system() == "Darwin":
    for path in demos:
        demoNumber += 1
        #Gets filename
        if(notInProcessedDemos(path)):
            storeProcessedDemos(path)
            head, tail = os.path.split(path)
            ext = ".command"
            setup = "./"
            createCommand()
