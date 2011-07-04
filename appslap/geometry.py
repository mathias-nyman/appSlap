
# Represents X Geometry
class Geometry:

    def __init__( self ):
        self.__screenWidth = 800 # pixels
        self.__screenHeight = 600 # pixels
        self.__availableWidth = -1
        self.__availableHeight = -1
        # the following are in X geometry units
        self.__width = 1
        self.__height = 1
        self.__down = 0
        self.__right = 0

    def setDimensions( self, width, height ):
        # TODO: do more precise conversion from percentage to X geometry units
        maxWidth = self.__screenWidth if self.__availableWidth < 0 else self.__availableWidth
        maxHeight = self.__screenHeight if self.__availableHeight < 0 else self.__availableHeight

        self.__width = int(width / 100.0 * maxWidth / 6.0)
        self.__width += -1 #magic
        self.__height = int(height / 100.0 * maxHeight / 13.0)
        self.__height += -1 #magic

    def setPosition( self, down, right ):
        #TODO: geometry can be + or -, depending on from which end, and sometimes
        #  it makes more sense to use one rather then the other
        maxWidth = self.__screenWidth if self.__availableWidth < 0 else self.__availableWidth
        maxHeight = self.__screenHeight if self.__availableHeight < 0 else self.__availableHeight

        self.__down = int(down * maxHeight / 100.0) if down is not 0 else 0
        self.__right = int(right * maxWidth / 100.0) if right is not 0 else 0

        #TODO: this is true if e.g menubar is on top, but what if it is on the bottom?
        if maxWidth != self.__screenWidth and self.__down != 0:
            self.__right += self.__screenWidth - maxWidth
        if maxHeight != self.__screenHeight and self.__down != 0:
            self.__down += self.__screenHeight - maxHeight

    def setScreenSize( self, width, height ):
        self.__screenWidth = width
        self.__screenHeight = height

    #TODO: also specify from where the difference comes from ( e.g menubar at top or bottom? )
    def setAvailableArea( self, width, height ):
        self.__availableWidth = width if width > 0 else -1
        self.__availableHeight = height if height > 0 else -1

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

