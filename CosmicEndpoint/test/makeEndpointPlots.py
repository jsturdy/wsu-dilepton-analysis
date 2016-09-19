import sys,os

import ROOT as r
import numpy as np
import math

import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()

# keep a pointer to the original TCanvas constructor
caninit = r.TCanvas.__init__

# define a new TCanvas class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentCanvas(r.TCanvas):
  def __init__(self, *args):
    caninit(self,*args)
    r.SetOwnership(self,False)

# replace the old TCanvas class by the new one
r.TCanvas = GarbageCollectionResistentCanvas

# keep a pointer to the original TPad constructor
padinit = r.TPad.__init__

# define a new TPad class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentCanvas(r.TPad):
  def __init__(self, *args):
    padinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TPad class by the new one
r.TPad = GarbageCollectionResistentCanvas

# keep a pointer to the original TH1D constructor
th1dinit = r.TH1D.__init__

# define a new TH1D class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentH1D(r.TH1D):
  def __init__(self, *args):
    th1dinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TH1D class by the new one
r.TH1D = GarbageCollectionResistentH1D

# keep a pointer to the original TLegend constructor
leginit = r.TLegend.__init__

# define a new TLegend class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentLegend(r.TLegend):
  def __init__(self, *args):
    leginit(self,*args)
    r.SetOwnership(self,False)

# replace the old TLegend class by the new one
r.TLegend = GarbageCollectionResistentLegend

# keep a pointer to the original TFile constructor
fileinit = r.TFile.__init__

# define a new TFile class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentFile(r.TFile):
  def __init__(self, *args):
    fileinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TFile class by the new one
r.TFile = GarbageCollectionResistentFile

r.gROOT.SetBatch(True)
r.gErrorIgnoreLevel = r.kFatal

#infilename = "june30-shawn.tunep.pt100.uw.root"
infilename = "june30-shawn.tunep.pt200.uw.root"
#infilename = "june30-shawn.tracker.pt100.uw.root"
#infilename = "june30-shawn.tracker.pt200.uw.root"

infile = r.TFile(infilename,"read")

etaphibins = {
    "1All"             : "|#eta| < 0.9 && |#phi| < #pi",
    "3EtaPlus"         : "0 < #eta < 0.9 && |#phi| < #pi",
    "2EtaMinus"        : "-0.9 < #eta < 0 && |#phi| < #pi",
    # "PhiPlus"       : "|#eta| < 0.9 && #pi/3 < #phi < #pi",
    "7PhiZero"         : "|#eta| < 0.9 && -#pi/3 < #phi < #pi/3",
    "4PhiMinus"        : "|#eta| < 0.9 && -#pi < #phi < -#pi/3",
    "6EtaPlusPhiMinus" : "0 < #eta < 0.9 && -#pi < #phi < -#pi/3",
    "9EtaPlusPhiZero"  : "0 < #eta < 0.9 && -#pi/3 < #phi < #pi/3",
    #"EtaPlusPhiPlus" : "0 < #eta < 0.9 && #pi/3 < #phi < #pi",
    "5EtaMinusPhiMinus": "-0.9 < #eta < 0 && -#pi < #phi < -#pi/3",
    "8EtaMinusPhiZero" : "-0.9 < #eta < 0 && -#pi/3 < #phi < #pi/3",
    #"EtaMinusPhiPlus": "-0.9 < #eta < 0 && #pi/3 < #phi < #pi"
    }

etaphiexclusivebins = {
    "EtaPlusPhiMinus" :[2,1],
    "EtaPlusPhiZero"  :[2,2],
    "EtaPlusPhiPlus"  :[2,3],
    "EtaMinusPhiMinus":[1,1],
    "EtaMinusPhiZero" :[1,2],
    "EtaMinusPhiPlus" :[1,3],
    }

outcan = r.TCanvas("outcan","",1440,900)
outcan.Divide(3,3)

resultsHist = r.TH2D("resultsHist", "#Delta#kappa_{b} map: #eta vs. #phi",
                     2, -0.9, 0.9,
                     3, -math.pi, math.pi)

