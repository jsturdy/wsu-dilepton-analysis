#!/bin/env python

# # keep a pointer to the original TCanvas constructor
# caninit = r.TCanvas.__init__

# # define a new TCanvas class (inheriting from the original one),
# # setting the memory ownership in the constructor
# class GarbageCollectionResistentCanvas(r.TCanvas):
#   def __init__(self, *args):
#     caninit(self,*args)
#     r.SetOwnership(self,False)

# # replace the old TCanvas class by the new one
# r.TCanvas = GarbageCollectionResistentCanvas

# # keep a pointer to the original TPad constructor
# padinit = r.TPad.__init__

# # define a new TPad class (inheriting from the original one),
# # setting the memory ownership in the constructor
# class GarbageCollectionResistentCanvas(r.TPad):
#   def __init__(self, *args):
#     padinit(self,*args)
#     r.SetOwnership(self,False)

# # replace the old TPad class by the new one
# r.TPad = GarbageCollectionResistentCanvas

# # keep a pointer to the original TH1D constructor
# th1dinit = r.TH1D.__init__

# # define a new TH1D class (inheriting from the original one),
# # setting the memory ownership in the constructor
# class GarbageCollectionResistentH1D(r.TH1D):
#   def __init__(self, *args):
#     th1dinit(self,*args)
#     r.SetOwnership(self,False)

# # replace the old TH1D class by the new one
# r.TH1D = GarbageCollectionResistentH1D

# # keep a pointer to the original TLegend constructor
# leginit = r.TLegend.__init__

# # define a new TLegend class (inheriting from the original one),
# # setting the memory ownership in the constructor
# class GarbageCollectionResistentLegend(r.TLegend):
#   def __init__(self, *args):
#     leginit(self,*args)
#     r.SetOwnership(self,False)

# # replace the old TLegend class by the new one
# r.TLegend = GarbageCollectionResistentLegend

# # keep a pointer to the original TFile constructor
# fileinit = r.TFile.__init__

# # define a new TFile class (inheriting from the original one),
# # setting the memory ownership in the constructor
# class GarbageCollectionResistentFile(r.TFile):
#   def __init__(self, *args):
#     fileinit(self,*args)
#     r.SetOwnership(self,False)

# # replace the old TFile class by the new one
# r.TFile = GarbageCollectionResistentFile

