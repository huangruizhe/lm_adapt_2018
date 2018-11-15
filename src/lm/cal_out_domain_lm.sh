#!/usr/bin/env bash

vocab="/export/a12/rhuang/lmadapt/data/swbd/words.txt.int"
out_domain_train="/export/a12/rhuang/lmadapt/data/tedlium/tedlium.txt.int"
work_dir="/export/a12/rhuang/lmadapt/data/tedlium/"

echo "get count..."
ngram-count -text $out_domain_train -order 5 -write ${work_dir}5gram.count

echo "compute discount factor..."
dis_factor=$(/export/a12/rhuang/lmadapt/scripts/cal_dis_factor.py ${work_dir}5gram.count)
echo "The suggested discount factor is $dis_factor"  # 0.420150

echo "compute 5gram model..."
ngram-count -order 5 -lm ${work_dir}5gram.lm -vocab $vocab -unk -text $out_domain_train -cdiscount $dis_factor -interpolate -gt1min 0 -gt2min 0 -gt3min 0 -gt4min 0 -gt5min 0



ngram-count -text "/export/a12/rhuang/lmadapt/data/tedlium/train/tedlium.txt" -order 5 -limit-vocab -vocab "/export/a07/keli1/kaldi-2/egs/swbd/s5c/data/lang/words.txt" -unk -map-unk "<unk>" -kndiscount -interpolate -lm "/export/a12/rhuang/lmadapt/data/tedlium/5gram.kn.gz"