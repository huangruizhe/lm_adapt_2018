#!/usr/bin/env bash

ngram-count -text /export/a12/rhuang/lmadapt/data/tedlium/train/tedlium.txt -order 3 -limit-vocab \
  -vocab /export/a12/rhuang/pocolm/egs/swbd/data/srilm/wordlist -unk -map-unk "<unk>" -kndiscount -interpolate \
  -lm /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa

./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  0.5
