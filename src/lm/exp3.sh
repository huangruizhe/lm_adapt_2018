#!/usr/bin/env bash



awk '{print $s " " NR}' /export/a12/rhuang/pocolm/egs/swbd/data/srilm/wordlist > wordlist.id

sym2int.pl --map-oov 30278 wordlist.id /export/a12/rhuang/pocolm/egs/swbd/data/text/swbd1.txt > swbd1.txt.id
sym2int.pl --map-oov 30278 wordlist.id /export/a12/rhuang/lmadapt/data/tedlium/train/tedlium.txt > tedlium.txt.id
sym2int.pl --map-oov 30278 wordlist.id /export/a12/rhuang/pocolm/egs/swbd/data/text/dev.txt > dev.txt.id

ngram-count -text swbd1.txt.id -order 3 -limit-vocab -vocab wordlist.id.2 -unk -map-unk "<unk>" -kndiscount -interpolate -lm sw1.o3g.kn.gz
echo "Perplexity for SWBD1 trigram LM:"
ngram -order 3 -unk -lm sw1.o3g.kn.gz -ppl dev.txt.id

ngram-count -text tedlium.txt.id -order 3 -limit-vocab -vocab wordlist.id.2 -unk -map-unk "<unk>" -kndiscount -interpolate -lm tedlium.o3g.kn.gz
echo "Perplexity for TEDLIUM trigram LM:"
ngram -order 3 -unk -lm tedlium.o3g.kn.gz -ppl dev.txt.id