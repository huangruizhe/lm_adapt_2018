#!/usr/bin/env python3

# Copyright 2018  Ruizhe Huang

# This is an implementation of language model adaptatin method
# in "EFFICIENT LANGUAGE MODEL ADAPTATION THROUGH MDI ESTIMATION"
# (https://www.isca-speech.org/archive/archive_papers/eurospeech_1999/e99_1583.pdf)

import math
import arpa
from arpa.models.simple import ARPAModelSimple
from collections import defaultdict

default_encoding = "latin-1"


# TODO: specify external vocabulary for lm

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
        for e in B._entries(n):  # entry format: (log10(prob), hw, log10(bow))
            hw = e[1]
            h = hw[:-1]
            h_prime_w = hw[1:]
            f_B_star[hw] = B._base ** float(e[0]) - B._base ** (float(B._log_bo(h)) + float(B.log_p(h_prime_w)))

    # Index structure:
    # len(h) --> h --> {w | hw is seen in the corpus}, where len(h) >= 1
    B_hist_index = [defaultdict(list) for i in range(B.order())]
    for n in range(2, B.order() + 1):
        for e in B._entries(n):
            hw = e[1]
            h = hw[:-1]
            w = hw[-1]
            B_hist_index[len(h)][h].append(w)

    return B, f_B_star, B_hist_index


def load_adaptation_sample(filename, encoding=default_encoding):
    A_models = arpa.loadf(filename, encoding=encoding)
    A = A_models[0]
    return A


def cal_alpha(gamma, A, B):
    alpha = dict()
    for w in B.vocabulary():
        alpha[w] = B._base ** ((float(A.log_p(w)) - float(B.log_p(w))) * gamma)
    return alpha


# TODO: to speed up, caching mechanism can be applied here (even offline), for those z-values that are expensive to compute
def cal_z(h, B, f_B_star, B_hist_index, alpha, z_epsilon):
    # Note: type(h) == tuple

    if len(h) == 0:
        return z_epsilon
    else:
        # TODO: statistics can be done here
        z_h_prime = cal_z(h[1:], B, f_B_star, B_hist_index, alpha, z_epsilon)
        return sum([f_B_star[h + (w,)] * alpha[w] for w in B_hist_index[len(h)][h]]) + B._base ** float(B._log_bo(h)) * z_h_prime


def cal_p_A(hw, alpha, B, z_h):
    return float(B.p(hw)) * alpha[hw[-1]] / z_h


def cal_A_adapted_arpa(B, f_B_star, B_hist_index, alpha, z_epsilon):
    A_adapted = ARPAModelSimple()

    # unigram
    for e in B._entries(1):
        w = e[1]
        p_A_w = float(B.p(w)) * alpha[w[0]] / z_epsilon
        A_adapted.add_entry(ngram=w, p=math.log(p_A_w, B._base))

    # ngram, n >= 2
    for n in range(2, B.order() + 1):
        len_h = n - 1
        for h, w_list in B_hist_index[len_h].items():
            z_h = cal_z(h, B, f_B_star, B_hist_index, alpha, z_epsilon)
            z_h_prime = cal_z(h[1:], B, f_B_star, B_hist_index, alpha, z_epsilon)

            bow_A_h = (B._base ** float(B._log_bo(h))) * z_h_prime / z_h
            A_adapted._bos[h] = bow_A_h

            for w in w_list:
                hw = h + (w,)
                p_A_hw = cal_p_A(hw, alpha, B, z_h)
                A_adapted.add_entry(ngram=hw, p=math.log(p_A_hw, B._base))

    for order, count in B.counts():
        A_adapted.add_count(order, count)

    return A_adapted


def save_A_adapted_arpa(filename, A_adapted):
    arpa.dumpf(A_adapted, filename, encoding=default_encoding)


if __name__ == '__main__':

    # params
    B_filename = "/Users/huangruizhe/Downloads/PycharmProjects/lm_adapt/data/c5-inter.lm"
    A_filename = "/Users/huangruizhe/Downloads/PycharmProjects/lm_adapt/data/c5-inter.lm"
    gamma = 1  # 0 < gamma <= 1

    # Note: B should be an interpolated ngram model
    B, f_B_star, B_hist_index = load_background(B_filename)  # out-domain data

    A = load_adaptation_sample(A_filename)  # in-domain data

    alpha = cal_alpha(gamma, A, B)

    z_epsilon = sum([float(B.p(w)) * alpha[w] for w in B.vocabulary()])  # z_epsilon

    A_adapted = cal_A_adapted_arpa(B, f_B_star, B_hist_index, alpha, z_epsilon)
    save_A_adapted_arpa(A_filename + ".adapted", A_adapted)
