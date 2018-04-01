#! /usr/bin/python

# Argument format: ./fa2fa.py [INPUT FASTA FILE] [INPUT PROTEIN DESCRIPTION FILE] [OUTPUT FASTA FILE]

from sys import argv
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import csv

prefasta = list()

fasta_file = argv[1]
for seq_record in SeqIO.parse(fasta_file, "fasta"):
    with open(argv[2], newline='') as f:
        csvreader = csv.reader(f, delimiter=',')
        header = csvreader.__next__()
        symbol = header.index('Approved Symbol')
        geneName = header.index('Approved Name')
        synonyms = header.index('Synonyms')
        location = header.index('Chromosome')
        for row in csvreader:
            if seq_record.id == row[symbol]:
                fastaHeader = '%s | %s | %s' % (row[geneName], row[synonyms], row[location])
                row[symbol] = SeqRecord(seq_record.seq,id=fastaHeader)
                prefasta.append(row[symbol])

SeqIO.write(prefasta, argv[3], 'fasta')
