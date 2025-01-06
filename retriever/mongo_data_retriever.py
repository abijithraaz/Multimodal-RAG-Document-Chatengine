import os
from pymongo import MongoClient
from langchain.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch

from retriever.base_retriever import DataRetriever

class MongoDBRetriever(DataRetriever):
    def __init__(self) -> None:
        self.client = MongoClient(os.getenv('MONGODB_URI',''))

    def retrieve_data(self, embedd_client, query):

        collection = self.client[os.getenv('MONGODB_NAME','')][os.getenv('MONGODB_COLLECTION','')]

        print(f"Query:{query}")
        print("---------------")

        results = collection.aggregate([
                    {"$vectorSearch": {
                        "queryVector": embedd_client.embed.embed_query(query),
                        "path": "embeddings",
                        "numCandidates": 100,
                        "limit": 1,
                        "index": os.getenv('MONGO_INDEX_NAME',''),
                        }}
                    ])
        for document in results:
            print(f'Document Name: {document["doc_name"]},\nContent: {document["text"]}\n')

        return f'Document Name: {document["doc_name"]},\nContent: {document["text"]}\n'