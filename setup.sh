#!/bin/bash 
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'

setupATLAS

pip install progressbar --user

lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"
