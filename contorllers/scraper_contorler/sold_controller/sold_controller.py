import requests, time


class SoldController:

    def __init__(self, storage_controller):
        self.storage_controller = storage_controller

    def insert_to_sold(self, obj, collection):
        self.storage_controller.delete(obj, collection)
        ts = time.gmtime()
        ts = time.strftime("%Y-%m-%d", ts)
        obj['sold_date'] = ts
        self.storage_controller.insert(obj, 'sold')


sold_ctl = SoldController()
