from blend import BlendLinkedList
from warehouse import Warehouse

class Strategy:

    '''
    initialize blend_list and warehouse 

    these variables are read in within driver.py
    '''

    def __init__(self, warehouse, blend_list):

        self.blend_list = blend_list
        self.warehouse = warehouse

    '''
    can_make_blend returns a boolean type and contains logic for if we can produce the given batch of blend

    the can_make_blend method carries linked list logic, and traverses through until current is none

    this method comes into use also in the Minimize Strategies

    see bean_minimization.py for further representation
    '''

    def can_make_blend(self):
        current = self.blend_list.head
        while current is not None:
            if self.warehouse.can_make_batch(current):
                return True
            current = current.next
        return False

    def greedy_strategy(self):
        
        '''
        greedy_strategy is the primary algorithm for maximizing income and 

        minizming waste from beans during the making of batches

        each lambda is defined, assigned weights, and sorted 

        '''

        '''
        define lambdas for efficiency calculation

        calculate the overall efficiency or combined efficiency between income

        '''
        income_efficiency = lambda b: b.revenue_per_batch() / b.total_bean_usage()
        
        batches_made = {}
        total_income = 0


        '''
        initialize income - this will be used for reporting total income

        initialize batches_made - this dictionary will store total batches of coffee produced
        '''
        current = self.blend_list.head
        while current is not None:
            batches_made[current.name] = 0 # each blend count is set to 0
            current = current.next
        

        while self.can_make_blend():

            remaining = self.warehouse.remaining()

            # weighted calculation for each bean
            weighted_ethiopia = 1.0 / (remaining["Ethiopia"] + 0.000001)
            weighted_honduras = 1.0 / (remaining["Honduras"] + 0.000001)
            weighted_rwanda = 1.0 / (remaining["Rwanda"] + 0.000001) # added a small integer for rounding with 0


            best_blend = None
            best_score = -1

            '''
            linked list logic within greedy strategy
            
            current stores the current node during traversal

            best blend and best core are also initialized - this score will update and change

            upon evaluation of each blend here in the linked list
            '''
            current = self.blend_list.head
            while current is not None:
                if self.warehouse.can_make_batch(current):

                    '''
                    If conditional for making batches. If making batches is possible, 

                    calculate bean weights for income efficiency score and continue with the traversal

                    Use is the current node's (coffee blend) usage of beans 
                    '''
                    use = current.usage_per_batch()
                    scarce_beans = use["Ethiopia"] * weighted_ethiopia + use["Honduras"] * weighted_honduras + use["Rwanda"] * weighted_rwanda # denominator of weighted beans
                    score = income_efficiency(current) / scarce_beans if scarce_beans > 0 else 0 # weighted income efficiency score

                    '''
                    if the current score is greater than the previous best_score

                    set this score to the best

                    and the current node to best blend

                    continue to do this until current is none
                    '''

                    if score > best_score:
                        best_score = score
                        best_blend = current
                current = current.next 
            
            '''
            increment income from revenue of each best_blend

            increment batches_made from each best_blend
            '''
            if best_blend is not None:
                self.warehouse.make_batch(best_blend) 
                batches_made[best_blend.name] += 1
                total_income += best_blend.revenue_per_batch()
        

        print("Batches produced:")
        for name, count in batches_made.items():
            # print total batches produces overall while maxmimizing income

            # print the name of the blend and its associating count
            print(f"{name}: {count}")

        print(f"Total Income: ${total_income}")
        print("Remaining Beans:")
        
        # print leftover beans from the warehouse
        for bean, qty in self.warehouse.remaining().items():
            '''
            print the number of beans remaining in the warehouse

            where remaining() returns a copy of self.beans post make_batch
            '''
            print(f"{bean}: {qty} lbs")

        
        # return total batches made, total income, and the remaining beans in the warehouse after greedy_algorithm
        return batches_made, total_income, self.warehouse.remaining()
