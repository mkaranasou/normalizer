import unittest

from word_normalizer.parser import Parser


class ParserTests(unittest.TestCase):
    def test(self):
        parser = Parser(spell_check=True, deploy_abbreviations=True)
        result = parser.normalize("somename")
        self.assertEquals(['some', 'name'], result)