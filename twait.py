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
from subprocess import check_output;



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
-o : Output folder
-a : Start apache2
-b : Start beef-xss and inject
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
            print("%sPackage - %s - is installed.%s" % (colour_headers[0], x, colour_headers[2]));
        else: #If command returns false
            print("%sPackage - %s - is not installed.%s" % (colour_headers[1], x, colour_headers[2]));

def ArgCheck(arg):
    for x in range(0, len(sys.argv)): #For every item in the arguments
        y = sys.argv[x] #The argument text
        if y == arg: #If the argument is the same as the expected
            return x #Return the position of the argument
    return False #Else, return False



#Check Arguments
if len(sys.argv) == 1:
    print("%s%s%s%s" % (colour_headers[3], ascii_art, colour_headers[2], args)); #Print ascii_art in Purple, followed by available args.
    print("%sError: no arguments given%s" % (colour_headers[1], colour_headers[2]));
    sys.exit();
elif "-h" in sys.argv:
    print("%s%s%s%s" % (colour_headers[3], ascii_art, colour_headers[2], args)); #Print ascii_art in Purple, followed by available args.
elif "-c" in sys.argv:
    DependencyCheck(possible_packages); #Check dependencies
elif "-u" in sys.argv:
    pos = ArgCheck("-u") #Position of -u
    pos += 1 #Position of the url
    url = sys.argv[pos] #Declare the url
elif "-u" not in sys.argv:
    print("%sError: no URL specified%s" % (colour_headers[1], colour_headers[2])); #Throw error
