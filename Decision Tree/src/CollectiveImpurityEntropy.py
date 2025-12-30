from src.parent_strategy import ParentStrategy
import math

'''
Import Parent class ParentStrategy - we need to calculate probability for "high risk" and "low risk" labels for the gini calc

I also import Python's math module in order for the entropy formula to be accurate

Without math I would need to define log2 in a seperate method, and this could result in rounding and multiplication errors
'''

class CollectiveImpurityEntropy(ParentStrategy):

    def calculate(self, partition):

        '''
        calculate() used for the calculation of the entropy impurity
        
        similar method used for the gini impurity 

        weights like probability is inherited from the parent class

        weights required for entropy formula
        '''

        index = 0
        total_impurity = 0
        weights = self.calculate_weights(partition)

        for i in partition:

            '''
            for every i (subset) in the split partition, calculate the probability of each label "High Risk" and "Low Risk"

            weight assigns the current weight calculation of the current index in the partition 

            same goes for our entropy calculation

            
            '''

            p_high = self.probability(i, "High Risk")
            p_low = self.probability(i, "Low Risk")

            entropy_impurity = 0

            if p_high > 0:
                entropy_impurity -= p_high * math.log2(p_high) # entropy formula with math module
            if p_low > 0:
                entropy_impurity -= p_low * math.log2(p_low)  # entropy formula with math module

            weight = weights[index]
            
            total_impurity = total_impurity + (weight * entropy_impurity) # weighted impurity formula
            
            index += 1

        return total_impurity 




