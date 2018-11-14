#!/usr/bin/env python3

# Copyright 2018  Ruizhe Huang
#
# Apache 2.0.

# This is an implementation of computing Kneser-Ney smoothed language model.
# This is a interpolated, unmodified version of Kneser-Ney smoothing.
#
# Ref:
# [1] "EFFICIENT LANGUAGE MODEL ADAPTATION THROUGH MDI ESTIMATION"
# (https://www.isca-speech.org/archive/archive_papers/eurospeech_1999/e99_1583.pdf)
# [2] The smoothing algorithm is based on: http://www.speech.sri.com/projects/srilm/manpages/ngram-discount.7.html
# [3] The data structure is based on: kaldi/egs/wsj/s5/utils/lang/make_phone_lm.py

import sys
import os
import re
import io
import math
import argparse
from collections import Counter, defaultdict


parser = argparse.ArgumentParser(description="""
    Generate kneser-ney language model as arpa format. By default,
    it will read the corpus from standard input, and output to standard output.
    """)
parser.add_argument("-ngram-order", type=int, default=4, choices=[2, 3, 4, 5, 6, 7], help="Order of n-gram")
parser.add_argument("-text", type=str, default=None, help="Path to the corpus file")
parser.add_argument("-vocab", type=str, default=None, help="Path to the vocabulary file. If not specified (by default),"
                                                           "it will be derived from the corpus")
parser.add_argument("-lm", type=str, default=None, help="Path to output arpa file for language models")
parser.add_argument("-verbose", type=int, default=0, choices=[0, 1, 2, 3, 4, 5], help="Verbose level")
args = parser.parse_args()


default_encoding = "latin-1"  # For encoding-agnostic scripts, we assume byte stream as input.
                              # Need to be very careful about the use of strip() and split()
                              # in this case, because there is a latin-1 whitespace character
                              # (nbsp) which is part of the unicode encoding range.
strip_chars = " \t\r\n"
whitespace = re.compile("[ \t]+")


class CountsForHistory:
    # This class (which is more like a struct) stores the counts seen in a
    # particular history-state.  It is used inside class NgramCounts.
    # It really does the job of a dict from int to float, but it also
    # keeps track of the total count.
    def __init__(self):
        # The 'lambda: defaultdict(float)' is an anonymous function taking no
        # arguments that returns a new defaultdict(float).
        self.word_to_count = defaultdict(int)
        self.word_to_context = defaultdict(set)  # using a set to count the number of unique contexts
        self.word_to_f = dict()  # final interpolated probability
        self.word_to_g = dict()  # discounted probability
        self.word_to_bow = dict()  # back-off weight
        self.total_count = 0

    def words(self):
        return self.word_to_count.keys()

    def __str__(self):
        # e.g. returns ' total=12: 3->4, 4->6, -1->2'
        return ' total={0}: {1}'.format(
            str(self.total_count),
            ', '.join(['{0} -> {1}'.format(word, count)
                      for word, count in self.word_to_count.items()]))

    def add_count(self, predicted_word, context_word, count):
        assert count >= 0

        self.total_count += count
        self.word_to_count[predicted_word] += count
        if context_word is not None:
            self.word_to_context[predicted_word].add(context_word)


