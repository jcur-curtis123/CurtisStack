from node import node 

# import the node class from the node.py file.
# this is needed for the add_to_back, add_to_front, and remove_at_index methods


class ToDoLinkedList:
    '''
    Initialize self.head (beginning of linked list) as none

    This list is also empty at __init__

    This is required for start of our linked list
    '''
    def __init__(self):
        self.head = None
    
    def add_to_back(self, object):

        '''
        add_to_back takes a variable new_node (instance of the node class)

        we need a new node to be added (cannot reuse an existing node to add to our linked list)

        if the beginning of our linked list is empty, assign our new node to the first node

        if the linked list is not empty, assign a current (index) to the beginning of the list

        if the next node is not None or empty, continue through the list

        add the node after the while loop terminates (current.next is None)
        
        '''
        
        new_node = node(object)

        if self.head is None:
            self.head = new_node

        else:
            current = self.head
        
            while current.next is not None:
                current = current.next
        
            current.next = new_node
    
    def add_to_front(self, object):

        '''
        new node is an object of the node class

        the next node is set the beginning node of the linked list

        new_node.next can be "X" where X -> A -> B -> C

        X is set to the head where self.head points to X

        '''
        
        new_node = node(object)

        new_node.next = self.head

        self.head = new_node

    def remove_at_index(self, index):

        '''
        in order to remove the indexed node, we must set the neighboring node of head to the head

        for loop to iterate through the linked list since we are allowed to iterate vs recurse

        stop before we hit the index, current.next is the node we'd like to remove
        '''

        if index == 0:
            self.head = self.head.next
        
        current = self.head

        for i in range(index - 1): #stop at the index prior to the node we would like to delete
            if current.next is None:
                return
            current = current.next

        if current.next is not None:
            current.next = current.next.next # removes the node by skipping the original current.next

    def clear(self):
        '''
        clear the entire linked list by setting the head to None
        '''
        self.head = None


    def change_priority(self, index):
        '''
        This is the code chunk from canvas

        Required for creating an entry point to the recursive functions 

        change_priority, conditional_str, and filter
        '''
        return self.head.change_priority(index)

    def conditional_str(self, predicate):
        '''
        This is the code chunk from canvas

        Required for creating an entry point to the recursive functions 

        change_priority, conditional_str, and filter
        '''
        return self.head.conditional_str(predicate)

    def filter(self, predicate):
        '''
        This is the code chunk from canvas

        Required for creating an entry point to the recursive functions 

        change_priority, conditional_str, and filter
        '''
        return self.head.filter(predicate)