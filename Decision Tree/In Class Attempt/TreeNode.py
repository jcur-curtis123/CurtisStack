from config.pivots import PIVOTS
from src.parent_strategy import ParentStrategy

class TreeNode:

    def __init__(self, records, pivots):
        self.records = records
        self.pivots = pivots

        self.children = []

        self.partition_logic = None
        self.label_to_apply = None

        self.low_risk_count, self.high_risk_count = self.count_label()

    
    def count_label(self):
        lc0 = 0
        lc1 = 0

        for record in self.records:
            if record.actual_label == "Low Risk":
                lc0 += 1
            if record.actual_label == "High Risk":
                lc1 += 1
        return lc0, lc1


    def make_partition(self, record_objects, lam):
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


    def find_best_partition(self, strategy_object):

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
            partition = self.make_partition(self.records, lam)
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
        
    def grow_tree(self, calculator, i = 0):
        print("\t" * i, len(self.records), "records here")
        print("\t" * i, "low:", self.low_risk_count, "high:", self.high_risk_count)

        # do all records have the same label?
        # if so set TreeNode.label to apply to whatever that label is

        if self.low_risk_count == 0:
            print("\t" * i, "got to a leaf Applying HR Label")
            self.label_to_apply = "High Risk"
        elif self.high_risk_count == 0:
            print("\t" * i, "got to a leaf Applying LR Label")
            self.label_to_apply = "Low Risk"
        elif len(self.pivots) == 0:
            if self.low_risk_count < self.high_risk_count:
                print("\t" * i, "got to a leaf Applying HR Label")
                self.label_to_apply = "High Risk"
            else:
                print("\t" * i, "got to a leaf Applying LR Label")
                self.label_to_apply = "Low Risk"
        else:
        # recursive step
            # 1. Find best new lambda to split on
            partitioned_data, lambda_key = self.find_best_partition(calculator)
            self.partition_logic = PIVOTS(lambda_key)
            del(PIVOTS(lambda_key))
            # 2. Remove that lambda from our children's list of future
            child1 = TreeNode(partitioned_data[0], self.records)
            child2 = TreeNode(partitioned_data[1], self.records)
            self.children.append(child1)
            self.children.append(child2)
            # 3. Make 2 children TreeNode Objects
            for child in self.children:
                self.grow_tree(calculator)
            # 4 call our method for each child