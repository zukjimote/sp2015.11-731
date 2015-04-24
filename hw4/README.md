output2_a0.01_b0.3_g1.0_dep+sub+prev_next+end+uni.txt
Five feature types:
 - dep: dependency relation of the phrase's first word
 - sub: subject of the phrase's first word (if any)
 - prev_next: previous/next words of the phrase (separate features)
 - end: last two alphabets of the target's first word X {POS tag, dependency relation, subject of the phrase's first word} (separate features)
 - uni: nouns, verbs, adjectives in the sentence (separate features)

Relative goodness of the feature types: dep > sub > uni > prev_next > end > pos (not included)


There are three Python programs here (`-h` for usage):

 - `./rerank` a simple reranker that simply sorts candidate translations on log p(czech|english)
 - `./grade` computes the mean reciprocal rank of your output

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./rerank | ./check | ./grade


The `data/` directory contains the input set to be decoded and the models

 - `data/train.input` is the input side of training set in the format described on the homework webpage

 - `data/train.refs` are the references to the training set, giving the correct czech translation for the highlighted phrase in each sentence

 - `data/train.parses` are dependency parses of the training sentences, provided for convenience. (Note: these files are provided in gzip format to avoid the space limitations imposed by github)

 - `data/dev+test.input` is the input side of both the dev and test sets

 - `data/dev.refs` are the references to the dev set, which is the first half of the above dev+test file

 - `data/dev+test.parses` are dependency parses of the dev and test sentences, provided for convenience

 - `data/ttable` is the phrase translation table which contains candidates that you will rerank

 If you want the raw parallel data used to build the training data and translation tables English-Czech data (for example, to build word vectors), it is available at http://demo.clab.cs.cmu.edu/sp2015-11731/parallel.encs .
