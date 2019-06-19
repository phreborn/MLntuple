# HH-ML FW2
## How to run FW2 locally
HH-ML FW2 uses ttHML-GFW1 as an input. Pick a ttHML-GFW1 file and figure out what branches you want to be mirrored for your analysis.
(ttHML sample file: root://eosatlas.cern.ch:1094//eos/atlas/atlaslocalgroupdisk/dq2/rucio/group/phys-higgs/46/e3/group.phys-higgs.16493011._000001.output.root)

Add the identified branches to a text file. Alternatively you can use the official list of branches maintained in this software. 

### Setting up things
Use the setup script to setup things required for running
`source setup.sh`

Setup any ROOT release (prefereably newer than v6.10) and execute the following 

` python fw2_hhml.py -s branchList.txt <rootFile1>,<rootFile2>`

This will create an output file `output.root` which containes the ntuples and branches requested. 

## Running on the grid. 
