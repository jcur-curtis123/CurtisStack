import numpy as np
import pandas as pd

class Perceptron_DF:

    def __init__(self, weights):
        '''
        reassign weights to a np array with float as data type

        this will be useful in calculating the prediction labels
        '''
        self.weights = np.array(weights, float)

    '''
    add a column for bias 

    similar to that in utils, we add a bias column for further prediction calculation

    oo verison was (1,) + tuple(input_values) 

    the entire bias column is all 1's, and this is set in the beginning of our matrix
    '''
    def bias(dataframe):
        df = dataframe.copy()
        df.insert(0, "bias", 1)
        return df

    '''
    Now for the implementation of predict considerng DF -

    essentially want to compute weighted_sum similar to that of oo version
    '''

    def predict(self, X_Vector):
        
        # product is attrs values time self.weights
        product = X_Vector * self.weights


        activation_list = []

        '''
        np.add.reduce (dot product) allows for addition of row in matrix post multiplication
        '''
        for i in range(len(product)):
            result = np.add.reduce(product[i])
            activation_list.append(result)
        
        '''
        if our activation value in the list is greater than 0, this is a predict label of 1

        else, this is a zero. 
        
        Now we have a list of all prediction label values, SWEET!
        '''
        prediction_values = []

        for item in activation_list:
            if item > 0:
                prediction_values.append(1)
            else:
                prediction_values.append(0)
        
        return prediction_values
    
    '''
    To replicate that of our perceptron_oo, I must include update(), and train_model

    def update(), updates weights given error - the "behind the scenes" of our model training
    '''

    def update(self, x_row, actual, predicted_label):
        error = actual - predicted_label
        self.weights += error * x_row

    def train_model(self, X, y, iterations):

        '''
        train the model in a df version

        I must utilize a for loop to extract prediction labels and calcluate 

        accuracy scores. Param X_vector is the input values, y is the label vector

        '''

        scores = []
        for i in range(iterations):
           
            # set predictions from our defined predict function 
            predictions = self.predict(X)
            
            # Compute accuracy score - similar logic to score in perceptron_oo but using DF y_test 
            # calculate accuracy 
            # append this to scores list to keep track
            correct = sum(predictions[i] == y[i] for i in range(len(y)))
            scores.append(correct / len(y))

            for i in range(len(y)):
                if predictions[i] == y[i]:
                    correct += 1
                # if prediction does not equal y[i] update our weights to improve our model
                else:
                    self.update(X[i], y[i], predictions[i])
    
        return scores