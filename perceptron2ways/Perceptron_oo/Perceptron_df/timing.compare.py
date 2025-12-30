from timer import Timer
from perceptron import Perceptron
from perceptron_df import Perceptron_DF
from utils.utils import make_records
import pandas as pd
import numpy as np


def time_oo(training_records, iterations=20):
    
    '''
    For the purpose of timing perceptron_oo we need to assign weights, a perceptron object, and train the model

    weights will be a series of 1's for this, similar to our original train_model
    '''

    weights = [1] * 61
    model = Perceptron(weights)

    # use of context manager for OO
    with Timer() as time:
        model.train_model(training_records, iterations)

    print(f"OO time: {time.elapsed} seconds")

def time_df(df, iterations=20):

    '''
    similar to the oo verison, lets do the same for df

    this will look a little different as we dont need a perceptron object to run the model

    we can just run directly using Perceptron_DF
    '''

    weights = [1] * 61
    model = Perceptron_DF(weights)

    # Split the DF in a X, y format for our perceptron DF version
    # index-location-base selection is useful for this - I only want columns that are not labels
    # for float conversion purposes
    # also headers were giving me trouble within train_model
    X = df.iloc[:, :-1].astype(float).to_numpy()
    y = df.iloc[:, -1].replace({"Rock": 1, "Mine": 0}).astype(int).to_numpy() # needed to fix Rock and Mine as this is string in last column

    # use of context manager for DF
    with Timer() as time:
        model.train_model(X, y, iterations)

    print(f"DF time: {time.elapsed} seconds")

def main():

    '''
    maim() runs the overall comparison from time_oo and time_df

    read in csv for training records for our oo edition, a df for the vectorized df refactor
    '''

    print("Timing OO version:")
    # create training records for the purpose of timing of iterations
    training_records = make_records("/Users/jacobcurtis/Desktop/DS 5010 Perceptrons/Perceptron_oo/data/sonar_training.csv")

    # lets do 100 runs for timing purposes
    for i in range(100):
        time_oo(training_records)

    print("Timing DF version:")
    df = pd.read_csv("/Users/jacobcurtis/Desktop/DS 5010 Perceptrons/Perceptron_oo/Perceptron_df/data/sonar_training.csv", header=None, skiprows=1)
    df.insert(0, "bias", 1) # insert bias manually here, needs to be consistent to perceptron_oo

    # lets do 100 runs for timing purposes
    for i in range(100):
        time_df(df)


if __name__ == "__main__":
    main()
