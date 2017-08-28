import imp
import re

import nltk
from bs4 import BeautifulSoup
from nltk.tag.stanford import StanfordPOSTagger

import getDatafromSuzy

stanford_api = imp.load_source('StanfordAPI', './Stanford_pos_tagger/StanfordAPI.py')
obj = stanford_api.StanfordAPI()


def extract_q_without_code(question):
    """Question body is extracted without the code and blockquote sections"""
    soup = BeautifulSoup(question, 'lxml')

    # Obtaining the code segments and the blockquotes from the body
    codes = [c.extract() for c in soup('code')]
    errors = [e.extract() for e in soup('blockquote')]

    data = list(soup.recursiveChildGenerator())
    visit_to_a = False
    output = ''

    # Not adding the hyperlinks to the output
    for value in data:
        if value.name == 'a':
            visit_to_a = True
            if hasattr(value, 'href') and value.text != value['href']:
                output += value.text

        elif value.name is None and not visit_to_a:
            output += value
        else:
            visit_to_a = False

    # Converting HTML entities into Unicode characters
    output = unicode(output)
    return output


def sentence_phrases_separation(text):
    """Used for part of sentence extraction based on punctuation delimiters
    An additional space is added in between period and capital letter"""
    sentence_phrases = [sent for sent in
                        re.split(r'[.!:;?*()\n]+\s+|\s+[.!:;?*()\n]+', re.sub(r'(\.)([A-Z])', r'\1 \2', text)) if
                        sent != '']
    return sentence_phrases


def entity_extraction(text):
    """Used to extract entities based on part of speech tagging"""
    # ********************************
    path_to_model = "./Stanford_pos_tagger/english-bidirectional-distsim.tagger"
    path_to_jar = "./Stanford_pos_tagger/stanford-postagger.jar"
    tagger = StanfordPOSTagger(path_to_model, path_to_jar)
    # ********************************

    input_sentences = sentence_phrases_separation(text)
    all_entities = []
    for sentence in input_sentences:

        # Considering entities in the sentence
        sent_entities = []
        # This list should be given in simple case.
        unimp_tokens = ['thank', 'thanks', 'anyone', 'everyone', 'anyhelp', 'hi', 'please', 'help', 'welcome']
        abbrv = ['e.g', 'i.e', 'i', '(', ')']

        tokens = nltk.word_tokenize(sentence)
        pos_tagged_sentence = obj.pos_tag(tokens)
        # pos_tagged_sentence = tagger.tag(tokens)
        print pos_tagged_sentence
        # pos_tagged_sentence = nltk.pos_tag(tokens)
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

                    # Not appending the words in the abbrv list to the entity list
                    elif subtree[0] not in abbrv:
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
                last_word = sent_entities.pop()
                sent_entities.append(last_word + ' ' + en[0])
            else:
                sent_entities.append(en[0])

        for element in sent_entities:
            if element:
                all_entities.append(element)

    return all_entities


def word_combination(pos_tagged_sentence):
    """Chunking of a part of speech tagged sentence based on specific grammar"""
    grammar = r"""
    EN: {<JJ.*>*<NN.*>+}
    """
    # EN: { <JJ.*>*<NN.*>+<CD>*}

    cp = nltk.RegexpParser(grammar)
    result = cp.parse(pos_tagged_sentence)
    return result


def breaknplay_bot(q_has_code_error, questionIntent, bodyHTML):
    """If question has codes and blockquotes the questions are extracted into entities and they are fed to the bot"""
    if q_has_code_error:
        print '\033[1m' + '\033[4m' + questionIntent + '\033[1m'
        q_without_code = extract_q_without_code(bodyHTML)
        print '\033[94m' + q_without_code + '\033[0m'

        question_phrases = entity_extraction(q_without_code)
        print '\033[1m' + 'ENTITIES :' + '\033[0m',
        print question_phrases
        print '\033[1m' + 'BOT ANSWER :' + '\033[0m',
        print

        # Prints the answer only if the answer is different from the existing answer and if it is properly answered
        # by bot
        # prev_ans = ''
        for q in question_phrases:
            ans, is_answered = getDatafromSuzy.data_from_bot(q)
            # next_ans = ans
            if is_answered:
                print '\033[1m' + q + '\033[0m' + ":" + ans
                # prev_ans = next_ans
            else:
                print '\033[1m' + q + '\033[0m' + ":XXXXXXXXXXXXXXXXXXX"
        print


# TEST CASE
print entity_extraction("""I'm attempting to produce a stream of comments from a Facebook page. Ultimately I'd like a response from WSO2 like this:

I'm using the API module for WSO2 ESB to provide an abstraction layer over a Facebook page to get a simple stream of 
all the comments on a page after a given timestamp. The logic I'm working on right now is taking all the posts on a 
given Facebook page (using the WSO2 Facebook Connector), iterating over all the posts (using an iterate mediator), 
checking if the post has comments (using the filter mediator), if there are comments I'm then iterating over the 
comments and restructuring them into a simple XML element (using the PayloadFactory mediator). This is where I'm 
getting stuck. I've figured out that within an iterate mediator I can't update properties external to the iterator. 
My initial instinct was to enrich an external property with the comment payload generated in the second iterator as a 
child element, but no dice. I'm now attempting to aggregate the outputs of the second iterator as shown below but I'm 
not able to aggregate the payloads: 

Any assistance would be greatly appreciated.""")
