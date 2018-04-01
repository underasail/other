#! /usr/bin/python

from sys import argv
from Bio import SeqIO
fasta_file = argv[1]
for seq_record in SeqIO.parse(fasta_file, "fasta"):
	print(seq_record.id)
	print(repr(seq_record.seq))
	print(len(seq_record))
