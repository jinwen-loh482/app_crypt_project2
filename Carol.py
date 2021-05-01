''' Carol will compute matching on encrypted data on query
from Alice and compare'''
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import csv
import random
import pickle
import phe.encoding
from phe import paillier
import math
import copy

random.seed(2222)

def randomize():
    pos_or_neg = 1 if random.random() < 0.5 else -1
    return random.randint(0, 100000000)*pos_or_neg

# Carol finding Alice's query in the encrypted data without leaking any additional info to Alice
def Carol (category, data):
    rows = list()
    results = list()

    with open('pubkey.pickle', 'rb') as handle:
        pubkey = pickle.load(handle)
    with open('prikey.pickle', 'rb') as handle:
        prikey = pickle.load(handle)

    # read csv into lists
    with open('heart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    # get index to apply to
    catIndex = rows[0].index(category)
    
    # calculate bitstrings
    pdata = pubkey.encrypt(data)

    # apply xor method to zero out rows that do not match
    rows = rows[1:]
    for i in range(0, len(rows)):
        # get encrypted row
        rows[i] = [pubkey.encrypt(int(cell)) for cell in rows[i]]
        
        pcell = rows[i][catIndex]

        # subtract to extract correct answer
        temp = pcell - pdata
        
        # multiply by random number to hide values
        rows[i] = [temp*randomize() + cell for cell in rows[i]]

        # decrypt row
        rows[i] = [prikey.decrypt(cell) for cell in rows[i]]

    # filter garbage answers
    for row in rows:
        if int(row[catIndex]) == data:
            results.append(row)
    
    return results
        
def gen_keys():
    pubkey, prikey = paillier.generate_paillier_keypair()
    with open('pubkey.pickle', 'wb') as handle:
        pickle.dump(pubkey, handle)
    with open('prikey.pickle', 'wb') as handle:
        pickle.dump(prikey, handle)
            
# This is mimic Alice asking Carol for information
def main(category, data):
    query = Carol(category, data)
    if not query:
        print ("No such patient exists")
    else:
        for reply in query:
            print(reply, "\n")

gen_keys()
main('age', 63)
