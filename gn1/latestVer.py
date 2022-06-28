#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import re

camps = ['a', 'd', 'e']

usedMC = []
with open("usedDISDs.txt", 'r') as f:
  for line in f.readlines():
    usedMC.append(line.replace('\n', ''))

for camp in camps:

#### collect DSIDs ####
  mcids = []
  with open("mc16"+camp+"_raw.txt", 'r') as inf:
    for line in inf.readlines():
      mcid = line.split('.')[3]
      mcids.append(mcid)
  mcids=list(set(mcids))
  mcids.sort()
  print camp, len(mcids)

#### collect lattest version for each id ####
  idlabs = {}
  for mcid in mcids:
    print mcid
    versntuple = []
    with open("mc16"+camp+"_raw.txt", 'r') as inf:
      for line in inf.readlines():
        if mcid in line:
          versntuple.append(line)
    versntuple.sort()

    verlabs = []
    for ntuple in versntuple:
      rslt=re.search(r'(%s[0-9]?)_output_root'%(camp), ntuple)
      verlabs.append(rslt.group(1))
    verlabs.sort()
    vlabfin = verlabs[-1]
    print verlabs, vlabfin
    idlabs[mcid] = vlabfin

  outtxt = []
  with open("mc16"+camp+"_raw.txt", 'r') as inf:
    for line in inf.readlines():
      if 'Sh.DAOD' in line: continue
      if 'Sh_2' in line: continue
      mcid = line.split('.')[3]
      if mcid not in usedMC: continue
      print mcid, '%s_output_root'%(idlabs[mcid])
      if '%s_output_root'%(idlabs[mcid]) not in line: continue
      outtxt.append(line)

  with open("mc16"+camp+".txt", 'w') as outf:
    for line in outtxt:
      outf.write(line)
