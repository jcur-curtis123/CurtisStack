import csv
from src.utils.record import Record

def read_csv(filepath):
    '''
    The read_csv function allows any dataset to be opened and read for data pre-processing

    records is a list of record objects

    records are appended and stores one record object per row in the .csv

    '''
    records = []

    with open(filepath, "r", encoding="utf-8-sig") as f:
        
        reader = csv.DictReader(f)

        for row in reader:
    
        #loop through each row in the csv 

        #initialize the attrs dictionary, later will be used to edit key and values post-processing

        #then the inner for-loop allows for accessing each column in the row
    
            attrs = {}
            label = row["Assessment"].strip() # trim whitespace over target label - "High Risk" and "Low Risk"
            
            for key, value in row.items():
                clean_key = key.strip().replace("\ufeff", "") # remove BOM as Age was ufeffAge
                clean_value = value.strip()
        
               
                if clean_key != "Assessment": 
                    new_key = clean_key.replace(" ", "").lower() # skip assessment attribute, assign new_key with no white space

                # prior to this in-line set definition, I was receiving errors of attributes not recognized during normalization
                # I assumed all attrs as lowercase, and defined each set as those of boolean and int return types
                
                if new_key in {"onhypertensionmedication", "hasdiabetes", "issmoker", "isafricanamerican"}:
                    attrs[clean_key] = (clean_value.upper() == "TRUE") # all values of these attr keys are now TRUE 

                   
                elif new_key in {"age", "systolicbloodpressure", "totalcholesterol", "hdlcholesterol"}:
                    if clean_value.replace(".", "").isdigit(): # avoid str in the place of int 
                        attrs[clean_key] = int(float(clean_value)) # values of numeric attr keys must be int
                    else:
                        attrs[clean_key] = 0
                else:
                    attrs[clean_key] = clean_value

        records.append(Record(attrs, label)) # append record objects to records list w/ post-processing attrs 
    
    return records


    
def print_numeric_averages(records):
    
    '''
    predefine the set for numeric_value_keys

    this makes our for loop a little easier to build as we only care about 

    keys (attributes) that are numeric in our dataset
    '''

    numeric_value_keys = [
        "Age",
        "Systolic Blood Pressure",
        "Total Cholesterol",
        "HDL cholesterol"
    ]

    '''
    for loop to calculate the average of numeric attributes 

    total and count are initialized 

    nested for loop for record's numeric attributes - ie; Age, HDL cholesterol

    calculate the running total of each numeric key-value ie; record 1: Age 23, record 2: 54

    count is incremented for each record's numeric attribute
    '''
    for key in numeric_value_keys:
        total = 0
        count = 0
        for record in records:
            total += record.attrs[key]
            count += 1
        average = (total)/(count)
        print("Average Key Value: ", average)
    
    

