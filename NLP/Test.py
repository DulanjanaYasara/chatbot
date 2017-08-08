import nltk

sentence = "San Francisco is foggy."

tokens = nltk.word_tokenize(sentence)
print tokens
# Printing tagged tokens
tagged = nltk.pos_tag(tokens)

print tagged
entities = nltk.chunk.ne_chunk(tagged)
print entities

# print nltk.sent_tokenize("Hello. How are you?")
# print nltk.word_tokenize('WSO2 is a company')
# print nltk.wordpunct_tokenize("What's up?")

from nltk.stem import PorterStemmer, WordNetLemmatizer

stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()

print("Stem %s: %s" % ("studying", stemmer.stem("studying")))
print("Lemmatise %s: %s" % ("studying", lemmatiser.lemmatize("studying")))
print("Lemmatise %s: %s" % ("studying", lemmatiser.lemmatize("studying", pos="v")))

# .....................................................................
# Generating stopwords of English
# print set(nltk.corpus.stopwords.words('english'))

# Stemming Just stripping out the unnecessary elongations
ps = nltk.stem.PorterStemmer()

text = 'It is important to by very pythonly while you are pythoning with python. All pythoners have pythoned poorly at least once.'

words = nltk.word_tokenize(text)
for x in words:
    print ps.stem(x)

# .....................................................................
