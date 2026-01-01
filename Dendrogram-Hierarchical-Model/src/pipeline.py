from dataloader import DataLoader
from factory import LoaderFactory
from model import Model
from plotter import Plotter

class Pipeline:

    def __init__(self, fmr, wage, income):
        '''
        Pipeline's constructor for fmr, wage, and income data
        '''
        self.fmr = fmr
        self.wage = wage
        self.income = income

    def main(self):

        store = DataLoader()
        factory = LoaderFactory()

        '''
        In order to create specific loaders - factory is needed as each loader passes through factory

        create() is specifically from factory - which requires specific strings 

        The factory allots these loaders given these strings, and stores as Dataloader instances
        '''

        factory.create("fmr").load(self.fmr, store)
        factory.create("wage").load(self.wage, store)
        factory.create("income").load(self.income, store)

        '''
        counties are stored as usable county data instances
        '''

        counties = store.get_complete_counties()

        # Model object for building matrix 
        model = Model()

        '''
        Now that we have complete county labels, self.fmr, self.wage, and self.income

        let's construct our model
        '''
        X, labels = model.build_matrix(counties)
        X_norm = model.normalize(X)
        Z = model.cluster(X_norm)

        '''
        labels are values from counties, specifically county labels for the dendrogram- 

        Where these labels are utilized for plotting the Dendrogram

        Plotter plots the dendrogram and utilizes pythons scipy dendrogram

        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html
        '''
        labels = []
        for c in counties:
            labels.append(c.name)
        
        Plotter().plot(Z, labels)
        return labels

