import re

import nltk
from bs4 import BeautifulSoup

import get_data_from_suzy
from commons.stanford_pos_tagger.stanfordapi import StanfordAPI

# Code that execute in the import breaknplay
path_to_model = "./stanford_pos_tagger/english-bidirectional-distsim.tagger"
path_to_jar = "./stanford_pos_tagger/stanford-postagger.jar"

pos_tag_obj = StanfordAPI(path_to_model, path_to_jar)


def extract_q_without_code(question):
    """Question body is extracted without the code and blockquote sections"""
    soup = BeautifulSoup(question, 'lxml')

    # Obtaining the code segments and the blockquotes from the body
    [c.extract_entities() for c in soup('code')]
    [e.extract_entities() for e in soup('blockquote')]

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
                        re.split(r'[.!:;?*()\n]+\s+|\s+[.!:;?*()\n]+|(->)', re.sub(r'(\.)([A-Z])', r'\1 \2', text)) if
                        sent != '']
    return sentence_phrases


def entity_extraction(text):
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

            tokens = nltk.word_tokenize(sentence)
            # POS tagging using the Stanford POS tagger
            pos_tagged_sentence = pos_tag_obj.pos_tag(' '.join(tokens))
            # pos_tagged_sentence = tagger.tag(tokens)
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

                        # Not appending the words in the abbrv list to the entity list and the word should have at
                        # least more than one character
                        elif subtree[0] not in abbrv and len(subtree[0]) > 1:
                            entity.append([subtree[0], subtree[1]])

                    if entity and not neglect:
                        concat_word = ' '.join([word[0] for word in entity if word])
                        # Considering pos tag of the front word
                        front_pos_tag = entity[0][1]
                        whole_entity.append([concat_word, front_pos_tag])

            for en in whole_entity:
                if not sent_entities:
                    sent_entities.append(en[0])
                # The previous word and the new word are joined if the new word front_pos_tag is 'NN'
                elif en[1] == 'NN':
                    last_words = sent_entities.pop()
                    len_words = len(nltk.word_tokenize(last_words + ' ' + en[0]))
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
            ans, is_answered = get_data_from_suzy.data_from_bot(q)
            # next_ans = ans
            if is_answered:
                print '\033[1m' + q + '\033[0m' + ":" + ans
                # prev_ans = next_ans
            else:
                print '\033[1m' + q + '\033[0m' + ":XXXXXXXXXXXXXXXXXXX"
        print

# TEST CASE print entity_extraction("""My Scenario: I have server_1 (192.168.10.1) with  i wso2-ESB and ( Dulanjana )
#  123 _ liyanagama server_2 (192.168.10.2) with Glassfish-v3 + web services. Problem: I am trying to create a proxy
# in ESB using the java Web Services, but the created proxy does not respond properly. The log says:  for http or
# https does not change the result. I think I should configure the  but I am having trouble, and don't know what to
# do. What is the configuration for my scenario? Please help me! EDIT: To be clear, I can directly consume the
# WebService in the Glassfish server, it works normal, both port and url are accessible. Only when I create a "Pass
# through Proxy" in the ESB, it does not work. I don't think is matter of Proxy configuration...I never had problems
# while deployed locally, problems started once I have uploaded the ESB to a remote server. I really would need
# someone to point me what is the correct procedure when installing the ESB on a remote host: configuration of
# axis2.xml and carbon.xml, ports, transport receivers etc... P.S. I had a look at the official (wso2 esb and carbon)
#  guides with no luck, but I am missing something... Endpoint of Java Web Service: ESB Proxy Enpoint: The following
# is my axis2.xml configuration, please check it:""")
