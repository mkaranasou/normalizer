import enchant
from enchant.checker import SpellChecker
from utils.enums import DictTypeEnum


class SpellCheckerBase(object):
    pass


class EnchantSpellChecker(SpellCheckerBase):
    def __init__(self, dict_enum=DictTypeEnum.EN_US):
        self.lang = self._get_dict_lang(dict_enum)
        self.errors_in_text = []
        self.correct_list = []
        if not enchant.dict_exists(self.lang):
            raise Exception("Dictionary for {} was not found in the system.".format(self.lang))
        self._d = enchant.request_dict(self.lang)
        self.spell_checker = SpellChecker(self._d.tag)

    def get_errors_in_text(self, text):
        self.spell_checker.set_text(text)
        for err in self.spell_checker:
            self.errors_in_text.append(err.word)
        return self.errors_in_text

    def is_correct(self, word):
        return self.spell_checker.check(word)

    def correct_word(self, word):
        self.spell_checker.set_text(word)
        self.spell_checker.word = word
        return self.spell_checker.suggest()

    # so as not to create a new spellchecker object for every tweet
    def clean_up(self):
        self._d = None  #for the current dictionary
        self.spell_checker = None
        self.errors_in_text = []
        self.correct_list = []

    def get_suggestions(self, word):
        return self.spell_checker.suggest(word)

    def _get_dict_lang(self, dict_enum):
        if dict_enum == DictTypeEnum.EN_US:
            return 'en_US'
        raise Exception("Not supported")
