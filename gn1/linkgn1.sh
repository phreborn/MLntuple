#!/bin/bash

rse=CERN-PROD_PHYS-HDBS

#for camp in mc16a mc16d mc16e
for camp in mc16e
do
  rm ${camp}/*/* -r

  for ntuple in $(cat ${camp}.txt)
  do
    group=$(echo ${ntuple} | cut -d : -f 1)
    ntuple=$(echo ${ntuple} | cut -d : -f 2)
    dsid=$(echo ${ntuple} | cut -d . -f 3)

    if [ ! -d ${camp}/${ntuple} ];then mkdir ${camp}/${ntuple};fi

    #### get dataset RSES ####
    #rses=($(rucio list-dataset-replicas ${ntuple} | grep '|' | grep -v RSE | grep -v '+' | cut -d '|' -f 2 | sed 's/ //g'))
    #rse=${rses[0]}
    rses=$(rucio list-dataset-replicas ${ntuple} | grep '|' | grep -v RSE | grep -v '+' | cut -d '|' -f 2 | sed 's/ //g')
    rse=
    for rs in ${rses}
    do
      if [[ "${rs}" =~ "CERN" || "${rs}" =~ "MAINZ_LOCALGROUPDISK" ]];then rse=${rs};fi
    done

    #### get file replicas ####
    orifiles=$(rucio list-file-replicas --rses ${rse} ${ntuple} | grep root | cut -d '|' -f 6 | cut -d : -f 4 | cut -c 6- | sort)

    #### link file replicas ####
    listof=(${orifiles})
    numsub=${#listof[@]}
    for file in ${orifiles}
    do
      subnum=$(echo ${file} | cut -d . -f 4)
      ln -s /${file} ${camp}/${ntuple}/gn1_${subnum}.root
    done

    #### print info ####
    echo ${camp} ${dsid} ${rse} ${numsub}
  done
done
