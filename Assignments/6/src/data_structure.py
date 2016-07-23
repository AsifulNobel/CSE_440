from collections import deque

class BinaryTree:
    class _Node:
        """Class representation of nodes in binary tree"""

        def __init__(self, parent=None, left=None, right=None, attribute=None, threshold=None, distribution=None, gain=None):
            self._parent = parent
            self._left = left
            self._right = right
            self._attribute = attribute
            self._threshold = threshold
            self._gain = gain
            self._distribution = distribution   # not None only in leaf nodes

        def is_leaf(self):
            if self._left is None and self._right is None:
                return True
            return False

    def __init__(self):
        self._root = None


    def add_root(self, attribute=None, threshold=None, gain=None):
        self._root = self._Node(attribute=attribute, threshold=threshold, gain=gain)


    def add_left(self, attribute, threshold, distribution):
        if self._root:
            self._root._left = self._Node(parent=self._root, left=None, right=None, attribute=attribute, threshold=threshold, distribution=distribution)
        else:
            logger.error("No root in tree")


    def add_right(self, attribute, threshold, distribution):
        if self._root:
            self._root._right = self._Node(parent=self._root, attribute=attribute, threshold=threshold, distribution=distribution)
        else:
            logger.error("No root in tree")


    def attach_left(self, sub_tree):
        """attach a sub-tree to left child node"""

        if isinstance(sub_tree, BinaryTree):
            sub_tree_root = sub_tree.get_root()

            if sub_tree_root:
                self._root._left = sub_tree_root
                sub_tree_root._root = self._root
        elif isinstance(sub_tree, dict):
            # When sub_tree is actually distribution
            self.add_left(None, None, distribution=sub_tree)



    def attach_right(self, sub_tree):
        """attach a sub-tree to right child node"""
        if isinstance(sub_tree, BinaryTree):
            sub_tree_root = sub_tree.get_root()

            if sub_tree_root:
                self._root._right = sub_tree_root
                sub_tree_root._root = self._root
        elif isinstance(sub_tree, dict):
            # When sub_tree is actually distribution
            self.add_right(None, None, distribution=sub_tree)


    def get_root(self):
        if self._root:
            return self._root


    def children(self):
        """Iterator for child nodes"""

        if self._root._left:
            yield self._root._left

        if self._root._right:
            yield self._root._right

    def breadthFirst(self):
        """Iterator for BFS on tree nodes"""

        chain = deque()
        node_id_chain = deque()

        if self._root:
            chain.append(self._root)
            node_id_chain.append(1)

        while len(chain) > 0:
            node = chain.popleft()
            node_id = node_id_chain.popleft()
            yield node, node_id

            if node._left:
                chain.append(node._left)
                node_id_chain.append(node_id*2)

            if node._right:
                chain.append(node._right)
                node_id_chain.append(node_id*2+1)
