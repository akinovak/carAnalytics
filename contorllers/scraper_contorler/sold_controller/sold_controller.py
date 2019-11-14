import requests, time
from contorllers.db_controllers.storage_controller import StorageController
from adapters.mongo_adapter import MongoAdapter
class SoldController:

    def __init__(self, storage_controller):
        self.storage_controller = storage_controller

    def insert_to_sold(self, obj, collection_del, collection_ins):
        self.storage_controller.delete(obj, collection_del)
        ts = time.gmtime()
        ts = time.strftime("%Y-%m-%d", ts)
        obj[collection_ins + '_date'] = ts
        self.storage_controller.insert(obj, collection_ins)

    # def insert_to_expired(self, obj, collection):
    #     self.storage_controller.delete(obj, collection)
    #     ts = time.gmtime()
    #     ts = time.strftime("%Y-%m-%d", ts)
    #     obj['expired_date'] = ts
    #     self.storage_controller.insert(obj, 'expired')


mongoAdp = MongoAdapter('mongodb://localhost:27017/', 'cardb')
storageCtl = StorageController(mongoAdp)
sold_ctl = SoldController(storageCtl)

