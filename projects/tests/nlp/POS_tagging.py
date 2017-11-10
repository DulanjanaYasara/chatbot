from nltk.corpus import treebank

train_data=treebank.tagged_sents()[:3]
test_data=treebank.tagged_sents()[300:400]
print test_data[0]

from nltk.tag import tnt
tnt_post_tagger=tnt.TnT()
tnt_post_tagger.train(train_data)
print tnt_post_tagger.evaluate(test_data)

# see http://textminingonline.com/dive-into-nltk-part-iii-part-of-speech-tagging-and-pos-tagger

