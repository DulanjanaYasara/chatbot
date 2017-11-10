import difflib
import re
from string import uppercase

from nltk import RegexpParser

from commons.stanford_pos_tagger import StanfordAPI


class EntityExtractor:
    """Used to extract entities based on POS tagging"""

    def __init__(self):
        self.pos_tag_obj = StanfordAPI()

    def tokenize_words(self, sentence, preserve_case=True):

        words = []
        for word in re.split(r'^[-,.()!:+?\"\'*]+|[-,.()!:+?\"\'*]*\s+[-,.()!:+?\"\'*]*|[-,.()!:+?\"\'*]+$', sentence):
            if word != "":
                words.append(word)

        if not preserve_case:
            words = list(map((lambda x: x.lower()), words))
        return words

    def sentence_phrases_separation(self, text):
        """Used for part of sentence extraction based on punctuation delimiters.
        An additional space is added in between period and capital letter"""
        sentence_phrases = [sent for sent in
                            re.split(r'[.!:;?*()\n]+\s+|\s+[.!:;?*()\n]+|(->)', re.sub(r'(\.)([A-Z])', r'\1 \2', text))
                            if
                            sent != '']
        return sentence_phrases

    def word_combination(self, pos_tagged_sentence):
        """Chunking of a part of speech tagged sentence based on specific grammar"""
        # grammar = r"""
        # EN:{(<JJ>*<NN.*>+<IN>)?<JJ>*<NN.*>+}
        # """

        # Previous one
        grammar = r"""
        EN: {<JJ.*>*<NN.*>+}
        """

        cp = RegexpParser(grammar)
        result = cp.parse(pos_tagged_sentence)
        return result

    def extract(self, text):
        """Used to extract entities based on part of speech tagging"""
        input_sentences = self.sentence_phrases_separation(text)
        for sentence in input_sentences:

            # If sentence is not None
            if sentence:
                # Considering entities in the sentence
                sent_entities = []
                # This list should be given in simple case.
                unimp_tokens = ['thank', 'thanks', 'anyone', 'everyone', 'anyhelp', 'hi', 'please', 'help', 'welcome']
                abbrv = ['e.g', 'i.e', 'um', 'etc']

                tokens = self.tokenize_words(sentence)
                # POS tagging using the Stanford POS tagger
                pos_tagged_sentence = self.pos_tag_obj.pos_tag(' '.join(tokens))
                print pos_tagged_sentence
                result = self.word_combination(pos_tagged_sentence)

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
                            elif subtree[0].lower() not in abbrv and len(subtree[0]) > 1:
                                # entity.append([subtree[0], subtree[1]])
                                entity.append(subtree[0])

                        if entity and not neglect:
                            # concat_word = ' '.join([list[0] for list in entity if list])
                            concat_word = ' '.join([list for list in entity if list])
                            # Considering pos tag of the front word
                            # front_pos_tag = entity[0][1]
                            # whole_entity.append([concat_word, front_pos_tag])
                            whole_entity.append(concat_word)

                for en in whole_entity:
                    print en
                    # sent_entities.append(en[0])
                    sent_entities.append(en)

                    # if not sent_entities:
                    #     sent_entities.append(en[0])
                    # # The previous word and the new word are joined if the new word front_pos_tag is 'NN'
                    # elif en[1] == 'NN':
                    #     last_words = sent_entities.pop()
                    #     len_words = len(word_tokenize(last_words + ' ' + en[0]))
                    #     # Words are appended if the total no. of words is 4 or less
                    #     if len_words <= 4:
                    #         sent_entities.append(last_words + ' ' + en[0])
                    #     else:
                    #         sent_entities.append(last_words)
                    #         sent_entities.append(en[0])
                    # else:
                    #     sent_entities.append(en[0])

                for element in sent_entities:
                    if element:
                        yield element


def entities_comparator(entity_list1, entity_list2, threshold=0.93):
    """Find the similarity between two entities based on a specific threshold value"""
    equal_entities = []
    for entity1 in entity_list1:
        for entity2 in entity_list2:
            seq = difflib.SequenceMatcher(a=str(entity1).lower(), b=str(entity2).lower())
            if seq.ratio() > threshold:
                print entity2
                equal_entities.append(entity1)
    return equal_entities


def entity_reducer(entity_list, threshold=0.93, case_sensitive=True):
    """Find the similarity of entities in a list based on a specific threshold value"""
    for i in range(len(entity_list)):
        for j in range(i + 1, len(entity_list)):
            if case_sensitive:
                seq = difflib.SequenceMatcher(a=str(entity_list[i]).lower(), b=str(entity_list[j]).lower())
            else:
                seq = difflib.SequenceMatcher(a=entity_list[i], b=entity_list[j])
            if seq.ratio() > threshold:

                no_case1 = len(filter(lambda x: x in uppercase, entity_list[i]))
                no_case2 = len(filter(lambda x: x in uppercase, entity_list[j]))
                if no_case1 > no_case2:
                    entity_list[j] = entity_list[i]
                elif no_case2 > no_case1:
                    entity_list[i] = entity_list[j]
                else:

                    len1 = len(entity_list[i])
                    len2 = len(entity_list[j])
                    if len1 > len2:
                        entity_list[j] = entity_list[i]
                    else:
                        entity_list[i] = entity_list[j]

    reduced_set = set()
    for en in entity_list:
        if en not in reduced_set:
            reduced_set.add(en)
            yield en
        else:
            continue


text = ''''In a new browser window or tab, open https://localhost:9444/carbon/ and log into the Analytics management console using admin as the username as well as the password.'''
print list(EntityExtractor().extract(text))
