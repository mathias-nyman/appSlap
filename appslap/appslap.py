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


DEBUG=False
def debug( line ):
    if DEBUG:
        print line

VERBOSE=False
def verbose( line ):
    if VERBOSE:
        print line

class AppSlap:

    class Defaults:
        program=Xterm
        style=StyleFourFour

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
        self.__availableArea = (-1, -1)
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
        self.__availableArea = TkDimensionsGetter().getDimensions()
        debug( "MILESTONE: got dimensions from Tk: " + str(self.__availableArea) )


    def issueSystemCall( self, cmd ):
            subprocess.Popen( cmd.split(' ') )

    def launchWindows( self ):
        debug( "MILESTONE: launching windows with commands:")
        for launcher in self.__programLaunchers:
            cmd = str(launcher)
            verbose( cmd )
            self.issueSystemCall( cmd )


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
            geometry.setAvailableArea( *self.__availableArea )
            geometry.setGeometry( *lay )
            for program in self.Options.programs:
                if program.getName() == programName:
                    self.__programLaunchers.append( program() )
                    self.__programLaunchers[-1].setGeometry( geometry ) 
        if len(self.__programLaunchers) is 0:
            raise Exception( "No program found to match the name: " + programName )
        else:
            debug( "MILESTONE: using program: " + programName )

        self.optimizeGeometries()
       

    def optimizeGeometries( self ):
        geometries = [ p.getGeometry() for p in self.__programLaunchers ]
        geometryOptimizer = GeometryOptimizer( geometries )
        geometryOptimizer.optimize()


    def parseCmdLineOptions( self, argv ):
        try:
            import argparse

            # NOTE: we might want to give this to the constructor of ArgumentParser if we want to use
            # e.g newline characters in help text
            # formatter_class=RawTextHelpFormatter
            parser = argparse.ArgumentParser(description="Launch a set of windowed programs, e.g. xterm's.")
            parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False,
                    help='turn on debug output')
            parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                    help='turn on verbose output')
            parser.add_argument('-p', '--program', dest='program', nargs=1, default=[self.Defaults.program.getName()],
                    choices=[p.getName() for p in self.Options.programs],
                    help='program to launch')
            parser.add_argument('style', nargs='?', default=[self.Defaults.style.getName()],
                    choices=[s.getName() for s in self.Options.styles],
                    help='style of window positioning')
            #FIXME: argparse works outside this try, but only with one complex type argument
            #  UPDATE: this actually seems to work with python 2.7.1
            args = parser.parse_args(argv)

        except ImportError, e:
            #TODO: argparse is only in python >= 2.7, offer an alternative
            debug("ERROR: argparse failed.")
            self.setStyle( 'two' )
            self.setProgram( 'xterm' )

        global DEBUG
        global VERBOSE
        DEBUG = args.debug
        VERBOSE = True if args.debug else args.verbose
        # NOTE: we need to join() because argparse makes style a list if default, and a string if option given
        debug(''.join(args.style))
        self.setStyle( ''.join(args.style) )
        self.setProgram( args.program[0] )


def main():
    appslap = AppSlap()
    appslap.parseCmdLineOptions( sys.argv[1:] )
    appslap.launchWindows()

if __name__ == "__main__":
    main()

