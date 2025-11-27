import json
from src.utils.file_io import read_csv, print_numeric_averages
from src.CollectiveImpurityGini import CollectiveImpurityGini
from src.CollectiveImpurityEntropy import CollectiveImpurityEntropy
from src.utils.make_partition import find_best_partition

'''
Import new find_best_parition from make_partition

CollectiveImpurityGini and Entropy calc functions

and of course our ability to read in our csv from file_io and the additional print_numeric_averages
'''

def main():
    '''
    open and load the config.json

    this is needed to satisfy our conditionals later
    '''
    with open("/Users/jacobcurtis/Desktop/DS 5010 Week 5/config/config.json") as f:
        config = json.load(f)

    '''
    load the .csv from the assignment 

    read_csv is imported from our file_io file and uses with open(filepath)
    '''
    filepath = "/Users/jacobcurtis/Desktop/DS 5010 Week 5/data/input/training_data.csv"
    records = read_csv(filepath)

    
    if config["FIND_AVERAGES"]:
        print_numeric_averages(records)

    '''
    In our config Find Averages is set to true

    This prints numeric averages of the numeric columns

    This line loops through all numeric columns
    '''

    if config["FIND_BEST_SPLIT"]:
        '''
        If the config element "FIND_BEST_SPLIT" is set to true (which is the case)

        Define the calc type - either Gini or Entropy (config is set to Gini)

        Given the best partition as it loops through all lambdas and finds each impurity
        '''
        calc_type = config["CALCULATION_TO_USE"].upper()
        strategy = CollectiveImpurityGini() if calc_type == "GINI" else CollectiveImpurityEntropy()
        find_best_partition(records, strategy)


if __name__ == "__main__":
    main()
