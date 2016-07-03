#!/usr/bin/env python3

class HeapPriorityQueue():
    """A min priority queue implmented with a binary heap."""

    class _Item:
        """Class for storing priority queue items."""

        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key

    # Non-public behaviors
    def _parent(self, j):
        return (j-1) // 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _has_left(self, j):
        # index beyond end of list check
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        """Swap the elements at indices i and j of array"""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)

        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left

            if self._has_right(j):
                right = self._right(j)

                if self._data[right] < self._data[left]:
                    small_child = right

            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    # Public behaviors
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        """Return True if the priority queue is empty."""

        return len(self) == 0

    def add(self, key, value):
        """Add a key-value pair to the priority queue."""

        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)

    def min(self):
        """Return but do not remove (k, v) tuple with minimum key.

        Raise Empty exception if empty."""
        if self.is_empty():
            raise Empty('Priority queue is empty.')

        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (k, v) tuple with minimum key.

        Raise Empty exception if empty."""
        if self.is_empty():
            raise Empty('Priority queue is empty.')

        self._swap(0, len(self._data) - 1)  # put minimum item at the end
        item = self._data.pop()             # and remove it from list
        self._downheap(0)                   # fix new root

        return (item._key, item._value)


class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    """A locator-based priority queue implmented with a binary heap"""

    # nested locator class
    class Locator(HeapPriorityQueue._Item):
        """Token for locating an entry of the priority queue"""
        __slots__ = '_index'

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j

    # nonpublic behaviors
    # override swap to record new indices
    def _swap(self, i, j):
        super()._swap(i, j)
        self._data[i]._index = i        # reset locator index
        self._data[j]._index = j

    def _bubble(self, j):
        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)


    # public behaviors
    def add(self, key, value):
        """Add a key-value pair"""
        token = self.Locator(key, value, len(self._data))

        self._data.append(token)
        self._upheap(len(self._data) - 1)

        return token

    def update(self, loc, newKey, newVal):
        """Update the key and value for the entry identified by Locator loc."""
        j = loc._index

        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')

        loc._key = newKey
        loc._value = newVal

        self._bubble(j)

    def remove(self, loc):
        """Remove and return the (k, v) pair identified by Locator loc"""

        j = loc._index

        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')

        if j == len(self) - 1:
            self._data.pop()
        else:
            self._swap(j, len(self) - 1)
            self._data.pop()
            self._bubble(j)

        return (loc._key, loc._value)
