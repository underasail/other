#! /share/opt/python/3.3.1/bin/python
## /usr/bin/python3

import sys
import csv
from scipy import stats

with open(argv[1], 'r') as infcsv, open(argv[2]) as contcsv:
    infcsvReader = csv.reader(infcsv, delimiter = ' ')
    contcsvReader = csv.reader(contcsv, delimiter = ' ')
    next(infcsvReader)
    next(contcsvReader)
    for (infRow, contRow) in zip(infcsvReader, contcsvReader):
        a = infRow[1:]
        b = contRow[1:]
        ttest = stats.ttest_ind(a, b)
        print('This is the result array: (%d, %d) % ttest[0] ttest[1]')
