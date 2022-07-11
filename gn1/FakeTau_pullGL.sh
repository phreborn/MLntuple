#!/bin/bash

### igrid

#for mc16a
outf=ft_mc16a_raw.txt
>${outf}
tmplist=$(rucio list-dids group.phys-hdbs.*.DAOD_HIGG8D1.*r9364*.HHML_260122_FakeTau_mc16a_v*_output_root | grep group | cut -d '|' -f 2 | sed 's/ //g'| sort)
for it in ${tmplist};do
  echo ${it} >> ${outf}
done

#for mc16d
outf=ft_mc16d_raw.txt
>${outf}
tmplist=$(rucio list-dids group.phys-hdbs.*.DAOD_HIGG8D1.*r10201*.HHML_260122_FakeTau_mc16d_v*_output_root | grep group | cut -d '|' -f 2 | sed 's/ //g'| sort)
for it in ${tmplist};do
  echo ${it} >> ${outf}
done

#for mc16e
outf=ft_mc16e_raw.txt
>${outf}
tmplist=$(rucio list-dids group.phys-hdbs.*.DAOD_HIGG8D1.*r10724*.HHML_260122_FakeTau_mc16e_v*_output_root | grep group | cut -d '|' -f 2 | sed 's/ //g'| sort)
for it in ${tmplist};do
  echo ${it} >> ${outf}
done
