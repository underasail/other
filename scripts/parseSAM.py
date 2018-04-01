#! /share/opt/python/3.3.1/bin/python3

# Usage: ./parseSAM.py [INPUT SAME FILE] 
# prints to stout, redirect to destination file with >

from sys import argv
import csv
from Bio import Entrez
from Bio import SeqIO


totalreads = 0
refdict = {}
refdict_seq = {}
# refdict_count = {}
# refdict_per = {}
gi_list = list()
# all_list = list()
# refdict_alltogether = {}

"""Parsing of Bowtie2 SAM Output"""
with open(argv[1], newline='') as f:
    next(f)
    next(f)
    next(f)
    csvreader = csv.reader(f, delimiter = '\t')
    # above should skip header lines (might not work)
    for row in csvreader:
        if len(row) >= 14:
            if 'XM:i:0' or 'XM:i:1' or 'XM:i:2' in str(row):
                # if str(row[14]) in ('XM:i:0', 'XM:i:1', 'XM:i:2'):  
                # use to select only for allignments with two or fewer mismatchesashr
                readnum = row[0] # CAN EXPAND THIS TO LIST WITH OTHER VALUES LIKE STARTING POSITION
                refgen = row[2]
                seq = row[9]
                # http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#sam-output
                # Key can have multiple values
                # Set up ref genome as key and append read numbers as values
                # https://stackoverflow.com/questions/20585920/how-to-add-multiple-values-to-a-dictionary-key-in-python
                refdict.setdefault(refgen, []).append(readnum)
                # allows entry to be created if not and added to without disruption if previously generated
                # At this point the dictionary is set up
                refdict_seq.setdefault(refgen, []).append(seq)
        else:
            pass

"""Determination of Number of Sequences per Reference Genome"""
## for key, value in refdict.items():
    ## refdict_count.setdefault(key, []).append(len(value))
# estabilishes dictionary with GIs as keys and number of sequences mapped to that ref genome as value

if 'G002' in argv[1]:
    totalreads = 12085742
elif 'G006' in argv[1]:
    totalreads = 21960873
elif 'BTIRed' in argv[1]:
    totalreads = 13931847

## for key, value in refdict_count.items():
    ## percent = round(((value[0]/totalreads)*100), 2)
    ## refdict_per.setdefault(key, []).append(percent)
# Sums total reads caught and generates a percent for each reference genome


"""Use NCBI to Generate SeqRecord Object for Reference Genomes"""
# Need to generate a list of the keys(Genebank Identifiers)
# List will be searched against NCBI using Entrez
# http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc131
GIs = list(refdict.keys())
Entrez.email = 'mct30@miami.edu'
for (entry, olddictkey) in zip(GIs, refdict.keys()):
    handle = Entrez.esearch(db='nuccore', term = entry)
    record = Entrez.read(handle)
    result = record['IdList']
    # print(type(result)) returns: <class 'Bio.Entrez.Parser.ListElement'>
    # result = result[0] returned index error saying list index out of range on full dataset
    # gi_list.append(result) to avoid above problem, used below instead
    gi_list = gi_list + result
    refdict[result[0]] = refdict.pop(olddictkey)
    # changes keys in primary dictionary to GeneBank Identifiers unstead of SAM ID
gi_str = ",".join(gi_list)

handle = Entrez.efetch(db='nuccore', id=gi_str, rettype='gb', retmode='text') 
# Biopython should convert the query to a string of query GIs separated by commas (123,234,345)
# Genome database no longer supported for efretch calls; nuccore contains better info
# https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
# http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec:entrez-search-fetch-genbank
records = SeqIO.parse(handle, 'gb')
#for (record, GI, count, per, seq) in zip(records, gi_list, refdict_count.values(), refdict_per.values(), readdict_seq.values()):
    # record is a SeqRecord object and has all of its attributes
    # http://biopython.org/DIST/docs/api/Bio.SeqRecord-pysrc.html#SeqRecord.__init__
    # all_list.append(GI)
    # all_list.append(record.description)
    # all_list.append(count[0])
    # all_list.append(per[0])
    # refdict_alltogether.setdefault(record.id, []).append(all_list)
    # builds a final dictionary that houses all pertinate attributes stored under the SeqRecord ID/sequence ID
    # print('"""%s"""\nGenBank Identifier: %s\nDescription: %s\nNumber of matched reads: %s\nTotal reads mapped to this genome: %s%%\n' % (record.id, GI, record.description, count[0], per[0]))
    # can uncomment individual print statements in above sections based on necessary information


"""Output CSV"""
for ((GI, readnums), (key, seqs)) in zip(refdict.items(), refdict_seq.items()):
    values = []
    values.extend(readnums)
    seqlist = []
    seqlist.extend(seqs)
    for (genename, seq) in zip(values, seqlist):
        print('%s\t%s\t%s' % (genename, GI, seq))
