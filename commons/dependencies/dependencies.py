from re import search, split

from nltk import WordNetLemmatizer

from main import CoreNLP


def __coreference(parsed_text):
    """Used to extract the coreference of words from the dependency parsed text
    :type parsed_text: dict
    i.e. dependency parsed text from the StanfordCore NLP
    :return coref_dict:dict
    i.e. {word: [[sentence_no,word_coreference_instance ]],...}
    """
    # A dictionary to store the word and it's coreferece
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
    """
    Used to keep the coreferences in a sentence based dict keys
    :type co_dict: dict
    i.e. {word: [[sentence_no,word_coreference_instance ]],...}
    :return coref_dict:dict
    i.e. {sentence_no:[corefernced_word,...],...}
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
    """
    Used to obtain the dependencies of a text
    :type dependency_parsed_text: dict
    i.e. dependency parsed text from the StanfordCore NLP
    :return coreferences:list
    i.e. [{governor_word:noun_or_verb ,dependent_word:noun_or_verb},...]
    """
    prep_dict = __prep_dic(__coreference(dependency_parsed_text))

    # To obtain the sentence number
    sent_num = 1
    for sentence in dependency_parsed_text['sentences']:
        # A dict to keep the word index of nouns, verbs and pronouns
        indices = {element['index']: element['pos'][0] for element in sentence['tokens'] if
                   search(r'NN.*|VB.*|PRP.*', element['pos'])}
        # Adding important element of ROOT
        indices[0] = 'R'

        # Combining the prep_dict and indices dict
        combined_prep_dict = {}
        if sent_num in prep_dict.keys():
            coref_prep_list = prep_dict[sent_num]
            prep_indices = [index for index in indices.keys() if indices[index] == 'P']
            for index, value in enumerate(prep_indices):
                combined_prep_dict[value] = coref_prep_list[index]

        coreferences = []
        for value in sentence['enhancedPlusPlusDependencies']:
            if value['dependent'] in indices.keys() and value['governor'] in indices.keys():

                # Replacing the coreferenced words of dependent and the governor
                if value['dependent'] in combined_prep_dict.keys():
                    value['dependentGloss'] = combined_prep_dict[value['dependent']]
                if value['governor'] in combined_prep_dict.keys():
                    value['governorGloss'] = combined_prep_dict[value['governor']]
                # Lemmatizing the dependent and the governor
                lemmatized_governor = lemmatizer(value['governorGloss'], indices[value['governor']])
                lemmatized_dependent = lemmatizer(value['dependentGloss'], indices[value['dependent']])
                coreferences.append([(value['governor'], lemmatized_governor, indices[value['governor']]),
                                     (value['dependent'], lemmatized_dependent, indices[value['dependent']])])
        sent_num += 1
        yield coreferences


def tokenize_words(sentence, preserve_case=True):
    """Word separation in a sentence
    :param preserve_case:Boolean
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
    :param v_n: char
    :type entity: str
    """

    if v_n == 'V':
        return WordNetLemmatizer().lemmatize(entity.lower(), pos='v')
    elif v_n == 'N':
        # Conversion of plural words like 'APIs' into singular
        if search('([A-Z]s)$', entity):
            return entity[:-1]
        else:
            # Lemmatizing the last word
            words = tokenize_words(entity.lower())
            last_word = words.pop()
            lem_word = WordNetLemmatizer().lemmatize(last_word.lower(), pos='n')
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
                return entity.lower()
    else:
        return entity.lower()


def test():
    # The test case
    dependency_parse = CoreNLP()
    q_text = '''How to add a scheduled task into ESB?'''
    a_text = '''Yes. For information, contact us.'''
    print list(generate(dependency_parse.parse(a_text)))


if __name__ == "__main__":
    test()
