import requests, time


class SoldController:

    def __init__(self, storage_controller):
        self.storage_controller = storage_controller

    def check_object_on_website(self, obj, collection):
        # x = self.storage_controller.get(obj, collection)
        r = requests.get(url=obj['link'])

        if (r.url != obj['link'] and r.status_code == 200) or r.status_code == 404:
            self.storage_controller.delete(obj, collection)
            self.storage_controller.insert(obj, 'sold')
        elif r.status_code >= 500:
            time.sleep(10*60)
            self.check_object_on_website(obj, collection)