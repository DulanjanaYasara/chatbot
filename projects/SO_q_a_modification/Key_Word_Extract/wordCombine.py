import nltk


def word_combination(pos_tagged_sentence):
    # Finding entities
    grammar = r"""
    EN: {<CD>*<JJ.*>?<NN.*>*<CD>*}
    """

    cp = nltk.RegexpParser(grammar)
    result = cp.parse(pos_tagged_sentence)

    return result
