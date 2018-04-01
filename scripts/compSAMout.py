#! /share/opt/python/3.3.1/bin/python

# Usage: ./compSAMout.py [PARSED BUCHNERA FILE] [PARSED OTHER BACTERIA FILE] > output

from sys import argv
import csv

seqdict = {}
GIdict = {}
i = 1
buch_list = []
j = 1
other_list = []
zero = [0, 0, 0]

with open(argv[1], newline = '') as f_buchnera, open(argv[2], newline = '') as f_other:
    buch_csv = csv.reader(f_buchnera, delimiter = '\t')
    other_csv = csv.reader(f_other, delimiter = '\t')
    buch_header = next(buch_csv)
    other_header = next(other_csv)
    buch_len = int(buch_header[0])
    other_len = int(other_header[0])
        
    while i <= buch_len:
        buch_row = next(buch_csv)
        if int(buch_row[0]) == i:
            buch_list.append(buch_row)
        elif int(buch_row[0]) < i:
            buch_list.append(buch_row)
            i = i - 1
        else:
            while i != int(buch_row[0]):
                buch_list.append(zero)
                i = i + 1
            buch_list.append(buch_row)
        i = i + 1
    print('buch_list done'+buch_list[:10]+buch_list[-10:])
    while j <= other_len:
        other_row = next(other_csv)
        if int(other_row[0]) == j:
            other_list.append(other_row)
        elif int(other_row[0]) < i:
            buch_list.append(buch_row)
            j = j - 1
        else:
            while j != int(other_row[0]):
                other_list.append(zero)
                j = j + 1
            other_list.append(other_row)
        j = j + 1
print('other_list done'+other_list[:10]+other_list[-10:])
for (buch_list_row, other_list_row) in zip(buch_list, other_list):
    if buch_list_row[0] == other_list_row[0] and buch_list_row[0] != 0:
        print(buch_list_row[0]+' matches '+other_list_row[0])
        seqdict.setdefault(buch_list_row[0], []).append(other_list_row[2])
        GIdict.setdefault(buch_list_row[0], []).append(other_list_row[1])
                
print(GIdict)
print(seqdict)
