from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, uri, database_name):
        self.client = MongoClient(uri)
        self.db = self.client[database_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def get_documents(self, collection_name):
        collection = self.get_collection(collection_name)
        return list(collection.find())

    def close_connection(self):
        self.client.close()
        