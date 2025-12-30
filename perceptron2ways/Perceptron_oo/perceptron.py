class Perceptron:
    
    def __init__(self, weights):

        '''
        constructor takes in single param weights and is list specific
        '''

        self.weights = list(weights)

    def predict1(self, record):

        '''
        Predict the class of a single Record object.
        Uses the Record's attrs field and the weights in the Perceptron to calculate a weighted sum. Then returns 1 if that sum is greater than 0. Else 0
        param record: An object of Record 
        returns: The predicted output (0 or 1).
        '''

        attrs = record.attrs

        '''
        initalize weighted sum before iteration

        weighted sum formula E(w_i * x_i)
        '''

        weighted_sum = 0 

        for i in range(len(self.weights)):
            weighted_sum += self.weights[i] * attrs[i] # weighted sum for weight * attr

        if weighted_sum > 0:
            return 1
        else:
            return 0
    
    def predict_many(self, records):

        """
        Predict assign the predicted_label attr in each record to the result of calling predict1 
        Param records: a list of Record objects
        """

        '''
        for record items in records, define its predicted label as the value from predict_1 -

        it's classification as update_all and score rely on prediction label
        '''
        for record_item in records:
            record_item.predicted_label = self.predict1(record_item)

    def score(self, records):

        '''
        Calculates the prediction accuracy for a list of sample input/output pairs.
        param records: a list of record objects.
        returns: The predictive accuracy (proportion of correct predictions)
        '''

        predict1_correct = 0
        
        for record in records:
            if record.predicted_label == record.actual_label:
                predict1_correct += 1
        
        return predict1_correct/len(records)

    def update_single(self, record):

        """
        Updates the perceptron weights from a single sample input/output pair (stored in the Record object)
        param record: An object of record
        returns: None (mutates the weights attr)
        """

        # error is needed to update single weights for each attr
        # this allows for consistent change in direction of error
        error = record.actual_label - record.predicted_label

        for i in range(len(self.weights)):
            self.weights[i] += error * record.attrs[i]
    
    def update_all(self, records):

        '''
        Iterates through a list of records. 
        Calls update_single on any record where prediction and actual label do not match
        param records: An list of Record objects
        returns: None (mutates the weights attr)
        '''

        for record in records:
            if record.predicted_label != record.actual_label:
                self.update_single(record) # all records are updated - at each single record in records


    
    def train_model(self, records, iterations):

        '''
        Repeatedly calls predict_many, then score, then update_all for a number of iterations
        param records: An list of Record objects
        param iterations: the number of times to repeat this process
        '''
        scores = []
        for i in range(iterations): # in range of number of given iterations
            self.predict_many(records) # assign all predict_label with predict1
            score1 = self.score(records) # score each record 
            scores.append(score1) # append the score to scores

            # update all after predict_many and score
            self.update_all(records)

        return scores # list of scores is returned
