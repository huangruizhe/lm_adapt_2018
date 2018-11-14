#!/usr/bin/env bash

# compute interpolated kn lm on in-domain data only

vocab="/export/a07/keli1/kaldi-2/egs/swbd/s5c/data/lang/words.txt"  # swbd
oov2int=30278
in_domain_train="/export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm/text/swbd.txt"  # swbd
in_domain_dev="/export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm/text/dev.txt"  # swbd
in_domain_test="/export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/eval2000/eval2000.raw"  # swbd
out_domain_train="/export/a12/rhuang/lmadapt/data/tedlium/train/tedlium.txt"  # tedlium

cut -d ' ' -f 2- "/export/a07/keli1/one-billion-kaldi-rnnlm/egs/tedlium/s5_r2/data/train/text" > $out_domain_train

cut -d ' ' -f 2 $vocab > "/export/a12/rhuang/lmadapt/data/swbd/words.txt.int"

sym2int.pl --map-oov 30278 $vocab $in_domain_train > "/export/a12/rhuang/lmadapt/data/swbd/swbd.txt.int"
sym2int.pl --map-oov 30278 $vocab $in_domain_dev > "/export/a12/rhuang/lmadapt/data/swbd/dev.txt.int"
sym2int.pl --map-oov 30278 $vocab $in_domain_test > "/export/a12/rhuang/lmadapt/data/swbd/eval2000.txt.int"
sym2int.pl --map-oov 30278 $vocab $out_domain_train > "/export/a12/rhuang/lmadapt/data/tedlium/tedlium.txt.int"

