#!/usr/bin/env bash

# compute interpolated kn lm on in-domain data only

# first run: pocolm/egs/swbd/local/srilm_baseline.sh

ngram-count -text /export/a12/rhuang/pocolm/egs/swbd/data/text/swbd1.txt -order 3 -limit-vocab -vocab /export/a12/rhuang/pocolm/egs/swbd/data/srilm/wordlist \
  -unk -map-unk "<unk>" -kndiscount -interpolate -lm /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa

echo "Perplexity for SWBD1 trigram LM:"
ngram -order 3 -unk -lm /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa -ppl /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt

# Perplexity for SWBD1 trigram LM:
# file /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt: 10000 sentences, 118254 words, 0 OOVs
# 0 zeroprobs, logprob= -247200.5 ppl= 84.61146 ppl1= 123.1459


ngram-count -text /export/a12/rhuang/pocolm/egs/swbd/data/text/swbd1.txt -order 4 -limit-vocab -vocab /export/a12/rhuang/pocolm/egs/swbd/data/srilm/wordlist \
  -unk -map-unk "<unk>" -kndiscount -interpolate -lm /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa

echo "Perplexity for SWBD1 4-gram LM:"
ngram -order 4 -unk -lm /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa -ppl /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt

# Perplexity for SWBD1 4-gram LM:
# file /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt: 10000 sentences, 118254 words, 0 OOVs
# 0 zeroprobs, logprob= -246110.4 ppl= 82.97167 ppl1= 120.5596

