#!/bin/bash 

#DISCLAIMER: Not tested yet

#How to run:
#lsetup panda
#sh grid_run.sh <inputDS> user.<nickname>.<identifiers_extra>

lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"
prun --exec "python fw2_hhml.py -s branchList.txt %IN" --inDs $1 --outDs $2
