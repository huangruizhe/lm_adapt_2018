#!/usr/bin/env bash

# compute interpolated kn lm on in-domain data only

# words have been converted to int for time and space efficiency
vocab="/export/a12/rhuang/lmadapt/data/swbd/words.txt.int"
in_domain_train="/export/a12/rhuang/lmadapt/data/swbd/swbd.txt.int"

work_dir="/export/a12/rhuang/lmadapt/data/swbd/"

ngram-count -text $in_domain_train -order 5 -write ${work_dir}5gram.count
dis_factor=$(/export/a12/rhuang/lmadapt/scripts/cal_dis_factor.py ${work_dir}5gram.count)
echo "The suggested discount factor is $dis_factor"  # The suggested discount factor is 0.416549
ngram-count -order 5 -lm ${work_dir}5gram.lm -vocab $vocab -unk -text $in_domain_train -cdiscount $dis_factor -interpolate -gt1min 0 -gt2min 0 -gt3min 0 -gt4min 0 -gt5min 0

