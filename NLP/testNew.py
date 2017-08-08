import nltk
from nltk.tokenize import word_tokenize

document = "Sri Lanka's documented history spans 3,000 years, with evidence of pre-historic human settlements dating " \
           "back to at least 125,000 years. Its geographic location and deep harbours made it of great strategic " \
           "importance from the time of the ancient Silk Road through to World War II."
sentences = nltk.sent_tokenize(document)

for sentence in sentences:
    tokens = word_tokenize(sentence)
    #
    # stop_words=set(stopwords.words('english'))
    # clean_tokens=[words for words in tokens if words not in stop_words]
    # print clean_tokens
    #
    # tagged=nltk.pos_tag(clean_tokens)
    # print tagged
    #
    # # Named entity recognitionif True
    # NERtagged= nltk.ne_chunk(tagged)
    # print NERtagged

    # Stem the words ib the list
    from nltk.stem import PorterStemmer

    ps = PorterStemmer()
    stemTagged = []
    for word in tokens:
        stemTagged.append(ps.stem(word))
    print stemTagged
