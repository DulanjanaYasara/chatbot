from commons.database.mongodb import MongoDB

"""Used to get the HTML body context from the existing WSO2 documentation database"""
host = "mongodb://kb:ms-classified@supportkb-staging.private.wso2.com/support_knowledge_base?authMechanism=SCRAM-SHA-1"
db_name = "support_knowledge_base"
mongo = MongoDB(db_name, host)

for i in mongo.import_object(mongo.db.doc_pages, 'body', {}):
    print i
