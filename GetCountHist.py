import ROOT,sys

def saveHists(OF_name):
    #inFileList = open("input.txt",'r')
    inFileList = open(sys.argv[1],'r')

    
    rooF_li         = [ROOT.TFile.Open(f.rstrip()) for f in inFileList.read().rsplit()]

    fout = ROOT.TFile.Open(OF_name,"RECREATE")
    fout.mkdir("loose")
    sumWeightsTotal = sum([x.Get("loose/Count").At(2) for x in rooF_li])
    totalEvents     = sum([x.Get("loose/Count").At(1) for x in rooF_li])

    '''Special normalization for ttH samples with anomalous weights
    a) remove all the events with |MC_weight|>3*xsect (implemented in ttHMlEventSaver_Base and ttHMlEventSaver
    b) correct the total SumOfWeights of the samples to account for the events that need removing, that is a factor:
    MC16a:
    all-had (345672): 0.584946
    all-had (345873): 0.618463

    semilep (345673): 0.574414
    semilep (345874): 0.749914

    dilep (345674):   0.597573
    dilep (345875):   0.585052
    MC16c:
    all-had (345672): 0.945295
    all-had (345873): 0.93462

    semilep (345673): 0.918635
    semilep (345874): 0.936733

    dilep (345674):   0.944321
    dilep (345875):   0.931735 
    '''

    sumw = rooF_li[0].sumWeights
    sumw.GetEntry(0)
    dsid    = sumw.dsid
    
    '''Do not want to open the nominal tree for every DSID'''
    runy    = 0 
    if dsid == 345672 or dsid == 345673 or dsid == 345674 or dsid == 345873 or dsid == 345874 or dsid == 345875:
        nom     = rooF_li[0].nominal
        nom.GetEntry(0)
        runy    = nom.RunYear

    mrgdTotalWght   = reduce(lambda x,y: x+y, [x.Get("loose/Count") for x in rooF_li])
    mrgdLHEWght     = ROOT.TH1D()
    if rooF_li[0].Get("loose/Count_LHE"): mrgdLHEWght     = reduce(lambda x,y: x+y, [x.Get("loose/Count_LHE") for x in rooF_li])

    
    print "Sample dsid: %d"%dsid
    print "Existing total weights: %.2f"%mrgdTotalWght.At(2)
    sumWeights  = mrgdTotalWght.At(2)
    if dsid == 345672:
        if runy == 2015 or runy ==2016:
            sumWeights = sumWeights * 0.584946
            mrgdLHEWght.Scale(0.584946)
        elif runy == 2017:
            sumWeights = sumWeights * 0.945295
            mrgdLHEWght.Scale(0.945295)

    if dsid == 345673:
        if runy == 2015 or runy == 2016: 
            sumWeights = sumWeights * 0.748776
            mrgdLHEWght.Scale(0.748776)
        elif runy == 2017 :
            sumWeights = sumWeights * 0.942676
            mrgdLHEWght.Scale(0.942676)

    if dsid == 345674:
        if runy == 2015 or runy ==2016 : 
            sumWeights = sumWeights * 0.597573
            mrgdLHEWght.Scale(0.597573)
        elif runy == 2017:
            sumWeights = sumWeights * 0.944321
            mrgdLHEWght.Scale(0.944321)

    if dsid == 345873:
        if runy == 2015 or runy == 2016:
            sumWeights = sumWeights * 0.618463
            mrgdLHEWght.Scale(0.618463)
        elif runy == 2017:
            sumWeights = sumWeights * 0.93462 
            mrgdLHEWght.Scale(0.93462)

    if dsid == 345874:
        if runy == 2015 or runy == 2016:
            sumWeights = sumWeights * 0.749914
            mrgdLHEWght.Scale(0.749914)
        elif runy == 2017:
            sumWeights = sumWeights * 0.936733 
            mrgdLHEWght.Scale(0.936733)

    if dsid == 345875:
        if runy == 2015 or runy == 2016:
            sumWeights = sumWeights* 0.585052
            mrgdLHEWght.Scale(0.585052)
        elif runy == 2017:
            sumWeights = sumWeights* 0.931735 
            mrgdLHEWght.Scale(0.931735)

    mrgdTotalWght.SetBinContent(2,sumWeights)
    print "Corrected total weights: %.2f"%mrgdTotalWght.At(2)

    
    fout.cd("loose")
    mrgdTotalWght.Write()
    mrgdLHEWght.Write()
    fout.Close()
    print 'totalWeights: %.2f'%mrgdTotalWght.At(2)
    
saveHists(sys.argv[2])
