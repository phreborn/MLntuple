#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
from array import array
from ROOT import *

camp = 'mc16a'
rootdir = "../gn2/%s/"%(camp)
inrfs = os.listdir(rootdir)

for rf in inrfs:
 if '.root' not in rf:
  inrfs.remove(rf)

tname = 'leptau'

for rf in inrfs:
  outrfname = "%s/%s"%(camp, rf)
  outrf = TFile(outrfname, 'recreate')
  print 'processing '+outrfname
 
  ch = TChain(tname)
  ch.AddFile(rootdir+rf)
  #ch.SetBranchStatus("*",0)

  Mlep0lep1 = array('d', [0])
  Mlep0tau0 = array('d', [0])
  Mlep1tau0 = array('d', [0])
  Mlep0jet0 = array('d', [0])
  Mlep1jet0 = array('d', [0])
  Mlep0jet1 = array('d', [0])
  Mlep1jet1 = array('d', [0])
  Mtau0jet0 = array('d', [0])
  Mtau0jet1 = array('d', [0])

  p_DR_l1_l2 = array('d', [0])
  p_DR_l1_j1 = array('d', [0])
  p_invMass_l1_j1 = array('d', [0])
  p_invMass_l1_j2 = array('d', [0])
  p_invMass_l2_j1 = array('d', [0])
  p_invMl2j1j2 = array('d', [0])
  p_invMCloserLepToTau = array('d', [0])
  p_drCloserJetToLeadLep = array('d', [0])
  p_invMCloserJetToLeadLep = array('d', [0])
  p_drCloserJetToLep2 = array('d', [0])
  p_LBoost2L_AngleTauJ1 = array('d', [0])
  p_LBoost2L_AngleTauJ2 = array('d', [0])
  p_LBoostL1Tau_DRL1J2 = array('d', [0])
  p_LBoostL2Tau_DRL2J1 = array('d', [0])
 
  ch.SetBranchStatus("*",1)
  outtree = ch.CloneTree(0)
  outtree.SetName('nominal')
  outtree.Branch("Mlep0tau0",Mlep0tau0,"Mlep0tau0/D")
  outtree.Branch("Mlep1tau0",Mlep1tau0,"Mlep1tau0/D")
  outtree.Branch("p_DR_l1_l2",p_DR_l1_l2,"p_DR_l1_l2/D")
  outtree.Branch("p_DR_l1_j1",p_DR_l1_j1,"p_DR_l1_j1/D")
  outtree.Branch("p_invMass_l1_j1",p_invMass_l1_j1,"p_invMass_l1_j1/D")
  outtree.Branch("p_invMass_l1_j2",p_invMass_l1_j2,"p_invMass_l1_j2/D")
  outtree.Branch("p_invMass_l2_j1",p_invMass_l2_j1,"p_invMass_l2_j1/D")
  outtree.Branch("p_invMl2j1j2",p_invMl2j1j2,"p_invMl2j1j2/D")
  outtree.Branch("p_invMCloserLepToTau",p_invMCloserLepToTau,"p_invMCloserLepToTau/D")
  outtree.Branch("p_drCloserJetToLeadLep",p_drCloserJetToLeadLep,"p_drCloserJetToLeadLep/D")
  outtree.Branch("p_invMCloserJetToLeadLep",p_invMCloserJetToLeadLep,"p_invMCloserJetToLeadLep/D")
  outtree.Branch("p_drCloserJetToLep2",p_drCloserJetToLep2,"p_drCloserJetToLep2/D")
  outtree.Branch("p_LBoost2L_AngleTauJ1",p_LBoost2L_AngleTauJ1,"p_LBoost2L_AngleTauJ1/D")
  outtree.Branch("p_LBoost2L_AngleTauJ2",p_LBoost2L_AngleTauJ2,"p_LBoost2L_AngleTauJ2/D")
  outtree.Branch("p_LBoostL1Tau_DRL1J2",p_LBoostL1Tau_DRL1J2,"p_LBoostL1Tau_DRL1J2/D")
  outtree.Branch("p_LBoostL2Tau_DRL2J1",p_LBoostL2Tau_DRL2J1,"p_LBoostL2Tau_DRL2J1/D")
 
  nEntries = ch.GetEntries()
  print nEntries
  for i in range(nEntries):
    ch.GetEntry(i)

