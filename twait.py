#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Metadata
__author__ = "SherlockSec";
__version__ = "1.0";
__license__ = "GPL-3.0";

#Imports
import sys;
import os;
import subprocess;

#Declarations
possible_packages = [
    "httrack",
    "apache2",
    "beef-xss",
];

colour_headers = [
    "\x1b[1;32;40m", #Bright Green
    "\x1b[1;31;40m", #Bright Red
    "\x1b[0m", #White
    "\x1b[1;35;40m" #Purple
];
ascii_art = '''
 _____ _    _  ___ _____
|_   _| |  | |/ _ \_   _|
  | | | |  | / /_\ \| |
  | | | |/\| |  _  || |
  | | \  /\  / | | || |
  \_/  \/  \/\_| |_/\_/
'''

args = '''
Arguments:

-h : Help
-u : URL
-o : Output folder
-a : Start apache2
-b : Start beef-xss and inject
'''
#Check Arguments
if len(sys.argv) == 1:
    print("%sError: no arguments given%s" % (colour_headers[1], colour_headers[2]));
    #Display arguuments here
    sys.exit();
elif sys.argv[1] == "-h":
    print("%s%s%s%s" % (colour_headers[3], ascii_art, colour_headers[2], args)); #Print ascii_art in Purple, followed by available args.



#Functions
def DependencyCheck(possible_packages):
    for x in possible_packages:
        devnull = open(os.devnull, "w") # Opens the OS equivalent of /dev/null
        check = subprocess.Popen(["dpkg", "-s", x], stdout=devnull, stderr=subprocess.STDOUT); #Runs the debian command to check if a package is installed
        devnull.close(); #Closes /dev/null
        if check != 0: #If there is an error message
            print("%sPackage - %s - is not installed.%s" % (colour_headers[1], x, colour_headers[2]));
        else: #If there is no error message
            print("%sPackage - %s - is installed.%s" % (colour_headers[0], x, colour_headers[2]));
