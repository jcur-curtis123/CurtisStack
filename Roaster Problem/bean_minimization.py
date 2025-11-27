from strategies import Strategy
from blend import Blend, BlendLinkedList
from warehouse import Warehouse

class MinimizeEthiopia(Strategy):

    '''
    Define class MinimizeEthiopia for minimizing leftover Ethiopia beans

    MinimizeEthiopia inherits parent class Strategy

    '''


    def driver(self):

        '''
        driver is the method for producing the optimal usage of Ethiopia beans
        '''


        '''
        Ethiopia efficiency is defined as a lambda 

        lambda takes blend as parameter, and computes the blend's usage of ethiopia multiplied by it's sale price

        ethiopia efficiency will store the product and is used in the greedy algorithm

        '''

        ethiopia_efficiency = lambda b: b.usage_per_batch()["Ethiopia"] * b.price

        batches_made = {}
        total_income = 0

        '''
        initialize income - this will be used for reporting total income

        initialize batches_made - this dictionary will store total batches of coffee produced
        '''

        current = self.blend_list.head
        while current is not None:
            batches_made[current.name] = 0
            current = current.next
        
        while self.can_make_blend():
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
                    blend_score = ethiopia_efficiency(current)
                    if blend_score > best_score:
                        best_score = blend_score
                        best_blend = current
                current = current.next


            '''
            increment income from revenue of each best_blend

            increment batches_made from each best_blend
            '''


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
        

        for bean, qty in self.warehouse.remaining().items():
            '''
            print the number of beans remaining in the warehouse

            where remaining() returns a copy of self.beans post make_batch
            '''
            print(f"{bean}: {qty} lbs")

            

class MinimizeHonduras(Strategy):

    '''
    Define class MinimizeHonduras for minimizing leftover Honduras beans

    MinimizeHonduras inherits parent class Strategy
    '''

    def driver(self):

        '''
        driver is the method for producing the optimal usage of Honduras beans
        '''


        '''
        Honduras efficiency is defined as a lambda 

        lambda takes blend as parameter, and computes the blend's usage of honduras multiplied by it's sale price

        ethiopia efficiency will store the product and is used in the greedy algorithm

        '''    

        honduras_efficiency = lambda b: b.usage_per_batch()["Honduras"] * b.price

        batches_made = {}
        total_income = 0

        '''
        initialize income - this will be used for reporting total income

        initialize batches_made - this dictionary will store total batches of coffee produced
        '''

        current = self.blend_list.head
        while current is not None:
            batches_made[current.name] = 0
            current = current.next
        
        while self.can_make_blend():
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
                    blend_score = honduras_efficiency(current)
                    if blend_score > best_score:
                        best_score = blend_score
                        best_blend = current
                current = current.next

            '''
            increment income from revenue of each best_blend

            increment batches_made from each best_blend
            '''

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
        

        for bean, qty in self.warehouse.remaining().items():
            '''
            print the number of beans remaining in the warehouse

            where remaining() returns a copy of self.beans post make_batch
            '''
            print(f"{bean}: {qty} lbs")


class MinimizeRwanda(Strategy):

    '''
    Define class MinimizeRwanda for minimizing leftover Rwanda beans

    MinimizeRwanda inherits parent class Strategy
    '''

    def driver(self):

        '''
        driver is the method for producing the optimal usage of Rwanda beans
        '''
    
        '''
        Rwanda efficiency is defined as a lambda 

        lambda takes blend as parameter, and computes the blend's usage of Rwanda multiplied by it's sale price

        ethiopia efficiency will store the product and is used in the greedy algorithm

        '''

        rwanda_efficiency = lambda b: b.usage_per_batch()["Rwanda"] * b.price

        batches_made = {}
        total_income = 0

        '''
        initialize income - this will be used for reporting total income

        initialize batches_made - this dictionary will store total batches of coffee produced
        '''

        current = self.blend_list.head
        while current is not None:
            batches_made[current.name] = 0
            current = current.next
        
        while self.can_make_blend():
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
                    
                    blend_score = rwanda_efficiency(current)
                    if blend_score > best_score:
                        best_score = blend_score
                        best_blend = current
                current = current.next

            '''
            increment income from revenue of each best_blend

            increment batches_made from each best_blend
            '''

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
        

        for bean, qty in self.warehouse.remaining().items():
            '''
            print the number of beans remaining in the warehouse

            where remaining() returns a copy of self.beans post make_batch
            '''
            print(f"{bean}: {qty} lbs")