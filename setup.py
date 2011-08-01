#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install import install
import sys

class CustomInstall(install):
    def run(self):
        print "Doing custom install."
        if not checkPythonVersion():
            print "ERROR: Wrong python version!"
            pass
             # TODO: install python 2.7.1
        if not checkDependencies():
            print "ERROR: Missing python module!"
            pass
             # TODO: install missing modules
        install.run(self) # proceed with the installation

def checkPythonVersion():
    #TODO: this should not pass
    return sys.version_info >= (2, 7, 1) #TODO: does e.g python 3 work?

def checkDependencies():
    print "Checking python module dependencies..."

    modules = ['Tkinter', 
               'argparse', 
               'unittest', 
               'mock']

    missingModule = False
    for module in modules:
        try:
            __import__(module)
            print module, '- OK'
        except ImportError:
            missingModule = True
            print module, '- MISSING'
    return not missingModule 


long_description = 'Slaps your desired apps on your screen in your desired style'

setup(name = 'appslap',
        version = '0.1',
        description = 'Slap apps on your screen',
        maintainer = 'Mathias Nyman',
        maintainer_email = 'N/A',
        url = 'http://www.github.com/appSlap', #TODO: define url
        long_description = long_description,
        packages = ['appslap'],
        scripts=['bin/slap'],
        cmdclass=dict(install=CustomInstall)
        )

