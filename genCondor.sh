#!/bin/bash

camp=mc16a

dsids=$(ls gn1/${camp}/ | cut -d . -f 3 | sort)

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
  executable=${condor}/exe_${jobName}.sh
  > ${executable}
  subcfg=${condor}/${jobName}.sub
  > ${subcfg}

  echo "#!/bin/bash" >> ${executable}
  echo "" >> ${executable}
  echo "cd ${workarea}" >> ${executable}
  echo "export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase" >> ${executable}
  echo "alias setupATLAS='source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh'" >> ${executable}
  echo "setupATLAS" >> ${executable}
  echo "lsetup \"root 6.18.04-x86_64-centos7-gcc8-opt\"" >> ${executable}

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
  echo "python dumpleptau.py -s branchList.txt ${subfslist} -o gn2/${camp}/${dsid}.root -b" >> ${executable}
done

  cat example.sub | sed 's/??/'${jobName}'/g' > ${subcfg}

  echo "condor_submit ${subcfg}" >> ${allJobs}

  echo ""
done
