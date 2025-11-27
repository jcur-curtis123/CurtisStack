from src.parent_strategy import ParentStrategy

'''
Import the parent class ParentStrategy - need weight and probability methods
'''

class CollectiveImpurityGini(ParentStrategy):

    def calculate(self, partition):

        '''
        calculate is very similar to that of the entropy calculate method

        total_gini is initialized at 0.0 prior to the running total in the latter for loop

        for loop to access each susbet in our partition

        '''

      
        weights = self.calculate_weights(partition) # refactored for gini for weight variable given by calculate weights from parent_strategy
        total_gini = 0.0
        index = 0

        for group in partition:
            '''
            calculate the probability of "High Risk", "Low Risk" labels for the subset partitions

            calculate gini score with provided formula

            total gini for this partition includes the weight of each group in relevance to its partition 
            '''
            if group: # if group (subset) exists in our partition, compute the following
               
                p_high = self.probability(group, "High Risk")
                p_low = self.probability(group, "Low Risk")

                gini = 1 - (p_high ** 2 + p_low ** 2) # gini formula
                weight = weights[index] # weight is implemented here similar to that of entropy
                total_gini += weight * gini 
            
            index += 1 

        return total_gini # fixed indentation level for gini return - gini should now return properly