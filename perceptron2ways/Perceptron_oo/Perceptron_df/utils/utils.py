import csv
import matplotlib.pyplot as plt
import pandas as pd

from record import Record

def plot_scores(scores, num_iterations):
    """
    Param scores: list of floats representing a series of scores (between 0 and 1) that indicate how accurate our model was
    Param num_iterations: int representing how many iterations of training we performed

    Uses matplotlib to generate a line graph to view how the model improves over time.
    """
    x_axis = range(1, num_iterations+1)
    plt.plot(x_axis, scores)
    plt.xlabel("iteration_number")
    plt.ylabel("score")
    plt.show()

# code to process reading in a file and creating a Record object


def _get_class(row):
    """
    sonar.csv stores a class as 1 of 2 strings: "Mine" or "Rock".  This function converts it to an int
    
    Param row: dict representing a single row of our csv.
    Returns: either 0 or 1 if Class is correctly formatted.  Raises exception if data is invalid
    """
    if row['Class'] == "Mine":
        return 0
    elif row['Class'] == "Rock":
        return 1
    raise TypeError("Class " + row["Class"] + " is invalid.  Must be either `Mine` or `Rock`")
    
def _generate_attrs(row):
    return tuple([float(value) for key, value in row.items() if key != "Class"])

def _make_record(row):
    attrs = _generate_attrs(row)
    actual_label = _get_class(row)
    return Record(attrs, actual_label)

# call this function to create a list of Record objects
def make_records(filepath): 
   with open(filepath, newline='', mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        records = []
        for row in reader:
            records.append(_make_record(row))
        return records  

'''
Presented below is my edition for utils.py for the purpose of DF implementation
'''

'''
required for DF version of perceptron to make df records, and add bias

read csv as pd, and return this dataframe to be used in driver.py
'''
def make_df_records(filepath):
    df = pd.read_csv(filepath)
    return df

'''
add a column for bias 
'''
def add_bias(df):
    df = df.copy()
    df.insert(0, "bias", 1)
    return df
