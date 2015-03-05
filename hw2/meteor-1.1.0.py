#!/usr/bin/env python
import re
from nltk.corpus import wordnet as wn
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators

# Prec: (h1 & set(ref)) / h1
# Recl: (set(h1) & ref) / ref
# Remove special characters
# WordNet



# DRY
def word_matches(h, ref):
#	return sum(1 for w in h if w in ref)
	ref_set = set.union(*ref)
	sum = 0
	for s in h:
		for w in s:
			if w in ref_set:
				sum += 1
				break
	return sum

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

	cache = dict()

	outfile = open("output-meteor1.1.0-a"+str(a)+".txt", "w")

	# we create a generator and avoid loading all sentences into a list
	def sentences():
		with open(opts.input) as f:
			for pair in f:
				res = []
				for sentence in pair.split(' ||| '):
					res2 = []
					for y in [ re.sub("[^a-zA-Z]","",x) for x in sentence.strip().split() ]:
						if cache.has_key(y): res2.append( cache[y] )
						else:
							syns = wn.synsets(y)
							if len(syns) > 0: cache[y] = set([ syn.name() for syn in syns ])
							else: cache[y] = set([unicode(y)])
							res2.append( cache[y] )
					res.append(res2)
				yield res
 
	# note: the -n option does not work in the original code
	cnt = 0
	for h1, h2, ref in islice(sentences(), opts.num_sentences):
#			h1_match = word_matches(h1, ref)
		h1_prec = 1.0 * word_matches(h1, ref) / len(h1)
		h1_recl = 1.0 * word_matches(ref, h1) / len(ref)
		if a * h1_prec + h1_recl == 0: h1_fscore = 0
		else: h1_fscore = h1_prec * h1_recl / ( a * h1_prec + (1-a) * h1_recl )

#			h2_match = word_matches(h2, ref)
		h2_prec = 1.0 * word_matches(h2, ref) / len(h2)
		h2_recl = 1.0 * word_matches(ref, h2) / len(ref)
		if a * h2_prec + h2_recl == 0: h2_fscore = 0
		else: h2_fscore = h2_prec * h2_recl / ( a * h2_prec + (1-a) * h2_recl )

		decision = (-1 if h1_fscore > h2_fscore else # \begin{cases}
				(0 if h1_fscore == h2_fscore
					else 1)) # \end{cases}
		outfile.write(str(decision)+"\n")

		cnt += 1
 	outfile.close()

# convention to allow import of this file as a module
if __name__ == '__main__':
	main()
