from collections import defaultdict
from pprint import pprint

from commons.data.tree import WordTree
from commons.database import MongoDB
from commons.stanford_pos_tagger.stanfordapi import StanfordAPI

stanford_api = StanfordAPI()
mongodb = MongoDB(db_name='wso2_entities')
wso2_doc_entities_col = mongodb.db.get_collection('Entities_Scores_v1')

# Creation of entity list with wso2 entities
entity_list = []
for x in wso2_doc_entities_col.distinct('name'):
    entity_list.append(x.lower())

entity_tree = WordTree(is_reversed_tree=False)

t = entity_tree.creation_by_words(entity_list)
print t.get_ascii(compact=True)
dic = defaultdict(list)

for x in t.children:
    dic[len(x.children)].append(x.name)

pprint(dict(dic))

# Obtaining the child of the root
# x = set()
# nodes = t.iter_search_nodes(dist=float(1))
# for node in nodes:
#     pos_tag = stanford_api.pos_tag(node.name)[0][1]
#
#     if search(r'VBZ', pos_tag):
#         x.add(pos_tag)
#         print node.name, pos_tag
#         print node.get_ascii(compact=True)
# print x
