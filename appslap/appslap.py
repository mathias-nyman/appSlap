#!/usr/bin/env python

import sys
import os
import re
import subprocess
import commands

#TODO: remove this when setup.py is ok
from terminal   import *
from geometry   import *
from style      import *
from dimensions import *


DEBUG=True
def debug( line ):
    if DEBUG:
        print line

class AppSlap:

    class Defaults:
        program=['xterm']
        style=['fourfour']

    # TODO: fill this list by searching for all classes that implement some interface
    class Options:
        programs = [
            Xterm,
            GnomeTerminal
            ]

        styles = [
                StyleTwo,
                StyleThree,
                StyleFour,
                StyleFourFour
                ]


    def __init__( self ):
        self.__screenDimensions = (800, 600)
        self.__programLaunchers = []
        self.__style = None


    def parseXrandrOutput( self, xrandrOutput ):
        debug( "MILESTONE: attempting to parse xrandr output: " + xrandrOutput )
        pattern = re.compile(r"""
        (\d+)  # width pixels
        \s*    # optional whitespace
        x      # separator
        \s*    # optional whitespace
        (\d+)  # length pixels
        """, re.VERBOSE)
        match = pattern.search( xrandrOutput )
        if match is None:
            raise Exception("ERROR: xrandr output could not be parsed.")
        self.__screenDimensions= ( int(match.group(1)), int(match.group(2)) )
        debug( "MILESTONE: dimensions fetched: " + str(self.__screenDimensions) )


    def getFromSystem(self, cmd ):
        #TODO: handle nasty things, if cmd results in error
        debug( "MILESTONE: getting output of system command: " + cmd )
        return commands.getoutput( cmd )


    def getDimensions( self ):
        cmd = "xrandr -q | /bin/grep '*'"
        sysOut = self.getFromSystem( cmd )
        self.parseXrandrOutput( sysOut )
        dim = TkDimensionsGetter().getDimensions()
        debug( "MILESTONE: got dimensions from Tk: " + str(dim) )


    def launchWindows( self ):
        debug( "MILESTONE: launching windows with commands:")
        for launcher in self.__programLaunchers:
            cmd = str(launcher)
            debug( cmd )
            subprocess.Popen( cmd.split(' ') )


    def setStyle( self, styleName ):
        for style in self.Options.styles:
            if style.getName() == styleName:
                debug( "MILESTONE: using style: " + styleName )
                self.__style = style()
        if self.__style is None:
            raise Exception("No style has been specified.")
        self.getDimensions()


    def setProgram( self, programName ):
        if self.__style is None:
            raise Exception("No style has been specified.")
        layout = self.__style.getLayout()
        for lay in layout:
            geometry = Geometry()
            geometry.setScreenSize( *self.__screenDimensions )
            geometry.setGeometry( *lay )
            for program in self.Options.programs:
                if program.getName() == programName:
                    self.__programLaunchers.append( program() )
                    self.__programLaunchers[-1].setGeometry( geometry ) 
        if len(self.__programLaunchers) is 0:
            raise Exception( "No program found to match the name: " + programName )
        else:
            debug( "MILESTONE: using program: " + programName )


    def parseCmdLineOptions( self, argv ):
        try:
            import argparse
            parser = argparse.ArgumentParser(description="Launch a set of windowed programs, e.g. xterm's.")
            parser.add_argument('-p', '--program', dest='program', nargs=1, default=self.Defaults.program,
                    type=complex, choices=[p.getName() for p in self.Options.programs],
                    help='program to launch')
            parser.add_argument('-s', '--style', dest='style', nargs=1, default=self.Defaults.style,
                    type=complex, choices=[s.getName() for s in self.Options.styles],
                    help='style of window positioning')
            #FIXME: argparse works outside this try, but only with one complex type argument
            #  UPDATE: this actually seems to work with python 2.7.1
            args = parser.parse_args()

        except ImportError, e:
            #TODO: argparse is only in python >= 2.7, offer an alternative
            debug("ERROR: argparse failed.")
            self.setStyle( 'two' )
            self.setProgram( 'xterm' )

        self.setStyle(  args.style[0] )
        self.setProgram( args.program[0] )


if __name__ == "__main__":
    appslap = AppSlap()
    appslap.parseCmdLineOptions( sys.argv )
    appslap.launchWindows()

