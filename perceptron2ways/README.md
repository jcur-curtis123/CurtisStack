# Perceptron Assignment – Part 8 Results

## 1. How many iterations did you decide to train your model on?

I decided to train my model with 1000 iterations as this provided the highest accuracy overall. I have created a list of iterations values, and I iterated over the iterations to determine the highest accuracy score. Thus, the best_model or highest score was chosen.

## 2. What was the result of predicting and scoring sonar_test.csv?

After training the perceptron on the sonar training data and evaluating it on sonar_test.csv, the model achieved a test accuracy of approximately 0.673

## 3. When training our perceptron with different magnitudes of iterations, what happened as the number increased?

As the number increased, the accuracy score increased. The increase mostly occured from iteration 100 - 500, however, after the 500th iteration, the model stabilized. 


## 4.  Add in our time profiling context manager to both implementations.  What's the average time for a run using the OO implementation over 100 runs?  What about for the dataframe implementation?  One would assume the df version is faster but, how much faster?  What methods get the most out of being vectored and what doesn't?

Over 100 runs - the average time is 0.0074 in seconds for the Object Oriented version of Perceptron. 

The dataframe implementation is 0.0046 seconds. 

The dataframe implementation is ~50% faster. 

The predict method gets the most out of being vectored as matrix operations are existent for entire rows by a weight vector. The update does not get the most as it still has to update weights one at a time. 
