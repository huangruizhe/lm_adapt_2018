#!/usr/bin/env bash

ratio=0.5; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=0.1; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=0.2; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=0.3; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=0.4; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=0.6; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=0.7; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=0.8; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=0.9; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}
ratio=1.0; echo "ratio="$ratio; ./efficient_mdi.py /export/a12/rhuang/lmadapt/data/onebillion/4gram.arpa \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o3g.kn.arpa \
  $ratio \
  /export/a12/rhuang/pocolm/egs/swbd/data/srilm/sw1.o4g.kn.arpa.mdi.ob.${ratio}