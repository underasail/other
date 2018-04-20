#! /usr/bin/python3

from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio.Blast import NCBIXML

E_VALUE_THRESH = 0.01

file = input('/path/to/FASTA/file.fasta: ')
for record in SeqIO.parse(file, 'fasta'):
    result_handle = NCBIWWW.qblast('blastn', 'nt', record.seq)
    outfile = '/home/underasail/temp/%s.xml' % record.id
    with open(outfile, 'w') as out:
        out.write(result_handle.read() + '\n\n')
    result_handle.close()
    result_handle = open(outfile, 'r')
    blast_record = NCBIXML.read(result_handle)
    # .parse for multiple
    outfile = '/home/underasail/temp/%s.alignments' % record.id
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < E_VALUE_THRESH:
                with open(outfile, 'w') as out:
                    out.write('****Alignment****\n')
                    out.write('sequence:' + str(alignment.title) + '\n')
                    out.write('length:' + str(alignment.length) + '\n')
                    out.write('e value:' + str(hsp.expect) + '\n')
                    out.write(str(hsp.query[0:75]) + '...\n')
                    out.write(str(hsp.match[0:75]) + '...\n')
                    out.write(str(hsp.sbjct[0:75]) + '...\n')
