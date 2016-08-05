import json
import nltk as nltk
from utils.constants import C


class BackoffTagger(nltk.TaggerI):
    def __init__(self):
        self._taggers = [nltk.PerceptronTagger()]


class POSTagger(object):
    """
        Part of speech tagger. Uses a custom model and nltk to build
        a custom pos tagger that works well on short informal phrases.
        @tags_to_keep:
        @tags_to_remove:
    """
    def __init__(self, tags_to_keep=None, tags_to_remove=None):
        self.tags_to_keep = tags_to_keep if isinstance(tags_to_keep, list) else []
        self.tags_to_remove = tags_to_remove if isinstance(tags_to_remove, list) else []
        self.text_list = []
        self.gate_tagger = []
        self.result = {}
        self.gate_custom_model = self._load_custom_model()

    def pos_tag(self, text_list):
        if not isinstance(text_list, list):
            raise Exception("Invalid argument. text_list must be of type list")
        self.text_list = text_list
        self._custom_model_pos_tag()
        if len(self.tags_to_keep) > 0 or len(self.tags_to_remove) > 0:
            return self._filter_results()
        print self.result
        return self.result

    def _filter_results(self):
        filtered = {}
        for k, v in self.result.items():
            if k in self.tags_to_keep and k not in self.tags_to_remove:
                filtered[k] = v
        return filtered

    def _keep_nouns(self):
        nouns = []
        for k, v in self.result.items():
            if "NN" == v or "NNS" == v:
                # g.logger.debug("{0} has errors: {1}".format(k, self.spell_checker.spell_checker_for_word(k)))
                # if self.spell_checker.spell_checker_for_word(k) is None:
                nouns.append(k)
        if len(nouns) == 0:
            for k, v in self.result.items():
                if "NNP" == v:
                    # g.logger.debug("{0} has errors: {1}".format(k, self.spell_checker.spell_checker_for_word(k)))

                    # if self.spell_checker.spell_checker_for_word(k) is None:
                    nouns.append(k)
        if len(nouns) == 0:
            for k, v in self.result.items():
                if "VB" in v:
                    # if self.spell_checker.spell_checker_for_word(k) is None:
                    nouns.append(k)
        return nouns

    def _custom_model_pos_tag(self):
        """
            Get pos tagging results using custom tagger with the model provided by gate twitter tagger.
            Reference: https://gate.ac.uk/wiki/twitter-postagger.html
            L. Derczynski, A. Ritter, S. Clarke, and K. Bontcheva, 2013: "Twitter
            Part-of-Speech Tagging for All: Overcoming Sparse and Noisy Data". In:
            Proceedings of the International Conference on Recent Advances in Natural
            Language Processing.
        """
        tagger = nltk.tag.UnigramTagger(model=self.gate_custom_model, backoff=BackoffTagger())
        # if len(self.text_list) == 1:
        #     tagger = nltk.tag.UnigramTagger(model=train_model, backoff=default_tagger)
        # elif len(self.text_list) == 2:
        #     tagger = nltk.tag.BigramTagger(model=train_model, backoff=default_tagger)
        # elif len(self.text_list) >= 3:
        #     tagger = nltk.tag.TrigramTagger(model=train_model, backoff=default_tagger)

        self.result = dict(tagger.tag(self.text_list))

    def _load_custom_model(self):
        with open(C.ROOT_PATH + 'data/custom_gate_post_tag_model.json', 'r') as f:
            model = json.load(f)
        return model
