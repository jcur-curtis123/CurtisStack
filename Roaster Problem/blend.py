class Blend:
    '''
    Blend defines the name of the blend along with bean types
    
    __init__ initializes name, each type of bean, and corresponding price per pound within the blend

    floats are best for division

    self.next is set to none - this will be used in the linkedlist 

    define the batch size - used for calculation in strategy.py

    '''
    def __init__(self, name, ethiopia, honduras, rwanda, price):

        self.name = name
        self.ethiopia = float(ethiopia)
        self.honduras = float(honduras)
        self.rwanda = float(rwanda)
        self.price = float(price)
        self.batch_size = 100
        self.next = None


    def usage_per_batch(self):

        '''
        usage_per_batch stores each type of bean Ethiopia, Honduras, Rwanda

        and it's corresponding integer count

        this is required as 100 pounds are required per batch

        this data is used by the warehouse class to check bean quantities

        '''
        beans_usage = {
            "Ethiopia": (self.ethiopia),
            "Honduras": (self.honduras),
            "Rwanda": (self.rwanda) 
        }

        return beans_usage

    def total_bean_usage(self):

        '''
        In order to keep track of total beans used

        return the sum of all beans used across blends

        this is required for calculating blend efficiency in strategies.py

        '''
        return self.ethiopia + self.honduras + self.rwanda

    def revenue_per_batch(self):
        '''
        revenue per batch is calculated by taking the price per lb for a given blend

        and multiplies the batch size for a total revenue of the blend
        '''
        return self.price * self.batch_size


class BlendLinkedList:

    '''
    class BlendLinkedList holds the linked list logic

    __init__ starts the linked list as our head is empty

    append() allows for addition of nodes to the linked list

    traverse() allows for traversing through all nodes in list

    '''

    def __init__(self):
        # start with an empty list
        self.head = None

    def append(self, blend):
        # if the beginning of the list is empty
        # set the the head to blend object
        if self.head is None:
            self.head = blend
        else:
            current = self.head
            # walk or traverse through the list until 
            # current.next is None
            # when the while loop terminates, add blend object as the last node
            while current.next is not None:
                current = current.next
            current.next = blend

    def traverse(self):

        '''
        This method is purely for debug purposes

        Determines if nodes are present in the linked list
        '''

        current = self.head

        while current is not None:

            print(f"Ethiopia: {current.ethiopia}")
            print(f"Honduras: {current.honduras}")
            print(f"Rwanda: {current.rwanda}")
            print(f"Revenue per batch: ${current.revenue_per_batch()}")
            current = current.next



    
