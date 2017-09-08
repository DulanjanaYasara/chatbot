import re

from nltk import word_tokenize, RegexpParser

from Stanford_pos_tagger import StanfordAPI


class EntityExtractor:
    """Used to extract entities based on POS tagging"""

    def __init__(self):
        self.pos_tag_obj = StanfordAPI()

    def extract(self, text):
        """Used to extract entities based on part of speech tagging"""

        input_sentences = sentence_phrases_separation(text)
        all_entities = []
        for sentence in input_sentences:

            # If sentence is not None
            if sentence:
                # Considering entities in the sentence
                sent_entities = []
                # This list should be given in simple case.
                unimp_tokens = ['thank', 'thanks', 'anyone', 'everyone', 'anyhelp', 'hi', 'please', 'help', 'welcome']
                abbrv = ['e.g', 'i.e', 'um']

                tokens = word_tokenize(sentence)
                # POS tagging using the Stanford POS tagger
                pos_tagged_sentence = self.pos_tag_obj.pos_tag(' '.join(tokens))
                result = word_combination(pos_tagged_sentence)

                # Traversing through the tree
                whole_entity = []
                neglect = False
                for result_tree in result:
                    if type(result_tree) is not tuple:
                        entity = []
                        for subtree in result_tree:
                            # Neglecting the whole sentence if there's a word in the unimp_tokens list
                            if subtree[0].lower() in unimp_tokens:
                                neglect = True

                            # Not appending the words in the abbrv list to the entity list and the word should have at
                            # least more than one character
                            elif subtree[0] not in abbrv and len(subtree[0]) > 1:
                                entity.append([subtree[0], subtree[1]])

                        if entity and not neglect:
                            concat_word = ' '.join([list[0] for list in entity if list])
                            # Considering pos tag of the front word
                            front_pos_tag = entity[0][1]
                            whole_entity.append([concat_word, front_pos_tag])

                for en in whole_entity:
                    if not sent_entities:
                        sent_entities.append(en[0])
                    # The previous word and the new word are joined if the new word front_pos_tag is 'NN'
                    elif en[1] == 'NN':
                        last_words = sent_entities.pop()
                        len_words = len(word_tokenize(last_words + ' ' + en[0]))
                        # Words are appended if the total no. of words is 4 or less
                        if len_words <= 4:
                            sent_entities.append(last_words + ' ' + en[0])
                        else:
                            sent_entities.append(last_words)
                            sent_entities.append(en[0])
                    else:
                        sent_entities.append(en[0])

                for element in sent_entities:
                    if element:
                        all_entities.append(element)

        return all_entities


def sentence_phrases_separation(text):
    """Used for part of sentence extraction based on punctuation delimiters.
    An additional space is added in between period and capital letter"""
    sentence_phrases = [sent for sent in
                        re.split(r'[.!:;?*()\n]+\s+|\s+[.!:;?*()\n]+|(->)', re.sub(r'(\.)([A-Z])', r'\1 \2', text)) if
                        sent != '']
    return sentence_phrases


def word_combination(pos_tagged_sentence):
    """Chunking of a part of speech tagged sentence based on specific grammar"""
    grammar = r"""
    EN: {<JJ.*>*<NN.*>+}
    """

    cp = RegexpParser(grammar)
    result = cp.parse(pos_tagged_sentence)
    return result
