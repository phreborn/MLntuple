#!/bin/bash
#export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
#alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'

brnchList=$(readlink -f branchList.txt)
py_script=$(readlink -f fw2_hhml.py)
src_script=$(readlink -f setup.sh)
count_script=$(readlink -f GetCountHist.py)
output_file=$2
cd $(mktemp -d)
cp $brnchList .
cp $py_script .
cp $count_script .

#setupATLAS 
#lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"


rucio list-file-replicas --protocol root --pfns $1 | rev |sort -u -t/ -k1,1| rev | tee input.txt 
#fileList=$(rucio list-file-replicas --protocol root --pfns $1 | rev |sort -u -t/ -k1,1| rev | xargs echo  | sed -e s'/ /,/'g)
export X509_USER_PROXY=/users/rnarayan/code/HHML/HHMLFW2/x509up_u508555
echo $RUCIO_ACCOUNT

#source $src_script
#lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"
#lsetup xrootd 
python GetCountHist.py input.txt total_weights.root

#python fw2_hhml.py -s branchList.txt $fileList 


prun --official  --voms atlas:/atlas/phys-higgs/Role=production --exec "python fw2_hhml.py -s branchList.txt %IN" --inDS $1 --outDS $(echo $1 |rev|  cut -d "." -f3- | rev)_<changeme>--outputs output.root --extFile total_weights.root --rootVer=6.14/04 --cmtConfig=x86_64-slc6-gcc62-opt
