from county import CountyData

'''
Dataloader is soley for cleaning and returning a procesed

datastructure (dict) that will be used for loading csv data
'''

class DataLoader:

    '''
    child classes that inherit from this class, will have acces to cleaned version of counties
    '''
    def __init__(self):
        self.counties = {}

    def get(self, name):

        '''
        dataset will be read and get() will be used to clean variables

        clean variable is assigned to value in the key, value pair in self.counties dictionary
        '''
        clean = name.replace(" County", "").strip()
        if clean not in self.counties:
            self.counties[clean] = CountyData(clean)
        return self.counties[clean]
    
    def get_complete_counties(self):

        '''
        loop through clean values in counties and if these values pass the logic of complete() in our county.py

        let's consider these values - a good use case for validating csv files
        '''
        
        results = []
        for c in self.counties.values():
            if c.complete():
                results.append(c)
        return results