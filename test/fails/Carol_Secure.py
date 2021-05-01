''' Carol will compute matching on encrypted data on query
from Alice and compare'''
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import pickle
import csv
import numpy as np
import copy

# compute bitwise XOR without encryption
def bxor(HE, a, b):
    temp1 = HE.add(a, b, in_new_ctxt=True)
    temp2 = HE.multiply(a, b, in_new_ctxt=True)
    temp2 = HE.add(temp2, temp2)
    return HE.sub(temp1, temp2)

# compute bitwise OR without encryption
def bor(HE, a, b):
    temp1 = HE.add(a, b, in_new_ctxt=True)
    temp2 = HE.multiply(a, b, in_new_ctxt=True)
    return HE.sub(temp1, temp2)

# compute xor
def xor(HE, temp, data):
    t = HE.encryptInt(0)
    # XOR two bitstrings and bOR the results together
    for i,j in zip(temp, data):
        t = bor(HE, bxor(HE, i, j), t)
    return t
    

# Carol finding Alice's query in the encrypted data without leaking any additional info to Alice
def Carol (category, data):
    rows = list()
    results = list()
    publickey = 'public.pk'
    secretkey = 'private.sk'
    context = 'context.con'

    # retrieve public key
    HE = Pyfhel()
    HE.restoreContext(context)
    HE.restorepublicKey(publickey)
    HE.restoresecretKey(secretkey)

    # read csv into lists
    with open('heart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    # get index to apply to
    catIndex = rows[0].index(category)
    pdata = '{0:010b}'.format(data)
    pdata = [HE.encryptInt(int(i)) for i in pdata]

    # apply xor method to zero out rows that do not match
    rows = rows[1:]
    for i in range(0, len(rows)):
        pcell = int(rows[i][catIndex])
        pcell = '{0:010b}'.format(pcell)
        pcell = [HE.encryptInt(int(i)) for i in pcell]
        temp = HE.sub(HE.encryptInt(1), xor(HE, pcell, pdata), in_new_ctxt=True)
        rows[i] = [HE.decryptInt(HE.multiply(HE.encryptInt(int(cell)), temp, in_new_ctxt=True)) for cell in rows[i]]

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


main('age', 42)
