import csv
from dataloader import DataLoader

'''
loaders.py considers all types of loaders; FMR, Wage and Income

Each loader will load the county column - and each county's FMR, Wage, and Income values 
'''

class FMRLoader:
    '''
    FMRLoader opens given filepath 

    County and it's values are formatted - county values should be floats
    '''
    def load(self, path, store):
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                county = store.get(row["County"])
                county.fmr = float(row["FMR_2BR"])

class WageLoader:
    def load(self, path, store):
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                county = store.get(row["County"])
                county.wage = float(row["Average Weekly Wage"])

class IncomeLoader:

    '''
    IncomeLoader is a type of loader similar to that of Wage and FMR
    
    Other than the encoding = "utf-8-sig" which deletes BOM in the first header within my csv
    '''

    def load(self, path, store):
        with open(path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                county_name = row["County"].strip()  
                value = row["Value"].replace(",", "").strip()
                if value.isdigit():
                    county = store.get(county_name) # locate county_name is key here in counties dict
                    county.income = float(value) # save county income as float
