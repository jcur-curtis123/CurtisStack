from blend import Blend, BlendLinkedList


class Warehouse:
    
    def __init__(self, ethiopia, honduras, rwanda):

        '''
        warehouse manages the current inventory of the coffee beans

        checks if blends can be produced 

        deducts bean quantites when making a batch

        prints current inventory of the beans post making batches
        '''

        # store the current number of beans
        # we will read in the .csv and store the bean quantities here
        self.beans = {
            "Ethiopia": float(ethiopia),
            "Honduras": float(honduras),
            "Rwanda": float(rwanda)
        }

    def can_make_batch(self, blend):

        '''
        need conditional logic when making batches

        meaning, beans cannot be < 0, or nonnegative

        if the amount_needed in batch is greater than whats stored in the self.beans

        we cannot make that batch

        otherwise, lets assume we can and continue
        '''

        usage = blend.usage_per_batch()

        for bean, amount_needed in usage.items():
            if amount_needed > self.beans[bean]:
                return False
        return True
    
    def make_batch(self, blend):

        '''
        method for making batches given a blend object

        blend classifies the blend object

        usage keeps track of the blend usage of beans

        bean quantity is reduced at each iteration for self.beans

        '''

        usage = blend.usage_per_batch()

        for bean, amount_needed in usage.items():
            self.beans[bean] -= amount_needed

    def remaining(self):

        '''
        return a copy of beans - do not want to alter self.beans

        warehouse uses .remaining for showcasing remaining beans and quantities
        '''
        return self.beans.copy()

    def current_inventory(self):

        '''
        method to print the current inventory, easy for keeping track of beans post make_batch
        '''

        print("Inventory Current:")

        for bean, quantity in self.beans.items():
            print(f"{bean}, {quantity}:lbs")