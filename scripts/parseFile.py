#! /usr/bin/python

import sys, string  # for argv function and list modifications

file = open(sys.argv[1], ‘r’)  # opens file from first argument when script run
content = file.readlines()  # reads each line into a python list w/ \n characters
file.close()

listA = []
listB = []
for i in content:  # loop uses string functions to split each entry in prior list into two peices and its own new list and then add values to their own lists based on position (0 or 1) in newly create lists while also changing them to floats
    line = string.split(i)
    listA.append(string.atof(line[0]))
    listB.append(string.atof(line[1]))

file = open(sys.argv[2], ‘w’) # opens second argument from script run to create a new file for output to be written into
for i in listA:
    file.write(i+”\n”)  # write to output file with newlines after each entry
file.close()
