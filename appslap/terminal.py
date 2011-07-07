
# TODO: make Terminal -> App, and terminal.py app.py
class Terminal:

    class Color:
        BLACK   = 'black'
        GRAY    = 'gray'
        WHITE   = 'white'
        CYAN    = 'cyan'
        YELLOW  = 'yellow'
        GREEN   = 'green'
        MAGENTA = 'magenta'
        PURPLE  = 'purple'
        RED     = 'red'
        # TODO: more...

    # @returns: the name (str) of the Terminal
    @classmethod
    def getName( cls ):
        raise NotImplementedError

    def setBgColor( self, color ):
        raise NotImplementedError

    def setFgColor( self, color ):
        raise NotImplementedError

    def setShell( self, shell ):
        raise NotImplementedError

    def setGeometry( self, geometry ):
        raise NotImplementedError

    def __str__( self ):
        raise NotImplementedError


class Xterm( Terminal ):

    __program = 'xterm'

    def __init__( self ):
        self.__bg = Terminal.Color.BLACK
        self.__fg = Terminal.Color.GRAY
        self.__cr = Terminal.Color.CYAN
        self.__flags = "+cm +dc +sb"
        self.__shell = "zsh"
        self.__geometry = None

    @classmethod
    def getName( cls ):
        return cls.__program

    def setBgColor( self, color ):
        self.__bg = color

    def setFgColor( self, color ):
        self.__fg = color

    def setShell( self, shell ):
        self.__shell = shell

    def setGeometry( self, geometry ):
        self.__geometry = geometry

    def __str__( self ):
        asStr = self.__program + \
            ' -bg ' + self.__bg + \
            ' -fg ' + self.__fg + \
            ' -cr ' + self.__cr + \
            ' -geometry ' + str(self.__geometry) + \
            ' ' + self.__flags + \
            ' ' + self.__shell
        return asStr


class GnomeTerminal( Terminal ):

    __program = 'gnome-terminal'

    def __init__( self ):
        #TODO: how to set bg/fg colors in gnome-terminal
        self.__flags = "" #TODO: some needed, or should users default saved profile be respected??
        self.__shell = "zsh"
        self.__geometry = None

    @classmethod
    def getName( cls ):
        return cls.__program

    def setBgColor( self, color ):
        pass

    def setFgColor( self, color ):
        pass

    def setShell( self, shell ):
        self.__shell = shell

    def setGeometry( self, geometry ):
        self.__geometry = geometry

    def __str__( self ):
        asStr = self.__program + \
            ' --geometry ' + str(self.__geometry) + \
            ' -e ' + self.__shell
        return asStr
