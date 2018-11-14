#!/usr/bin/env python3

# This scripts computes the The suggested discount factor by kn:
# D = n1 / (n1 + 2*n2)

from subprocess import call
import sys
import numpy as np

corpus_file = sys.argv[1]

max_n = 5
max_counts = 2
temp_file = "temp.count"

# ngram-count -text corpus.txt -order 9 -write temp.count
call(["ngram-count", "-text", str(corpus_file), "-order", str(max_n), "-write", temp_file])

# That is, count_of_counts[n][m] represents the total number of n-grams with exactly m counts.
count_of_counts = np.zeros((max_n + 1, max_counts + 1))

with open(temp_file) as fp:
    for line in fp:
        line = line.strip()
        if len(line) == 0:
            continue

        ll = line.split("\t")
        n = len(ll[0].split(" "))
        counts = int(ll[1])

        if n <= max_n:
            ni = n-1
        else:
            ni = max_n

        if counts <= max_counts:
            ci = counts - 1
        else:
            ci = max_counts

        count_of_counts[ni][ci] += 1


total_count_of_counts = np.sum(count_of_counts, axis=0)

dis_factor = float(total_count_of_counts[0]) / (total_count_of_counts[0] + 2 * total_count_of_counts[1])
print(dis_factor)

