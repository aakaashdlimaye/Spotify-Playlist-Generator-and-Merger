# Define the Node class
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None  # Doubly linked list

# Define the LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        """ Append a node with the given data to the end of the doubly linked list """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
        self.size += 1

    def insert(self, data, position):
        """ Insert a node with the given data at the specified position """
        if position < 0 or position > self.size:
            print("Invalid position")
            return
        new_node = Node(data)
        if position == 0:  # Insert at the head
            new_node.next = self.head
            if self.head:
                self.head.prev = new_node
            self.head = new_node
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            new_node.next = current.next
            if current.next:
                current.next.prev = new_node
            current.next = new_node
            new_node.prev = current
        self.size += 1

    def delete(self, position):
        """ Delete a node at the specified position """
        if position < 0 or position >= self.size:
            print("Invalid position")
            return
        current = self.head
        if position == 0:  # Delete the head
            self.head = current.next
            if self.head:
                self.head.prev = None
        else:
            for _ in range(position):
                current = current.next
            current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
        self.size -= 1

    def to_list(self):
        """ Convert the linked list to a Python list for easier manipulation """
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def binary_search(self, target):
        """ Perform binary search on the linked list (converted to list) """
        data_list = self.to_list()  # Convert linked list to Python list since binary search needs random access of memory
        low = 0
        high = len(data_list) - 1

        while low <= high:
            mid = (low + high) // 2
            if data_list[mid] == target:
                return True
            elif data_list[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return False
