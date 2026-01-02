from loaders import FMRLoader, WageLoader, IncomeLoader

class LoaderFactory:
    '''
    A part of this assignment required students to implement a object oriented

    concept from refactoring guru. I chose the factoring method to implement, where it made sense consider loaders for certain pieces of information

    Here, create() considers string keys for creating associated class objects

    see https://refactoring.guru/design-patterns/factory-method for factory method
    '''
    def create(self, loader_type):
        if loader_type == "fmr":
            return FMRLoader()
        if loader_type == "wage":
            return WageLoader()
        if loader_type == "income":
            return IncomeLoader()

