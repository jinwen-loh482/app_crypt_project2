''' Carol will compute matching on encrypted data on query
from Alice and compare'''
import argparse
import copy
import csv
import math
import pandas as pd
import phe.encoding
from phe import paillier
import pickle
import random

random.seed(2222)

def randomize():
    pos_or_neg = 1 if random.random() < 0.5 else -1
    return random.randint(0, 10000000000)*pos_or_neg

def get_rows(pklfile):
    # get csv as dataframe
    df = pd.read_pickle(pklfile)
    df = df.dropna()
    header = df.columns
    rows = df.to_numpy()
   
    return header, rows

def compute_matching(header, rows, category, data):
    # get index to apply to
    catIndex = header.get_loc(category)

    # apply subtracting method to identify matching row
    for i in range(0, len(rows)):
        catcell = rows[i][catIndex]

        # subtract to extract correct answer
        temp = catcell - int(data)
        
        # multiply by random number to hide values (also ruins the 'valid' cell)
        rows[i] = [temp*randomize() + cell for cell in rows[i]]
    
    return rows, header

# Carol finding Alice's query in the encrypted data without leaking any additional info to Alice
def Carol (category, data):
    header, rows = get_rows('encrypted.pickle')
    return compute_matching(header, rows, category, data)
            
# This is mimic Alice asking Carol for information
def main():
    parser = argparse.ArgumentParser(description='Given a category and data, query with carol and return results as encrypted_carol.pickle')
    parser.add_argument('--category', help='The category to match')
    parser.add_argument('--data', help='The data to match')
    cmdline = parser.parse_args()
    category = ""
    if cmdline.category:
    	category = cmdline.category
    else:
    	category = input("Enter category: ")
    
    data = ""
    if cmdline.data:
    	data = cmdline.data
    else:
    	data = input("Enter data: ")

    rows, header = Carol(category, data)
    
    # write to file
    mydf = pd.DataFrame(rows, columns=header)
    pd.to_pickle(mydf, 'encrypted_carol.pickle')

if __name__ == "__main__":
    main()
