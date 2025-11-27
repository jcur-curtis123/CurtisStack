class Record:
    def __init__(self, input_values, actual_label):

        '''
        as defined in assignment on canvas

        record will consider input values and an actual label

        attrs considers 1 for bias, and the remaining values are input values

        this is how input values is structured
        '''

        self.attrs = (1,) + tuple(input_values)
        self.actual_label = actual_label
        self.predicted_label = None
    