import random
from ParentAgent import ParentAgent

class ConformingAgent(ParentAgent):
    '''
    created ConformingAgent class, a child of ParentAgent

    __init__ constructor similar to DiverAgent class
    '''
    def __init__(self, group_str):
        super().__init__(group_str)
        self.threshold = round(random.uniform(0.5, 0.7), 2)