#    if ch.nJets_OR_DL1r_77 < 2: continue

    VLlep_0 = TLorentzVector()
    VLlep_1 = TLorentzVector()
    VLtau_0 = TLorentzVector()
    VLjet_0 = TLorentzVector()
    VLjet_1 = TLorentzVector()
    VLlep_0.SetPtEtaPhiE(ch.lep_Pt_0, ch.lep_Eta_0, ch.lep_Phi_0, ch.lep_E_0)
    VLlep_1.SetPtEtaPhiE(ch.lep_Pt_1, ch.lep_Eta_1, ch.lep_Phi_1, ch.lep_E_1)
    VLtau_0.SetPtEtaPhiE(ch.tau_pt_0, ch.tau_eta_0, ch.tau_phi_0, ch.tau_E_0)
    VLjet_0.SetPtEtaPhiE(ch.lead_jetPt, ch.lead_jetEta, ch.lead_jetPhi, ch.lead_jetE)
    VLjet_1.SetPtEtaPhiE(ch.sublead_jetPt, ch.sublead_jetEta, ch.sublead_jetPhi, ch.sublead_jetE)

    leps = [VLlep_0, VLlep_1]
    taus = [VLtau_0]
    jets = [VLjet_0, VLjet_1]
 
    Mlep0lep1[0] = (VLlep_0 + VLlep_1).M()
    Mlep0tau0[0] = (VLlep_0 + VLtau_0).M()
    Mlep1tau0[0] = (VLlep_1 + VLtau_0).M()
    Mlep0jet0[0] = (VLlep_0 + VLjet_0).M()
    Mlep1jet0[0] = (VLlep_1 + VLjet_0).M()
    Mlep0jet1[0] = (VLlep_0 + VLjet_1).M()
    Mlep1jet1[0] = (VLlep_1 + VLjet_1).M()
    Mtau0jet0[0] = (VLtau_0 + VLjet_0).M()
    Mtau0jet1[0] = (VLtau_0 + VLjet_1).M()

### Bartek BDT inputs ###
    p_DR_l1_l2[0] = VLlep_0.DeltaR(VLlep_1)
    p_DR_l1_j1[0] = VLlep_0.DeltaR(VLjet_0)
    p_invMass_l1_j1[0] = (VLlep_0 + VLjet_0).M()
    p_invMass_l1_j2[0] = (VLlep_0 + VLjet_1).M()
    p_invMass_l2_j1[0] = (VLlep_1 + VLjet_0).M()
    p_invMl2j1j2[0] = (VLlep_1 + VLjet_0 + VLjet_1).M()

    minDR = 999
    for lep in leps:
      dr = abs(VLtau_0.DeltaR(lep))
      if dr < minDR: 
        p_invMCloserLepToTau[0] = (VLtau_0+lep).M()
        minDR = dr

    minDR = 999
    for jet in jets:
      dr = abs(VLlep_0.DeltaR(jet))
      if dr < minDR: 
        p_invMCloserJetToLeadLep[0] = (VLlep_0+jet).M()
        p_drCloserJetToLeadLep[0] = VLlep_0.DeltaR(jet)
        minDR = dr

    minDR = 999
    for jet in jets:
      dr = abs(VLlep_1.DeltaR(jet))
      if dr < minDR: 
        p_drCloserJetToLep2[0] = VLlep_1.DeltaR(jet)
        minDR = dr

    TLV_tau1_b1 = VLtau_0
    TLV_j1_b1 = VLjet_0
    TLV_j2_b1 = VLjet_1
    TLV_tau1_b1.Boost(-(VLlep_0+VLlep_1).BoostVector())
    TLV_j1_b1.Boost(-(VLlep_0+VLlep_1).BoostVector())
    TLV_j2_b1.Boost(-(VLlep_0+VLlep_1).BoostVector())
    p_LBoost2L_AngleTauJ1[0] = TLV_tau1_b1.Angle(TLV_j1_b1.Vect())
    p_LBoost2L_AngleTauJ2[0] = TLV_tau1_b1.Angle(TLV_j2_b1.Vect())

    TLV_Lep1_b2 = VLlep_0
    TLV_j2_b2 = VLjet_1
    TLV_Lep1_b2.Boost(-(VLlep_0 + VLtau_0).BoostVector())
    TLV_j2_b2.Boost(-(VLlep_0 + VLtau_0).BoostVector())
    p_LBoostL1Tau_DRL1J2[0] = TLV_Lep1_b2.DeltaR(TLV_j2_b2)

    TLV_Lep2_b2 = VLlep_1
    TLV_j1_b2 = VLjet_0
    TLV_Lep2_b2.Boost(-(VLlep_1 + VLtau_0).BoostVector())
    TLV_j1_b2.Boost(-(VLlep_1 + VLtau_0).BoostVector())
    p_LBoostL2Tau_DRL2J1[0] = TLV_Lep2_b2.DeltaR(TLV_j1_b2)
 
    outtree.Fill()
 
  outrf.cd()
  outtree.AutoSave()

  outrf.Close()
