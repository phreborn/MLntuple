#!/bin/bash

rse=CERN-PROD_PHYS-HDBS

#for camp in mc16a mc16d mc16e
for camp in mc16e
do
  dir=faketau/${camp}
  rm ${dir}/* -r

  #for ntuple in $(cat ft_${camp}_raw.txt | grep -v "#" | grep -v "Sh.DAOD_" | grep -v "Sh_")
  for ntuple in $(cat ft_${camp}_raw.txt | grep -v "#")
  do
    group=$(echo ${ntuple} | cut -d : -f 1)
    ntuple=$(echo ${ntuple} | cut -d : -f 2)
    dsid=$(echo ${ntuple} | cut -d . -f 3)

    if [ ! -d ${dir}/${ntuple} ];then mkdir ${dir}/${ntuple};fi

    #### get dataset RSES ####
    #rses=($(rucio list-dataset-replicas ${ntuple} | grep '|' | grep -v RSE | grep -v '+' | cut -d '|' -f 2 | sed 's/ //g'))
    #rse=${rses[0]}
    rses=$(rucio list-dataset-replicas ${ntuple} | grep '|' | grep -v RSE | grep -v '+' | cut -d '|' -f 2 | sed 's/ //g')
    rse=
    for rs in ${rses}
    do
      if [[ "${rs}" =~ "CERN" ]];then rse=${rs};fi
    done

    #### get file replicas ####
    orifiles=$(rucio list-file-replicas --rses ${rse} ${ntuple} | grep root | cut -d '|' -f 6 | cut -d : -f 4 | cut -c 6- | sort)

    #### link file replicas ####
    listof=(${orifiles})
    numsub=${#listof[@]}
    for file in ${orifiles}
    do
      subnum=$(echo ${file} | cut -d . -f 4)
      ln -s /${file} ${dir}/${ntuple}/gn1_${subnum}.root
    done

    #### print info ####
    echo ${camp} ${dsid} ${rse} ${numsub}
  done
done
