#!/bin/bash

### igrid

#for mc16a
outf=mc16a_raw.txt
>${outf}
tmplist=$(rucio list-dids group.phys-hdbs.*r9364*040621*root | grep group | grep nom | cut -d '|' -f 2 | sed 's/ //g' | sort)
tmplist="${tmplist} $(rucio list-dids user.operrin:*r9364*040621*root | grep operrin | cut -d '|' -f 2 | sed 's/ //g' | sort)"
for it in ${tmplist};do
  echo ${it} >> ${outf}
done

#for mc16d
outf=mc16d_raw.txt
>${outf}
tmplist=$(rucio list-dids group.phys-hdbs.*r10201*040621*root | grep group | grep nom | cut -d '|' -f 2 | sed 's/ //g'| sort)
tmplist="${tmplist} $(rucio list-dids user.operrin:*r10201*040621*root | grep operrin | cut -d '|' -f 2 | sed 's/ //g'| sort)"
for it in ${tmplist};do
  echo ${it} >> ${outf}
done

#for mc16e
outf=mc16e_raw.txt
>${outf}
tmplist=$(rucio list-dids group.phys-hdbs.*r10724*040621*e2*root | grep group | grep -v sys_e2 | cut -d '|' -f 2 | sed 's/ //g' | grep -v data | sort)
for it in ${tmplist};do
  echo ${it} >> ${outf}
done
