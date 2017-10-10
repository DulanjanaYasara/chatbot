from commons.database.mongodb import MongoDB
from commons.spreadsheet.basic import SpreadsheetConnector

"""Generation of a spreadsheet with WSO2 documentation entities for the process of finding acronyms and the 
suitability of them in the WSO2 domain"""

connector = SpreadsheetConnector('./entity_scoring/wso2-domain-words.json')
mongodb = MongoDB("wso2_entities")
collection = mongodb.db.Entities_v5

row = 3835
num = 3834
print 'Out of 3884'
# Only the important entities are considered
for x in sorted(collection.find({}).distinct("imp.entity"), key=lambda s: s.lower())[3834:]:
    connector.export("WSO2 Domain Words", row, sheetNo=1, column_data=list([x]), columnIndex=list([1]))
    row += 1
    num += 1
    print num
