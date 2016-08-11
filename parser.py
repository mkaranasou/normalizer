import os
import sys
from math import log

sys.path.extend([os.path.dirname(os.path.realpath(__file__))])

import string
from nltk import WordNetLemmatizer, re

from models.pos_tagger import POSTagger
from models.spell_checker import EnchantSpellChecker
from utils.constants import C
from utils.enums import DictTypeEnum

__author__ = 'm.karanasou'

# Globals
wnl = WordNetLemmatizer()


class Parser(object):
    """

    """
    def __init__(self, spellcheck=True, deploy_abbreviations=True, pos_tag=True, tags_to_keep=None, tags_to_remove=None):
        self.spellcheck = spellcheck
        self.deploy_abbreviations = deploy_abbreviations
        self.str_seq = ""
        self.split_str_seq = None
        self.result = None
        self.has_been_split = False
        self.pos_tagger = None
        self.pos_tag = pos_tag
        if self.pos_tag:
            self.pos_tagger = POSTagger(tags_to_keep, tags_to_remove)
        self.spell_checker = None
        self.abbreviations = None
        # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
        self._words = open(C.ROOT_PATH + 'data/words_by_frequency.txt').read().split()
        self._wordcost = dict((k, log((i + 1) * log(len(self._words)))) for i, k in enumerate(self._words))
        self._maxword = max(len(x) for x in self._words)

        if self.spellcheck:
            self.spell_checker = EnchantSpellChecker(DictTypeEnum.EN_US)
        if self.deploy_abbreviations:
            self.abbreviations = self._load_abbreviations()

    def normalize(self, str_seq):
        if str_seq == "" or str_seq is None:
            raise Exception("Even I can't normalize emptiness...")
        self.str_seq = self._remove_non_ascii_chars(str_seq)
        return self._normalize_string()

    def _normalize_string(self):
        self.has_been_split = self._can_be_split()
        if self.has_been_split:
            if self.deploy_abbreviations:
                self._deploy_abbreviations()
            self._remove_special_chars()
            if self.pos_tag:
                self.proper_names = [v for v in self.pos_tagger.pos_tag(self.split_str_seq)]
            else:
                self.proper_names = self.split_str_seq
        else:
            self.proper_names.append(self.str_seq)

        self._plurar_to_singular()

        return self.proper_names

    def _load_abbreviations(self):
        abbrev = {}
        with open(C.ROOT_PATH + '/data/abbreviations.csv', 'rb') as abbrev_file:
            for line in abbrev_file.readlines():
                split_line = line.split(",")
                term = split_line[0].replace(".", "")
                deployed_term = split_line[1].replace("\n", "") \
                    .replace("\"", "") \
                    .replace("\r", "") \
                    .replace("(in the Bible) ", "") \
                    .replace("(s)", "") \
                    .replace("(n)", "") \
                    .replace("(ly)", "") \
                    .replace(" (to)", "") \
                    .replace(" (dialect)", "") \
                    .replace(" (with)", "") \
                    .replace("(al)", "") \
                    .replace(" (of)", "") \
                    .replace("(in dates) ", "") \
                    .replace("(in the Apocrypha) ", "")
                if term not in abbrev:
                    abbrev[term.lower()] = deployed_term.lower()

        return abbrev

    def _deploy_abbreviations(self):
        for each in self.split_str_seq:
            if each in self.abbreviations:
                self.split_str_seq[self.split_str_seq.index(each)] = self.abbreviations[each]

    def _split_all_lower(self, word):
        """Uses dynamic programming to infer the location of spaces in a string
        without spaces."""

        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        def best_match(i):
            candidates = enumerate(reversed(cost[max(0, i-self._maxword):i]))
            return min((c + self._wordcost.get(word[i-k-1:i], 9e999), k+1) for k, c in candidates)

        # Build the cost array.
        cost = [0]
        for i in range(1, len(word)+1):
            c, k = best_match(i)
            cost.append(c)

        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(word)
        while i > 0:
            c, k = best_match(i)
            assert c == cost[i]
            out.append(word[i-k:i])
            i -= k

        return reversed(out)

    def _remove_special_chars(self):
        """

            :return:
        """

        for each in self.split_str_seq:
            clean = re.sub(r'\W|\d', '', each)
            if len(clean) > 1 or len(self.split_str_seq) == 1:
                self.split_str_seq[self.split_str_seq.index(each)] = clean
            else:
                self.split_str_seq.remove(each)

    @staticmethod
    def _is_plural(word):
        lemma = wnl.lemmatize(word, 'n')
        plural = True if word is not lemma else False
        return plural, lemma

    def _singularize(self, word_plural):
        """
        http://stackoverflow.com/questions/18911589/how-to-test-whether-a-word-is-in-singular-form-or-not-in-python
        :param word_plural:
        :return:
        """
        # todo: check this out https://pypi.python.org/pypi/inflect

        plurar_result = self._is_plural(word_plural)

        if plurar_result[0]:
            return plurar_result[1]
        else:
            return word_plural

    def _plurar_to_singular(self):
        for nameIndex in range(0, len(self.proper_names)):
            self.proper_names[nameIndex] = self._singularize(self.proper_names[nameIndex])
        return self.proper_names

    def _can_be_split(self):
        # a name can be like TollControl_AFM or sourcetype
        has_been_split = False
        pascal_or_camel_case = False
        all_lower = False
        temp = []

        # Remove digits
        self.str_seq = re.sub(r'\d', '', self.str_seq)
        self.str_seq = re.sub(r'!@#\$\%\^&\*\(\)', '', self.str_seq)

        # check if word in capitals exist
        # capitalized = re.findall(r'\b[A-Z]{3,}\b', self.name)
        # print("capitalized", capitalized)

        # Check snake_case
        if "_" in self.str_seq:
            self.split_str_seq = self.str_seq.split("_")
            has_been_split = True

        # this means we have a possible TollControl_AFM-like attribute
        if has_been_split:
            # try further split for each in split words
            for split_word in self.split_str_seq:
                if split_word != '':
                    word = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', split_word)
                    split_temp = word.split(' ')

                    # we split 'Toll Control' to 'Toll' 'Control'
                    if len(split_temp) > 1:
                        for each in split_temp:
                            temp.append(each)
                        pascal_or_camel_case = True
                    else:
                        temp.append(split_temp[0])
        else:
            temp_word = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', self.str_seq)
            temp = temp_word.split(' ')

        if len(temp) == 1:
            is_correct = self.spell_checker.is_correct(temp[0])
            # if len([c for c in temp[0] if c.islower()]) == len(temp[0]) or not is_correct:
            if temp[0].islower() or temp[0].isupper() or not is_correct:
                all_lower = True
                temp = [x for x in self._split_all_lower(temp[0].lower())]  # tollcontrol or Iscustomer
                # print "after split", temp

        if pascal_or_camel_case or len(temp) >= 1 or all_lower:
            self.split_str_seq = [a.lower() for a in temp]
            has_been_split = True

        return has_been_split

    def _remove_non_ascii_chars(self, txt):
        """
        Returns an ascii free string
        :return:
        """
        return str(filter(lambda x: x in string.printable, txt))


if __name__ == "__main__":
    parser = Parser(spellcheck=True, deploy_abbreviations=True)
    print parser.normalize("somename")
    print parser.normalize("some_name")
    print parser.normalize("someName")
    print parser.normalize("SomeName")
    print parser.normalize("SomeName123435")
    print parser.normalize("s123435somename")
    print parser.normalize("ClientName")
    print parser.normalize("Iscustomer")

    parser = Parser(spellcheck=True, deploy_abbreviations=False)
    print parser.normalize("s123435somename")
