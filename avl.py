from node import Node

def comp_1(node_1, node_2):
    if node_1.key < node_2.key:
        return -1
    elif node_1.key > node_2.key:
        return 1
    else:
        return 0

class AVLTree:
    def __init__(self, compare_function=comp_1):
        self.root = None
        self.size = 0
        self.comparator = compare_function

    def _left_height(self, node):
        return node.left.height if node.left else 0

    def _right_height(self, node):
        return node.right.height if node.right else 0

    def _recompute_height(self, node):
        node.height = 1 + max(self._left_height(node), self._right_height(node))

    def _is_balanced(self, node):
        return abs(self._left_height(node) - self._right_height(node)) <= 1

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node
        new_root.parent = node.parent
        if node.parent is None:
            self.root = new_root
        elif node == node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root
        new_root.left = node
        node.parent = new_root

        self._recompute_height(node)
        self._recompute_height(new_root)

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node
        new_root.parent = node.parent
        if node.parent is None:
            self.root = new_root
        elif node == node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root
        new_root.right = node
        node.parent = new_root

        self._recompute_height(node)
        self._recompute_height(new_root)

    def _rebalance(self, node):
        while node:
            self._recompute_height(node)
            if not self._is_balanced(node):
                if self._left_height(node) > self._right_height(node):
                    if self._left_height(node.left) < self._right_height(node.left):
                        self._rotate_left(node.left)
                    self._rotate_right(node)
                else:
                    if self._right_height(node.right) < self._left_height(node.right):
                        self._rotate_right(node.right)
                    self._rotate_left(node)
            node = node.parent

    def insert(self, key, value):
        new_node = Node(key, value)
        if not self.root:
            self.root = new_node
            return

        current = self.root
        parent = None

        while current:
            parent = current
            if self.comparator(new_node, current) < 0:
                current = current.left
            else:
                current = current.right

        if self.comparator(new_node, parent) < 0:
            parent.left = new_node
        else:
            parent.right = new_node
        new_node.parent = parent

        self._rebalance(new_node)

    def search(self, key):
        current = self.root
        search_node = Node(key)

        while current:
            comparison = self.comparator(search_node, current)
            if comparison == 0:
                return current
            elif comparison < 0:
                current = current.left
            else:
                current = current.right

        return None

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self, key):
        node_to_delete = self.search(key)
        if not node_to_delete:
            return

        self._delete_node(node_to_delete)

    def _delete_node(self, node):
        if not node.left and not node.right:
            self._delete_leaf(node)
        elif not node.left or not node.right:
            self._delete_single_child(node)
        else:
            self._delete_two_children(node)

    def _delete_leaf(self, node):
        parent = node.parent
        if parent:
            if parent.left == node:
                parent.left = None
            else:
                parent.right = None
            self._rebalance(parent)
        else:
            self.root = None

    def _delete_single_child(self, node):
        child = node.left if node.left else node.right
        parent = node.parent
        if parent:
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child
            child.parent = parent
            self._rebalance(parent)
        else:
            self.root = child
            child.parent = None

    def _delete_two_children(self, node):
        successor = self._find_min(node.right)
        node.key = successor.key
        node.value = successor.value
        self._delete_node(successor)

    def inorder(self):
        return self._inorder(self.root)
    
    def _inorder(self, node):
        return self._inorder(node.left) + [(node.key)] + self._inorder(node.right) if node else []