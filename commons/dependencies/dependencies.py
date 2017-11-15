#!/usr/bin/env python
# -*- coding: utf-8 -*
from re import search, split

from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer
from unidecode import unidecode

from main import CoreNLP

porter_stemmer = PorterStemmer()


def __coreference(parsed_text):
    """Used to extract the coreference of words from the dependency parsed text

    :type parsed_text: dict
    :param parsed_text: Parsed text from the StanfordCore NLP
    :return: i.e. {word: [[sentence_no,word_coreference_instance ]],...}
    :rtype: dict
    """
    # A dictionary to store the word and it's coreference
    coref_dict = {}
    for coref in parsed_text['corefs'].keys():
        head_noun = ''
        position = []
        for data in parsed_text['corefs'][coref]:
            # If representative is mentioned head_noun is assigned else it's position is considered
            if data['isRepresentativeMention']:
                head_noun = data['text']
            else:
                position.append(data['position'])
        coref_dict[head_noun] = position
    return coref_dict


def __prep_dic(co_dict):
    """Used to keep the coreferences in a sentence based dict keys

    :type co_dict: dict
    :param co_dict: i.e. {word: [[sentence_no,word_coreference_instance ]],...}
    :return: coref_dict i.e. {sentence_no:[corefernced_word,...],...}
    :rtype: dict
    """
    # A dictionary to store the sentence number and it's coreferenced words
    prep_dict = {}
    for key in co_dict.keys():
        for value in co_dict[key]:
            if value[0] in prep_dict:
                # append the new value to the existing list
                prep_dict[value[0]].append(key)
            else:
                # create a new list
                prep_dict[value[0]] = [key]
    return prep_dict


def generate(dependency_parsed_text):
    """Used to obtain the dependencies of a text

    :type dependency_parsed_text: dict
    :param dependency_parsed_text: i.e. dependency parsed text from the StanfordCore NLP
    :return: coreferences i.e. [{governor_word:noun_or_verb ,dependent_word:noun_or_verb},...]
    :rtype: list
    """
    prep_dict = __prep_dic(__coreference(dependency_parsed_text))

    # To obtain the sentence number
    sent_num = 1
    for sentence in dependency_parsed_text['sentences']:
        # A dict to keep the word index of nouns, verbs, pronouns and WH verbs
        indices = {element['index']: element['pos'][0] for element in sentence['tokens'] if
                   search(r'^(NN.*|VB.*|PRP.*|W.+|RB.*|JJ.*)', element['pos'])}
        # Adding important element of ROOT
        indices[0] = 'A'

        # Checking for the availability of the 'ROOT' in the indices list. If not, adding them to 'indices' list,
        # without considering the pos tag form
        if sentence['basicDependencies'][0]['dep'] == 'ROOT':
            root_index = sentence['basicDependencies'][0]['dependent']
            if root_index not in indices:
                for element in sentence['tokens']:
                    if element['index'] == root_index:
                        indices[root_index] = element['pos']

        # Combining the prep_dict and indices dict
        combined_prep_dict = {}
        if sent_num in prep_dict.keys():
            coref_prep_list = prep_dict[sent_num]
            prep_indices = [index for index in indices.keys() if indices[index] == 'P']
            for index, value in enumerate(prep_indices):

                if len(coref_prep_list) > index:
                    combined_prep_dict[value] = \
                        [x for x in coref_prep_list[index].split(' ') if not (x[0] == '-' and x[-1] == '-')][-1]
                else:
                    # Removing the prepositions which doesn't have coreferences from the indices dict
                    del indices[value]
        else:
            indices = {k: v for k, v in indices.items() if v != 'P'}

        coreferences = []
        # Out of enhancedDependencies,basicDependencies and enhancedPlusPlusDependencies
        for value in sentence['basicDependencies']:
            if value['dependent'] in indices.keys() and value['governor'] in indices.keys():

                # Replacing the coreferenced words of dependent and the governor
                if value['dependent'] in combined_prep_dict.keys():
                    value['dependentGloss'] = combined_prep_dict[value['dependent']]
                if value['governor'] in combined_prep_dict.keys():
                    value['governorGloss'] = combined_prep_dict[value['governor']]
                # Lemming the dependent and the governor
                lemmatized_governor = lemmatizer(value['governorGloss'], indices[value['governor']])
                lemmatized_dependent = lemmatizer(value['dependentGloss'], indices[value['dependent']])
                coreferences.append([(value['governor'], lemmatized_governor, indices[value['governor']]),
                                     (value['dependent'], lemmatized_dependent, indices[value['dependent']])])
        sent_num += 1
        yield coreferences


def tokenize_words(sentence, preserve_case=True):
    """Word separation in a sentence

    :type preserve_case: bool
    :type sentence: str
    """
    words = []
    for word in split(r'^[-,.()!:+?\"\'*]+|[-,.()!:+?\"\'*]*\s+[-,.()!:+?\"\'*]*|[-,.()!:+?\"\'*]+$', sentence):
        if word != "":
            words.append(word)

    if not preserve_case:
        words = list(map((lambda x: x.lower()), words))
    return words


def lemmatizer(entity, v_n):
    """Used to lemmatize the entities checking if it's a verb or a noun

    :type v_n: char
    :type entity: str
    """

    result = ''

    if v_n == 'V':
        result = WordNetLemmatizer().lemmatize(entity.lower(), pos='v')
    elif v_n == 'N':
        # Conversion of plural words like 'APIs' into singular
        if search('([A-Z]s)$', entity):
            result = entity[:-1]
        else:
            # Lemming the last word
            words = tokenize_words(entity.lower())
            last_word = unidecode(words.pop())
            lem_word = WordNetLemmatizer().lemmatize(last_word.lower(), pos='n')
            # The lemmed word should have at least more than one character
            # (Unless the lemmed word of 'xs', 'x' will also be considered)
            if len(lem_word) > 1:
                out = ''
                for i, e in enumerate(lem_word):
                    out += str(e).upper() if len(last_word) > i and str(
                        last_word[i]).isupper() else e
                words.append(out)
                result = str(' '.join(words))

            elif len(words) == 1:
                result = entity.lower()
    else:
        result = entity.lower()

    return porter_stemmer.stem(result)


def test():
    dependency_parse = CoreNLP()
    text1 = ''' What is the mediator to be used for lightweight transformations on messages?'''
    text2 = '''BPMN Explorer is the web application that allows you to view and work with BPMN processes. It is a 
    Jaggery-based, lightweight web application that you can customize and deploy in a web server. '''
    text3 = '''In this case, the SOAP Header field To is matched against a regular expression that checks to see 
    whether the To field contains StockQuote. validate [line 34 in ESB config] - Performs validation on the SOAP body 
    using the XML Schema defined in the localEntry (line 2 in ESB config). on-fail [line 36 in ESB config] - If the 
    validation fails, the on-fail element provides a detour, which can be used to channel the message through a 
    different route and ultimately passed on to the intended service. In the example scenario, a fault is produced 
    and the fault is sent back to the requesting client. send [line 44 in ESB config] - the send mediator is used to 
    send the message to the intended receiver - however if the makeFault inside the on-fail element (line 37 in ESB 
    config) is executed before this mediator is reached, then the fault is returned to the requesting client. '''
    text3 = '''Is there commercial support available for WSO2 Enterprise Integrator?'''
    print list(generate(dependency_parse.parse(text3)))


if __name__ == "__main__":
    test()
