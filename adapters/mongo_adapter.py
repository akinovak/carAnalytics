import pymongo
from interfaces.databases.storage_interface import StorageInterface


class MongoAdapter(StorageInterface):

    def __init__(self, link, database):
        self.my_client = pymongo.MongoClient(link)
        self.db = self.my_client[database]

    def insert_object(self, obj, collection):
        self.db[collection].insert_one(obj)

    def update_object(self, obj_match, obj_update, collection):
        self.db[collection].update_one(obj_match, {"$set": obj_update})

    def delete_object(self, obj, collection):
        self.db[collection].delete_one(obj)

    def get_object(self, obj, collection):
        return self.db[collection].find_one(obj)
