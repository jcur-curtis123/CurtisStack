class CountyData:
    def __init__(self, name):
        self.name = name
        self.fmr = None
        self.wage = None
        self.income = None

    def complete(self):

        '''
        return fmr, wage, and income values if they are not None

        since self.fmr, self.wage, and self.income are loaded via csv 

        we need a method to validate that these values exist ie; not none
        '''
        return (
            self.fmr is not None and
            self.wage is not None and
            self.income is not None
        )
    
    def compute_features(self):
        '''
        Convert county economic attributes into a numeric vector for clustering

        features are needed for matrix building 

        Integer or float type for features as division error will occur

        '''
        return [
            float(self.fmr),
            float(self.wage),
            float(self.income)
        ]