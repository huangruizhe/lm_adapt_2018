#!/usr/bin/env bash

ngram-count -text /export/a12/rhuang/lmadapt/data/tedlium/train/tedlium.txt -order 3 -limit-vocab \
  -vocab /export/a12/rhuang/pocolm/egs/swbd/data/srilm/wordlist -unk -map-unk "<unk>" -kndiscount -interpolate \
  -lm /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa

ngram-count -text /export/a12/rhuang/lmadapt/data/tedlium/train/tedlium.txt -order 4 -limit-vocab \
  -vocab /export/a12/rhuang/pocolm/egs/swbd/data/srilm/wordlist -unk -map-unk "<unk>" -kndiscount -interpolate \
  -lm /export/a12/rhuang/lmadapt/data/tedlium/4gram.kn.arpa

./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  0.5


ngram-count -text /export/a07/keli1/one-billion-kaldi-rnnlm/egs/tedlium/s5_r2/data/rnnlm/lm1b/lm1b.en.train.all -order 3 \
  -limit-vocab -vocab /export/a12/rhuang/pocolm/egs/swbd/data/srilm/wordlist \
  -unk -map-unk "<unk>" -kndiscount -interpolate -lm /export/a12/rhuang/lmadapt/data/onebillion/3gram.arpa



#!/usr/bin/env bash

ratio=0.1; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=0.2; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=0.3; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=0.4; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=0.5; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=0.6; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=0.7; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=0.8; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=0.9; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}
ratio=1.0; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/tedlium/3gram.kn.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa.mdi.${ratio}