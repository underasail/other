#! /nethome/mct30/python/bin/python3.6

# USAGE: $_./matchedPer.py [PRIMARY SAM FILE (APHID OR BUCHNERA)] [SECNDARY SAM FILE]

from sys import argv
import csv

# argv = [0, 'C:\\Users\Thompson\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\LocalState\\rootfs\home\\underasail\\bmds\G002_Bac_Buchnera_aphidicola_all.map', 'C:\\Users\Thompson\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\LocalState\\rootfs\home\\underasail\\bmds\G002_Bac--bacteria.map']
# argv = [0, './G002_Bac_Buchnera_aphidicola_all.map', './G002_Bac--bacteria.map']

primary_matched_dict = {}
primary_unmatched_dict = {}
secondary_matched_dict = {}
secondary_unmatched_dict = {}
# dicts containing read numbers as keys with reference genomes as values

if 'G002' in argv[1]:
    totalreads = 12085742
elif 'G006' in argv[1]:
    totalreads = 21960873
elif 'BTIRed' in argv[1]:
    totalreads = 13931847

with open(argv[1], newline='') as f:
    next(f)
    next(f)
    next(f)
    # skips through header lines
    csvreader = csv.reader(f, delimiter = '\t')
    for row in csvreader:
        if len(row) >= 14 and 'XM:i:0' in str(row):
            # used to select only for allignments with no mismatches
            readnum = row[0]
            refgen = row[2]
            seq = row[9]
            # http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#sam-output
            primary_matched_dict.setdefault(readnum, []).append(refgen)
            # allows entry to be created if not and added to without disruption
            # if previously generated
        elif len(row) >= 14:
            readnum = row[0]
            refgen = row[2]
            seq = row[9]
            primary_unmatched_dict.setdefault(readnum, []).append(refgen)
            # print(str(primary_unmatched_dict[readnum][0]) + ' unmatched pri')
        else:
            pass
primary_matched_per = round((len(primary_matched_dict.keys())*100)/totalreads, 4)
    # percentage of reads that mapped to the primary genome (aphid or buchnera)
primary_unmatched_num = len(primary_unmatched_dict.keys())
    # number of reads that failed to map to primary genome
    # used to generate alternate percentage below
print('Done with primary matches')
        
with open(argv[2], newline='') as f:
    next(f)
    next(f)
    next(f)
    csvreader = csv.reader(f, delimiter = '\t')
    for row in csvreader:
        if len(row) >= 14 and 'XM:i:0' in str(row):
            readnum = row[0]
            refgen = row[2]
            seq = row[9]
            try:
                e = primary_matched_dict[readnum]
                secondary_matched_dict.setdefault(readnum, []).append(refgen)
                # print(str(secondary_matched_dict[readnum][0]) + ' matched')
            except KeyError:
                pass
            # fast checking to see if read that mapped to primary also mapped to secondary
            try:
                e = primary_unmatched_dict[readnum]
                secondary_unmatched_dict.setdefault(readnum, []).append(refgen)
                # print(str(secondary_unmatched_dict[readnum][0]) + ' unmatched')
            except KeyError:
                pass
            # see if read that failed to map to primary maps to secondary
        else:
            pass
secondary_matched_per = round((len(secondary_matched_dict.keys())*100)/totalreads, 4)
    # percentage of reads that mapped to both primary and secondary
secondary_unmatched_per_total = \
round((len(secondary_unmatched_dict.keys())*100)/totalreads, 4)
    # percentage of primarily unmatched reads that map to secondary
secondary_unmatched_per_cont = \
round((len(secondary_unmatched_dict.keys())*100)/primary_unmatched_num, 8)
    # percentage of primarily unmatched reads that map to secondary
print('Done with secondary matches')

print('%s%% of the %s reads mapped to the primary genome.' \
% (primary_matched_per, totalreads))
print('%s%% of the %s reads mapped to both the primary and the secondary genome.' \
% (secondary_matched_per, totalreads))
print('%s%% of the %s reads, that failed to map to the primary genome, \
mapped to the secondary genome.' % (secondary_unmatched_per_cont, primary_unmatched_num))
print(len(primary_matched_dict.keys()))
print(len(primary_unmatched_dict.keys()))
print(len(secondary_matched_dict.keys()))
print(len(secondary_unmatched_dict.keys()))