if __name__ == "__main__":
    import sys,os,re
    from optparse import OptionParser

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
    parser.add_option("--xroot", action="store_true", dest="xroot",
                      metavar="xroot",
                      help="[OPTIONAL] Access files over xrootd")
    parser.add_option("--etaphi", type="string", dest="etaphi",
                      metavar="etaphi", default="",
                      help="[OPTIONAL] Eta/Phi bin to use")
    parser.add_option("--algo", type="string", dest="algo",
                      metavar="algo", default="TuneP",
                      help="[OPTIONAL] Tracking algorithm to use")
    parser.add_option("--runperiod", type="string", dest="runperiod",
                      metavar="runperiod", default="2015",
                      help="[OPTIONAL] Running period (default is 2015)")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      metavar="debug",
                      help="[OPTIONAL] Debug mode")

    (options, args) = parser.parse_args()
    print options
    print args

    # from histograms import outputHistograms
    from wsuPythonUtils import checkRequiredArguments,etaphiexclusivebins,etaphiinclusivebins,etaphibins,getHistogram
    from wsuPyROOTUtils import *

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

    inputfile = None
    if (options.infile).find("root://") > -1:
        print "using TNetXNGFile for EOS access"
        inputfile = r.TNetXNGFile(options.infile,"read")
    else:
        inputfile = r.TFile(options.infile,"READ")
        pass

    if not inputfile.IsOpen() or inputfile.IsZombie():
        print "Unable to open %s"%(options.infile)
        exit(1)

    if options.etaphi not in etaphibins.keys():
        errmsg = "Invalid eta/phi option specified: %s.  Allowed options are:"%(options.etaphi)
        errmsg += etaphibins.keys()
        exit(1)
        pass

    etaphi = options.etaphi

    output = r.TFile(options.outfile,"RECREATE")
    output.cd()
    #looseCanvas    = r.TCanvas("loose",   "loose",   1600,900)
    #combinedCanvas = r.TCanvas("combined","combined",1600,900)
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

    tightmuons = [
        "TightMuon",
        "AntiTightMuon",
        ]

    ## upper/lower
    ## plus/minus
    cutmuons = [
        "upperPlus",
        "upperMinus",
        "looseMuLowerPlus",
        "looseMuLowerMinus",
        "tightMuLowerPlus",
        "tightMuLowerMinus",
        ]

    #looseCanvas.Divide(5,4)
    #combinedCanvas.Divide(5,4)

    #plus/upper is red
    paramsP = {"color":r.kRed,  "marker":r.kFullCross  , "stats":111111, "coords": {"x": [-1,-1], "y": [0.5,0.7]}}
    #minus/lower is blue
    paramsM = {"color":r.kBlue, "marker":r.kFullDiamond, "stats":111111, "coords": {"x": [-1,-1], "y": [0.7,0.9]}}

    if options.debug:
        print inputfile

    # for j,etaphi in enumerate(etaphibins):
    looseEtaPhiCanvas  = r.TCanvas("loose%s"%(etaphi),  "loose%s"%(etaphi),  1600,900)
    looseEtaPhiCanvas.Divide(5,4)

    looseMuPlusEtaPhi  = []
    looseMuMinusEtaPhi = []

    for i,hist in enumerate(histograms):
        # looseMuPlusEtaPhi  = endpointStudy.getHistogram(Null,inputfile.Get("%s/%s%s%s"%(etaphi,cutmuons[0],hist,etaphi))
        looseMuPlusEtaPhi.append(getHistogram(inputfile,options.etaphi,"%s%s"%(cutmuons[0],hist),"",
                                              "%s%s_%s_clone"%(cutmuons[0],hist,etaphi),debug))
        looseMuMinusEtaPhi.append(getHistogram(inputfile,options.etaphi,"%s%s"%(cutmuons[1],hist),"",
                                               "%s%s_%s_clone"%(cutmuons[1],hist,etaphi),debug))

        # combinedMuUpper = inputfile.Get("%s%s"%("upper",hist))
        # combinedMuLower = inputfile.Get("%s%s"%("lower",hist))

        # looseMuPlus  = looseMuPlusEtaPhi[i].Clone("looseMuPlus")
        # looseMuMinus = looseMuMinusEtaPhi[i].Clone("looseMuMinus")

        if hist == "Curve":
            # combinedMuUpper.Rebin(options.rebins)
            # combinedMuLower.Rebin(options.rebins)

            # looseMuPlus.Rebin(options.rebins)
            # looseMuMinus.Rebin(options.rebins)

            looseMuPlusEtaPhi[i].Rebin(options.rebins)
            looseMuMinusEtaPhi[i].Rebin(options.rebins)
            pass

        elif hist == "TrackPt":
            # combinedMuUpper.Rebin(5)
            # combinedMuLower.Rebin(5)

            # looseMuPlus.Rebin(5)
            # looseMuMinus.Rebin(5)

            looseMuPlusEtaPhi[i].Rebin(5)
            looseMuMinusEtaPhi[i].Rebin(5)
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
        ### set up the different pads, depending on plot mode
        pad = r.TPad("pad","pad",0.0,0.3,1.0,1.0)
        r.SetOwnership(pad,False)
        pad.Draw()
        looseEtaPhiCanvas.cd(i+1)
        ratiopad = r.TPad("Ratiopad","Ratiopad",0.0,0.0,1.0,0.3)
        r.SetOwnership(ratiopad,False)
        ratiopad.Draw()

        pad.cd()
        looseEtaPhiMax = max(looseMuMinusEtaPhi[i].GetMaximum(),looseMuPlusEtaPhi[i].GetMaximum())
        looseMuMinusEtaPhi[i].SetMaximum(looseEtaPhiMax*1.2)
        looseMuMinusEtaPhi[i].SetTitle(hist)
        looseMuMinusEtaPhi[i].Draw("ep0")
        looseMuPlusEtaPhi[i].Draw("ep0sames")
        r.gPad.Update()
        looseMuPlusEtaPhi[i]  = makeNicePlot(looseMuPlusEtaPhi[i], paramsP,debug)
        looseMuMinusEtaPhi[i] = makeNicePlot(looseMuMinusEtaPhi[i],paramsM,debug)
        r.gPad.Update()

        ratiopad.cd()
        ratiohist = looseMuPlusEtaPhi[i].Clone("%s_ratio"%(looseMuPlusEtaPhi[i].GetName()))
        ratiohist.Divide(looseMuMinusEtaPhi[i])
        r.SetOwnership(ratiohist,False)
        ratiohist.SetTitle("%s #mu^{+}/#mu^{-} ratio"%(hist))
        ratiohist.SetMarkerColor(r.kBlack)
        ratiohist.SetLineColor(r.kBlack)
        ratiohist.Draw("ep")
        ratiohist.SetMaximum(1.75)
        ratiohist.SetMinimum(0.5)

        ratioline = r.TLine(ratiohist.GetXaxis().GetXmin(), 1.0,
                            ratiohist.GetXaxis().GetXmax(), 1.0)
        ratioline.SetLineColor(r.kGreen)
        ratioline.SetLineWidth(2)
        r.SetOwnership(ratioline,False)
        ratioline.Draw("same")

        r.gPad.Update()
        # if options.debug:
        #     raw_input("enter to continue")
        #     pass
        #combinedCanvas.cd(i+1)
        #combinedMax = max(combinedMuLower.GetMaximum(),combinedMuUpper.GetMaximum())
        #combinedMuLower.SetMaximum(combinedMax*1.2)
        #combinedMuLower.Draw("ep0")
        #combinedMuUpper.Draw("ep0sames")
        #r.gPad.Update()
        #combinedMuUpper = makeNicePlot(combinedMuUpper,paramsP,debug)
        #combinedMuLower = makeNicePlot(combinedMuLower,paramsM,debug)
        #r.gPad.Update()
        if debug:
            print("End setup of {} histogram".format(hist))
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
    counterMuLower.Draw("ep0text")
    counterMuUpper.Draw("ep0samestext")
    r.gPad.Update()
    paramsP["stats"] = 11
    paramsP["coords"]["x"] = [0.8,0.9]
    paramsP["coords"]["y"] = [0.7,0.8]
    counterMuUpper = makeNicePlot(counterMuUpper,paramsP,debug)
    paramsM["stats"] = 11
    paramsM["coords"]["x"] = [0.8,0.9]
    paramsM["coords"]["y"] = [0.8,0.9]
    counterMuLower = makeNicePlot(counterMuLower,paramsM,debug)
    r.gPad.Update()

    #looseCanvas.Update()
    #combinedCanvas.Update()
    counterCanvas.Update()
    if options.debug:
        raw_input("enter to end")
    #looseCanvas.Write()
    #combinedCanvas.Write()
    counterCanvas.Write()
    output.Write()
    output.Close()
