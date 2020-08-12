#!/usr/bin/python3
import sys, csv, getopt, pprint
from roles import roles

# TODO -- what if someone wins pres and vice pres? Just get last person to be elimiated from the role the person does not take


NUM_PREFERENCES = 3
NUM_VOTES = 9

def getCSVColumns(csv_filename: str) -> dict:

    with open(csv_filename, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
    
        columns = {}
        for row in csv_reader:
            for fieldname in csv_reader.fieldnames:
                columns.setdefault(fieldname, []).append(row.get(fieldname))
                
        columns.pop('Timestamp')
    
    return columns

def getCSVRows(csv_filename: str) -> dict:

    with open(csv_filename, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
    
        for row in csv_reader:
           row.pop("Timestamp")
                
    
    return csv_reader    

def tuple_insert(tup,pos,ele):
    tup = tup[:pos]+(ele,)+tup[pos:]
    return tup

def generateInitialVotes():
    initialVotes = {k:[] for k in roles}
    column_headings = [key for key in columns.keys()]


    for num, role in enumerate(roles):
        for j in range(NUM_VOTES):
            vote = ()
            for i in range(NUM_PREFERENCES):
                csv_col_num = num*NUM_PREFERENCES + i
                vote = tuple_insert(vote, i, columns[column_headings[csv_col_num]][j])
              
            initialVotes[role].append(vote)
    
    return initialVotes        

if __name__ == "__main__":
    # TODO: add error checking + commandline handling 
    csv_filename = sys.argv[1].strip()
    
    columns = getCSVColumns(csv_filename)

    pp = pprint.PrettyPrinter()
    initialVotes = generateInitialVotes()
 

    pp.pprint(initialVotes)

    

