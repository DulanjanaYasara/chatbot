from commons.database import MongoDB, compare_collections

mongodb = MongoDB(db_name='wso2_entities')

wso2_doc_entities_col = mongodb.db.get_collection('Entities_Scores_v4')
ordinary_entities_col = mongodb.db.get_collection('Ordinary_entities')
tech_entities_col = mongodb.db.get_collection('Tech_entities')

# Identifying entities in WSO2 domain
set_wso2 = set()
for x in wso2_doc_entities_col.distinct('_id'):
    set_wso2.add(x)

common_ele_tech_wso2 = compare_collections(tech_entities_col, wso2_doc_entities_col)
common_ele_ordi_wso2 = compare_collections(wso2_doc_entities_col, ordinary_entities_col)

entities_to_removed = set(common_ele_ordi_wso2).difference(set(common_ele_tech_wso2))
print '\033[4m' + 'Entities to be removed from WSO2 entities :' + '\033[0m',
print entities_to_removed
print len(entities_to_removed)

entities_specific_wso2 = (set_wso2.difference(set(common_ele_tech_wso2))).difference(set(common_ele_ordi_wso2))
print '\033[4m' + 'Entities specific to WSO2 :' + '\033[0m',
print entities_specific_wso2
print len(entities_specific_wso2)

entities_second_priori = set(common_ele_tech_wso2).difference(set(common_ele_ordi_wso2))
print '\033[4m' + 'Entities secondly prioritized :' + '\033[0m',
print entities_second_priori
print len(entities_second_priori)

entities_third_priori = set(common_ele_tech_wso2).union(set(common_ele_ordi_wso2))
print '\033[4m' + 'Entities thirdly prioritized :' + '\033[0m',
print entities_third_priori
print len(entities_third_priori)
