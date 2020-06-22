# HH-ML FW2
## How to run FW2 locally
HH-ML FW2 uses ttHML-GFW1 as an input. Pick a ttHML-GFW1 file and figure out what branches you want to be mirrored for your analysis.
(ttHML sample file: root://eosatlas.cern.ch:1094//eos/atlas/atlaslocalgroupdisk/dq2/rucio/group/phys-higgs/46/e3/group.phys-higgs.16493011._000001.output.root)

Add the identified branches to a text file. Alternatively you can use the official list of branches maintained in this software. 

### Setting up things
Use the setup script to setup things required for running
`source setup.sh`

To run the script execute the following 

` python fw2_hhml.py -s branchList.txt <rootFile1>,<rootFile2>`

This will create an output file `output.root` which containes the ntuples and branches requested. 

### Background samples 
#https://gitlab.cern.ch/atlasHTop/ttHMultiGFW2/tree/master/ttHMultilepton/share 

## Running on the grid. 

Run commmand: 

  source setup.sh

Job submission to the grid is recommended from lxplus machines due to the fact that GetCountHist.py script requires data files to calculate a number of total weighted events from a current dataset.
In the other case, the number of weighted events will be calculated from a single file from the current dataset and the sum of 1/scale_nom from all outputs will be necessary to obtain the total number of weighted events.  

For the run jobs use command below.

./grid_sub.sh sample_name vTag


e.g
./grid_sub.sh user.sparajul.364250.Sherpa.DAOD_HIGG8D1.e5894_s3126_r9364_r9315_p3983.2104_hhmlv2_mc16_a_output_root TEST_GFW2_V1

