#!/usr/bin/env python
import re
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators

# Prec: (h1 & set(ref)) / h1
# Recl: (set(h1) & ref) / ref
# Remove special characters



# DRY
def word_matches(h, ref):
	return sum(1 for w in h if w in ref)
	# or sum(w in ref for w in f) # cast bool -> int
	# or sum(map(ref.__contains__, h)) # ugly!
 
def main():


	parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
	# PEP8: use ' and not " for strings
	parser.add_argument('-i', '--input', default='data/train-test.hyp1-hyp2-ref',
			help='input file (default data/train-test.hyp1-hyp2-ref)')
	parser.add_argument('-n', '--num_sentences', default=None, type=int,
			help='Number of hypothesis pairs to evaluate')
	# note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
	parser.add_argument('-a', '--a', default=1.0, type=float,
			help='weight a')

	opts = parser.parse_args()
 
	a = opts.a

	outfile = open("output-meteor1.0.2-a"+str(a)+".txt", "w")

	# we create a generator and avoid loading all sentences into a list
	def sentences():
		with open(opts.input) as f:
			for pair in f:
				yield [ [ re.sub("[^a-zA-Z]","",y) for y in sentence.strip().split() ] for sentence in pair.split(' ||| ')]
 
	# note: the -n option does not work in the original code
	for h1, h2, ref in islice(sentences(), opts.num_sentences):
#			h1_match = word_matches(h1, ref)
		h1_prec = 1.0 * word_matches(h1, set(ref)) / len(h1)
		h1_recl = 1.0 * word_matches(ref, set(h1)) / len(ref)
		if a * h1_prec + h1_recl == 0: h1_fscore = 0
		else: h1_fscore = h1_prec * h1_recl / ( a * h1_prec + (1-a) * h1_recl )

#			h2_match = word_matches(h2, ref)
		h2_prec = 1.0 * word_matches(h2, set(ref)) / len(h2)
		h2_recl = 1.0 * word_matches(ref, set(h2)) / len(ref)
		if a * h2_prec + h2_recl == 0: h2_fscore = 0
		else: h2_fscore = h2_prec * h2_recl / ( a * h2_prec + (1-a) * h2_recl )

		decision = (-1 if h1_fscore > h2_fscore else # \begin{cases}
				(0 if h1_fscore == h2_fscore
					else 1)) # \end{cases}
		outfile.write(str(decision)+"\n")
 	outfile.close()

# convention to allow import of this file as a module
if __name__ == '__main__':
	main()
