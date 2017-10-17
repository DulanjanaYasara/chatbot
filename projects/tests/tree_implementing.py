from re import split

from ete2 import Tree
from nltk.tree import *


def tree_generation(entities):
    for entity in entities:
        words = split(r'[\s-]+', entity)
        reversed_words_list = [words[i - 1:] for i in range(len(words), 0, -1)]
        t = Tree()
        for word in reversed_words_list:
            string = ' '.join(word)
            z = t.add_child(name=string)
            t = z
        print t.show()


# tree_generation(['Enterprise Service Bus'])
t1 = Tree()
x = t1.add_child(name="sdfsdf")
z = t1.add_sister(name="456")
y = x.add_child(name="wef")

# t=Tree()
# t.populate(10)
print t1
