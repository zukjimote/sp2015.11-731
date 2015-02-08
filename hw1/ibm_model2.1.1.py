import optparse
import sys
from collections import defaultdict

optparser = optparse.OptionParser()
optparser.add_option("-b", "--bitext", dest="bitext", default="data/dev-test-train.de-en", help="Parallel corpus (default data/dev-test-train.de-en)")
#optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()


bitext = [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open(opts.bitext)][:opts.num_sents]

# Initialize t
t = defaultdict(float)
q = defaultdict(float)
for (k, (f, e)) in enumerate(bitext):
	for (i, f_i) in enumerate(f):
		for (j, e_j) in enumerate(e+["##NULL##"]):
			t[(f_i,e_j)] = 1
			q[(j,i,len(e),len(f))] = 1


# Iteration
for iter in range(0,4):
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
				d_i[f_i] += q[(j,i,len(e),len(f))]*t[(f_i,e_j)]	
			for (j, e_j) in enumerate(e+["##NULL##"]):
				d_i_j = q[(j,i,len(e),len(f))]*t[(f_i,e_j)] / d_i[f_i]
				c_e_f[(e_j,f_i)] += d_i_j
				c_e[e_j] += d_i_j
				c_j_i_l_m[(j,i,len(e),len(f))] += d_i_j
				c_i_l_m[(i,len(e),len(f))] += d_i_j

	# Expectation
	for (k, (f, e)) in enumerate(bitext):
		for (i, f_i) in enumerate(f):
			for (j, e_j) in enumerate(e+["##NULL##"]):
				if c_e[e_j] > 0:
					t[(f_i,e_j)] = 1.0* c_e_f[(e_j,f_i)] / c_e[e_j]
				if c_i_l_m[(i,len(e),len(f))] > 0:
					q[(j,i,len(e),len(f))] = 1.0* c_j_i_l_m[(j,i,len(e),len(f))] / c_i_l_m[(i,len(e),len(f))]


# Print output
outfile = open("output-model2.txt", "w")
for (f, e) in bitext:
	for (i, f_i) in enumerate(f):
		i_pos = 1.0 * i / len(f)
		max_e_j_value = 0
		max_j = 0
		max_pos = sys.float_info.max
		for (j, e_j) in enumerate(e):
			j_pos = 1.0 * j / len(e)
			value = q[(j,i,len(e),len(f))]*t[(f_i,e_j)]
			if value > max_e_j_value or ( value == max_e_j_value and abs(j_pos-i_pos) < abs(max_pos-i_pos) ):
				max_e_j_value = value
				max_j = j
				max_pos = j_pos
		outfile.write("%i-%i " % (i,max_j))
	outfile.write("\n")
outfile.close()