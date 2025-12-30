from ParentAgent import ParentAgent
import random


class DiverseAgent(ParentAgent):
    def __init__(self, group_str):
        super().__init__(group_str)
        self.threshold = round(random.uniform(0.1, 0.3),2)