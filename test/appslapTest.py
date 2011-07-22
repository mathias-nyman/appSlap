import appslap
import unittest
import mock

# This class is for black-box testing.
#
# It is intended for easy testing with real life data, since
# nothing seems to be the same from system to system.
class TestAppSlap(unittest.TestCase):
    
    def setUp(self):
        self.__appslap = appslap.AppSlap()

        self.__appslap.getFromSystem = mock.Mock( return_value="""
           1024x768       50.0*+   60.0     40.0  
        """)

        # TODO: this would be the output of only `xrandr`, make getFromSystem() actually get that,
        #       instead of `xrandr -q | grep '*'`

        #self.__appslap.getFromSystem = mock.Mock(return_value="""
        #    Screen 0: minimum 320 x 200, current 1024 x 768, maximum 8192 x 8192
        #    LVDS1 connected 1024x768+0+0 (normal left inverted right x axis y axis) 246mm x 184mm
        #       1024x768       50.0*+   60.0     40.0  
        #       800x600        60.3     56.2  
        #       640x480        60.0     59.9  
        #    VGA1 disconnected (normal left inverted right x axis y axis)
        #""")
        self.__appslap.issueSystemCall = mock.Mock(return_value=True)

        #TODO: how to make appslap use this? 
        #TODO: also mock the constructor, or change so that the contructor does not launch Tk window
        self.__dimGetter = appslap.TkDimensionsGetter()
        self.__dimGetter.getDimensions = mock.Mock(return_value=(1024, 728)) 
        pass

    # NOTE: if needed to make a testcase fail expectedly, use this:
    #@unittest.expectedFailure
    def testStyleThreeOn1024x768(self):
        self.__appslap.parseCmdLineOptions(['-p', 'xterm', '-s', 'three'])
        self.__appslap.getFromSystem.assert_called_with("xrandr -q | /bin/grep '*'")
        self.__appslap.launchWindows()

        # This feature to assert multiple calls to a mocked function is comming sometime in 2011
        #self.__appslap.issueSystemCall.assert_called_once_with('xterm -bg black -fg gray -cr cyan -geometry 84x27+0+0 +cm +dc +sb zsh')
        #self.__appslap.issueSystemCall.assert_called_once_with('xterm -bg black -fg gray -cr cyan -geometry 84x27+0-0 +cm +dc +sb zsh')
        #self.__appslap.issueSystemCall.assert_called_once_with('xterm -bg black -fg gray -cr cyan -geometry 84x55-0+0 +cm +dc +sb zsh')
        #self.__appslap.issueSystemCall = mock.Mock(return_value=True)

        expectedCallsWithArguments = [
                (('xterm -bg black -fg gray -cr cyan -geometry 84x26+0+0 +cm +dc +sb zsh',), {}), 
                (('xterm -bg black -fg gray -cr cyan -geometry 84x27+0-0 +cm +dc +sb zsh',), {}),
                (('xterm -bg black -fg gray -cr cyan -geometry 84x55-0+0 +cm +dc +sb zsh',), {})
                ]
        self.assertTrue( expectedCallsWithArguments == self.__appslap.issueSystemCall.call_args_list )
        pass
