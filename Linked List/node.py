from task import Task

'''
define our class node with the __str__, __init__, change_priority, conditional_str, and filter
'''
class node:
    def __init__(self, data, next=None):
        '''
        initialize our class node with the __init__ construct 

        self.data is needed for task data

        self.next is the next node in our linked list

        '''
        self.data = data
        self.next = next
    
    def __str__(self):
        '''
        we return the str of the self.data

        self.data in the __init__ constructor
        '''
        return str(self.data)

    def change_priority(self, index, current=0):
        '''
        Current is parameter for change_priority, almost like a count during iteration

        current keeps track of which node we are currently on
        
        index is the position within the linked list
        '''
        if current == index:
            self.data.update_priority()
        elif self.next:
            self.next.change_priority(index, current + 1)

    def conditional_str(self, lam):
        
        '''
        Condition_str takes a lambda as param.

        Depending on how the node object is returned...

        The conditional_str could return a linked chain evenutually leading to "None" - The end of the chain

        '''

        if lam(self):
            if self.next:
                return f"{self.data}" + "-->" + self.next.conditional_str(lam)
            else:
                return f"{self.data}" + "-->" + "None"
            '''
            if the node fails the lambda, return the conditional_str to check the next node

            if the next node exists run through the function again

            without the outer else, the function would return None and terminate
            '''
        else:
             if self.next:
                return self.next.conditional_str(lam)
             else:
                return "None"
    def filter(self, lam2):

        '''
        Given the lambda, filter and build a copy of the linkedlist

        if the current node passes the filter, return this node and the function for the next node

        if there is not a next node, return none

        if the lambda fails, keep filtering
        
        if the lambda fails and there is no further nodes, terminate
        '''

        if lam2(self):
            if self.next:
                return node(self.data, self.next.filter(lam2))
            else:
                return node(self.data, None)
        else:
            if self.next:
                return self.next.filter(lam2)
            else:
                return None