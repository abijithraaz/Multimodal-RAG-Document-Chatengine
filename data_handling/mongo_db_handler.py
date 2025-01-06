import os
from pymongo import MongoClient
from data_handling.base_db_handling import DBModify, DataStoring

class MongoDB(DataStoring, DBModify):
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI',''))

    def vectordata_storing(self, document_chunks, document_name, collection_name='test'):

        collection = self.client[os.getenv('MONGODB_NAME')][collection_name]

        docs_to_insert = [{ "doc_name":document_name,
                            "text": doc,
                            "embeddings": embedd}
                            for doc,embedd in zip(document_chunks['text'],document_chunks['embeddings'])]

        # Insert documents into the collection
        result = collection.insert_many(docs_to_insert)
        return result
    
    def clear_db(self, sql_query=''):
        return 
