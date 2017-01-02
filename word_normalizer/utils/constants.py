import os


class C(object):
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).replace("utils", "")
    NOUNS = ['N', 'NP', 'NN', 'NNS', 'NNP', 'NNPS']
    VERBS = ['V', 'VD', 'VG', 'VN', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    ADJECTIVES = ['ADJ', 'JJ', 'JJR', 'JJS']
    ADVERBS = ['RB', 'RBR', 'RBS', 'WRB']