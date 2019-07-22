#!/usr/bin/env python
import ROOT, sys,optparse,os,traceback,fnmatch
from itertools import *
from array import array

import warnings 
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )

def options():
    parser = optparse.OptionParser(description="HHML framework 2")
    parser.add_option("-s","--select_branches",dest="branches_file",type=str,help="text file containing list of branches",default='inBrList')
    #parser.add_option("-i","--inputFile",dest="input_file",type=str,help="Input ROOT File",default='')
    parser.add_option("-o","--outputFile",dest="output_file",type=str,help="Output ROOT File",default='output.root')
    parser.add_option("-t","--tree",dest="tree",type=str,help="Input/Output tree name",default='nominal')
    return parser.parse_args()

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

class CutSelector:
    def __init__(self,name,cut):
        self.name 	= name
	self.cutString  = cut

    def addORCut(self,cutString):
	if self.cutString:
	    self.cutString+="||(%s)"%cutString
	else:
	    self.cutString="(%s)"%cutString
    def addANDCut(self,cutString):
	if self.cutString:
	    self.cutString+="&&(%s)"%cutString
	else:
	    self.cutString="(%s)"%cutString

    def getCuts(self):
	return self.cutString
    
    def AND(obj):
        self.cutString="(%s)&&(%s)"%(self.cutString,obj.getCuts())

    def OR(obj):
        self.cutString="(%s)||(%s)"%(self.cutString,obj.getCuts())

class Analyze:
    def __init__(self,chain,outTreeName,outFile):
        self.chain 	= chain
	self.chain.LoadTree(0)

	self.newTree	= None
	self.outTreeName= outTreeName
	
	self.outFile	= outFile
        if os.path.exists('total_weights.root'):
            wghtFile = ROOT.TFile.Open('total_weights.root')
	    self.totalWghts,self.LHE_wghts = self.getMrgdTotalWghts(['total_weights.root'])
	    print 'Weight: ',self.totalWghts
	else:
    	    self.totalWghts, self.LHE_wghts = self.getMrgdTotalWghts(inRootFiles)
	    print "Weight from local file"


	##Dirty implementation
	from array import array 
	self.scale_nom = array('d', [0])
	

	#Write the sumweights Histograms to the output file
	#Check if the 'loose' folder already exist
	#if len([x.ReadObj() for x in self.outFile.GetListOfKeys() if x.ReadObj().GetName()=='loose']) ==0:
  	#    print "Merging weight histograms..."
    	#    ldir = self.outFile.mkdir('loose')
    	#    ldir.WriteTObject(self.totalWghts)
    	#    ldir.WriteTObject(self.LHE_wghts)
	#    ldir.Write()
    	#    print "done !"

    def getMrgdTotalWghts(self,filenames):
    	rooF_li 		= [ROOT.TFile.Open(x) for x in filenames]
    	mrgdTotalWght   	= reduce(lambda x,y: x+y, [x.Get("loose/Count") for x in rooF_li])
    	mrgdLHEWght     	= ROOT.TH1D()
    	if rooF_li[0].Get("loose/Count_LHE"):
            mrgdLHEWght     = reduce(lambda x,y: x+y, [x.Get("loose/Count_LHE") for x in rooF_li])
	mrgdLHEWght.SetDirectory(0)
	mrgdTotalWght.SetDirectory(0)
    	return(mrgdTotalWght,mrgdLHEWght)

    def selectBranches(self,brnchFileName):
        try:
    	    f=open(brnchFileName,'r')
        except Exception:
    	    print traceback.print_exc()
    
        brLi=[x.rstrip('\n') for x in f.read().rsplit()]
    	self.chain.SetBranchStatus("*",0)
    	
    	for x in brLi:
    	    self.chain.SetBranchStatus(x,1)

    def prepareSelection(self,brnchFileName,Cuts):
    	self.selectBranches(ops.branches_file)
	#Also turn the branches in cutformula
	import re
	cutVars = [x for x in re.findall(r'\w+',Cuts) if len(x)>=4]
	for x in cutVars:
	    self.chain.SetBranchStatus(x,1)
	self.chain.LoadTree(0)
	self.outFile.cd()
	self.newTree= self.chain.CloneTree(0)
	self.newTree.SetName(self.outTreeName)
	self.newTree.Branch("scale_nom",self.scale_nom,"scale_nom/D")

	self.treeFormula = ROOT.TTreeFormula("cut",Cuts,self.chain)
	self.chain.SetNotify(self.treeFormula)

    def execute(self):
	self.outFile.cd()
        for i in progressbar(xrange(ch.GetEntries()),"Progress"):
            self.chain.GetEntry(i)
	    self.scale_nom[0] = ch.mc_rawXSection*ch.mc_kFactor/self.totalWghts.At(2)
            if self.treeFormula.EvalInstance(): 
	        self.newTree.Fill()

    def finalize(self):
	self.outFile.cd()
	self.newTree.AutoSave()

if __name__ == '__main__': 

    ops,args = options()

    
    ch = ROOT.TChain(ops.tree)
    #The root files are given as argument to CLI. Add them to the chain
    if not len(args) >0:
	print "No input ROOT file specified"
	sys.exit()

    inRootFiles = []
    if len(args) ==1: 
        inRootFiles = args[0].split(',')
    else:
	inRootFiles = args

    print "Adding %d files to the TChain"%len(inRootFiles)

    [ch.AddFile(x) for x in inRootFiles]

    onelepCuts = CutSelector("1l","onelep_type>0")

    dilepCuts 	= CutSelector("2l","dilep_type>0")

    trilepCuts 	= CutSelector("3l","trilep_type>0")

    quadCuts = CutSelector("4l","quadlep_type>0")

    pentaCuts = CutSelector("5l","total_leptons>=5")

    outFile = ROOT.TFile.Open(ops.output_file,"RECREATE","",512)

    one_ana = Analyze(ch,"onelep",outFile)
    one_ana.prepareSelection(ops.branches_file,onelepCuts.getCuts())
    one_ana.execute()
    one_ana.finalize()

    di_ana = Analyze(ch,"dilep",outFile)
    di_ana.prepareSelection(ops.branches_file,dilepCuts.getCuts())
    di_ana.execute()
    di_ana.finalize()

    tri_ana = Analyze(ch,"trilep",outFile)
    tri_ana.prepareSelection(ops.branches_file,trilepCuts.getCuts())
    tri_ana.execute()
    tri_ana.finalize()

    quad_ana = Analyze(ch,"quadlep",outFile)
    quad_ana.prepareSelection(ops.branches_file,quadCuts.getCuts())
    quad_ana.execute()
    quad_ana.finalize()

    penta_ana = Analyze(ch,"pentalep",outFile)
    penta_ana.prepareSelection(ops.branches_file,pentaCuts.getCuts())
    penta_ana.execute()
    penta_ana.finalize()
