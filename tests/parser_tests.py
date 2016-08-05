import unittest
from parser import Parser

class ParserTests(unittest.TestCase):
    def test(self):
        parser = Parser(spellcheck=True, deploy_abbreviations=True)
        result = parser.normalize("somename")
        self.assertEquals(['some', 'name'], result)