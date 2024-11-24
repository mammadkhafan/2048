class DoublyLinkedNode:
    def __init__(self, value=None, i=None, j=None):
        """
        Initialize the node with optional value, row index, and column index.
        """
        self._value = value  # Internal storage for value
        self._i = i          # Internal storage for row index
        self._j = j          # Internal storage for column index
        self._prev = None    # Pointer to the previous node
        self._next = None    # Pointer to the next node

    # Property for value
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    # Property for row index
    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, val):
        self._i = val

    # Property for column index
    @property
    def j(self):
        return self._j

    @j.setter
    def j(self, val):
        self._j = val

    # Property for previous node
    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, node):
        self._prev = node

    # Property for next node
    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node

    def __repr__(self):
        """
        Debug-friendly representation of the node.
        """
        return f"Node(value={self._value}, i={self._i}, j={self._j})"

    def __str__(self):
        """
        User-friendly string representation of the node.
        """
        return f"Value: {self._value}, Position: ({self._i}, {self._j})"
