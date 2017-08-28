import operator
import re

from nltk import RegexpParser


class KeyWordExtract:
    def __init__(self):
        pass

    def _get_stopwords(self, stop_path):
        """Get the stop words from the specified location of stop_path"""
        with open(stop_path, 'r') as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]

        return set(content)

    def _extract_words_from_sentence(self, sentence, preserve_case=True):

        words = []
        for word in re.split(r'^[-,.()!:+?\"\'*]+|[-,.()!:+?\"\'*]*\s+[-,.()!:+?\"\'*]*|[-,.()!:+?\"\'*]+$', sentence):
            if word != "":
                words.append(word)

        if not preserve_case:
            words = list(map((lambda x: x.lower()), words))
        return words

    def _word_separation(self, sentence):
        tokens = self._extract_words_from_sentence(sentence, preserve_case=False)
        # pos_tagged_sentence = pos_tag(tokens)
        # result = self._word_combination(pos_tagged_sentence)
        #
        # tokens = []
        # # Traversing through the tree
        # for result_tree in result:
        #     if type(result_tree) is tuple:
        #         tokens.append(result_tree[0])
        #     else:
        #         entity = []
        #         for subtree in result_tree:
        #             entity.append(subtree[0])
        #         tokens.append(' '.join(entity))

        return tokens

    def _word_combination(self, pos_tagged_sentence):

        # Finding entities still testing
        grammar = r"""
        EN: {<NN.*><CD>+}
        """
        cp = RegexpParser(grammar)
        result = cp.parse(pos_tagged_sentence)

        return result

    def _sentence_phrases_separation(self, text):
        sentence_phrases = re.split(r'[-,.()!:;+?*\n]+\s+|\s+[-,.()!:;+?*\n]+', text)

        return sentence_phrases

    def _generate_candidate_keywords(self, text, stop_words):
        """Generating the possible keywords within a text removing stop words and punctuations"""
        keywords = []
        # sentence_list = sent_tokenize(text)
        # print sentence_list

        sentence_list = self._sentence_phrases_separation(text)

        for sent in sentence_list:

            tokens = self._word_separation(sent)
            phrases = []

            for word in tokens:
                # Has to done more on regular expressions
                # Finding for punctuation symbols and stop words
                if word in stop_words:
                    phrases.append("|")
                else:
                    phrases.append(word)

            phrases_string = " ".join(phrases)
            for phrase in re.split(r"[|]", phrases_string):
                if phrase.strip() != "":
                    keywords.append(phrase.strip())

        return keywords

    def _generate_word_scores(self, keywords):
        """Gives the word scores of a keyword list"""
        word_list = []
        for keyword in keywords:
            word_list.append(self._word_separation(keyword))

        freq_word = {}
        deg_word = {}
        for word_collection in word_list:
            no_words = len(word_collection)

            for word in word_collection:

                if word in freq_word:
                    freq_word[word] += 1
                    deg_word[word] += 1
                else:
                    freq_word[word] = 1
                    deg_word[word] = 1
                if no_words != 1:
                    deg_word[word] += no_words - 1

        word_score = {}
        for key, value in freq_word.iteritems():
            word_score[key] = deg_word[key] / float(value)

        total_no_words = len(freq_word)
        return word_score, total_no_words

    def _generate_phrase_score(self, word_score, keywords):
        """Generate the phrase score of the keywords using the phrase score"""
        phrase_score = {}
        for keyword in keywords:
            phrase_score[keyword] = 0
            for word in self._word_separation(keyword):
                phrase_score[keyword] = phrase_score[keyword] + word_score[word]
        return phrase_score

    def _essential_keywords(self, phrase_score, total_words):
        """Gives one third of the total_words number of keywords with the highest scores"""
        sorted_dict = list(reversed(sorted(phrase_score.items(), key=operator.itemgetter(1))))
        x = 0
        ultimate_keywords = []
        no_keywords = total_words / 3
        for key in sorted_dict:
            if x > no_keywords:
                continue
            else:
                x += 1
                ultimate_keywords.append(key[0])
        return ultimate_keywords

    def extract(self, text):
        setpath = "../../rake/SmartStoplist.txt"
        stop_words = self._get_stopwords(setpath)
        keywords = self._generate_candidate_keywords(text, stop_words)
        word_score, total_words = self._generate_word_scores(keywords)
        phrase_score = self._generate_phrase_score(word_score, keywords)
        print phrase_score
        # print nltk.pos_tag([key for key in phrase_score])

        print self._essential_keywords(phrase_score, total_words)

    def test(self):
        text = """The WSO2 have two tutorials, to each folder.
        """
        print self._extract_words_from_sentence(text)


if __name__ == "__main__":
    rake = KeyWordExtract()
    rake.test()

"""The WSO2 have 2 tutorials, to each folder. Well, with a probability of .9 it isn't.
        Did he mind? Adam Jones Jr. thinks he didn't.In any case, this isn't true...
   """
