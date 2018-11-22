#!/usr/bin/env python3

import sys
import arpa
import os
import math
import numpy as np


lmfile = sys.argv[1]

print("lmfile=", lmfile)

lms = arpa.loadf(lmfile)
lm = lms[0]

def log_p(B, ngram):
    # words = B._check_input(ngram)
    # if B._unk:
    #     words = B._replace_unks(words)
    # return log_p_raw(B, words)
    return log_p_raw(B, ngram)


def log_p_raw(B, ngram):
    ret = B._ps.get(ngram, None)
    if ret is not None:
        return ret
    else:
        # if len(ngram) == 1:
        #     raise KeyError
        # else:
        #     log_bo = B._bos.get(ngram[:-1], 0)
        #     return log_bo + log_p_raw(B, ngram[1:])
        log_bo = B._bos.get(ngram[:-1], 0)
        return log_bo + log_p_raw(B, ngram[1:])


def p(B, ngram):
    return B._base ** log_p(B, ngram)


log_10_e = math.log10(math.e)


def logsumexp10(a, b):
    return np.logaddexp(a/log_10_e, b/log_10_e) * log_10_e


with open(os.path.basename(lmfile) + ".unigram", 'w') as f:
    cnt = 0
    psum = float("-inf")
    for w in lm.vocabulary():
        lp = log_p(lm, (w,))
        print("%s\t%f" % (w, lp), file=f)
        psum = logsumexp10(psum, lp)
        cnt += 1
    print("unigram:", cnt, "psum=", psum)

w1 = "<s>"
with open(os.path.basename(lmfile) + ".%s.bigram" % w1, 'w') as f:
    cnt = 0
    psum = float("-inf")
    for e in lm._entries(2):
        if e[1][0] == w1:
            lp = log_p(lm, e[1])
            print("%s\t%f" % (" ".join(list(e[1])), lp), file=f)
            psum = logsumexp10(psum, lp)
            cnt += 1
    print("%s-bigram:" % w1, cnt, "psum(seen)=", psum)


psum = float("-inf")
cnt = 0
for w in lm.vocabulary():
    lp = log_p(lm, (w1, w))
    psum = logsumexp10(psum, lp)
    cnt += 1
print("%s-bigram:" % w1, cnt, "psum(all)=", psum)
