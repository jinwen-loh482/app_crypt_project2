''' Carol will compute matching on encrypted data on query
from Alice and compare'''
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import pickle
import csv
import numpy as np
import copy

# compute bitwise XOR without encryption
def bxor(a, b):
    return a + b - 2*a*b

# compute bitwise OR without encryption
def bor(a, b):
    return a + b - a*b

# compute xor
def xor(temp, data):
    # calculate bitstrings
    tempbits = '{0:032b}'.format(temp)
    tempdata = '{0:032b}'.format(data)
    tempbits = [int(i) for i in tempbits]
    tempdata = [int(i) for i in tempdata]
    t = 0

    # XOR two bitstrings and OR the results together
    for i,j in zip(tempbits, tempdata):
        t = bor(bxor(i, j), t)
    return t
    

# Carol finding Alice's query in the encrypted data without leaking any additional info to Alice
def Carol (category, data):
    rows = list()
    results = list()

    # retrieve public key
    publickey = 'public.pk'
    context = 'context.con'
    HE_Cloud = Pyfhel()
    HE_Cloud.restoreContext(context)
    HE_Cloud.restorepublicKey(publickey)

    # read csv into lists
    with open('heart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    # get index to apply to
    catIndex = rows[0].index(category)


    # apply xor method to zero out rows that do not match
    rows = rows[1:]
    for i in range(0, len(rows)):
        temp = 1 - xor(int(rows[i][catIndex]), data)
        rows[i] = [int(cell)*temp for cell in rows[i]]

    # filter zero'd out answers
    for row in rows:
        if not all([int(cell) == 0 for cell in row]):
            results.append(row)
    
    return results
        
    
            
# This is mimic Alice asking Carol for information
def main(category, data):
    query = Carol(category, data)
    if not query:
        print ("No such patient exists")
    else:
        for reply in query:
            print(reply, "\n")


main('age', 63)
