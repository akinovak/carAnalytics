class CarContorller:

    def __init__(self, storage_controller):
        self.storage_controller = storage_controller

    def check_object(self, obj, collection):
        x = self.storage_controller.get(obj, collection)
        if x is None:
            return False
        else:
            self.storage_controller.update({'link': obj['link']}, obj, collection)
            return True

    def insert_object(self, obj, collection):
        self.storage_controller.insert(obj, collection)
