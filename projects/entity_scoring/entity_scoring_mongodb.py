import csv
from re import sub

from commons.data.entity import lemmatizer
from commons.data.entity import search_acronyms
from commons.database.mongodb import MongoDB
from commons.spreadsheet.basic import SpreadsheetConnector

"""Using the manually configured data for the proper entity scoring"""


def upload_csv(csv_path, csv_file, all_data, fieldnames):
    """Write to a csv file
    :param csv_path: str
    :type csv_file: str
    :type all_data: dict
    :type fieldnames: list
    """

    with open(csv_path + csv_file, "wb") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerows(all_data)


# Importing all values in the spreadsheet
connector = SpreadsheetConnector('./projects/entity_scoring/wso2-domain-words.json')
all_values = connector.import_all(workbook_name="WSO2 Domain Words")
manually_prioritized = {}
rows = []
for val in all_values:
    if val[1] == 't':
        lemmatized_entity = lemmatizer(val[0])
        new_entity = search_acronyms(lemmatized_entity)
        new_id = sub(r'[\s-]+', '', str(new_entity).lower())
        # Making the manually_prioritized dictionary of entities
        if new_id not in manually_prioritized.keys():
            manually_prioritized[new_id] = new_entity
            rows += [{'_id': new_id, 'entity': new_entity}]
            print '.',

path = './projects/entity_scoring/'
upload_csv(path, "manually_prioritized_entities.csv", rows, ['_id', 'entity'])
print 'Done uploading to csv file'

# Updating the existing database
mongodb = MongoDB("wso2_entities")
collection = mongodb.db.Entities_Scores_v4_new
for _id in manually_prioritized:
    existing_score = collection.find_one({'_id': _id})
    if existing_score:
        existing_score = existing_score['score']
        # Adding fixed score of 2500 for the existing score.
        mongodb.update_object(collection, _id, 'score', existing_score + 2500)
