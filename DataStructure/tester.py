from DataStructure.DoublyLinkedList import DoublyLinkedList

# Create a new doubly linked list
dll = DoublyLinkedList()

# Add nodes
dll.add_node(5, 1, 2)
dll.add_node(10, 0, 1)
dll.add_node(15, 1, 1)
dll.add_node(20, 2, 0)

# Print the list
print(dll)  # Output will show nodes in order by (i, j)

print("---")

# Use a for loop to iterate through the list
for node in dll:
    print(node)
