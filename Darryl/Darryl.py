''' Darryl will compute matching on non-encrypted data on query
from Alice and compare'''

import argparse
import csv
import sys

# Darryl finding Alice's query in the unencrypted data
def Darryl (category, data):
    answer = list()
    csvfile = 'Heart.csv'

    # read csvfile
    with open(csvfile, newline='') as csvhandle:
        reader = csv.reader(csvhandle)
        rows = list(reader)

    header = rows[0]

    if category not in header:
        sys.stderr.write('Error: "{}" is not a valid category\n'.format(category))
        sys.exit(1)

    # get index
    catIndex = rows[0].index(category)

    rows = rows[1:]
    for row in rows:
        # append if string matches
        if row[catIndex] == str(data):
            answer.append(row)
    return answer

def parse(category, data):
    # create parser for data and category
    parser = argparse.ArgumentParser(description='Given a category and data, query with Darryl and return results')

    # parse if no input
    if not category:
        parser.add_argument('--category', help='The category to match. "valid" cannot be searched')
    if not data:
        parser.add_argument('--data', help='The data to match')
    cmdline = parser.parse_args()
    
    if not category:
        # check for category
        if cmdline.category:
            category = cmdline.category
        else:
            category = input('Enter category: ')

    if not data:
        # check for data
        data = ''
        if cmdline.data:
            data = cmdline.data
        else:
            data = input('Enter data: ')

    # prevent 'valid' from being searched as a category
    if category in ['valid']:
        sys.stderr.write('Error: "valid" cannot be searched\n')
        parser.print_help()
        sys.exit(1)

    # prevent invalid data from being searched
    try:
        float(data)
    except ValueError:
        sys.stderr.write('Error: "{}" is not a float or int\n'.format(data))
        parser.print_help()
        sys.exit(1)

    return category, data

# This is mimic Alice asking Darryl for information
def main(category=None, data=None):
    category, data = parse(category, data)

    query = Darryl(category, data)
    # return successful queries
    if not query:
        print ("No such patient exists")
    else:
        for reply in query:
            print(reply, "\n")


main()
