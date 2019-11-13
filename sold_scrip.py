from contorllers.scraper_contorler.sold_controller.sold_controller import SoldController
from contorllers.db_controllers.storage_controller import StorageController
from adapters.mongo_adapter import MongoAdapter
import pymongo

mongoAdp = MongoAdapter('mongodb://localhost:27017/', 'cardb')
storageCtl = StorageController(mongoAdp)
controller = SoldController(storageCtl)
collections = ['polovni']

my_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = my_client['cardb']

def parse_collection(collection):
    for document in db[collection].find():
        controller.check_object_on_website(document, collection)


parse_collection('cars')