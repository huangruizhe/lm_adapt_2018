#!/usr/bin/env python3

# Copyright 2018  Ruizhe Huang

# This is an implementation of language model adaptatin method
# in "EFFICIENT LANGUAGE MODEL ADAPTATION THROUGH MDI ESTIMATION"
# (https://www.isca-speech.org/archive/archive_papers/eurospeech_1999/e99_1583.pdf)

import arpa

B_arpa_path = "/Users/huangruizhe/Downloads/PycharmProjects/lm_adapt/data/c5-end.arpa"  # background sample
A_arpa_path = "/Users/huangruizhe/Downloads/PycharmProjects/lm_adapt/data/c5-end.arpa"  # adaptation sample

B_models = arpa.loadf(B_arpa_path)
B = B_models[0]  # ARPA files may contain several models.

A_models = arpa.loadf(A_arpa_path)
A = A_models[0]  # A should be a unigram model here

gamma = 1  # in [0, 1], where γ=0 is equivalent to non adaptation, γ=1 corresponds to the standard GIS solution


