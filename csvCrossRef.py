#! /usr/bin/python3

import csv

compdict = {}

with open('C:\\Users\Thompson\Downloads\\nsf-gov_researchExperienceSites_cellbiology.csv'\
, newline = '') as fone, open('C:\\Users\Thompson\Downloads\\nsf-gov_researchExperienceSites_molecularbiology.csv'\
, newline = '') as ftwo:
    onecsv = csv.reader(fone, delimiter = ',')
    twocsv = csv.reader(ftwo, delimiter = ',')
    oneheader = next(onecsv)
    twoheader = next(twocsv)
    for onerow in onecsv:
        compdict[onerow[0]] = onerow
    for tworow in twocsv:
        if tworow[0] in compdict:
            print(tworow[0])