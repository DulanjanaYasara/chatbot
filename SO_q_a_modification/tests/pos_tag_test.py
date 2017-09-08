import re

from nltk.tag.stanford import StanfordPOSTagger


def sentence_phrases_separation(text):
    """Used for part of sentence extraction based on punctuation delimiters"""
    sentence_phrases = [sent for sent in
                        re.split(r'[.,!:;?*()\n]+\s+|\s+[.,!:;?*()\n]+', re.sub(r'(\.)([A-Z])', r'\1 \2', text)) if
                        sent != '']
    return sentence_phrases


sentence = """I could get some response like this, This is dynamic response value. These frameId amount can be change.Here is my response.


I need to craete new id using FrameId values.like,

I used for this For Each mediator for do  this task. here is my code

Here is Genarated_Id sequense


I could print only bellow value.

I have two questions.

How can I separate this FrameId values using "_" mark.Like 206_110_109
How to assign these FrameId values to each property mediator
"""

path_to_model = "../../Stanford_pos_tagger/english-bidirectional-distsim.tagger"
path_to_jar = "../../Stanford_pos_tagger/stanford-postagger.jar"
tagger = StanfordPOSTagger(path_to_model, path_to_jar)

input_sentences = sentence_phrases_separation(sentence)
print input_sentences

# for sentence in input_sentences:
#
#     tokens = word_tokenize(sentence)
# print tagger.tag(tokens)
