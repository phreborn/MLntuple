#!/usr/bin/env python
import ROOT, sys,optparse,os,traceback,fnmatch
from progressbar import ProgressBar
from itertools import *
from array import array

def options():
    parser = optparse.OptionParser(description="HHML framework 2")
    parser.add_option("-s","--select_branches",dest="select_branches",type=str,help="text file containing list of branches",default='inBrList')
    #parser.add_option("-i","--inputFile",dest="input_file",type=str,help="Input ROOT File",default='')
    parser.add_option("-o","--outputFile",dest="output_file",type=str,help="Output ROOT File",default='output.root')
    parser.add_option("-t","--tree",dest="tree",type=str,help="Input/Output tree name",default='nominal')
    return parser.parse_args()

def selectBranches(brnchFileName,chain):
        try:
	    f=open(brnchFileName,'r')
        except Exception:
	    print traceback.print_exc()

        brLi=[x.rstrip('\n') for x in f.read().rsplit()]
	chain.SetBranchStatus("*",0)
	
	for x in brLi:
	    chain.SetBranchStatus(x,1)
	return chain

'''
Retrieve count histograms from each root file 
merge them and save it in the outputfile
'''
def getMrgdTotalWghts(filenames):
    rooF_li 		= [ROOT.TFile.Open(x) for x in filenames]
    mrgdTotalWght   	= reduce(lambda x,y: x+y, [x.Get("loose/Count") for x in rooF_li])
    mrgdLHEWght     	= ROOT.TH1D()
    if rooF_li[0].Get("loose/Count_LHE"):
         mrgdLHEWght     = reduce(lambda x,y: x+y, [x.Get("loose/Count_LHE") for x in rooF_li])
    return(mrgdTotalWght,mrgdLHEWght)



def main():
    ops,args = options()
    
    ch = ROOT.TChain(ops.tree)
    #The root files are given as argument to CLI. Add them to the chain
    if not len(args) >0:
	print "No input ROOT file specified"
	sys.exit()

    inRootFiles= []
    #inRootFiles = [x.split(',') for x in args]
    inRootFiles = filter(lambda arg: fnmatch.fnmatch(arg, '*.root*') , args)

    #try:
    #    [os.path.exists(x) for x in inRootFiles]
    #except Exception:
    #    traceback.print_exc()
    
    [ch.AddFile(x) for x in inRootFiles]
    ch.LoadTree(0)
    ch = selectBranches(ops.select_branches,ch)
	
    outfile = ROOT.TFile.Open(ops.output_file, 'RECREATE')

    newtree = ch.CloneTree(0)
    print "Merging weight histograms..."
    totalWghts, LHE_wghts = getMrgdTotalWghts(inRootFiles)
    print "done !"

    pbar = ProgressBar()
    for event in pbar(ch):
	newtree.Fill()
    newtree.AutoSave()
    ldir = outfile.mkdir('loose')
    ldir.WriteTObject(totalWghts)
    ldir.WriteTObject(LHE_wghts)
    outfile.Close()

main()
