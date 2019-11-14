import time
class CarContorller:

    def __init__(self, storage_controller):
        self.storage_controller = storage_controller

    def check_object(self, obj, collection):
        x = self.storage_controller.get(obj, collection)
        if x is None:
            return False
        else:
            ts = time.gmtime()
            ts = time.strftime("%Y-%m-%d", ts)
            self.storage_controller.update({'link': obj['link']},
                                           {"$set": {'cena': obj['cena'], 'datum_obnove': obj['datum_obnove']}, "$push":{'istorija': {ts: obj['cena']} }},
                                           collection)
            return True

    def insert_object(self, obj, collection):
        self.storage_controller.insert(obj, collection)
