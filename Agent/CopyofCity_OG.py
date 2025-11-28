import random 
from diverse import DiverseAgent
from conform import ConformingAgent




'''
import class Agent from Agent.py

import random from Python's random class

importing class Agent is cruicial as Agent must interact with city

see simulate() for is_satisfied() agent implementation 
'''
class City:
    def __init__(self, width, height, rounds):
        self.width = width
        self.height = height
        self.rounds = rounds
        self.grid = []
        self.set_up() # attribute set_up method

    
    def set_up(self):
        '''
        set_up allows for random selection of agents to be appending in the cells in the defined x by y grid

        outer for loop assigns row to an empty list

        this allows for cells to append either an agent or None in the inner loop

        outer loop look at the number of rows vs number of columns, hence the self.height in outer loop and self.width in the inner

        if row = [] happened to be in the inner loop, this would reset the cell at every iteration
        '''
        for x in range(self.height):
            row = []
            for y in range(self.width):
                random_selection = random.choice(["X", "O", None])
                if random_selection is None:
                    row.append(None) # cell is empty, append none to the cell
                else:
                    if random_selection == "X":
                        agent = DiverseAgent("X")
                    elif random_selection == "O":
                        agent = ConformingAgent("O")
            
                    agent.city = self
                    agent.x = x
                    agent.y = y
                    row.append(agent)
            self.grid.append(row)


    def __str__(self):
        '''
        __str__ prints the city grid as a string representation

        "|" and "-|" are present in the construction of the grid   

        A output string must "store" the collective strings as a whole

        As the inner loop runs, the index of row (cell) is added with it's string

        row_ele += adds the string to var row_ele and assigns it back to the original var

        this allows for begin_str (string overall output) to assign each row_ele var on a new line after cell passes through inner loop

        __str__ allows for object to inherit City class and ignore printing each row and column "manually"
        '''
        begin_str = ""
        for row in self.grid:
            row_ele = "|"
            for cell in row:
                if cell is None:
                    row_ele += "-|"
                else:
                    row_ele += str(cell) + "|"
            begin_str += row_ele + "\n" # this is where the collective strings are "stored" as mentioned
        return begin_str
    
    def get_neighbors(self,x,y):
        '''
        get_neighbors locates all surrounding neighbors of agent at x,y from attributes

        range(x-1, x+2) produces [x-1, x, x+1]

        range(y-1, y+2) produces [y-1, y, y+1] 

        where x is the row and y is the column

        height and width are set with boundaries

        append cells that are neighbors in the neighbors list

        '''
        neighbors = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (0 <= i < self.height) and (0 <= j < self.width):
                    if not (i == x and j == y):
                        neighbors.append((self.grid[i][j])) # append all surrounding neighbors to neighbors list
        return neighbors

    def move_agent(self,x,y):
        '''
        move_agent allows for agent to be moved from a given cell to an empty cell

        if the cell is empty, append this to the empty_cells

        if empty_cells exist, choose at random, to assign new cells

        if agent moved from cell, that cell is now empty via self.grid[x][y] = None

        self.grid[new_x][new_y] = self.grid[x][y] is the assignment of the new cell post movement
        '''

        
        empty_cells = []

        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] is None:
                    empty_cells.append((i,j))
        
        if empty_cells: # all empty cells
            new_x, new_y = random.choice(empty_cells)
            self.grid[new_x][new_y] = self.grid[x][y] # set new cells to current cells (where agent is currently)
            self.grid[x][y] = None # set cell to none after leaving 
    
    '''
    simulate() simulates methods of moving of agents if in the defined list, unsatisfied_agents

    agents are defined as cells via self.grid[i][j]

    if the agent is not None, meaning if there exists an agent, and it is unsatifsfied, append to unsatisfied list

    from the list, move agents that are unsatisfied to a random cell - given from the move_agent method
    '''
    '''
    def simulate(self):
        
        for round_num in range(self.rounds):
            unsatisfied_agents = []
            for i in range(self.height):
                for j in range(self.width):
                    agent = self.grid[i][j]
                    if agent is not None:
                        if not agent.is_satisfied(self.get_neighbors(i,j)): # if the agent is not satisfied with neighbors
                            unsatisfied_agents.append((i,j)) #add to unsatisfied_agents list
            
            for i,j in unsatisfied_agents:
                self.move_agent(i,j) # move all unsatisfied agents to random location on grid
            print(self)
''' 

def update_simulate(simulations=1000, width=5, height=5, rounds=100):
    stabilized_rounds = []
    '''
    update_simulate is utilized for the analysis portion of the report

    where stabilized_rounds is initialized as an empty list, and once agents satisfied, append to the list

    do this for however many rounds exist

    n_simulations is fixed at 1000 and each simulation has 100 rounds

    the overall stabaiization is calculated after the 1000 simulation completes

    if the agent is stabilized, append this round into stabilized_rounds

    continue to move agents that are not satisfied

    round_num is a created var from the next for loop, and loops within range of rounds set in attribute
    '''
    for i in range(simulations):
        city = City(width, height, rounds) # city is an object and instance of class City
        for round_num in range(city.rounds):
            unsatisfied_agents = [] # initialize the unsatisifed_agents list
            for i in range(city.height):
                for j in range(city.width):
                    agent = city.grid[i][j] # define the agent as cell from city.grid - established by nested for loop
                    if agent is not None:
                        if not agent.is_satisfied(city.get_neighbors(i, j)): 
                            unsatisfied_agents.append((i, j))
            
            if not unsatisfied_agents:
                stabilized_rounds.append(round_num + 1)
            
            for i, j in unsatisfied_agents:
                city.move_agent(i, j) # move the unsatisfied agent

    frequency = len(stabilized_rounds) / simulations # calculate the frequency of stabilization across all simulations
    average_round = sum(stabilized_rounds) / len(stabilized_rounds) # calculate the average round that stablization occurs

    return frequency, average_round

'''
assign object city_test as an instance from City class

print the object 

run the simulations via city_test.simulate

'''

if __name__ == "__main__":
    city_test = City(5, 5, 10)
    print(city_test)
    freq, avg_round = update_simulate()
    print(f"Stabilization frequency", freq)
    print(f"Average round where agents stabilized", avg_round)


