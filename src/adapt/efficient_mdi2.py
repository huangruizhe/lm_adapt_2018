#!/usr/bin/env python3

# Copyright 2018  Ruizhe Huang

# This is an implementation of language model adaptatin method
# in "EFFICIENT LANGUAGE MODEL ADAPTATION THROUGH MDI ESTIMATION"
# (https://www.isca-speech.org/archive/archive_papers/eurospeech_1999/e99_1583.pdf)

import argparse
import math
import arpa
import sys
import numpy as np
from arpa.models.simple import ARPAModelSimple
from collections import defaultdict

default_encoding = "latin-1"


# TODO: logsumexp
# TODO: all operations in log domain

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


# compute log(1+x) without losing precision for small values of x
def log10_1addx(x, base=10):
    assert x > -1.0

    if abs(x) > 1e-4:
        return math.log(1.0 + x, base)

    # Use Taylor approx. log(1 + x) = x - x^2/2 with error roughly x^3/3
    # Since |x| < 10^-4, |x|^3 < 10^-12, relative error less than 10^-8

    return (-0.5*x + 1.0)*x


def logminusexp10(x, y):
    # x >= y
    # ref: http://www.cs.jhu.edu/~jason/465/hw-hmm/hw-hmm.pdf
    if y > x:
        print("error in logminusexp10")
        exit()

    # y <= x
    return x + log10_1addx(- 10 ** (y-x))


def load_background(filename, encoding=default_encoding):
    B_models = arpa.loadf(filename, encoding=encoding)
    B = B_models[0]  # ARPA files may contain several models.

    # We can recover f_B_star (i.e., discounted probabilities) from interpolated probabilities
    # As B is an interpolated model, i.e., p_B(w|h) = f_B_star(w|h) + bow_B(h) * p_B(w|h')
    # Thus,
    #
    #    f_B_star(w|h) = p_B(w|h) - bow_B(h) * p_B(w|h')
    #
    # where h' = h[1:]
    f_B_star = dict()
    for n in range(2, B.order() + 1):
        print("%d-gram" % n)
        # progress_count = 0
        for e in B._entries(n):  # entry format: (log10(prob), hw, log10(bow))
            hw = e[1]
            h = hw[:-1]
            h_prime_w = hw[1:]
            # f_B_star[hw] = B._base ** float(e[0]) - B._base ** (float(B._log_bo(h)) + float(B.log_p(h_prime_w)))
            # f_B_star[hw] = B._base ** float(e[0]) - B._base ** (float(B._bos[h]) + float(log_p(B, h_prime_w)))
            f_B_star[hw] = logminusexp10(float(e[0]), float(B._bos[h]) + log_p(B, h_prime_w))  # float()?

            # progress_count += 1
            # if progress_count % 2000 == 0:
            #     print(progress_count)

    # Index structure:
    # len(h) --> h --> {w | hw is seen in the corpus}, where len(h) >= 1
    B_hist_index = [defaultdict(list) for i in range(B.order())]
    for n in range(2, B.order() + 1):
        print("%d-gram" % n)
        # progress_count = 0
        for e in B._entries(n):
            hw = e[1]
            h = hw[:-1]
            w = hw[-1]
            B_hist_index[len(h)][h].append(w)

            # progress_count += 1
            # if progress_count % 2000 == 0:
            #     print(progress_count)

    return B, f_B_star, B_hist_index


def load_adaptation_sample(filename, encoding=default_encoding):
    A_models = arpa.loadf(filename, encoding=encoding)
    A = A_models[0]
    return A


def cal_alpha(gamma, A, B):
    alpha = dict()
    for w in B.vocabulary():
        alpha[w] = (float(log_p(A, (w,))) - float(log_p(B, (w,)))) * gamma
    return alpha


def cal_z(h, B, f_B_star, B_hist_index, alpha, z_epsilon):
    # Note: type(h) == tuple

    if len(h) == 0:
        return z_epsilon
    else:
        # TODO: statistics can be done here
        # z_h_prime = cal_z(h[1:], B, f_B_star, B_hist_index, alpha, z_epsilon)
        z_h_prime = zh1.get(h[1:], None)
        if z_h_prime is None:
            z_h_prime = cal_z(h[1:], B, f_B_star, B_hist_index, alpha, z_epsilon)

        z_h = float("-inf")
        for w in B_hist_index[len(h)][h]:
            z_h = logsumexp10(z_h, f_B_star[h + (w,)] + alpha[w])
        z_h = logsumexp10(z_h, float(B._bos[h]) + z_h_prime)
        zh2[h] = z_h
        return z_h


