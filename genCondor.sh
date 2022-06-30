#!/bin/bash

camp=mc16a

dsids=$(ls gn1/${camp}/ | grep root | cut -d . -f 3 | sort)

ldsids=(${dsids})
numID=${#ldsids[@]}

intvl=20
seqs=$(seq 0 ${intvl} ${numID})

workarea=$(pwd)

allJobs=jobsSub.sh
> ${allJobs}

condor=condor
for init in ${seqs}
do
  fin=$((${init} + ${intvl} - 1))
  jobName=dump_${camp}_${init}_${fin}; echo ${jobName}
  hepout=${condor}/sub_${jobName}
  if [ ! -d ${hepout} ]; then mkdir -p ${hepout}; fi
  rm ${hepout}/* -r
  executable=${condor}/exe_${jobName}.sh
  > ${executable}
  subcfg=${condor}/${jobName}.sub
  > ${subcfg}

  echo "#!/bin/bash" >> ${executable}
  echo "" >> ${executable}
  echo "cd /afs/cern.ch/work/h/huirun/workspace/multilepton/ttHMulti/caf" >> ${executable}
  echo "source setup.sh" >> ${executable}
  echo "cd ${workarea}" >> ${executable}
  #echo "export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase" >> ${executable}
  #echo "source \${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh" >> ${executable}
  #echo "lsetup \"root 6.20.06-x86_64-centos7-gcc8-opt\"" >> ${executable}

for it in $(seq ${init} 1 ${fin})
do
  if [ ${it} -ge ${numID} ];then continue;fi
  echo "----- ${it}"
  dsid=${ldsids[${it}]}
  dir=$(ls -d gn1/${camp}/*${dsid}*)
  subfs=$(ls ${dir}/*)
  subfslist=
  for file in ${subfs}
  do
    subfslist="${subfslist} ${file}"
  done
  echo ${subfslist}

  echo "" >> ${executable}
  echo "python dumpleptau.py -s branchList.txt ${subfslist} -o /eos/user/h/huirun/multilepton/leptau/gn2/${camp}/${dsid}.root -b" >> ${executable}
done

  cat example.sub | sed 's/??/'${jobName}'/g' > ${subcfg}

  echo "condor_submit ${subcfg}" >> ${allJobs}

  echo ""
done
