#!/usr/bin/python3
import sys, csv, pprint
from roles import roles

from optparse import OptionParser

# TODO -- what if someone wins pres and vice pres? Just get last person to be elimiated from the role the person does not take


NUM_PREFERENCES = 3
NUM_VOTES = 9

def getCSVColumns(csv_filename: str) -> dict:
    try:
        with open(csv_filename, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
        
            columns = {}
            for row in csv_reader:
                for fieldname in csv_reader.fieldnames:
                    columns.setdefault(fieldname, []).append(row.get(fieldname))
                    
            columns.pop('Timestamp')
        return columns
    except Exception as e:
        raise ("Please pass in the correct filename")    

def getCSVRows(csv_filename: str) -> dict:

    with open(csv_filename, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
    
        for row in csv_reader:
           row.pop("Timestamp")
                
    
    return csv_reader    

def tuple_insert(tup,pos,ele) -> tuple:
    tup = tup[:pos]+(ele,)+tup[pos:]
    return tup

def generateInitialVotes(columns) -> dict:
    '''
    each vote record is a tuple of (first, second, third) preferences
    Records are appended to the list stored at the key inside the initialVotes dictionary 
    ie

    initialVotes = {
        'pres' : [
                    (Jelinna, Roary, Ian)
                    (Roary, Jelinna, Xavier)
                    ...
                ]
        'vice-pres' : [
                (Roary, Jelinna, Ian)
                (Roary, Jelinna, Xavier)
                ...
            ]
        ...
    }
    '''
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
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename",
                      help="read csv voting data from FILENAME")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")

    (options, args) = parser.parse_args()


    if options.verbose:
        print("reading %s..." % options.filename)

    if not options.filename:
        parser.error("Please profide filename!")
        sys.exit(2)
    else:
        csv_filename = options.filename.strip()
        columns = getCSVColumns(csv_filename)

        initialVotes = generateInitialVotes(columns)
    
        pp = pprint.PrettyPrinter()
        pp.pprint(initialVotes)
    #TODO 
    #  - unique list of applicants - with list of roles
    # ie {
    #     "Ian" : ["Vp", "pres", "secretary"]
    # }



