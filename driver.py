import csv
from blend import Blend, BlendLinkedList
from warehouse import Warehouse
from strategies import Strategy
from bean_minimization import MinimizeEthiopia, MinimizeHonduras, MinimizeRwanda


def read_in_resources(filename):
    '''
    read in the resources.csv for all quantities of beans

    column headers should be specific to 'Origin' and 'Quantity' 

    quantites are stored as value under 'Quantity' 

    upon opening the file, quantities is initalized to an empty dictionary

    {Ethiopia: 10000, Honduras: 15000, Rwanda: 7000} is the desired output of quantities
    '''

    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        quantities = {}

        for row in reader:

            '''
            for each row - clean text via removing utf-8 BOM

            rebuild each row post-processing

            the cleaned elements in the csv are returned as a warehouse object

            this is needed for the strategy portion
            '''
            clean_row = {}
            for k, v in row.items():
                clean_key = k.strip().replace('\ufeff', '') # remove whitespace/utf-8 BOM
                clean_value = v.strip()
                clean_row[clean_key] = clean_value
            
            origin = clean_row['Origin'].strip() # extract bean name, quantities post-processing
            quantity = float(row['Quantity'])
            quantities[origin] = quantity

    ethiopia = quantities["Ethiopia"]
    honduras = quantities["Honduras"]
    rwanda = quantities["Rwanda"]

    return Warehouse(ethiopia, honduras, rwanda)

def read_in_recipes(filename):

    '''
    read_in_recipes reads the recipe blend file and conducts data preprocessing for cleaning the .csv

    this allows for accurate importing of the blends and total bean quantities

    for each row in the .csv - assign bean quantities to floats

    return blends as instance of Blend class

    blend_list is an instance of the BlendLinkedList - accurate data for linked list
    
    '''

    blend_list = BlendLinkedList()

    with open(filename, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"].strip() # remove header whitespace
            ethiopia = float(row["Ethiopia"]) # convert bean quantity to float
            honduras = float(row["Honduras"])
            rwanda = float(row["Rwanda"]) 
            price = float(row["Price/lb"].replace("$", "").strip())

            blend = Blend(name, ethiopia, honduras, rwanda, price) # object of Blend class
            blend_list.append(blend) # append the post-processed blends to the blend_list

    return blend_list


def main():

    '''
    assign variables for reading in resources and recipes

    the greedy_strategy will take these as parameters

    formatting as linkedlist and warehouse objects are completed

    '''

    warehouse = read_in_resources("/Users/jacobcurtis/Desktop/Low Waste Strategies /input/resources.csv")

    blend_list = read_in_recipes("/Users/jacobcurtis/Desktop/Low Waste Strategies /input/blends.csv")

    # give user option to pick desired strategy
    print("Select a strategy:")
    print("1. Maxmimize Income")
    print("2. Minimize Ethiopia")
    print("3. Minimize Honduras")
    print("4. Minimize Rwanda")

    # user will enter their option per strategy
    option = input("Option: 1, 2, 3, 4")

    if option == "1":
        strategy = Strategy(warehouse, blend_list)
        strategy.greedy_strategy()
    elif option == "2":
        strategy = MinimizeEthiopia(warehouse, blend_list)
        strategy.driver()
    elif option == "3":
        strategy = MinimizeHonduras(warehouse, blend_list)
        strategy.driver()
    elif option == "4":
        strategy = MinimizeRwanda(warehouse, blend_list)
        strategy.driver()
    else:
        print("Invalid input")

if __name__ == "__main__":
    main()


