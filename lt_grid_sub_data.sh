#!/bin/bash
#export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
#alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'

###
#
###
brnchList=$(readlink -f Br_data.txt)
py_script=$(readlink -f dumpleptau_data.py)
src_script=$(readlink -f setup.sh)
count_script=$(readlink -f GetCountHist.py)
id_text=$2
cd $(mktemp -d)
cp $brnchList .
cp $py_script .
cp $count_script .

#setupATLAS 
#lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"


   rucio list-file-replicas --protocol root --pfns $1 | grep phys-hdbs | tee input.txt 
   #fileList=$(rucio list-file-replicas --protocol root --pfns $1 | rev |sort -u -t/ -k1,1| rev | xargs echo  | sed -e s'/ /,/'g)
   #export X509_USER_PROXY=/users/rnarayan/code/HHML/HHMLFW2/x509up_u508555
   echo $RUCIO_ACCOUNT
   grid_user=$RUCIO_ACCOUNT

   out_name="user."$grid_user"."$(echo $1 |rev|  cut -d "." -f5 | rev)"."$(echo $1 |rev|  cut -d "." -f3 | rev)"."$(echo $1 |rev|  cut -d "." -f2 | rev)"."$2

   #source $src_script
   #lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"
   #lsetup xrootd 
   if [ -s input.txt ]
    then
      python GetCountHist.py input.txt total_weights.root
   fi
    #python fw2_hhml.py -s Br_data.txt $fileList 


    #prun --official  --voms atlas:/atlas/phys-higgs/Role=production --exec "python fw2_hhml.py -s Br_data.txt %IN" --inDS $1 --outDS $(echo $1 |rev|  cut -d "." -f5 | rev)_$2 --outputs output.root --extFile total_weights.root --rootVer=6.14/04 --cmtConfig=x86_64-slc6-gcc62-opt
   if [ -s total_weights.root ] 
    then
      prun --exec "python dumpleptau_data.py -s Br_data.txt %IN" --inDS $1 --outDS $out_name --outputs output.root --extFile total_weights.root --rootVer=6.18/04 --cmtConfig=x86_64-centos7-gcc8-opt
    else
      prun --exec "python dumpleptau_data.py -s Br_data.txt %IN" --inDS $1 --outDS $out_name --outputs output.root --rootVer=6.18/04 --cmtConfig=x86_64-centos7-gcc8-opt
   fi


#fi
