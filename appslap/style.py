
# An abstract Style class that all styles must implement
class Style:

    # @returns: the name (str) of the style
    @classmethod
    def getName( cls ):
        raise NotImplementedError

    # @returns: a description (str) of the style
    def getDescription( self ):
        raise NotImplementedError

    # @returns: array of Tuple( width, height, down, right )
    # all expressed as percentages of screen size
    #
    #  --> right
    # |
    # v
    #   down
    #
    # NOTE: for some yet unknown reason it is best to give
    #       the percentages in equal ten's
    #
    def getLayout( self ):
        raise NotImplementedError


class StyleTwo( Style ):

    @classmethod
    def getName( cls ):
        return "two"

    def getDescription( self ):
        return "The screen split in two equal horizontal splits."

    def getLayout( self ):
        return [ self.__getLeft(), self.__getRight() ]

    def __getLeft( self ):  return ( 50, 100, 0, 0 )
    def __getRight( self ): return ( 50, 100, 0, 50 )


class StyleThree( Style ):

    @classmethod
    def getName( cls ):
        return "three"

    def getDescription( self ):
        return "The screen split in three, one bigger to the left, two equal smaller to the left."

    def getLayout( self ):
        return [ self.__getLeftUp(), self.__getLeftDown(), self.__getRight() ]

    def __getLeftUp( self ):   return ( 50,  50,  0,  0 )
    def __getLeftDown( self ): return ( 50,  50, 50,  0 )
    def __getRight( self ):    return ( 50, 100,  0, 50 )


class StyleFour( Style ):

    @classmethod
    def getName( cls ):
        return "four"

    def getDescription( self ):
        return "The screen split in four equal splits."

    def getLayout( self ):
        return [ self.__getLeftUp(), self.__getLeftDown(), 
                self.__getRightUp(), self.__getRightDown() ]

    def __getLeftUp( self ):    return ( 50, 50,  0,  0 )
    def __getLeftDown( self ):  return ( 50, 50, 50,  0 )
    def __getRightUp( self ):   return ( 50, 50,  0, 50 )
    def __getRightDown( self ): return ( 50, 50, 50, 50 )


class StyleFourFour( Style ):

    @classmethod
    def getName( cls ):
        return "fourfour"

    def getDescription( self ):
        return "The screen split in four splits, a bigger to the right, three equal smaller to the left."

    def getLayout( self ):
        return [ self.__getLeftUp(), self.__getLeftMiddle(),  self.__getLeftDown(), 
                self.__getRight() ]

    def __getLeftUp( self ):     return ( 40,  30,  0,  0 )
    def __getLeftMiddle( self ): return ( 40,  30, 30,  0 )
    def __getLeftDown( self ):   return ( 40,  40, 60,  0 )
    def __getRight( self ):      return ( 60, 100,  0, 50 )