class NgramCounts:
    # A note on data-structure.  Firstly, all words are represented as
    # integers.  We store n-gram counts as an array, indexed by (history-length
    # == n-gram order minus one) (note: python calls arrays "lists") of dicts
    # from histories to counts, where histories are arrays of integers and
    # "counts" are dicts from integer to float.  For instance, when
    # accumulating the 4-gram count for the '8' in the sequence '5 6 7 8', we'd
    # do as follows: self.counts[3][[5,6,7]][8] += 1.0 where the [3] indexes an
    # array, the [[5,6,7]] indexes a dict, and the [8] indexes a dict.
    def __init__(self, ngram_order, bos_symbol='<s>', eos_symbol='</s>'):
        assert ngram_order >= 2

        self.ngram_order = ngram_order
        self.bos_symbol = bos_symbol
        self.eos_symbol = eos_symbol

        self.counts = []
        for n in range(ngram_order):
            self.counts.append(defaultdict(lambda: CountsForHistory()))

        # self.D = 0  # constant discounting factor
        self.d = []  # list of discounting factor for each order of ngram

        self.V = set()  # vocabulary
        self.V_corpus = set()  # vocabulary in the corpus

    # adds a raw count (called while processing input data).
    # Suppose we see the sequence '6 7 8 9' and ngram_order=4, 'history'
    # would be (6,7,8) and 'predicted_word' would be 9; 'count' would be
    # 1.
    def add_count(self, history, predicted_word, context_word, count):
        self.counts[len(history)][history].add_count(predicted_word, context_word, count)

    # 'line' is a string containing a sequence of integer word-ids.
    # This function adds the un-smoothed counts from this line of text.
    def add_raw_counts_from_line(self, line):
        words = [self.bos_symbol] + whitespace.split(line) + [self.eos_symbol]

        for i in range(len(words)):
            for n in range(1, self.ngram_order+1):
                if i + n > len(words):
                    break

                ngram = words[i: i + n]
                predicted_word = ngram[-1]
                history = tuple(ngram[: -1])
                if i == 0 or n == self.ngram_order:
                    context_word = None
                else:
                    context_word = words[i-1]

                self.add_count(history, predicted_word, context_word, 1)

    def add_raw_counts_from_standard_input(self):
        lines_processed = 0
        infile = io.TextIOWrapper(sys.stdin.buffer, encoding=default_encoding)  # byte stream as input
        for line in infile:
            line = line.strip(strip_chars)
            if line == '':
                break
            self.add_raw_counts_from_line(line)
            lines_processed += 1
        if lines_processed == 0 or args.verbose > 0:
            print("add_raw_counts_from_standard_input: processed {0} lines of input".format(lines_processed), file=sys.stderr)

    def add_raw_counts_from_file(self, filename):
        lines_processed = 0
        with open(filename, encoding=default_encoding) as fp:
            for line in fp:
                line = line.strip(strip_chars)
                if line == '':
                    break
                self.add_raw_counts_from_line(line)
                lines_processed += 1
        if lines_processed == 0 or args.verbose > 0:
            print("add_raw_counts_from_file: processed {0} lines of input".format(lines_processed), file=sys.stderr)

    def load_dictionary(self, filename):
        lines_processed = 0
        with open(filename, encoding=default_encoding) as fp:
            for line in fp:
                line = line.strip(strip_chars)
                if line == '':
                    continue
                self.V.add(line)
                lines_processed += 1
        if lines_processed == 0 or args.verbose > 0:
            print("load_dictionary: processed {0} lines of input".format(lines_processed), file=sys.stderr)

    def cal_interpolated_kn(self):
        # 1) discounting constant
        # ------------------------
        # Ney's absolute discounting using D as the constant to subtract.
        # The suggested discount factor is:
        # D = n1 / (n1 + 2*n2)
        # where n1 and n2 are the total number of N-grams with exactly one and
        # two counts, respectively.
        # Note: D should be between 0 and 1.
        #
        # 2) discounted probabilities
        # ------------------------
        # g(a_z) is discounted a probability distribution of word sequence a_z.
        # Typically g(a_z) is discounted to be less than the ML estimate so we have
        # some leftover probability for the z words unseen in the context (a_).
        # g(a_z)  = max(0, c(a_z) - D) / c(a_)
        #
        # final interpolated probability:
        # f(a_z) = g(a_z) + bow(a_) p(_z)
        #
        # 3) backoff weights
        # ------------------------
        # The leftover probability for unseen ngrams
        # bow(a_) = 1 - Sum_Z1 g(a_z)
        #         = D n(a_*) / c(a_)

        # We also discount 1st order, which will be interpolated with uniform distribution over V

        # 1) compute discounting constant
        self.d = [0]  # TODO: vocabulary
        # for n in range(1, self.ngram_order):
        #     this_order_counts = self.counts[n]
        #     n1 = 0
        #     n2 = 0
        #     for hist, counts_for_hist in this_order_counts.items():
        #         stat = Counter(counts_for_hist.word_to_count.values())
        #         n1 += stat[1]
        #         n2 += stat[2]
        #     assert n1 + 2 * n2 > 0
        #     d_n = n1 * 1.0 / (n1 + 2 * n2)
        #     assert d_n < 1
        #     self.d.append(d_n)

        # discount uniformly
        n1 = 0
        n2 = 0
        for n in range(0, self.ngram_order):
            this_order_counts = self.counts[n]
            for hist, counts_for_hist in this_order_counts.items():
                stat = Counter(counts_for_hist.word_to_count.values())
                n1 += stat[1]
                n2 += stat[2]
        assert n1 + 2 * n2 > 0
        d_n = n1 * 1.0 / (n1 + 2 * n2)
        assert d_n < 1
        self.d.extend([d_n] * (self.ngram_order - 1))

        print("discounting constants:", self.d)

        # 2) compute discounted probabilities -- as well as final interpolated probabilities
        # and 3) back-off weights

        # unigrams
        this_order_counts = self.counts[0]
        for a_, counts_for_hist in this_order_counts.items():
            c_a_ = counts_for_hist.total_count - counts_for_hist.word_to_count[self.bos_symbol]
            for z, c_a_z in counts_for_hist.word_to_count.items():
                if z is self.bos_symbol:
                    counts_for_hist.word_to_f[z] = 0  # why p(<s>) is always 0? -- just follow srilm implementation
                else:
                    counts_for_hist.word_to_f[z] = float(c_a_z) / c_a_

        # ngrams where n >= 2
        for n in range(1, self.ngram_order):
            this_order_counts = self.counts[n]
            for a_, counts_for_hist in this_order_counts.items():
                c_a_ = counts_for_hist.total_count

                # back-off weight
                n_a_star = len(counts_for_hist.word_to_count)
                bow_a_ = float(self.d[n] * n_a_star) / c_a_
                self.counts[n - 1][a_[:-1]].word_to_bow[a_[-1]] = bow_a_

                # probabilities
                for z, c_a_z in counts_for_hist.word_to_count.items():
                    g_a_z = max((c_a_z - self.d[n]), 0) * 1.0 / c_a_
                    counts_for_hist.word_to_g[z] = g_a_z
                    print("%s" % str(a_ + tuple([z])), g_a_z)
                    counts_for_hist.word_to_f[z] = g_a_z + bow_a_ * self.counts[n - 1][a_[1:]].word_to_f[z]


    # TODO: remember to leave interface for MDI calculation
    # TODO: might need to specify vocabulary -- not assuming the corpus contains all vocabulary

    def print_as_arpa(self, fout=io.TextIOWrapper(sys.stdout.buffer, encoding='latin-1')):
        # print as ARPA format.

        print('\\data\\', file=fout)
        for hist_len in range(self.ngram_order):
            # print the number of n-grams.
            print('ngram {0}={1}'.format(
                hist_len + 1,
                sum([len(counts_for_hist.word_to_f) for counts_for_hist in self.counts[hist_len].values()])),
                file=fout
            )

        print('', file=fout)

        for hist_len in range(self.ngram_order):
            print('\\{0}-grams:'.format(hist_len + 1), file=fout)

            this_order_counts = self.counts[hist_len]
            for hist, counts_for_hist in this_order_counts.items():
                for word in counts_for_hist.word_to_count.keys():
                    ngram = hist + (word,)
                    prob = counts_for_hist.word_to_f[word]
                    bow = counts_for_hist.word_to_bow.get(word, None)

                    if prob == 0:  # f(<s>) is always 0
                        prob = 1e-99

                    line = '{0}\t{1}'.format('%.7f' % math.log10(prob), ' '.join(ngram))
                    if bow is not None:
                        line += '\t{0}'.format('%.7f' % math.log10(bow))
                    print(line, file=fout)
            print('', file=fout)
        print('\\end\\', file=fout)


if __name__ == "__main__":

    ngram_counts = NgramCounts(args.ngram_order)

    if args.text is None:
        ngram_counts.add_raw_counts_from_standard_input()
    else:
        assert os.path.isfile(args.text)
        ngram_counts.add_raw_counts_from_file(args.text)

    ngram_counts.cal_interpolated_kn()

    if args.lm is None:
        ngram_counts.print_as_arpa()
    else:
        with open(args.lm, 'w', encoding=default_encoding) as f:
            ngram_counts.print_as_arpa(fout=f)
