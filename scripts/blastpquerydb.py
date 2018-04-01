#! /usr/bin/python

# CL Structure: ./blastpquerydb.py [QUERY FASTA FILE] [DATABASE TO SEARCH (MAKE WITH MAKEBLASTDB)]

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.SubsMat.MatrixInfo import blosum62
from Bio.Blast import NCBIStandalone
from sys import argv

queryList = argv[1]

for seq_record in SeqIO.parse(queryList, "fasta"):
    SeqIO.write(SeqRecord(seq_record.seq, id = seq_record.id), '/home/underasail/temp/seq.fa', 'fasta')
    blastp_cli = NcbiblastpCommandline(cmd = "/home/underasail/ncbi-blast/ncbi-blast-2.7.1+/bin/blastp", query = '/home/underasail/temp/seq.fa', db = argv[2], matrix = 'blosum62', evalue = 0.01, num_descriptions = 1, num_alignments = 1, out = '~/temp/output.txt')
    blastp_cli()
    result_handle = open('/home/underasail/temp/output.txt', 'r')
    blast_parser = NCBIStandalone.BlastParser()
    blast_record = blast_parser.parse(result_handle)
    print('Human ID: ', seq_record.id)
    for description in blast_record.descriptions:
        print('Mouse Match ID: ', description.title)
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            print('Score: ', hsp.score)
            print('Bits: ', hsp.bits)
            print('E-value: ', hsp.expect)
            print('Alignment (Query/Match): ')
            print(hsp.query)
            print(hsp.match)
            print(hsp.sbjct, \n\n)