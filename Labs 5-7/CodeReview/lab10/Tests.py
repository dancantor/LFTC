import unittest

from Parser import Parser
from ParserOutput import ParserOutput


class MyTestCase(unittest.TestCase):
    def testCanonicalCollection(self):
        parser = Parser("input/g1.txt")
        print(parser.computeCanonicalCollection())
        self.assertEqual(parser.computeCanonicalCollection().pop(1), [("S'", ['S.'])])
        self.assertNotEqual(parser.computeCanonicalCollection().pop(0), [("S'", ['.aA'])])
        self.assertEqual(parser.computeCanonicalCollection().pop(0), [("S'", ['.S']), ('S', ['.aA'])])

    def testClosure(self):
        parser = Parser("input/g1.txt")
        self.assertEqual(parser.closure([("S'", ['S.'])]), [("S'", ['S.'])])
        self.assertNotEqual(parser.closure([("S'", ['S.'])]), [("S'", ['.aA'])])

    def testGoTo(self):
        parser = Parser("input/g1.txt")
        self.assertEqual(parser.goTo([("S'", ['.S']), ('S', ['.aA'])],"S"),  [("S'", ['S.'])])
        self.assertNotEqual(parser.goTo([("S'", ['.S']), ('S', ['.aA'])], "A"),  [("S'", ['S.'])])
        self.assertEqual(parser.goTo([("S'", ['.S']), ('S', ['.aA'])], "A"), None)


if __name__ == '__main__':
    unittest.main()
