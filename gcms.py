from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.capacity1 = AVLTree()
        self.object_info_tree = AVLTree()
        self.bin_id_tree = AVLTree()
        self.capacity2 = AVLTree()

    def add_bin(self, bin_id, capacity):
        if self.bin_id_tree.search(bin_id) == None:
            bin_object = Bin(bin_id, capacity)
            self.bin_id_tree.insert(bin_id, bin_object)
            self.capacity1.insert((capacity, bin_id), bin_object)
            self.capacity2.insert((capacity, -bin_id), bin_object)

    def add_object(self, object_id, size, color):
        if color==Color.BLUE:
            rt = self.capacity1.root
            possible_node=None
            while rt!=None:
                if rt.value.capacity>=size:
                    possible_node = rt
                    rt = rt.left
                else:
                    rt = rt.right
        if color==Color.YELLOW:
            rt = self.capacity2.root
            possible_node=None
            while rt!=None:
                if rt.value.capacity>=size:
                    possible_node = rt
                    rt=rt.left
                else:
                    rt=rt.right
        if color==Color.GREEN:
            rt = self.capacity1.root
            possible_node=None
            while rt!=None:
                if rt.value.capacity>=size:    
                    possible_node = rt
                rt=rt.right
        if color==Color.RED:
            rt = self.capacity2.root
            possible_node=None
            while rt!=None:
                if rt.value.capacity>=size:    
                    possible_node = rt
                rt=rt.right

        if possible_node==None:
            raise NoBinFoundException()

        bin_obj=possible_node.value
        y=Object(object_id, size, color,bin_obj.bin_id)
        self.object_info_tree.insert(object_id, bin_obj.bin_id)
        bin_obj.objects.insert(object_id,y)
        self.capacity1.delete((bin_obj.capacity, bin_obj.bin_id))
        self.capacity2.delete((bin_obj.capacity, -bin_obj.bin_id))
        self.bin_id_tree.delete(bin_obj.bin_id)
        bin_obj.capacity-=size
        self.capacity1.insert((bin_obj.capacity, bin_obj.bin_id), bin_obj)
        self.capacity2.insert((bin_obj.capacity, -bin_obj.bin_id), bin_obj)
        self.bin_id_tree.insert(bin_obj.bin_id, bin_obj)

    def delete_object(self, object_id):
        # Implement logic to remove an object from its bin
        bn = self.object_info_tree.search(object_id)
        if bn:
            node = self.bin_id_tree.search(bn.value)
            if node:
                bin_obj = node.value
                obj_node = bin_obj.objects.search(object_id).value
                sz = obj_node.size
                self.object_info_tree.delete(object_id)
                bin_obj.objects.delete(object_id)
                self.capacity1.delete((bin_obj.capacity, bin_obj.bin_id))
                self.capacity2.delete((bin_obj.capacity, -bin_obj.bin_id))
                self.bin_id_tree.delete(bin_obj.bin_id)
                bin_obj.capacity += sz
                self.capacity1.insert((bin_obj.capacity, bin_obj.bin_id), bin_obj)
                self.capacity2.insert((bin_obj.capacity, -bin_obj.bin_id), bin_obj)
                self.bin_id_tree.insert(bin_obj.bin_id, bin_obj)

    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        bin_item = self.bin_id_tree.search(bin_id)
        bn = bin_item.value
        capac = bn.capacity
        if bn:
            l = bn.objects.inorder()
            return (capac, l)
        return None

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        node = self.object_info_tree.search(object_id)
        if node:
            return node.value