
#############################################################
# 
# Filename: cmdln.py
# Description: Develop command-line apps in a standard way.
#                   
# Author: Eng. Hazem Anwer
# Github: https://github.com/hazemanwer2000
# 
#############################################################

import sys

# Function: Print to 'stderr'.
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# API: Print error and exit.
def error(msg):
    eprint('[Error]: ' + msg)
    exit(1)

# Code: Check for invalid argument format.
if len(sys.argv) > 1 and sys.argv[1][0] != '-':
    error("Invalid option/argument(s) format.")

# Variable:
args = {}

# Code: Generate 'args' dictionary.
lastKey = None
for arg in sys.argv[1:]:
    if arg[0] == '-':
        lastKey = arg[1:]
        args[lastKey] = []
    else:
        args[lastKey].append(arg)
del(lastKey)

# Code: Check if '-h' option specified, then display documentation and exit.
if args.get('h') != None:
    with open('help.txt', 'r') as f:
        print(f.read())
        exit(0)