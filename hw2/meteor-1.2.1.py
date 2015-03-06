#!/usr/bin/env python
import re
import sys
from nltk.corpus import wordnet as wn
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators

# METEOR
# Prec: (h1 & set(ref)) / h1
# Recl: (set(h1) & ref) / ref
# Remove special characters
# WordNet
# Lowercase
# fraction

wn_cache = dict()


def get_wn(s):
	if not wn_cache.has_key(s): wn_cache[s] = set(wn.synsets(s))
	return wn_cache[s]

# DRY
def word_matches(h, ref):
	align = dict()
	consumed = set()

	# unigrams
	for (i, e) in enumerate(ref):
		for (j, f) in enumerate(h):
			if j not in consumed and e==f:
				align[i] = j
				consumed.add(j)
				break

	# stemmed
	for (i, e) in enumerate(ref):
		if align.has_key(i): continue
		for (j, f) in enumerate(h):
			if j not in consumed and e[:4]==f[:4]:
				align[i] = j
				consumed.add(j)
				break

	# wordnet
	for (i, e) in enumerate(ref):
		if align.has_key(i): continue
		e_wn = get_wn(e)
		for (j, f) in enumerate(h):
			if j not in consumed and len(e_wn & get_wn(f)) > 0:
				align[i] = j
				consumed.add(j)
				break

#	sys.stderr.write("ref: ")
#	for (i, e) in enumerate(ref):
#		sys.stderr.write(e+"("+ (str(align[i]) if align.has_key(i) else "") + ") ")
#	sys.stderr.write("\n")
#	sys.stderr.write("h: ")
#	for (j, f) in enumerate(h):
#		sys.stderr.write("["+str(j)+"]"+f+" ")
#	sys.stderr.write("\n")
#	print "--------------\n"

	return align

	# or sum(w in ref for w in f) # cast bool -> int
	# or sum(map(ref.__contains__, h)) # ugly!
 
def frag(align):
	if len(align) == 0: return 1.0

	num_frag = 0
	i = 0
	max_i = max(align.keys())
	while True:
		while not align.has_key(i) and i <= max_i: i += 1
		if i > max_i: break
		j = align[i]
		while True:
			i += 1
			j += 1
			if not align.has_key(i) or align[i] != j: break
		num_frag += 1
#	print "frag: ", 1.0*num_frag / len(align)
#	print "----------------------\n"
	return 1.0*num_frag / len(align)

def main():
	
	parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
	# PEP8: use ' and not " for strings
	parser.add_argument('-i', '--input', default='data/train-test.hyp1-hyp2-ref',
			help='input file (default data/train-test.hyp1-hyp2-ref)')
	parser.add_argument('-n', '--num_sentences', default=None, type=int,
			help='Number of hypothesis pairs to evaluate')
	# note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
	parser.add_argument('-a', '--a', default=0.5, type=float, help='weight a')
	parser.add_argument('-c', '--c', default=0.3, type=float, help='weight c')

	opts = parser.parse_args()
 
	a = opts.a
	c = opts.c

	cache = dict()

	outfile = open("output-meteor1.2.1-a"+str(a)+"-c"+str(c)+".txt", "w")

	# we create a generator and avoid loading all sentences into a list
	def sentences():
		with open(opts.input) as f:
			for pair in f:
				res = []
				for sentence in pair.split(' ||| '):
					res2 = []
					for y in [ re.sub("[^a-zA-Z0-9]","",x).lower() for x in sentence.strip().split() ]:
						if len(y) > 0: res2.append(y)
					res.append(res2)
				yield res
 
	# note: the -n option does not work in the original code
	cnt = 0
	for h1, h2, ref in islice(sentences(), opts.num_sentences):

		h1_align = word_matches(h1, ref)
		h1_prec = (1.0 * len(h1_align) / len(h1) if len(h1) > 0 else 0)
		h1_recl = (1.0 * len(h1_align) / len(ref) if len(ref) > 0 else 0)
		if a * h1_prec + h1_recl == 0: h1_fscore = 0
		else: h1_fscore = h1_prec * h1_recl / ( a * h1_prec + (1-a) * h1_recl )
		h1_fscore *= 1-c*pow(frag(h1_align),0.8)


		h2_align = word_matches(h2, ref)
		h2_prec = (1.0 * len(h2_align) / len(h2) if len(h2) > 0 else 0)
		h2_recl = (1.0 * len(h2_align) / len(ref) if len(ref) > 0 else 0)
		if a * h2_prec + h2_recl == 0: h2_fscore = 0
		else: h2_fscore = h2_prec * h2_recl / ( a * h2_prec + (1-a) * h2_recl )
		h2_fscore *= 1-c*pow(frag(h2_align),0.8)

		decision = (-1 if h1_fscore > h2_fscore else # \begin{cases}
				(0 if h1_fscore == h2_fscore
					else 1)) # \end{cases}
		outfile.write(str(decision)+"\n")

		cnt += 1
 	outfile.close()

# convention to allow import of this file as a module
if __name__ == '__main__':
	main()
