''' Darryl will compute matching on non-encrypted data on query
from Alice and compare'''

import csv

# Darryl finding Alice's query in the unencrypted data
def Darryl (category, data):
    with open('heart.csv', newline='') as csvfile:
        file = csv.DictReader(csvfile)
        answer = []
        for row in file:
            if row[category] == str(data):
                answer.append(list(row.items()))
        return answer
            
# This is mimic Alice asking Darryl for information
def main(category, data):
    query = Darryl(category, data)
    if not query:
        print ("No such patient exists")
    else:
        for reply in query:
            print(reply, "\n")


main('age', 63)
