class Record:
    '''
    Record holds the __init__ constructor

    Each `Record` object will hold all the data for one patient — their attributes (like age, cholesterol, smoker status) and their label (“High Risk” or “Low Risk”).

    self.attrs is the dataset's input values (attributes from the dataset)

    self.actual_label is the label assigned to the patient's record

    record will look like:
    
    Record(
    {"Age": 14, "IsSmoker": False, "Total Cholesterol": 177},
    "Low Risk")
    '''
    def __init__(self, input_values, actual_label):
        self.attrs = input_values
        self.actual_label = actual_label
        self.predicted_label = None