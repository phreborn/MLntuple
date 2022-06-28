#!/bin/bash

vTag=23Jun22try01

grid_user=$RUCIO_ACCOUNT

for camp in mc16a mc16d mc16e
do
  allJobs=jobGrid${camp}.sh
  > ${allJobs}
  if [ ! -d gn2/${camp} ];then mkdir gn2/${camp};fi
  fetchs=gn2/${camp}/getgn2.sh
  > ${fetchs}

  inDSs=$(cat gn1/${camp}.txt)
  inDSs=$(cat gn1/${camp}.txt | grep -v Sh.DAOD_HIGG8D1 | grep -v "#")
  for inDS in ${inDSs}
  do
    inDS=$(echo ${inDS} | cut -d : -f 2)
    echo "./lt_grid_sub.sh ${inDS} ${vTag}" >> ${allJobs}

    outDS="user."$grid_user"."$(echo ${inDS} |rev|  cut -d "." -f5 | rev)"."$(echo ${inDS} |rev|  cut -d "." -f3 | rev)"."$(echo ${inDS} |rev|  cut -d "." -f2 | rev)"."${vTag}
    echo "rucio get ${outDS}_output.root" >> ${fetchs}
  done
done

for camp in data1516 data17 data18
do
  allJobs=jobGrid${camp}.sh
  > ${allJobs}
  if [ ! -d gn2/${camp} ];then mkdir gn2/${camp};fi
  fetchs=/eos/user/h/huirun/multilepton/leptau/gn2/${camp}/getgn2.sh
  > ${fetchs}

  inDSs=$(cat gn1/${camp}.txt)
  inDSs=$(cat gn1/${camp}.txt | grep -v Sh.DAOD_HIGG8D1)
  for inDS in ${inDSs}
  do
    inDS=$(echo ${inDS} | cut -d : -f 2)
    echo "./lt_grid_sub_data.sh ${inDS} ${vTag}" >> ${allJobs}

    outDS="user."$grid_user"."$(echo ${inDS} |rev|  cut -d "." -f5 | rev)"."$(echo ${inDS} |rev|  cut -d "." -f3 | rev)"."$(echo ${inDS} |rev|  cut -d "." -f2 | rev)"."${vTag}
    echo "rucio get ${outDS}_output.root" >> ${fetchs}
  done
done
