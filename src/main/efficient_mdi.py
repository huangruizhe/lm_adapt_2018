#!/usr/bin/env python3

# Copyright 2018  Ruizhe Huang

# This is an implementation of language model adaptatin method
# in "EFFICIENT LANGUAGE MODEL ADAPTATION THROUGH MDI ESTIMATION"
# (https://www.isca-speech.org/archive/archive_papers/eurospeech_1999/e99_1583.pdf)

import arpa

default_encoding = "latin-1"


def load_background(filename, encoding=default_encoding):

    B_models = arpa.loadf(filename, encoding=encoding)
    B = B_models[0]  # ARPA files may contain several models.

    f_B_star = dict()

    # we can recover f_B_star (i.e., discounted probabilities) from interpolated probabilities
    # p_B(w|h) = f_B_star(w|h) + bow_B(h) * p_B(w|h')
    # Thus, f_B_star(w|h) = p_B(w|h) - bow_B(h) * p_B(w|h')
    # where h' = h[1:]
    for n in range(2, B.order() + 1):
        for e in B._entries(n):  # entry format: (log10(prob), hw, log10(bow))
            hw = e[1]
            h = hw[:-1]
            h_prime_w = hw[1:]
            f_B_star[hw] = B._base ** float(e[0]) - B._base ** (float(B._entry(h)[2]) + float(B.log_p(h_prime_w)))

    return B, f_B_star


if __name__ == '__main__':

    B_filename = "/Users/huangruizhe/Downloads/PycharmProjects/lm_adapt/data/c5-inter.lm"
    B, f_B_star = load_background(B_filename)

    print(f_B_star)
