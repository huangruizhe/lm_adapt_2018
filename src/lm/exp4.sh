#!/usr/bin/env bash

# --------------- simple interpolation --------------- #

mkdir exp4

ngram -order 3 -unk -lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz -ppl /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt -debug 2 > exp4/sw1.output

ngram -order 3 -unk -lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/ted.o3g.kn.gz -ppl /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt -debug 2 > exp4/ted.output

PATH=$PATH:"/home/rhuang/kaldi/kaldi/tools/srilm/bin/i686-m64/"

compute-best-mix lambda="0.5 0.5" precision=0.1 exp4/sw1.output exp4/ted.output

ngram -unk -lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz -mix-lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/ted.o3g.kn.gz -lambda 0.45 -ppl /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt

ngram -unk -lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz -mix-lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/ted.o3g.kn.gz -lambda 0.45 -ppl /export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/eval2000/eval2000.raw

ngram -unk -lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz -mix-lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/ted.o3g.kn.gz -lambda 0.45 -ppl /export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/rt03/rt03.raw


# --------------- efficient mdi-based interpolation --------------- #

time ./efficient_mdi.py /export/a07/keli1/pocolm/egs/swbd/data/srilm/lm1b.o3g.kn.gz \
      /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz \
      1.0 \
      exp4/swbd_lm1b/sw1.o1g.gt.arpa.mdi.lm1b.o3g.1.0

time ./efficient_mdi.py /export/a07/keli1/pocolm/egs/swbd/data/srilm/lm1b.o2g.kn.gz \
      /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz \
      1.0 \
      exp4/swbd_lm1b/sw1.o1g.gt.arpa.mdi.lm1b.o2g.1.0

time ./efficient_mdi.py /export/a07/keli1/pocolm/egs/swbd/data/srilm/lm1b.o1g.kn.gz \
      /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz \
      1.0 \
      exp4/swbd_lm1b/sw1.o1g.gt.arpa.mdi.lm1b.o1g.1.0


n=3; r=1.0; ngram -order $n -unk -lm exp4/swbd_lm1b/sw1.o1g.gt.arpa.mdi.lm1b.o${n}g.${r} -ppl /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt
n=3; r=1.0; ngram -order $n -unk -lm exp4/swbd_lm1b/sw1.o1g.gt.arpa.mdi.lm1b.o${n}g.${r} -ppl /export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/eval2000/eval2000.raw
n=3; r=1.0; ngram -order $n -unk -lm exp4/swbd_lm1b/sw1.o1g.gt.arpa.mdi.lm1b.o${n}g.${r} -ppl /export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/rt03/rt03.raw



# ---------------  --------------- #

ngram -unk -lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz -mix-lm /export/a07/keli1/pocolm/egs/swbd/data/srilm/lm1b.o3g.kn.gz -lambda 0.5 -write-lm exp4/sw1.o1g_0.5_lm1b.o3g.arpa.gz
ngram -unk -lm exp4/sw1.o1g_0.5_lm1b.o3g.arpa.gz -ppl /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt
ngram -unk -lm exp4/sw1.o1g_0.5_lm1b.o3g.arpa.gz -ppl /export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/eval2000/eval2000.raw
ngram -unk -lm exp4/sw1.o1g_0.5_lm1b.o3g.arpa.gz -ppl /export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/rt03/rt03.raw

ngram -unk -lm exp4/sw1.o1g_0.5_lm1b.o3g.arpa.gz -ppl /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt -debug 2 > exp4/sw1.o1g_0.5_lm1b.o3g_dev.output
ngram -unk -lm exp4/sw1.o1g_0.5_lm1b.o3g.arpa.gz -ppl /export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/eval2000/eval2000.raw -debug 2 > exp4/sw1.o1g_0.5_lm1b.o3g_eval2000.output
ngram -unk -lm exp4/sw1.o1g_0.5_lm1b.o3g.arpa.gz -ppl /export/a07/keli1/kaldi-2/egs/swbd/s5c/data/rnnlm_adapt/rt03/rt03.raw -debug 2 > exp4/sw1.o1g_0.5_lm1b.o3g_rt03.output





time ./efficient_mdi.py /export/a07/keli1/pocolm/egs/swbd/data/srilm/ted.o3g.kn.gz \
      /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz \
      0.3 \
      exp4/swbd_ted/sw1.o1g.gt.arpa.mdi.ted.o3g.0.3 &

time ./efficient_mdi.py /export/a07/keli1/pocolm/egs/swbd/data/srilm/ted.o2g.kn.gz \
      /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz \
      0.3 \
      exp4/swbd_ted/sw1.o1g.gt.arpa.mdi.ted.o2g.0.3 &

time ./efficient_mdi.py /export/a07/keli1/pocolm/egs/swbd/data/srilm/ted.o1g.kn.gz \
      /export/a07/keli1/pocolm/egs/swbd/data/srilm/sw1.o1g.kn.gz \
      0.3 \
      exp4/swbd_ted/sw1.o1g.gt.arpa.mdi.ted.o1g.0.3 &



