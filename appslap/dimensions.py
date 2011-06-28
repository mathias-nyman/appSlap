import Tkinter #FIXME: make this a requirement, and then the setup.py will take care of requiring it ( or does it??? )

class TkDimensionsGetter:

    def __init__( self, initialWidthGuess = 2000, initialHeightGuess = 2000 ):
        self.__dim = (0,0)

        # This will "flash" a window, to get the real window size
        self.__root= Tkinter.Tk();
        self.__root.title('')
        self.__frame = Tkinter.Frame(self.__root, bg="black", width=initialWidthGuess, height=initialHeightGuess)
        self.makeKeyBindings()
        self.__frame.pack()
        self.__root.mainloop()
        self.__root.destroy()

    def getDimensions( self ):
        return self.__dim

    def tellSize(self, event):
        width = event.widget.winfo_width()
        height = event.widget.winfo_height()
        self.__dim = (width, height)
        self.__root.quit()
    
    # Unless there is some event to subscribe to for when
    # the window has loaded, this hack can be used
    def makeKeyBindings(self):
        # The mouse pointer entered the widget 
        # (this event doesn't mean that the user pressed the Enter key!)
        self.__frame.bind("<Enter>", self.tellSize)
        # The mouse pointer left the widget
        self.__frame.bind("<Leave>", self.tellSize)
        # Any key is pressed
        self.__frame.bind("<Key>", self.tellSize)
        
