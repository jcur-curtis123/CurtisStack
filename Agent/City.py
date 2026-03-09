import random 
from Agent import Agent


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

    '''
    set_up allows for random selection of agents to be appending in the cells in the defined x by y grid

    outer for loop assigns row to an empty list

    this allows for cells to append either an agent or None in the inner loop

    outer loop look at the number of rows vs number of columns, hence the self.height in outer loop and self.width in the inner

    if row = [] happened to be in the inner loop, this would reset the cell at every iteration

    * for creative portion of this assignment, agent is defined with random_selection *
    '''
    def set_up(self):

        for x in range(self.height):
            row = []
            for y in range(self.width):
                random_selection = random.choice(["X", "O", None])
                if random_selection is None:
                    row.append(None) # cell is empty, append none to the cell
                else:
                    agent = (Agent(random_selection)) 
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
            for j in range(y-1, y+2): # this is where bounds are set for entire grid
                if (0 <= i < self.height) and (0 <= j < self.width):
                    if not (i == x and j == y):
                        neighbors.append((self.grid[i][j])) # append all surrounding neighbors to neighbors list
        return neighbors

    def move_agent(self, agent, new_x, new_y):
        '''
        move_agent was adjusted due to the removal of the random.choice

        in this creative portion of the assignment, agents are moved based on a scoring metric

        this give optionality for agents to make decisions
    
        agent.x and agent.y is the attribute from the Agent object

        self.grid assigns the agent.x and agent.y (agent cell location) to empty

        agents are moved to the new x,y cell
        '''

        self.grid[agent.x][agent.y] = None # must set cell that agent is in to empty before moving
       
        agent.x = new_x
        agent.y = new_y
        self.agent = agent

        self.grid[new_x][new_y] = agent 
        
    def get_empty_cells(self):
        '''
        added this method for update_move_agent in Agent.py. When is_satisfied bug was fixed, this caused an error in the update_move_agent method. 
    
        this is a simple method that just takes all empty cells in our grid and appends to a list called empty

        get_empty_cells is used and assigned to a var in update_move_agent, this way, the choose_neighbor method can use empty cells as a potential neighbor
        '''
        empty = []
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] is None:
                    empty.append((i, j))
        return empty # return the empty list post iteration

    def simulate(self):
        '''
        simulate() simulates methods of moving of agents if in the defined list, unsatisfied_agents

        agents are defined as cells via self.grid[i][j]

        if the agent is not None, meaning if there exists an agent, and it is unsatifsfied, append to unsatisfied list

        from the list, move agents that are unsatisfied to a random cell - given from the move_agent method
        '''
        
        for round_num in range(self.rounds):
            unsatisfied_agents = []
            for i in range(self.height):
                for j in range(self.width):
                    agent = self.grid[i][j]
                    if agent is not None:
                        neighbors = self.get_neighbors(i, j)
                        if not agent.is_satisfied(neighbors): # if the agent is not satisfied with neighbors
                            unsatisfied_agents.append((agent)) # add to unsatisfied_agents list
            
            for agent in unsatisfied_agents:
                agent.update_move_agent() # move all unsatisfied agents to best_spot given best_score
            print(self)

    
    '''
    assign object city_test as an instance from City class

    print the object 

    run the simulations via city_test.simulate
    '''

if __name__ == "__main__":
    city_test = City(5, 5, 10)
    print(city_test)
    city_test.simulate()