for i,etaphi in enumerate(sorted(etaphibins.keys())):
    outcan.cd(i+1)
    
    graphname  = "chi2_looseMuLower%s"%(etaphi[1:])
    prefitname = "preFitPoly_looseMuLower%s"%(etaphi[1:])
    fitname    = "fitPoly_looseMuLower%s"%(etaphi[1:])
    graph  = infile.Get(graphname)
    prefit = infile.Get(prefitname)
    fit    = infile.Get(fitname)

    print graphname
    print graph
    graph.SetTitle("#chi^{2} vs. #Delta#kappa_{b}: %s"%(etaphibins[etaphi]))
    graph.SetMarkerStyle(r.kFullDiamond)
    graph.SetMarkerSize(0.5)
    graph.Draw("ap")
    graph.GetYaxis().SetTitle("#chi^{2}")
    graph.GetXaxis().SetTitle("#Delta#kappa_{b} [c/TeV]")
    prefit.Draw("same")
    fit.SetLineColor(r.kGreen)
    fit.Draw("same")

    thelegend = r.TLegend(0.2,0.7,0.7,0.9)
    #thelegend.SetTextSize(0.025)
    thelegend.SetFillColor(0)
    thelegend.SetFillStyle(3000)

    value   = prefit.GetMinimum(-0.8,0.8)
    minbias = prefit.GetMinimumX(-0.8,0.8)
    lowerr  = prefit.GetX(value+1.0, -0.8,   minbias)
    uperr   = prefit.GetX(value+1.0, minbias, 0.8)
    thelegend.AddEntry(prefit,"pre-fit: #kappa_{b} = %2.4g^{+%2.4g}_{-%2.4g}"%( minbias,
                                                                                uperr-minbias,
                                                                                minbias-lowerr))
    value   = fit.GetMinimum(-0.8,0.8)
    minbias = fit.GetMinimumX(-0.8,0.8)
    lowerr  = fit.GetX(value+1.0, -0.8,   minbias)
    uperr   = fit.GetX(value+1.0, minbias, 0.8)
    thelegend.AddEntry(fit,   "post-fit: #kappa_{b} = %2.4g^{+%2.4g}_{-%2.4g}"%(minbias,
                                                                                uperr-minbias,
                                                                                minbias-lowerr))
    thelegend.Draw()

    graph.GetYaxis().SetRangeUser(value*0.8,value+25)
    r.gPad.Update()

    if etaphi in etaphiexclusivebins.keys():
        resultsHist.SetBinContent(etaphiexclusivebins[etaphi][0],etaphiexclusivebins[etaphi][1],minbias)
        resultsHist.SetBinError(  etaphiexclusivebins[etaphi][0],etaphiexclusivebins[etaphi][1],uperr-minbias)
        pass

    pass

outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_tunep_pt200.png")
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_tunep_pt200.pdf")
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_tunep_pt200.eps")
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_tunep_pt200.C"  )
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_tunep_pt200.png")
#raw_input("press enter to exit")
outcan.cd()
resultsHist.Draw("colztexte")
resultsHist.SetStats(r.kFALSE)
resultsHist.GetXaxis().SetBinLabel(1,"-0.9 < #eta < 0")
resultsHist.GetXaxis().SetBinLabel(2,"0 < #eta < 0.9")
resultsHist.GetYaxis().SetBinLabel(1,"-#pi < #phi < -#pi/3")
resultsHist.GetYaxis().SetBinLabel(2,"-#pi/3 < #phi < #pi/3")
resultsHist.GetYaxis().SetBinLabel(3,"-#pi/3 < #phi < #pi")
r.gPad.Update()
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_2d_map_tunep_pt200.png")
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_2d_map_tunep_pt200.pdf")
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_2d_map_tunep_pt200.eps")
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_2d_map_tunep_pt200.C"  )
outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/results_2d_map_tunep_pt200.png")
#raw_input("press enter to exit")

pr.disable()
#s = StringIO.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print s.getvalue()
