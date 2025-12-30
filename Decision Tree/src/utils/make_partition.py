from config.pivots import PIVOTS
from src.parent_strategy import ParentStrategy


def make_partition(record_objects, lam):
    '''
    initialize true list and false list

    the basis of partitioning dataset into two (True or False)
    '''
    returned_list_true = []
    returned_list_false = []

    for i in record_objects:
        '''
        if the lam returns True, append to the true list
        '''
        if lam(i) == True:
            returned_list_true.append(i)
        else:
            '''
            anything else shoukd be false if the lam is not True
            '''
            returned_list_false.append(i)

    return returned_list_true, returned_list_false


def find_best_partition(record_objects, strategy_object):

    '''
    initalize result list, best_attribute, and lowest_impurity (either gini or entrpopy)

    this find_best_partition is an add on from part 7 in the homework -

    this is used to determine the best partition 
    '''

    results = []
    best_attribute = None
    lowest_impurity = 1.0 #highest possible impurity score
    
    for attribute_name, lam in PIVOTS.items():
        '''
        for loop for accessing the Pivots dictionary of attributes and its corresponding lambdas

        define a var partition from our original make_partition method

        calculate the impurity of the specific partition

        ie; partition[0] is all Smokers, and partition[1] is all non-smokers
        '''
        partition = make_partition(record_objects, lam)
        impurity = strategy_object.calculate(partition)
    
        if impurity < lowest_impurity:
            '''
            conditional on deciding if the current impurity is less than the prev lowest_impurity
            '''
            lowest_impurity = impurity
            best_attribute = attribute_name
    
        # append the attribute name with its associated impurity score
        results.append((attribute_name, impurity))

    # print the best attribute and the lowest impurity score calculated
    print("Best attribute:", best_attribute)
    print("Lowest impurity:", lowest_impurity)
        
