#!/bin/bash

camp=data1516

dsids=$(ls gn1/${camp}/ | cut -d . -f 6 | sort | cut -d _ -f 1)

ldsids=(${dsids})
numID=${#ldsids[@]}

workarea=$(pwd)

allJobs=jobsSub_data.sh
> ${allJobs}

condor=condor_data
for dsid in ${dsids}
do
  subfiles=$(ls gn1/${camp}/*${dsid}*/*)
  lsubfiles=(${subfiles})
  numf=${#lsubfiles[@]}

  intvl=20
  seqs=$(seq 0 ${intvl} ${numf})

for init in ${seqs}
do
  fin=$((${init} + ${intvl} - 1))
  jobName=dump_${camp}_${dsid}_${init}; echo ${jobName}
  hepout=${condor}/sub_${jobName}
  if [ ! -d ${hepout} ]; then mkdir -p ${hepout}; fi
  rm ${hepout}/* -r
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

  subfslist=
  for it in $(seq ${init} 1 ${fin})
  do
    if [ ${it} -ge ${numf} ];then continue;fi
    echo "----- ${it}"
    subfile=${lsubfiles[${it}]}
    subfslist="${subfslist} ${subfile}"
  done
  echo ${subfslist}
  
  echo "" >> ${executable}
  echo "python dumpleptau_data.py -s Br_data.txt ${subfslist} -o gn2/${camp}/${dsid}_${init}.root -b" >> ${executable}

  cat example_data.sub | sed 's/??/'${jobName}'/g' > ${subcfg}

  echo "condor_submit ${subcfg}" >> ${allJobs}

  echo ""
done
done
