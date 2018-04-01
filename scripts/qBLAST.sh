#! /bin/bash

# Runs a python script on an ANSI encoded FASTA file to retrieve qBLAST Alignment results
# Output is fed into a text file

echo -n "Specify /path/to/output_file.txt: "
read outputFile
# echo "Enter path to an ANSI encoded FASTA file: "
# python 
/home/underasail/Documents/Python_Scripts/Bioinformatics/BLAST_Search.py | grep -iv "Please provide the path to an ANSI encoded FASTA file and press Enter: " >> $outputFile
echo "Results can be found at $outputFile"
