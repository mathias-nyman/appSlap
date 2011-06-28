
# Represents X Geometry
class Geometry:

    def __init__( self ):
        self.__screenWidth = 800 # pixels
        self.__screenHeight = 600 # pixels
        # the following are in X geometry units
        self.__width = 1
        self.__height = 1
        self.__down = 0
        self.__right = 0

    def setDimensions( self, width, height ):
        # TODO: do more precise conversion from percentage to X geometry units
        self.__width = int(width / 100.0 * self.__screenWidth / 6.1)
        self.__width += 1 #magic
        self.__height = int(height / 100.0 * self.__screenHeight / 14.3)
        self.__height -= 0 #magic

    def setPosition( self, down, right ):
        #TODO: geometry can be + or -, depending on from which end, and sometimes
        #  it makes more sense to use one rather then the other
        self.__down = int(down * self.__screenHeight / 100.0) if down is not 0 else 0
        self.__right = int(right * self.__screenWidth / 100.0) if right is not 0 else 0

    def setScreenSize( self, width, height ):
        self.__screenWidth = width
        self.__screenHeight = height

    def setGeometry( self, width, height, down, right ):
        self.setDimensions( width, height )
        self.setPosition( down, right )

    def __str__( self ):
        asStr = str(self.__width)
        asStr += 'x' + str(self.__height)
        #TODO: this is sort of a hack, make it better!
        asStr += '+' + str(self.__right) if (self.__right - self.__screenWidth/2) < 0 else '-0'
        asStr += '+' + str(self.__down) if (self.__down - self.__screenHeight/2) < 0 else '-0'
        return asStr

