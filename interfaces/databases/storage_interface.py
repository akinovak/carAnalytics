from abc import ABC


class StorageInterface(ABC):

    def insert_object(self, obj, collection):
        pass

    def get_object(self, obj, collection):
        pass

    def delete_object(self, obj, collection):
        pass

    def update_object(self, obj_match, obj_update, collection):
        pass
