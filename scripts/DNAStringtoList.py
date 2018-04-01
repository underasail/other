#! /usr/bin/python

sequence = input('Enter a DNA/RNA sequence: ')

codon = 0
codon2 = 3
codon_list = []
codon_list.append(sequence[codon:codon2])
range_end = len(sequence)/3

if type(range_end) == float:
	print('Your sequence is not a multiple of three.\nThis program will default to starting your codons at the first position,\nand any trailing bases (past the last multiple of three) will be ingnored.')
	range_end = int(range_end)

for codon in range(1, range_end):
	codon = codon2
	codon2 = codon2+3
	codon_list.append(sequence[codon:codon2])

print(codon_list)
