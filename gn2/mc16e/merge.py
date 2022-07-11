#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os, sys, commands
from ROOT import *
from array import array

cmps = ['mc16a', 'mc16d', 'mc16e']
Dir = "unmerged/"

def merge(files, outname, tname = 'leptau'):
  sumOfWeights = 0.
  for f in files:
    rf = TFile(f, 'read')
    ch = TChain(tname)
    ch.AddFile(f)
    ch.GetEntry(0)
    if ch.scale_nom == 0:
      print outname, 'warning, 0 sum of weights'
      files.remove(f)
      continue
    print 1/ch.scale_nom
    sumOfWeights += 1./ch.scale_nom
  print outname, len(files), sumOfWeights, 1./sumOfWeights

  outf = TFile(outname+'.root', 'recreate')

  ch = TChain(tname)
  [ch.AddFile(x) for x in files]
  ch.SetBranchStatus("*",1)
  ch.SetBranchStatus("scale_nom",0)
  ch.LoadTree(0)

  scale_nom = array('d', [0])

  otree = ch.CloneTree(0)
  otree.SetName(tname)
  otree.Branch('scale_nom', scale_nom, 'scale_nom/D')

  for i in range(ch.GetEntries()):
    ch.GetEntry(i)
    scale_nom[0] = 1./sumOfWeights
    otree.Fill()

  outf.cd()
  otree.AutoSave()

  outf.Close()

indir = sys.argv[1]

files = os.listdir(indir)
dsid = indir.split('.')[2]
print dsid, len(files)
if len(files) == 1:
  os.system('cp '+indir+'/'+files[0]+' '+ dsid+'.root')
elif len(files) > 1:
  infiles = []
  [infiles.append(indir+'/'+x) for x in files]
  merge(infiles, dsid)
