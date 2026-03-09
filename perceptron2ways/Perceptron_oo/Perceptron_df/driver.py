import pandas as pd
import numpy as np
from perceptron_df import Perceptron_DF
from utils.utils import make_df_records, add_bias


def df_run_training(iterations, df):

    # split df into X and y - see timing.compare for similar implementation
    # this is for training labels, test labels must have the same replacement
    # headers were giving me an issue - this is the reason for the included index-location-base selection
    X = df.iloc[:, :-1].astype(float).to_numpy()
    y = df.iloc[:, -1].replace({"Rock":1, "Mine":0}).astype(int).to_numpy()

    # assign model directly from Perceptron_DF object
    # weights will be a series of 1's here for testing and training purposes
    model = Perceptron_DF(weights=[1]*61)

    # calculate the scores for df's version of train model
    # scores should be a list of how many correct/len(y)
    scores = model.train_model(X, y, iterations)

    print(f"Final DF training accuracy after {iterations} iterations: {scores[-1]}")
    return model

def main():

    # Load training CSV
    train_df = pd.read_csv("/Users/jacobcurtis/Desktop/DS 5010 Perceptrons/Perceptron_oo/Perceptron_df/data/sonar_training.csv", header=None, skiprows=1)
    
    # Add bias column
    train_df = Perceptron_DF.bias(train_df)


    # Load test CSV
    test_df = pd.read_csv("/Users/jacobcurtis/Desktop/DS 5010 Perceptrons/Perceptron_oo/Perceptron_df/data/sonar_test.csv", header=None, skiprows=1)
    
    # Add bias column
    test_df = Perceptron_DF.bias(test_df)
    print(test_df)

    iterations = 1000

    # Model training using prior function
    trained_model = df_run_training(iterations, train_df)

    # split df into X and y using iloc (index-location-base selection) - see timing.compare for similar implementation
    X_test = test_df.iloc[:, :-1].astype(float).to_numpy()
    y_test = test_df.iloc[:, -1].replace({"Rock":1, "Mine":0}).astype(int).to_numpy()

    # calculate prediction labels for the purpose of accuracy score
    predictions = trained_model.predict(X_test)

    # Compute accuracy score - similar logic to score in perceptron_oo but using DF y_test 
    correct = sum(predictions[i] == y_test[i] for i in range(len(y_test)))
    test_accuracy = correct / len(y_test)

    print(f"Test accuracy after {iterations} training iterations: {test_accuracy}")


if __name__ == "__main__":
    main()
