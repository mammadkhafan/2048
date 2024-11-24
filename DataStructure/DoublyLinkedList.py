# from DoublyLinkedNode import DoublyLinkedNode

import copy


class DoublyLinkedList:
    def __init__(self):
        """
        Initialize an empty doubly linked list.
        """
        self.head = None  # Pointer to the first node
        self.tail = None  # Pointer to the last node
        self._size = 0

    def add_node(self, value, i, j):
        """
        Add a new node to the list in the correct position based on (i, j).
        :param value: The value of the node.
        :param i: The row index.
        :param j: The column index.
        """
        new_node = DoublyLinkedNode(value=value, i=i, j=j)
        
        # Case 1: List is empty
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self._size += 1
            return

        # Case 2: Insert at the beginning
        if (i < self.head.i) or (i == self.head.i and j < self.head.j):
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            self._size += 1
            return

        # Case 3: Traverse the list to find the correct position
        current = self.head
        while current.next and (current.next.i < i or (current.next.i == i and current.next.j < j)):
            current = current.next

        # Case 3.1: Insert at the end
        if current.next is None:
            current.next = new_node
            new_node.prev = current
            self.tail = new_node
            self._size += 1
            return

        # Case 3.2: Insert in the middle
        new_node.next = current.next
        new_node.prev = current
        current.next.prev = new_node
        current.next = new_node
        self._size += 1
        return
    
        print("you can't add at this position!")
        
        
        
    def delete_node(self, node):
        """
        Delete a node from the list.
        :param node: The node to be deleted.
        """
        if node is None:
            return

        # Update pointers of surrounding nodes
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        # Update head and tail if needed
        if self.head == node:
            self.head = node.next
        if self.tail == node:
            self.tail = node.prev

        # Disconnect the node completely
        node.next = None
        node.prev = None
        
        self._size -= 1

    def update_node(self, node, value):
        """
        Update the value of a node.
        :param node: The node to be updated.
        :param value: The new value to assign to the node.
        """
        if node is not None:
            node.value = value

    def get_node(self, i, j):
        """
        Find a node based on its position (i, j).
        :param i: Row index of the node.
        :param j: Column index of the node.
        :return: The node if found, otherwise None.
        """
        current = self.head
        while current:
            if current.i == i and current.j == j:
                return current
            current = current.next
        return None
    
    
    @property
    def size(self):
        return self._size

        
        
    def __iter__(self):
        """
        Initialize the iteration pointer to the head of the list.
        """
        self._current = self.head
        return self

    def __next__(self):
        """
        Return the next node in the iteration.
        """
        if self._current is None:
            raise StopIteration  # End of the iteration
        node = self._current
        self._current = self._current.next
        return node

    def __repr__(self):
        """
        Debug-friendly representation of the list.
        """
        nodes = []
        current = self.head
        while current:
            nodes.append(repr(current))
            current = current.next
        return " -> ".join(nodes)
    
    def __deepcopy__(self, memo):
        """
        Create a deep copy of the doubly linked list.
        :param memo: A dictionary used to store already copied objects (used by deepcopy).
        :return: A deep copy of the list.
        """
        copied_list = DoublyLinkedList()
        
        current = self.head
        while current:
            # Add a node to the copied list using the original node's data
            copied_list.add_node(
                value = copy.deepcopy(current.value, memo), 
                i = current.i, 
                j = current.j
            )
            current = current.next
        
        return copied_list

    def __str__(self):
        """
        User-friendly representation of the list.
        """
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current))
            current = current.next
        return "\n".join(nodes)
    
    
    
    
    
    
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