def cal_p_A_old(hw, alpha, B, z_h):
    return log_p(B, hw) + alpha[hw[-1]] - z_h


def cal_p_A(hw, f_B_star, alpha, z_h, bow_A_h, A):
    f_A_star_hw = f_B_star[hw] + alpha[hw[-1]] - z_h

    p_A_hw = f_A_star_hw + bow_A_h * p(A, hw[1:])
    return p_A_hw


def cal_A_adapted_arpa(B, f_B_star, B_hist_index, alpha, z_epsilon):
    A_adapted = ARPAModelSimple()

    global zh1, zh2

    check_sum = float("-inf")

    # unigram
    print("processing unigram...")
    for e in B._entries(1):
        w = e[1]
        p_A_w = log_p(B, w) + alpha[w[0]] - z_epsilon
        A_adapted.add_entry(ngram=w, p=p_A_w)
        check_sum = logsumexp10(check_sum, p_A_w)
    assert abs(check_sum - 0) < 0.0001
    zh2[tuple()] = z_epsilon

    # ngram, n >= 2
    for n in range(2, B.order() + 1):
        print("processing %d-gram..." % n)
        progress_count = 0

        zh1.clear()
        zh1 = zh2
        zh2 = dict()

        len_h = n - 1
        for h, w_list in B_hist_index[len_h].items():
            z_h = cal_z(h, B, f_B_star, B_hist_index, alpha, z_epsilon)
            z_h_prime = zh1.get(h[1:], None)  # we can cache this
            if z_h_prime is None:
                z_h_prime = cal_z(h[1:], B, f_B_star, B_hist_index, alpha, z_epsilon)

            bow_A_h = float(B._bos[h]) + z_h_prime - z_h
            A_adapted._bos[h] = bow_A_h

            for w in w_list:
                hw = h + (w,)
                # p_A_hw = cal_p_A(hw, f_B_star, alpha, z_h, bow_A_h, A_adapted)
                p_A_hw = cal_p_A_old(hw, alpha, B, z_h)
                # if p_A_hw - p_A_hw2 > 0.0001:
                #     print("p_A_hw=", p_A_hw, "p_A_hw2=", p_A_hw2)
                #     exit(0)
                A_adapted.add_entry(ngram=hw, p=math.log(p_A_hw, B._base))

                progress_count += 1
                if progress_count % 50000 == 0:
                    print(progress_count)

    for order, count in B.counts():
        A_adapted.add_count(order, count)

    return A_adapted


def save_A_adapted_arpa(filename, A_adapted):
    arpa.dumpf(A_adapted, filename, encoding=default_encoding)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('out_domain', type=str, help='out-domain (background) lm')
    parser.add_argument('in_domain', type=str, help='in-domain lm')
    parser.add_argument('gamma', type=str, help='0 < gamma <= 1')
    parser.add_argument('outfile', type=str, help='output arpa file')
    args = parser.parse_args()  # store the input in args

    # params
    out_domain_lm = args.out_domain  # out-domain (background)
    in_domain_lm = args.in_domain   # in-domain
    gamma = float(args.gamma)   # 0 < gamma <= 1
    outfile = args.outfile        # output arpa file

    print("out:", out_domain_lm)
    print("in:", in_domain_lm)
    print("gamma: %f" % gamma)
    print("outfile: ", outfile)

    global zh1, zh2
    zh1 = dict()  # h'
    zh2 = dict()  # h

    # Note: B should be an interpolated ngram model
    print("loading out-domain lm...")
    B, f_B_star, B_hist_index = load_background(out_domain_lm)  # out-domain data

    print("loading in-domain lm...")
    A = load_adaptation_sample(in_domain_lm)  # in-domain data

    print("cal alpha...")
    alpha = cal_alpha(gamma, A, B)

    print("cal z_epsilon...")
    # z_epsilon = sum([p(B, (w,)) * alpha[w] for w in B.vocabulary()])  # z_epsilon
    z_epsilon = 0
    print("z_epsilon = %f" % z_epsilon)

    print("cal adapted model...")
    A_adapted = cal_A_adapted_arpa(B, f_B_star, B_hist_index, alpha, z_epsilon)
    save_A_adapted_arpa(outfile, A_adapted)

    print("Adapted lm saved to: %s" % outfile)

