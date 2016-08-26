#!/bin/env python
import sys,os,re
import ROOT as r

from optparse import OptionParser
#from histograms import outputHistograms
from wsuPythonUtils import checkRequiredArguments
from wsuPyROOTUtils import makeNicePlot

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog -i inputfile.root -o outputfile.root [-d]")
    parser.add_option("-i", "--infile", type="string", dest="infile",
                      metavar="infile",
                      help="[REQUIRED] Location of the input ROOT files")
    parser.add_option("-o", "--outfile", type="string", dest="outfile",
                      metavar="outfile",
                      help="[REQUIRED] Name of the output ROOT file")
    parser.add_option("-b", "--rebins", type="int", dest="rebins",
                      metavar="rebins", default=1,
                      help="[OPTIONAL] Number of bins to combine in the q/pT plot (default is 1)")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      metavar="debug",
                      help="[OPTIONAL] Debug mode")
    
    (options, args) = parser.parse_args()
    print options
    print args
    checkRequiredArguments(options, parser)

    debug = False

    r.gROOT.SetBatch(False)
    r.gErrorIgnoreLevel = r.kFatal

    if not options.debug:
        print "setting batch mode True"
        r.gROOT.SetBatch(True)
    else:
        print "setting batch mode False"
        r.gROOT.SetBatch(False)
        debug = True
        pass
    
    inputfile = r.TFile(options.infile,"READ")
    if not inputfile.IsOpen() or inputfile.IsZombie():
        print "Unable to open %s"%(options.infile)
        exit(1)

    output = r.TFile(options.outfile,"RECREATE")
    output.cd()
    looseCanvas    = r.TCanvas("loose",   "loose",   1600,900)
    #tightCanvas    = r.TCanvas("tight",   "tight",   1600,900)
    combinedCanvas = r.TCanvas("combined","combined",1600,900)
    counterCanvas  = r.TCanvas("counter", "counter", 1600,900)
    
    histograms = [
        "Chi2",
        "Ndof",
        "Charge",
        "TrackPt",
        "TrackEta",
        "TrackPhi",
        "PtRelErr",
        "Dz",
        "Dxy",
        "Curve",
        "ValidHits",
        "PixelHits",
        "TrackerHits",
        "ValidMuonHits",
        "MuonStationHits",
        "MatchedMuonStations",
        "TrackerLayersWithMeasurement",
        ]

    etaphibins = [
        "EtaPlusPhiMinus",
        "EtaPlusPhiZero",
        #"EtaPlusPhiPlus",
        "EtaMinusPhiMinus",
        "EtaMinusPhiZero",
        #"EtaMinusPhiPlus"
        ]

    tightmuons = [
        "TightMuon",
        "AntiTightMuon",
        ]
    cutmuons = [
        "looseMuLowerPlus",
        "looseMuLowerMinus",
        "tightMuLowerPlus",
        "tightMuLowerMinus",
        ]
    
    looseCanvas.Divide(5,4)
    combinedCanvas.Divide(5,4)

    #plus/upper is red
    paramsP = {"color":r.kRed,  "marker":r.kFullCross  , "stats":111111, "coords": {"x": [-1,-1], "y": [0.5,0.7]}}
    #minus/lower is blue
    paramsM = {"color":r.kBlue, "marker":r.kFullDiamond, "stats":111111, "coords": {"x": [-1,-1], "y": [0.7,0.9]}}

    if options.debug:
        print inputfile

    for j,etaphi in enumerate(etaphibins):
        looseEtaPhiCanvas  = r.TCanvas("loose%s"%(etaphi),  "loose%s"%(etaphi),  1600,900)
        looseEtaPhiCanvas.Divide(5,4)
        
        for i,hist in enumerate(histograms):
            looseMuPlusEtaPhi  = inputfile.Get("%s/%s%s%s"%(etaphi,cutmuons[0],hist,etaphi))
            looseMuMinusEtaPhi = inputfile.Get("%s/%s%s%s"%(etaphi,cutmuons[1],hist,etaphi))

            #combinedMuUpper = inputfile.Get("%s%s"%("upper",hist))
            #combinedMuLower = inputfile.Get("%s%s"%("lower",hist))
            
            #looseMuPlus  = looseMuPlusEtaPhi.Clone("looseMuPlus")
            #looseMuMinus = looseMuMinusEtaPhi.Clone("looseMuMinus")
            
            if hist == "Curve":
                #combinedMuUpper.Rebin(options.rebins)
                #combinedMuLower.Rebin(options.rebins)
                
                #looseMuPlus.Rebin(options.rebins)
                #looseMuMinus.Rebin(options.rebins)
            
                looseMuPlusEtaPhi.Rebin(options.rebins)
                looseMuMinusEtaPhi.Rebin(options.rebins)
                pass

            #looseCanvas.cd(i+1)
            #looseMax = max(looseMuMinus.GetMaximum(),looseMuPlus.GetMaximum())
            #looseMuMinus.SetMaximum(looseMax*1.2)
            #looseMuMinus.Draw("ep0")
            #looseMuPlus.Draw("ep0sames")
            #r.gPad.Update()
            #looseMuPlus = makeNicePlot(looseMuPlus,paramsP,debug)
            #looseMuMinus = makeNicePlot(looseMuMinus,paramsM,debug)
            #r.gPad.Update()

            looseEtaPhiCanvas.cd(i+1)
            looseEtaPhiMax = max(looseMuMinusEtaPhi.GetMaximum(),looseMuPlusEtaPhi.GetMaximum())
            looseMuMinusEtaPhi.SetMaximum(looseEtaPhiMax*1.2)
            looseMuMinusEtaPhi.SetTitle(hist)
            looseMuMinusEtaPhi.Draw("ep0")
            looseMuPlusEtaPhi.Draw("ep0sames")
            r.gPad.Update()
            looseMuPlusEtaPhi = makeNicePlot(looseMuPlusEtaPhi,paramsP,debug)
            looseMuMinusEtaPhi = makeNicePlot(looseMuMinusEtaPhi,paramsM,debug)
            r.gPad.Update()

            #combinedCanvas.cd(i+1)
            #combinedMax = max(combinedMuLower.GetMaximum(),combinedMuUpper.GetMaximum())
            #combinedMuLower.SetMaximum(combinedMax*1.2)
            #combinedMuLower.Draw("ep0")
            #combinedMuUpper.Draw("ep0sames")
            #r.gPad.Update()
            #combinedMuUpper = makeNicePlot(combinedMuUpper,paramsP,debug)
            #combinedMuLower = makeNicePlot(combinedMuLower,paramsM,debug)
            #r.gPad.Update()
            pass # end loop over histograms
        looseEtaPhiCanvas.Write()
        if options.debug:
            raw_input("enter to continue")
        
        pass
    # event counters after applying various cuts
    counterCanvas.cd()
    counterMuUpper = inputfile.Get("upperCounters")
    counterMuLower = inputfile.Get("lowerCounters")
    counterMuLower.SetTitle("Cut event counters")
    counterMuLower.Draw("ep0")
    counterMuUpper.Draw("ep0sames")
    r.gPad.Update()
    paramsP["stats"] = 11
    paramsP["coords"]["x"] = [0.8,0.9]
    paramsP["coords"]["y"] = [0.7,0.8]
    counterMuUpper = makeNicePlot(counterMuUpper,paramsP)
    paramsM["stats"] = 11
    paramsM["coords"]["x"] = [0.8,0.9]
    paramsM["coords"]["y"] = [0.8,0.9]
    counterMuLower = makeNicePlot(counterMuLower,paramsM)
    r.gPad.Update()
    
    looseCanvas.Update()
    #tightCanvas.Update()
    combinedCanvas.Update()
    counterCanvas.Update()
    if options.debug:
        raw_input("enter to end")
    #looseCanvas.Write()
    #combinedCanvas.Write()
    counterCanvas.Write()
    output.Write()
    output.Close()
