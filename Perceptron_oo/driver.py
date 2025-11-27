from perceptron import Perceptron
from utils.utils import make_records, plot_scores


def run_oo_training(iterations, training_data):

    '''
    run_oo_training similar to that of df_training manages the scoring and training of our model for

    the purpose of the driver
    
    The driver is used to utilize record.py and perceptron.py - this will "drive" the model training

    weights are a series of 1's here for the purpose of model training
    '''

    weights = [1] * 61

    model = Perceptron(weights)

    scores = model.train_model(training_data, iterations)

    print(f"Final training accuracy after {iterations} iterations: {scores[-1]}")
    plot_scores(scores, iterations)

    return model, scores[-1] 


def main():

    '''
    Main() takes both the training and test data csv files for making test and training records

    define a iteration list for finding highest accuracy score on all iterations

    need to find best model given different sets of iterations - I've defined a list here


    '''

    training_path = "/Users/jacobcurtis/Desktop/DS 5010 Perceptrons/Perceptron_oo/data/sonar_training.csv"
    # make records from the training dataset
    training_data = make_records(training_path)

    # Iterations to test defined in a list
    iteration_list = [100, 150, 300, 500, 1000, 10000]

    trained_models = {}

    # for the purpose of iterating on multiple different instances of iterations counts
    # lets assign a list and determine the best upon scoring
    for iterations in iteration_list:
        model, score = run_oo_training(iterations, training_data)
        trained_models[iterations] = model
  

    # 1000 iterations by chice - please see README.md for further explanation
    found_best_iteration = 1000
    best_model = trained_models[found_best_iteration]

    '''
    let's create test_records similar process of creating training records
    '''
    test_path = "/Users/jacobcurtis/Desktop/DS 5010 Perceptrons/Perceptron_oo/data/sonar_test.csv"
    test_records = make_records(test_path)

    # test is only ran once to generalize how well the model is doing
    # avoids underfitting or overfitting of the model
    best_model.predict_many(test_records)
    test_score = best_model.score(test_records)

    print(f"Test accuracy after {found_best_iteration} iterations: {test_score}")


if __name__ == "__main__":
    main()
