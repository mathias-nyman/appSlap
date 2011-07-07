import appslap
import unittest

# This class is for black-box testing, not unit testing
class TestAppSlap(unittest.TestCase):
    
    def setUp(self):
        self.__appslap = appslap.AppSlap()
        self.__appslap.parseCmdLineOptions(['-p', 'xterm', '-s', 'three'])
        pass

    def testSomething(self):
        #TODO: can we do black-box testing here?
        pass
