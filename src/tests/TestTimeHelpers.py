import unittest
from Helpers import TimeHelpers

class TestTimeHelpers(unittest.TestCase):

    def testRewind(self):
        inn = '2020-02-29 00:15:00'
        expected = "2020-02-28 23:15:00"
        actual = TimeHelpers.rewind(inn, 1, 60)
        self.assertEqual(expected, TimeHelpers.convertNumericTimeToString(actual))


    def testConvertNumericToString(self):
        inn = "1588899600000"
        expected = "2020-05-08 01:00:00"
        actual = TimeHelpers.convertNumericTimeToString(int(inn))
        self.assertEqual(actual, expected)
