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
            print("Weight from local file")


	##Dirty implementation
        from array import array
        self.scale_nom = array('d', [0])
        self.mc_channel_number = array('d', [0])
        self.pileupEventWeight_090 = array('d', [0])
        self.JVT_EventWeight = array('d', [0])
        self.mcWeightOrg = array('d', [0])

#        self.njets = array('i', [0])
#        self.jet_pt_0 = array('d', [0])
#        self.jet_eta_0 = array('d', [0])
#        self.jet_phi_0 = array('d', [0])
#        self.jet_e_0 = array('d', [0])
#        self.jet_pt_1 = array('d', [0])
#        self.jet_eta_1 = array('d', [0])
#        self.jet_phi_1 = array('d', [0])
#        self.jet_e_1 = array('d', [0])
	

	#Write the sumweights Histograms to the output file
	#Check if the 'loose' folder already exist
	#if len([x.ReadObj() for x in self.outFile.GetListOfKeys() if x.ReadObj().GetName()=='loose']) ==0:
  	#    print "Merging weight histograms..."
    	#    ldir = self.outFile.mkdir('loose')
    	#    ldir.WriteTObject(self.totalWghts)
    	#    ldir.WriteTObject(self.LHE_wghts)
	#    ldir.Write()
    	#    print "done !"
    # def getSumtotalEventsWeighted(self,filename):
    #     rFile = ROOT.TFile.Open(filename)
    #     print rFile
    #     weightTree = rFile.Get("sumWeights")
    #     vec = ROOT.std.vector('float')()
    #     weightTree.SetBranchAddress('totalEventsWeighted', vec)
    #
    #     for i in range(weightTree.GetEntries()):
    #         weightTree.GetEntry(i)
    #         print(vec.size())
    #     sumWeights = 1
    #
    #     return(sumWeights)

    def getMrgdTotalWghts(self,filenames):
    	rooF_li = [ROOT.TFile.Open(x) for x in filenames]
        #print "aa ",rooF_li[0]
        #print "aaa2 ",filenames[0]
        mrgdLHEWght = ROOT.TH1D()
        mrgdTotalWght = 1
        if filenames[0] == 'total_weights.root':
            #print "AAAABBB "
            mrgdTotalWght1 = reduce(lambda x, y: x + y, [x.Get("loose/Count") for x in rooF_li])
            if rooF_li[0].Get("loose/Count_LHE"):
                mrgdLHEWght     = reduce(lambda x,y: x+y, [x.Get("loose/Count_LHE") for x in rooF_li])
            #print "WWWW ",mrgdTotalWght1
            mrgdLHEWght.SetDirectory(0)
            mrgdTotalWght1.SetDirectory(0)
            mrgdTotalWght = mrgdTotalWght1.At(2)
            #print "FFF ", mrgdTotalWght
        else:
            totalSum=[]
            for w in rooF_li:
                #print("XXX ",w)
                # for events in weightTree:
                #     print events.totalEventsWeighted
                wdf = ROOT.RDataFrame("sumWeights",w)
                sumEvents= wdf.Sum("totalEventsWeighted").GetValue()
                totalSum.append(sumEvents)


            mrgdTotalWght = sum(totalSum)
        # mrgdTotalWght   	= reduce(lambda x,y: x+y, [x.Get("loose/Count") for x in rooF_li])
    	# if rooF_li[0].Get("loose/Count_LHE"):
        #     mrgdLHEWght     = reduce(lambda x,y: x+y, [x.Get("loose/Count_LHE") for x in rooF_li])
	    # mrgdLHEWght.SetDirectory(0)
    	# mrgdTotalWght.SetDirectory(0)
        print "bbb",mrgdTotalWght
        # print "CCCC ",
    #     print "RRR ",mrgdTotalWght
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
        self.newTree.Branch("mc_channel_number",self.mc_channel_number,"mc_channel_number/D")
        self.newTree.Branch("mcWeightOrg",self.mcWeightOrg,"mcWeightOrg/D")
        self.newTree.Branch("pileupEventWeight_090",self.pileupEventWeight_090,"pileupEventWeight_090/D")
        self.newTree.Branch("JVT_EventWeight",self.JVT_EventWeight,"JVT_EventWeight/D")

#        self.newTree.Branch("njets",self.njets,"njets/I")
#        self.newTree.Branch("jet_pt_0",self.jet_pt_0,"jet_pt_0/D")
#        self.newTree.Branch("jet_eta_0",self.jet_eta_0,"jet_eta_0/D")
#        self.newTree.Branch("jet_phi_0",self.jet_phi_0,"jet_phi_0/D")
#        self.newTree.Branch("jet_e_0",self.jet_e_0,"jet_e_0/D")
#        self.newTree.Branch("jet_pt_1",self.jet_pt_1,"jet_pt_1/D")
#        self.newTree.Branch("jet_eta_1",self.jet_eta_1,"jet_eta_1/D")
#        self.newTree.Branch("jet_phi_1",self.jet_phi_1,"jet_phi_1/D")
#        self.newTree.Branch("jet_e_1",self.jet_e_1,"jet_e_1/D")

        self.treeFormula = ROOT.TTreeFormula("cut",Cuts,self.chain)
        self.chain.SetNotify(self.treeFormula)

    def execute(self):
        self.outFile.cd()
        for i in progressbar(xrange(ch.GetEntries()),"Progress"):
            self.chain.GetEntry(i)
            # self.scale_nom[0] = ch.mc_rawXSection*ch.mc_kFactor/self.totalWghts.At(2)
            self.scale_nom[0] = 1.
            self.mc_channel_number[0] = ch.mcChannelNumber
            self.mcWeightOrg[0]= 1.
            self.pileupEventWeight_090[0] = 1.
            self.JVT_EventWeight[0] = 1.
            # print("WWW ",ch.mcChannelNumber)

#            self.njets[0] = ch.jet_pt.size()
#            self.jet_pt_0[0] = ch.jet_pt[0] if ch.jet_pt.size() > 0 else 0
#            self.jet_eta_0[0] = ch.jet_eta[0] if ch.jet_eta.size() > 0 else 0
#            self.jet_phi_0[0] = ch.jet_phi[0] if ch.jet_phi.size() > 0 else 0
#            self.jet_e_0[0] = ch.jet_e[0] if ch.jet_e.size() > 0 else 0
#            self.jet_pt_1[0] = ch.jet_pt[1] if ch.jet_pt.size() > 1 else 0
#            self.jet_eta_1[0] = ch.jet_eta[1] if ch.jet_eta.size() > 1 else 0
#            self.jet_phi_1[0] = ch.jet_phi[1] if ch.jet_phi.size() > 1 else 0
#            self.jet_e_1[0] = ch.jet_e[1] if ch.jet_e.size() > 1 else 0

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

    leptauCuts 	= CutSelector("2l","dilep_type>0 && tau_pt_0>0")

    outFile = ROOT.TFile.Open(ops.output_file,"RECREATE","",512)

    leptau_ana = Analyze(ch,"leptau",outFile)
    leptau_ana.prepareSelection(ops.branches_file,leptauCuts.getCuts())
    leptau_ana.execute()
    leptau_ana.finalize()
