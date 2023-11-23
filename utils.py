from pymongo import MongoClient

client = MongoClient('mongodb://flashcard-mongodb:zAzswXuHI8BcygTdcypHXeRdH54UIfZeORiJSLBPAZMAoQKW1CtzvWLN9QRNfw1MIdOLekfgvKLdACDbZn72EQ==@flashcard-mongodb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@flashcard-mongodb@')
dbname = client['mongodbhackathon']
collection_name = dbname["notes"]