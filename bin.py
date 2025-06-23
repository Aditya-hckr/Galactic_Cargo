from object import *
from avl import *
from exceptions import *

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.objects = AVLTree()

    def add_object(self, object):
        # Implement logic to add an object to this bin
        if(self.space_left < object.size):
            raise NoBinFoundException()
        else:
            self.space_left -= object.size
            self.obejcts.insert(object.object_id, object.size)
            
    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        if self.objects.search(object_id):
            node = self.objects.search(object_id)
            self.objects.delete(object_id)
            self.space_left += node.size