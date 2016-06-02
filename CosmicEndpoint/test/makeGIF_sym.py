#!/bin/env python

import ROOT as r
import sys,os
import numpy as np

from optparse import OptionParser
from wsuPythonUtils import *

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog -i inputfile.root --p100infile p100inputfile.root --p500infile p500inputfile.root -o outputfile.root [-d]")
    parser.add_option("-i", "--infile", type="string", dest="infile",
                      metavar="infile",
                      help="[REQUIRED] Location of the input ROOT files")
    parser.add_option("--p100infile", type="string", dest="p100infile",
                      metavar="p100infile",
                      help="[REQUIRED] Location of the comparison input p100 ROOT file")
    parser.add_option("--p500infile", type="string", dest="p500infile",
                      metavar="p500infile",
                      help="[REQUIRED] Location of the comparison input p500 ROOT file")
    parser.add_option("-b", "--rebins", type="int", dest="rebins",
                      metavar="rebins", default=1,
                      help="[OPTIONAL] Number of bins to combine in the q/pT plot (default is 1)")
    parser.add_option("-n", "--biasbins", type="int", dest="biasbins",
                      metavar="biasbins", default=1000,
                      help="[OPTIONAL] Total number of injected bias points (default is 1000)")
    parser.add_option("-t", "--totalbins", type="int", dest="totalbins",
                      metavar="totalbins", default=5000,
                      help="[OPTIONAL] Total number of bins in the original curvature distribution (default is 5000)")
    parser.add_option("-m", "--maxbias", type="float", dest="maxbias",
                      metavar="maxbias", default=0.1,
                      help="[OPTIONAL] Maximum injected bias (default is 0.1 c/TeV)")
    parser.add_option("-s", "--stepsize", type="int", dest="stepsize",
                      metavar="stepsize", default=1,
                      help="[OPTIONAL] Step size in the GIF (default is 1)")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      metavar="debug",
                      help="[OPTIONAL] Debug mode")
    parser.add_option("--histbase", type="string", dest="histbase",
                      metavar="histbase", default="looseMuLower",
                      help="[OPTIONAL] Base name of the histogram object (default is \"looseMuLower\")")
    parser.add_option("--study", type="string", dest="study",
                      metavar="study", default="pm",
                      help="[OPTIONAL]  Study to perform (default is \"pm\", options are: \"pm\",\"dmc[a-h]\")")
    parser.add_option("--minpt", type="float", dest="minpt",
                      metavar="minpt", default=200.,
                      help="[OPTIONAL] Minimum pT cut to apply in the curvature plots (default is 200 c/TeV)")
    parser.add_option("--residuals", action="store_true", dest="residuals",
                      metavar="residuals",
                      help="[OPTIONAL] Display residuals")
    parser.add_option("--etaphi", type="string", dest="etaphi",
                      metavar="etaphi", default="",
                      help="[OPTIONAL] Eta/Phi bin to use")

    ## Need to be able to combine multiple MC samples together
    # - p10, p100, p500
    # - p100, p500: scale p100 by (1028051./58898.)
    p100top500ScaleFactor = 1028051./58898.

    ## binning options
    # - bin in eta (positive/negative)
    # - bin in phi [-pi, -pi/3, pi/3, pi]
    # - bin in eta/and phi
    # - inclusive

    ## back burner ##
    # want to do several studies
    # 1) compare plus to minus (in data or MC, separately, scaling minus to plus)
    # 2) compare data to MC (varying the bias in MC)
    #   requires two input files
    #   scaling will be done as follows
    #   a) scaling MC to data (integral before cutting on pT) at each bias step
    #   b) scaling MC to data (integral before cutting on pT) for the unbiased histograms
    #   c) scaling MC to data (integral after cutting on pT) at each bias step
    #   d) scaling MC to data (integral after cutting on pT) for the unbiased histograms
    #   e-h) perform the scaling on the plus and minus separately, but follow the steps from above
    # may want to manually move the entries that migrate from plus to minus?

    (options, args) = parser.parse_args()
    print options
    print args

    if options.study not in ["pm","dmca","dmcb","dmcc","dmcd","dmce","dmcf","dmcg","dmch"]:
        print "Invalid study specified: %s. Valid options are \"pm\" or \"dmc[a-h]\""%(options.study)
        exit(1)
        pass

    if options.study in ["dmca","dmcb","dmcc","dmcd","dmce","dmcf","dmcg","dmch"] and options.infile2 == None:
        print "Must specify second input file for \"dmc\"-type study"
        exit(1)
        pass

    r.gROOT.SetBatch(False)
    if not options.debug:
        print "setting batch mode True"
        r.gROOT.SetBatch(True)
    else:
        print "setting batch mode False"
        r.gROOT.SetBatch(False)
        pass
    
    checkRequiredArguments(options, parser)
    
    etaphibins = ["", "EtaPlus", "EtaMinus",
                  "EtaPlusPhiMinus","EtaPlusPhiZero","EtaPlusPhiPlus",
                  "EtaMinusPhiMinus","EtaMinusPhiZero","EtaMinusPhiPlus"
                  ]
    if options.etaphi not in etaphibins:
        print "Invalid eta/phi bin specified: %s"%(options.etaphi)
        print "Allowed options are:"
        print etaphibins
        exit(0)

    myInFileName = options.infile
    myInFile = r.TFile(myInFileName,"READ")

    p100InFileName = options.p100infile
    p100InFile = r.TFile(p100InFileName,"READ")
    
    p500InFileName = options.p500infile
    p500InFile = r.TFile(p500InFileName,"READ")
    
    gifDir = "sampleGif"
    histName = options.histbase

    testHist = myInFile.Get("%s%s%s"%(histName,"PlusCurve",options.etaphi)).Clone("test")
    testHist = setMinPT(testHist,options.totalbins,options.minpt/1000.,True)
    testHist.Rebin(options.rebins)
    refmax = testHist.GetMaximum()

    #need two arrays, length = (2*nBiasBins)+1
    xVals = np.zeros(2*options.biasbins/options.stepsize+1,np.dtype('float64'))
    
    legLabel = {}
    legLabel["pm"] = {}
    
    yVals = {}
    for test in ["KS","Chi2"]:
        yVals[test] = np.zeros(2*options.biasbins/options.stepsize+1,np.dtype('float64'))
        pass

    gifcanvas = r.TCanvas("gifcanvas","gifcanvas",750,750)

    pad    = None
    resPad = None
    if options.residuals:
        pad = r.TPad("pad","pad",0.0,0.3,1.0,1.0)
        pad.Draw()
        gifcanvas.cd()
        resPad = r.TPad("Respad","Respad",0.0,0.0,1.0,0.3)
        resPad.Draw()
    pass

    r.gStyle.SetOptStat(0)
    print histName
    ## use data histogram as reference
    plusRefHist  = myInFile.Get("%s%s%s"%(histName,"MinusCurve",options.etaphi))
    minusRefHist = myInFile.Get("%s%s%s"%(histName,"PlusCurve", options.etaphi))

    refHist = plusRefHist.Clone("%s_refHist"%(histName))
    refHist.Add(minusRefHist)

    refHist.Rebin(options.rebins)
    refHist = setMinPT(refHist,options.totalbins,options.minpt/1000.,True)

    refinto = refHist.Integral()
    refinta = refHist.Integral()
    refHist.SetLineColor(r.kBlue)
    refHist.SetLineWidth(2)

    # doing the "pm" study (comparing plus to minus in data or MC separately)
    #if options.study == "pm":
    for step in range(0,options.biasbins/options.stepsize):
        gifcanvas.cd()

        plusHistp100  = p100InFile.Get("%s%s%sMinusBias%03d"%(histName,"PlusCurve", options.etaphi,
                                                              options.biasbins-step*options.stepsize))
        minusHistp100 = p100InFile.Get("%s%s%sMinusBias%03d"%(histName,"MinusCurve",options.etaphi,
                                                              options.biasbins-step*options.stepsize))
        plusHistp100.Scale(p100top500ScaleFactor)
        minusHistp100.Scale(p100top500ScaleFactor)
        
        plusHistp500  = p500InFile.Get("%s%s%sMinusBias%03d"%(histName,"PlusCurve", options.etaphi,
                                                            options.biasbins-step*options.stepsize))
        minusHistp500 = p500InFile.Get("%s%s%sMinusBias%03d"%(histName,"MinusCurve",options.etaphi,
                                                            options.biasbins-step*options.stepsize))
        
        plusHist  = plusHistp500.Clone("%s%s_combined_MinusBias%03d"%(histName,"PlusCurve",
                                                                      options.biasbins-step*options.stepsize))
        plusHist.Add(plusHistp100)

        minusHist = minusHistp500.Clone("%s%s_combined_MinusBias%03d"%(histName,"MinusCurve",
                                                                       options.biasbins-step*options.stepsize))
        minusHist.Add(minusHistp100)
        
        compHist = plusHist.Clone("%s_compHist_MinusBias%03d"%(histName,options.biasbins-step*options.stepsize))
        compHist.Add(minusHist)

        if options.debug:
            print "refNBins %d, compNBins %d"%(refHist.GetNbinsX(),compHist.GetNbinsX())
        compHist.Rebin(options.rebins)
        compHist = setMinPT(compHist,options.totalbins,options.minpt/1000.,True)
        compinto = compHist.Integral()
        if (compHist.Integral() > 0):
            compHist.Scale(refHist.Integral()/compHist.Integral())
        else:
            print "unable to scale comp histogram, integral is 0"
            pass
        compinta = compHist.Integral()
        compHist.SetTitle("#Delta#kappa = %2.4f [c/TeV]"%(-(options.maxbias/options.biasbins)*(options.biasbins-step*options.stepsize)))
        compHist.SetLineColor(r.kRed)
        compHist.SetLineWidth(2)
        if options.residuals:
            pad.cd()
        compHist.Draw()
        compHist.GetXaxis().SetTitle("#kappa [c/TeV]")
        compHist.SetMaximum(1.2*refmax)
        compHist.SetMinimum(0.001)
        refHist.Draw("sames")

        r.gPad.Update()

        #compHist.FindObject("stats").SetOptStat(0)
        #refHist.FindObject("stats").SetOptStat(0)

        r.gPad.Update()
        chi2Val  = r.Double(0.) # necessary for pass-by-reference in python
        chi2ndf  = r.Long(0)    # necessary for pass-by-reference in python
        igood    = r.Long(0)    # necessary for pass-by-reference in python
        histopts = "UU,NORM" # unweighted/weighted, normalized
        resids = np.zeros(refHist.GetNbinsX(),np.dtype('float64')) # pointer argument, one per bin, not quite working
        ## if doing pm study, use flipHist
        #prob   = refHist.Chi2TestX(flipHist(compHist),chi2Val,chi2ndf,igood,histopts,resids)
        #ksprob = refHist.KolmogorovTest(flipHist(compHist),"D")

        # else add plus to minus
        prob   = refHist.Chi2TestX(compHist,chi2Val,chi2ndf,igood,histopts,resids)
        ksprob = refHist.KolmogorovTest(compHist,"D")

        if options.residuals:
            resHist = r.TH1D("ResHist", "ResHist", len(resids), -8.0,8.0)
            resHist.Sumw2();
            for i,res in enumerate(resids):
                if options.debug:
                    print "residual %d = %2.4f"%(i,res)
                    pass
                resHist.SetBinContent(i+1, res)
                pass
            resPad.cd()
            resHist.SetLineColor(r.kBlack)
            resHist.SetLineWidth(2)
            resHist.SetMarkerColor(r.kBlack)
            resHist.SetMarkerStyle(r.kFullDiamond)
            resHist.SetMarkerSize(1)
            resHist.Draw("ep0")
            resHist.SetMaximum(15.)
            resHist.SetMinimum(-15.)
            pass

        xVals[step] = -(options.maxbias/options.biasbins)*(options.biasbins-step*options.stepsize)
        yVals["Chi2"][step] = chi2Val/chi2ndf

        yVals["KS"][step]   = ksprob

        thetext = r.TPaveText(0.4,0.8,0.6,0.9,"ndc")
        thetext.SetFillColor(0)
        thetext.SetFillStyle(3000)
        thetext.AddText("#chi^{2}/ndf = %2.2f(%2.2f/%d)"%(chi2Val/chi2ndf,chi2Val,chi2ndf))
        thetext.AddText("KS prob = %2.4e"%(ksprob))
        thelegend = r.TLegend(0.4,0.7,0.6,0.8)
        thelegend.SetFillColor(0)
        thelegend.SetFillStyle(3000)

        thelegend.AddEntry(refHist, "data (%d,%d)"%(refinto,refinta))
        thelegend.AddEntry(compHist,"MC (%d,%d)"%(compinto,compinta))

        gifcanvas.cd()
        if options.residuals:
            pad.cd()
        thetext.Draw("nb")
        thelegend.Draw()
        r.gPad.Update()
        gifcanvas.SaveAs("%s/%sbiasBin%04d_sym.png"%(gifDir,options.etaphi,step*options.stepsize))
        pass

    if options.debug:
        raw_input("press enter to exit")
        pass
    gifcanvas.cd()

    plusHistp100  = p100InFile.Get("%s%s%s"%(histName,"PlusCurve",options.etaphi))
    minusHistp100 = p100InFile.Get("%s%s%s"%(histName,"MinusCurve",options.etaphi))
    plusHistp100.Scale(p100top500ScaleFactor)
    minusHistp100.Scale(p100top500ScaleFactor)

    plusHistp500  = p500InFile.Get("%s%s%s"%(histName,"PlusCurve",options.etaphi))
    minusHistp500 = p500InFile.Get("%s%s%s"%(histName,"MinusCurve",options.etaphi))
    
    plusHist  = plusHistp500.Clone("%s%s_combined"%(histName,"PlusCurve"))
    plusHist.Add(plusHistp100)

    minusHist = minusHistp500.Clone("%s%s_combined"%(histName,"MinusCurve"))
    minusHist.Add(minusHistp100)

    compHist = plusHist.Clone("%s_compHist"%(histName))
    compHist.Add(minusHist)

    if options.debug:
        print "refNBins %d, compNBins %d"%(refHist.GetNbinsX(),compHist.GetNbinsX())
    compHist.Rebin(options.rebins)
    compHist = setMinPT(compHist,options.totalbins,options.minpt/1000.,True,True)
    compinto = compHist.Integral()
    if (compHist.Integral() > 0):
        compHist.Scale(refHist.Integral()/compHist.Integral())
    else:
        print "unable to scale comp histogram, integral is 0"
        pass
    compinta = compHist.Integral()
    compHist.SetTitle("#Delta#kappa = %2.4f [c/TeV]"%(0))
    compHist.SetLineColor(r.kRed)
    compHist.SetLineWidth(2)
    if options.residuals:
        pad.cd()
    compHist.Draw()
    compHist.GetXaxis().SetTitle("#kappa [c/TeV]")
    compHist.SetMaximum(1.2*refmax)
    compHist.SetMinimum(0.001)
    refHist.Draw("sames")

    r.gPad.Update()

    #compHist.FindObject("stats").SetOptStat(0)
    #refHist.FindObject("stats").SetOptStat(0)

    r.gPad.Update()
    chi2Val  = r.Double(0.) # necessary for pass-by-reference in python
    chi2ndf  = r.Long(0)    # necessary for pass-by-reference in python
    igood    = r.Long(0)    # necessary for pass-by-reference in python
    histopts = "UU,NORM" # unweighted/weighted, normalized
    resids = np.zeros(refHist.GetNbinsX(),np.dtype('float64')) # pointer argument, one per bin, not quite working
    ## if doing pm study, use flipHist
    #prob   = refHist.Chi2TestX(flipHist(compHist),chi2Val,chi2ndf,igood,histopts,resids)
    #ksprob = refHist.KolmogorovTest(flipHist(compHist),"D")
    
    # else add plus to minus
    prob   = refHist.Chi2TestX(compHist,chi2Val,chi2ndf,igood,histopts,resids)
    ksprob = refHist.KolmogorovTest(compHist,"D")

    if options.residuals:
        resHist = r.TH1D("ResHist", "ResHist", len(resids), -8.0,8.0)
        resHist.Sumw2();
        for i,res in enumerate(resids):
            if options.debug:
                print "residual %d = %2.4f"%(i,res)
                pass
            resHist.SetBinContent(i+1, res)
            pass
        resPad.cd()
        resHist.SetLineColor(r.kBlack)
        resHist.SetLineWidth(2)
        resHist.SetMarkerColor(r.kBlack)
        resHist.SetMarkerStyle(r.kFullDiamond)
        resHist.SetMarkerSize(1)
        resHist.Draw("ep0")
        resHist.SetMaximum(15.)
        resHist.SetMinimum(-15.)
        pass

    xVals[options.biasbins/options.stepsize] = 0.0
    yVals["Chi2"][options.biasbins/options.stepsize] = chi2Val/chi2ndf

    yVals["KS"][options.biasbins/options.stepsize]   = ksprob
    
    thetext = r.TPaveText(0.4,0.8,0.6,0.9,"ndc")
    thetext.SetFillColor(0)
    thetext.SetFillStyle(3000)
    thetext.AddText("#chi^{2}/ndf = %2.2f(%2.2f/%d)"%(chi2Val/chi2ndf,chi2Val,chi2ndf))
    thetext.AddText("KS prob = %2.4e"%(ksprob))
    thelegend = r.TLegend(0.4,0.7,0.6,0.8)
    thelegend.SetFillColor(0)
    thelegend.SetFillStyle(3000)

    thelegend.AddEntry(refHist,"data (%d,%d)"%(refinto,refinta))
    thelegend.AddEntry(compHist,"MC (%d,%d)"%(compinto,compinta))

    gifcanvas.cd()
    if options.residuals:
        pad.cd()
    thetext.Draw("nb")
    thelegend.Draw()
    r.gPad.Update()
    gifcanvas.SaveAs("%s/%sbiasBin%04d_sym.png"%(gifDir,options.etaphi,options.biasbins))

    if options.debug:
        raw_input("press enter to exit")
        pass

    for step in range(0,options.biasbins/options.stepsize):
        gifcanvas.cd()

        plusHistp100  = p100InFile.Get("%s%s%sPlusBias%03d"%(histName,"PlusCurve", options.etaphi,(1+step)*options.stepsize))
        minusHistp100 = p100InFile.Get("%s%s%sPlusBias%03d"%(histName,"MinusCurve",options.etaphi,(1+step)*options.stepsize))
        plusHistp100.Scale(p100top500ScaleFactor)
        minusHistp100.Scale(p100top500ScaleFactor)
        
        plusHistp500  = p500InFile.Get("%s%s%sPlusBias%03d"%(histName,"PlusCurve", options.etaphi,(1+step)*options.stepsize))
        minusHistp500 = p500InFile.Get("%s%s%sPlusBias%03d"%(histName,"MinusCurve",options.etaphi,(1+step)*options.stepsize))
        
        plusHist  = plusHistp500.Clone("%s%s_combined_PlusBias%03d"%(histName,"PlusCurve",(1+step)*options.stepsize))
        plusHist.Add(plusHistp100)

        minusHist = minusHistp500.Clone("%s%s_combined_PlusBias%03d"%(histName,"MinusCurve",(1+step)*options.stepsize))
        minusHist.Add(minusHistp100)
        
        compHist = plusHist.Clone("%s_compHist_PlusBias%03d"%(histName,(1+step)*options.stepsize))
        compHist.Add(minusHist)

        if options.debug:
            print "refNBins %d, compNBins %d"%(refHist.GetNbinsX(),compHist.GetNbinsX())
        compHist.Rebin(options.rebins)
        compHist = setMinPT(compHist,options.totalbins,options.minpt/1000.,True)
        compinto = compHist.Integral()
        if (compHist.Integral() > 0):
            compHist.Scale(refHist.Integral()/compHist.Integral())
        else:
            print "unable to scale comp histogram, integral is 0"
            pass
        compinta = compHist.Integral()
        compHist.SetTitle("#Delta#kappa = %2.4f [c/TeV]"%((options.maxbias/options.biasbins)*((step+1)*options.stepsize)))
        compHist.SetLineColor(r.kRed)
        compHist.SetLineWidth(2)
        if options.residuals:
            pad.cd()
        compHist.Draw()
        compHist.GetXaxis().SetTitle("#kappa [c/TeV]")
        compHist.SetMaximum(1.2*refmax)
        compHist.SetMinimum(0.001)
        refHist.Draw("sames")

        r.gPad.Update()

        #compHist.FindObject("stats").SetOptStat(0)
        #refHist.FindObject("stats").SetOptStat(0)

        r.gPad.Update()
        chi2Val  = r.Double(0.) # necessary for pass-by-reference in python
        chi2ndf  = r.Long(0)    # necessary for pass-by-reference in python
        igood    = r.Long(0)    # necessary for pass-by-reference in python
        histopts = "UU,NORM" # unweighted/weighted, normalized
        resids = np.zeros(refHist.GetNbinsX(),np.dtype('float64')) # pointer argument, one per bin, not quite working
        ## if doing pm study, use flipHist
        #prob   = refHist.Chi2TestX(flipHist(compHist),chi2Val,chi2ndf,igood,histopts,resids)
        #ksprob = refHist.KolmogorovTest(flipHist(compHist),"D")

        # else add plus to minus
        prob   = refHist.Chi2TestX(compHist,chi2Val,chi2ndf,igood,histopts,resids)
        ksprob = refHist.KolmogorovTest(compHist,"D")

        if options.residuals:
            resHist = r.TH1D("ResHist", "ResHist", len(resids), -8.0,8.0)
            resHist.Sumw2();
            for i,res in enumerate(resids):
                if options.debug:
                    print "residual %d = %2.4f"%(i,res)
                    pass
                resHist.SetBinContent(i+1, res)
                pass
            resPad.cd()
            resHist.SetLineColor(r.kBlack)
            resHist.SetLineWidth(2)
            resHist.SetMarkerColor(r.kBlack)
            resHist.SetMarkerStyle(r.kFullDiamond)
            resHist.SetMarkerSize(1)
            resHist.Draw("ep0")
            resHist.SetMaximum(15.)
            resHist.SetMinimum(-15.)
            pass

        xVals[options.biasbins/options.stepsize+1+step] = (options.maxbias/options.biasbins)*((step+1)*options.stepsize)
        yVals["Chi2"][options.biasbins/options.stepsize+1+step] = chi2Val/chi2ndf

        yVals["KS"][options.biasbins/options.stepsize+1+step]   = ksprob

        thetext = r.TPaveText(0.4,0.8,0.6,0.9,"ndc")
        thetext.SetFillColor(0)
        thetext.SetFillStyle(3000)
        thetext.AddText("#chi^{2}/ndf = %2.2f(%2.2f/%d)"%(chi2Val/chi2ndf,chi2Val,chi2ndf))
        thetext.AddText("KS prob = %2.4e"%(ksprob))
        thelegend = r.TLegend(0.4,0.7,0.6,0.8)
        thelegend.SetFillColor(0)
        thelegend.SetFillStyle(3000)

        thelegend.AddEntry(refHist, "data (%d,%d)"%(refinto,refinta))
        thelegend.AddEntry(compHist,"MC (%d,%d)"%(compinto,compinta))

        gifcanvas.cd()
        if options.residuals:
            pad.cd()
        thetext.Draw("nb")
        thelegend.Draw()
        r.gPad.Update()
        gifcanvas.SaveAs("%s/%sbiasBin%04d_sym.png"%(gifDir,options.etaphi,options.biasbins+(1+step)*options.stepsize))
        pass
    
    if options.debug:
        raw_input("press enter to exit")
        pass


    graphInfo = {}
    graphInfo["KS"]   = {"color":r.kRed,"marker":r.kFullCircle,
                         "title":"Kolmogorov test statistic",
                         "yaxis":""}
    graphInfo["Chi2"] = {"color":r.kBlue, "marker":r.kFullCircle,
                         "title":"ROOT #chi^{2}/ndf",
                         "yaxis":""}
    
    chi2graph = prettifyGraph(r.TGraph(xVals.size,xVals,yVals["Chi2"]),graphInfo["Chi2"])
    ksgraph   = prettifyGraph(r.TGraph(xVals.size,xVals,yVals["KS"])  ,graphInfo["KS"]  )
    chi2graph.Draw("ALP")
    gifcanvas.SetGridx(1)
    gifcanvas.SetGridy(1)
    chi2graph.GetYaxis().SetRangeUser(0,5)
    chi2graph.SaveAs("chi2_%s%s.C"%(  options.histbase,options.etaphi))
    chi2graph.SaveAs("chi2_%s%s.pdf"%(options.histbase,options.etaphi))
    chi2graph.SaveAs("chi2_%s%s.png"%(options.histbase,options.etaphi))

    if options.debug:
        ksgraph.Draw("LPSAMES")
    else:
        ksgraph.Draw("ALP")
        pass
    ksgraph.SaveAs("ks_%s%s.C"%(  options.histbase,options.etaphi))
    ksgraph.SaveAs("ks_%s%s.pdf"%(options.histbase,options.etaphi))
    ksgraph.SaveAs("ks_%s%s.png"%(options.histbase,options.etaphi))
    if options.debug:
        raw_input("press enter to exit")
        pass
    

