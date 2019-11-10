class StorageController:
    def __init__(self, adapter):
        self.adapter = adapter

    def insert(self, obj, collection):
        self.adapter.insert_object(obj, collection)

    def get(self, obj, collection):
        return self.adapter.get_object(obj, collection)

    def update(self, obj_match, obj_update, collection):
        self.adapter.update_object(obj_match, obj_update, collection)