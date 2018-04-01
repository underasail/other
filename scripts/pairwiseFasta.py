#! /usr/bin/python

from sys import argv
from Bio import pairwise2  # uses Biopython wrapper for pairwise alignment
from Bio import SeqIO  # to parse the sequences
seq1 = SeqIO.read(argv[1], 'fasta')
seq2 = SeqIO.read(argv[2], 'fasta')
alignments = pairwise2.align.globalxx(seq1.seq, seq2.seq)  
# xx represents two character code to determine first the match score 
and then the cost for gaps

print(pairwise2.format_alignment(*alignments[0]))
