import re

from commons.data.entity import reducer
from commons.database import MongoDB


def reduce_entites(entity_name, collection_name):
    """Used to import entities from a database and reduce them"""
    num = 0
    list1 = set()
    for x in mongodb.import_object(collection_name, entity_name, parameters={}):
        for y in x:
            for z in y:

                if re.search(r'([A-Z][a-z]+\s?){2,}', z['entity']):
                    list1.add(z['entity'])
                    num += 1
                    # if re.search(r'[A-Z]{5,}', z['entity']):
                    #     print z['entity']

    print 'Number of ' + entity_name + 'entities: ',
    print num
    new_entities = list(reducer(list(list1)))
    print 'Reduced list :',
    print new_entities
    print 'Number of reduced entities: ',
    print len(new_entities)


mongodb = MongoDB("wso2_entities")
collection = mongodb.db.Entities_v3
reduce_entites("imp", collection)
print '__________________________________________________________'
reduce_entites("plain", collection)
