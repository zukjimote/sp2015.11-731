This is the implementation of IBM Model 1 combined with some heuristics.
(1) Alignments are made such that each English word is aligned with one or zero German word. This allows several English words to be aligned with one German word, which is often correct.
(2) Special characters can be aligned with either special characters or null. It enhances precision.
(3) After training the parameters, both argmax_f p(e|f) and argmax_e p(e|f) are calculated and intersected. This intersection is in conflict with (1) where multiple English words are aligned with one German word. However, this still enhances performance.

Many more unsuccessful trials:
(1) IBM Model 2 with random initialization and Model 1-based initialization did not improve performance.
(2) Gibbs sampling with the following heuristics did not outperform Model 1.
  (2-1) Dirichlet prior on t(f|e).
  (2-2) Alignment score q(j|j-1) based on the distance between the current alignment and the previous one.
  (2-3) Alignment score q(i|j,l,m) based on the difference between i/l and j/m.
(3) Alignment score q(i|j,l,m) based on the different between i/l and j/m did not improve performance.
(4) Intersecting the results of p(e|f) and p(f|e) did not improve performance.



---

There are three Python programs here (`-h` for usage):

 - `./align` aligns words using Dice's coefficient.
 - `./check` checks for out-of-bounds alignment points.
 - `./grade` computes alignment error rate.

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./align -t 0.9 -n 1000 | ./check | ./grade -n 5


The `data/` directory contains a fragment of the German/English Europarl corpus.

 - `data/dev-test-train.de-en` is the German/English parallel data to be aligned. The first 150 sentences are for development; the next 150 is a blind set you will be evaluated on; and the remainder of the file is unannotated parallel data.

 - `data/dev.align` contains 150 manual alignments corresponding to the first 150 sentences of the parallel corpus. When you run `./check` these are used to compute the alignment error rate. You may use these in any way you choose. The notation `i-j` means the word at position *i* (0-indexed) in the German sentence is aligned to the word at position *j* in the English sentence; the notation `i?j` means they are "probably" aligned.

