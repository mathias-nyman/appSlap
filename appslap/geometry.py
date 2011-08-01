
# Represents X Geometry
class Geometry:

    COLUMN_SIZE = 6
    ROW_SIZE = 13

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

        self.__width = int(width / 100.0 * float(maxWidth) / Geometry.COLUMN_SIZE)
        self.__height = int(height / 100.0 * float(maxHeight) / Geometry.ROW_SIZE)

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

    # NOTE: use with caution!
    def setHardCodedGeometry( self, width, height, down, right ):
        self.__width = width
        self.__height = height
        self.__down = down
        self.__right = right

    def getWidth( self ):
        return self.__width

    def getHeight( self ):
        return self.__height

    def getDown( self ):
        return self.__down

    def getRight( self ):
        return self.__right

    def getWidthInPixels( self ):
        return self.__width * Geometry.COLUMN_SIZE

    def getHeightInPixels( self ):
        return self.__height * Geometry.ROW_SIZE

    def getAvailableAreaInCharacters( self ):
        return ( int(self.__availableWidth / Geometry.COLUMN_SIZE), 
                int(self.__availableHeight / Geometry.ROW_SIZE) )

    def __str__( self ):
        asStr = str(self.__width)
        asStr += 'x' + str(self.__height)
        #TODO: this is sort of a hack, make it better!
        asStr += '+' + str(self.__right) if (self.__right - self.__screenWidth/2) < 0 else '-0'
        asStr += '+' + str(self.__down) if (self.__down - self.__screenHeight/2) < 0 else '-0'
        return asStr


# A class to optimze geomertries to perfectly fit the screen
# This is needed e.g when two geometries are 50% width, but when
# converted to columns, both together are one column less then
# the whole screen width
class GeometryOptimizer:

    #TODO: Optimization might not always be wanted, so the style should define if
    # it wants it or not!
    # geometries is a list of Geometry objects
    def __init__( self, geometries):
        self.__geometries = geometries

    def optimize( self ):
        for geometry in self.__geometries:
            self.__adjustWidth( geometry )
            self.__adjustHeight( geometry )

    def __adjustWidth( self, geometry ):
        toOptimize = []
        for otherGeometry in self.__geometries:
            if self.__onSameHorizontalLine( geometry, otherGeometry ):
                # NOTE: alse the geometry to compare with will be appended here
                # FIXME: only compare two at a time, since the onSameXXXLine func does 
                #       not actually check if they ALL are on the same line, this should work, right?
                # THIS DOES NOT WORK
                if len(toOptimize) < 2: 
                    toOptimize.append(otherGeometry)
        self.__optimizeRow( toOptimize )

    def __adjustHeight( self, geometry ):
        toOptimize = []
        for otherGeometry in self.__geometries:
            if self.__onSameVerticalLine( geometry, otherGeometry ):
                # NOTE: alse the geometry to compare with will be appended here
                # FIXME: only compare two at a time, since the onSameXXXLine func does 
                #        not actually check if they ALL are on the same line, this should work, right?
                # THIS DOES NOT WORK
                if len(toOptimize) <= 2:
                    toOptimize.append(otherGeometry)
        self.__optimizeColumn( toOptimize )

    #
    #              ----  
    #  ---------->|    | 
    #   r1        |    | 
    #        ---- | w1 |
    #  ---->| w2 ||    |
    #   r2  |    ||    |
    #        ----  ---- 
    #
    def __onSameVerticalLine( self, geometry, otherGeometry ):
        w1 = geometry.getWidthInPixels()
        r1 = geometry.getRight()

        w2 = otherGeometry.getWidthInPixels()
        r2 = otherGeometry.getRight()

        if r1 + w1 < r2:
            return False
        if r1 > w2 + r2:
            return False

        # they are on the same vertical line
        return True

    #
    #  |      |
    #  | d1   | d2
    #  V      |
    #   ----  |
    #  |    | |
    #  |    | V
    #  | h1 | ----
    #  |    || h2 |
    #  |    ||    |
    #   ----  ----
    #
    def __onSameHorizontalLine( self, geometry, otherGeometry ):
        h1 = geometry.getHeightInPixels()
        d1 = geometry.getDown()

        h2 = otherGeometry.getHeightInPixels()
        d2 = otherGeometry.getDown()

        if d1 + h1 < d2:
            return False
        if d1 > d2 + h2:
            return False

        # they are on the same horizontal line
        return True

    def __optimizeRow( self, geometries ):
        #NOTE: optimze the biggest geometry!
        #NOTE: direction of the increase, e.g width -> increase width rightwards, might want to change offset instead

        totalColumnsUsed = 0
        maxColumns = geometries[-1].getAvailableAreaInCharacters()[0]
        if maxColumns < 0:
            # TODO: handle this "error" in a more fluent way
            return False

        for g in geometries:
            totalColumnsUsed += g.getWidth()
            #FIXME: This is a very dirty hack to take into account the window borders!
            #       Make the Tk dimensions getter also take care of reading window border widths!
            totalColumnsUsed += 0.75

        # TODO: handle more increasing/decreasing then +/- 1
        for g in geometries:
            newWidth = g.getWidth()
            if totalColumnsUsed > maxColumns:
                newWidth -= 1
                totalColumnsUsed -= 1
            elif totalColumnsUsed < maxColumns:
                newWidth += 1
                totalColumnsUsed += 1
            g.setHardCodedGeometry( newWidth, g.getHeight(), g.getDown(), g.getRight() )

        return True

    def __optimizeColumn( self, geometries ):
        #NOTE: optimze the biggest geometry!
        #NOTE: direction of the increase, e.g height -> increase height downards, might want to change offset instead

        totalRowsUsed = 0
        maxRows = geometries[-1].getAvailableAreaInCharacters()[1]
        if maxRows < 0:
            # TODO: handle this "error" in a more fluent way
            return False

        for g in geometries:
            totalRowsUsed += g.getHeight()
            #FIXME: This is a very dirty hack to take into account the window borders!
            #       Make the Tk dimensions getter also take care of reading window border widths!
            totalRowsUsed += 1.5 

        # TODO: handle more increasing/decreasing then +/- 1
        for g in geometries:
            newHeight = g.getHeight()
            if totalRowsUsed > maxRows:
                newHeight -= 1
                totalRowsUsed -= 1
            elif totalRowsUsed < maxRows:
                newHeight += 1
                totalRowsUsed += 1
            g.setHardCodedGeometry( g.getWidth(), newHeight, g.getDown(), g.getRight() )

        return True


