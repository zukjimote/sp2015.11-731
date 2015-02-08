import optparse
import sys
from collections import defaultdict

optparser = optparse.OptionParser()
optparser.add_option("-b", "--bitext", dest="bitext", default="data/dev-test-train.de-en", help="Parallel corpus (default data/dev-test-train.de-en)")
#optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()


bitext = [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open(opts.bitext)][:opts.num_sents]

f_set = set()
e_set = set()
#for (k, (f, e)) in enumerate(bitext):
#	f_set = f_set | set(f)
#	e_set = e_set | set(e)

# Initialize t
t = defaultdict(float)
#for f in f_set:
#	for e in e_set|set(["##NULL##"]):
#		t[(f,e)] = 1
for (k, (f, e)) in enumerate(bitext):
	for f_i in f:
		for e_j in e+["##NULL##"]:
			t[(f_i,e_j)] = 1


# Iteration
for iter in range(0,5):
	sys.stderr.write("Iter "+str(iter)+"\n")

	# set counter to 0
	c_e_f = defaultdict(int)
	c_e = defaultdict(int)
	c_j_i_l_m = defaultdict(int)
	c_i_l_m = defaultdict(int)

	for (k, (f, e)) in enumerate(bitext):
		for (i, f_i) in enumerate(f):
			d_i = defaultdict(float)
			for (j, e_j) in enumerate(e+["##NULL##"]):
				d_i[f_i] += t[(f_i,e_j)]
			for (j, e_j) in enumerate(e+["##NULL##"]):
				d_i_j = t[(f_i,e_j)] / d_i[f_i]
				c_e_f[(e_j,f_i)] += d_i_j
				c_e[e_j] += d_i_j

#	for f_i in f_set:
#		for e_j in e_set|set(["##NULL##"]):
#			if (c_e[e_j] > 0):
#				t[(f_i,e_j)] = 1.0* c_e_f[(e_j,f_i)] / c_e[e_j]

	for (k, (f, e)) in enumerate(bitext):
		for f_i in f:
			for e_j in e+["##NULL##"]:
				if c_e[e_j] > 0:
					t[(f_i,e_j)] = 1.0* c_e_f[(e_j,f_i)] / c_e[e_j]



# Print output
outfile = open("output-model1.2.3.txt", "w")
for (f, e) in bitext:
	list_f_e = []
	for (i, f_i) in enumerate(f):
		i_pos = 1.0 * i / len(f)
		max_e_j_value = 0
		max_j = 0
		max_pos = sys.float_info.max
		for (j, e_j) in enumerate(e):
			j_pos = 1.0 * j / len(e)
			if t[(f_i,e_j)] > max_e_j_value or ( t[(f_i,e_j)] == max_e_j_value and abs(j_pos-i_pos) < abs(max_pos-i_pos) ):
				max_e_j_value = t[(f_i,e_j)]
				max_j = j
				max_pos = j_pos
		list_f_e += [ (i,max_j) ]

	list_e_f = []
	for (j, e_j) in enumerate(e):
		j_pos = 1.0 * j / len(e)
		max_f_i_value = 0
		max_i = 0
		max_pos = sys.float_info.max
		for (i, f_i) in enumerate(f):
			i_pos = 1.0 * i / len(f)
			if t[(f_i,e_j)] > max_f_i_value or ( t[(f_i,e_j)] == max_f_i_value and abs(i_pos-j_pos) < abs(max_pos-j_pos) ):
				max_f_i_value = t[(f_i,e_j)]
				max_i = i
				max_pos = i_pos
		list_e_f += [ (max_i,j) ]

	for (i,j) in set(list_f_e) & set(list_e_f):
		outfile.write("%i-%i " % (i,j))
	outfile.write("\n")

outfile.close()