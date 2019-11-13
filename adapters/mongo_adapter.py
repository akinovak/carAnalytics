import pymongo
from interfaces.databases.storage_interface import StorageInterface
from conf import ctx


class MongoAdapter(StorageInterface):

    def __init__(self, link, database):
        self.my_client = pymongo.MongoClient(link)
        self.db = self.my_client[database]

    def insert_object(self, obj, collection):
        try:
            self.db[collection].insert_one(obj)
        except Exception as e:
            ctx.log.warning("Obj not inserted")
            ctx.log.warning(e)

    def update_object(self, obj_match, obj_update, collection):
        try:
            self.db[collection].update_one(obj_match, obj_update)
        except Exception as e:
            ctx.log.warning("Obj not updated")
            ctx.log.warning(e)

    def delete_object(self, obj, collection):
        try:
            self.db[collection].delete_one(obj)
        except Exception as e:
            ctx.log.warning("Obj not deleted")
            ctx.log.warning(e)

    def get_object(self, obj, collection):
        try:
            return self.db[collection].find_one(obj)
        except Exception as e:
            ctx.log.warning("Obj not found")
            ctx.log.warning(e)
            return None

