from re import findall, search, split

from nltk import RegexpParser
from nltk.stem import WordNetLemmatizer

from main import CoreNLP


def noun_verbs(text):
    """Used to obtain the nouns and verbs of the text in the lemmatized form"""
    for sentence in text:
        pos_tagged_text = []
        for parameter in sentence['tokens']:
            pos_tagged_text.append((parameter['word'].encode('ascii'), parameter['pos'].encode('ascii')))

        nouns = list(entity_generation(word_combination(pos_tagged_text)[0], 'n'))
        verbs = list(entity_generation(word_combination(pos_tagged_text)[1], 'v'))

        yield nouns, verbs


def entity_generation(pos_tagged_tree, verb_noun):
    """Used for the entity generation using the chunked entity tree
    :param verb_noun: String
    :type pos_tagged_tree: Tree
    """
    # Considering entities in the sentence
    sent_entities = []
    # This list should be given in simple case.
    unimp_tokens = ['thank', 'thanks', 'anyone', 'everyone', 'anyhelp', 'hi', 'please', 'help', 'welcome']
    abbrv = ['e.g', 'i.e', 'um', 'etc']

    # Traversing through the tree
    whole_entity = []
    neglect = False
    for result_tree in pos_tagged_tree:
        if type(result_tree) is not tuple:
            entity = []
            for subtree in result_tree:
                # Neglecting the whole sentence if there's a word in the unimp_tokens list
                if subtree[0].lower() in unimp_tokens:
                    neglect = True

                # Not appending the words in the abbrv list to the entity list and the word should have at
                # least more than one character
                elif subtree[0].lower() not in abbrv and len(subtree[0]) > 1:
                    entity.append(subtree[0])

            if entity and not neglect:
                concat_word = ' '.join([word for word in entity if word])
                whole_entity.append(concat_word)

    for en in whole_entity:
        sent_entities.append(en)

    for element in sent_entities:
        if element:
            symbol_ratio = calculate_symbol_ratio(element)
            if symbol_ratio <= 0.5:
                yield lemmatizer(element, verb_noun)
            else:
                print str(element) + " entity rejected due to symbol ratio :" + str(symbol_ratio)


def lemmatizer(entity, v_n):
    """Used to lemmatize the entities checking if it's a verb or a noun"""
    # Conversion of plural words like 'APIs' into singular
    if search('([A-Z]s)$', entity):
        return entity[:-1]
    else:
        # Lemmatizing the last word
        words = tokenize_words(entity)
        last_word = words.pop()
        lem_word = WordNetLemmatizer().lemmatize(last_word.lower(), pos=v_n)
        # The lemmatized word should have at least more than one character
        # (Unless the lemmatized word of 'xs', 'x' will also be considered)
        if len(lem_word) > 1:
            out = ''
            for i, e in enumerate(lem_word):
                out += str(e).upper() if len(last_word) > i and str(
                    last_word[i]).isupper() else e
            words.append(out)
            return str(' '.join(words))

        elif len(words) == 1:
            return entity


def calculate_symbol_ratio(word):
    """Calculating the symbol ratio of an element"""
    symbol_ratio = float(len(findall(r'[^A-Za-z\s]', word))) / len(word)
    return symbol_ratio


def tokenize_words(sentence, preserve_case=True):
    """Word separation in a sentence"""
    words = []
    for word in split(r'^[-,.()!:+?\"\'*]+|[-,.()!:+?\"\'*]*\s+[-,.()!:+?\"\'*]*|[-,.()!:+?\"\'*]+$', sentence):
        if word != "":
            words.append(word)

    if not preserve_case:
        words = list(map((lambda x: x.lower()), words))
    return words


def word_combination(pos_tagged):
    """Chunking of a part of speech tagged sentence based on specific grammar"""
    # Entity grammar used for the Penn Tree Bank Tagset for nouns and verbs
    grammar_noun = r"""
    NU: {<NN.*>+}
    """
    grammar_verb = r"""
    VE: {<VB.*>+}
    """

    cp_noun = RegexpParser(grammar_noun)
    nouns = cp_noun.parse(pos_tagged)

    cp_verb = RegexpParser(grammar_verb)
    verbs = cp_verb.parse(pos_tagged)
    return nouns, verbs


def test():
    dependency_parse = CoreNLP()
    text = '''How to send an e-mail through ESB Connector?'''
    print list(noun_verbs(dependency_parse.parse(text)))


if __name__ == "__main__":
    test()
