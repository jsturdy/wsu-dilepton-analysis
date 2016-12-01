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

    (options, args) = parser.parse_args()
    print options
    print args

    lowcut = 0.0025
    randcan = r.TCanvas("randcan","randcan",1280,1024)
    full = r.TH1D("full","full",1000,0,1);
    low  = r.TH1D("low", "low", 1000,0,lowcut);
    high = r.TH1D("high","high",1000,0,1);

    for seed in range(10):
        myrand = r.TRandom3(12345)
        for i in range(10):
            val = myrand.Rndm()
            print seed, val
            pass
        pass
    exit(0)
    #    if val > lowcut:
    #        high.Fill(val)
    #    else:
    #        low.Fill(val)
    #    full.Fill(val)

    randcan.Divide(2,2)
    randcan.cd(1)
    high.Draw()
    randcan.cd(2)
    low.Draw()
    randcan.cd(3)
    full.Draw()
    raw_input("press enter to exit")
    exit(0)

    checkRequiredArguments(options, parser)
    
    ## Need to be able to combine multiple MC samples together
    # - p10, p100, p500
    # - p100, p500: scale p100 by (1028051./58898.)
    p100top500ScaleFactor = 1028051./58898.

    p100InFileName = options.p100infile
    p100InFile = r.TFile(p100InFileName,"READ")
    
    p500InFileName = options.p500infile
    p500InFile = r.TFile(p500InFileName,"READ")

    histName   = "looseMuLower"    
    etaphi     = ""
    mcBiasSign = "Minus"
    mcBiasBin  = 50
    totalbins  = 1600
    minpt      = 150

    mycan = r.TCanvas("mycan","mycan",1280,1024)
    mycan.Divide(2,2)
    mycan.cd(1)
    plusClosureHistp100  = p100InFile.Get("%s%s%s%sBias%03d"%(histName,"PlusCurve",etaphi,mcBiasSign,mcBiasBin))
    minusClosureHistp100 = p100InFile.Get("%s%s%s%sBias%03d"%(histName,"MinusCurve",etaphi,mcBiasSign,mcBiasBin))
    plusClosureHistp100.Scale(p100top500ScaleFactor)
    minusClosureHistp100.Scale(p100top500ScaleFactor)
    plusClosureHistp500  = p500InFile.Get("%s%s%s%sBias%03d"%(histName,"PlusCurve",etaphi,mcBiasSign,mcBiasBin))
    minusClosureHistp500 = p500InFile.Get("%s%s%s%sBias%03d"%(histName,"MinusCurve",etaphi,mcBiasSign,mcBiasBin))
    
    plusClosureHist  = plusClosureHistp500.Clone("%s%s%sBias%03d_scaling"%(histName,"PlusCurve",mcBiasSign,mcBiasBin))
    plusClosureHist.Add(plusClosureHistp100)
    
    minusClosureHist = minusClosureHistp500.Clone("%s%s%sBias%03d_scaling"%(histName,"MinusCurve",mcBiasSign,mcBiasBin))
    minusClosureHist.Add(minusClosureHistp100)

    plusClosureHist.SetLineColor(r.kBlue)
    plusClosureHist.SetLineWidth(2)
    plusClosureHist.SetLineStyle(2)

    minusClosureHist.SetLineColor(r.kRed)
    minusClosureHist.SetLineWidth(2)
    minusClosureHist.SetLineStyle(2)
    
    refHist = plusClosureHist.Clone("%s_refHist"%(histName))
    refHist.Add(minusClosureHist)
    refHist.SetLineColor(r.kRed)
    refHist.SetLineWidth(2)

    plusScaleHistp100  = p100InFile.Get("%s%s%s"%(histName,"PlusCurve",etaphi))
    minusScaleHistp100 = p100InFile.Get("%s%s%s"%(histName,"MinusCurve",etaphi))
    plusScaleHistp100.Scale(p100top500ScaleFactor)
    minusScaleHistp100.Scale(p100top500ScaleFactor)

    plusScaleHistp500  = p500InFile.Get("%s%s%s"%(histName,"PlusCurve",etaphi))
    minusScaleHistp500 = p500InFile.Get("%s%s%s"%(histName,"MinusCurve",etaphi))
    
    plusScaleHist  = plusScaleHistp500.Clone("%s%s_scaling"%(histName,"PlusCurve"))
    plusScaleHist.Add(plusScaleHistp100)

    minusScaleHist = minusScaleHistp500.Clone("%s%s_scaling"%(histName,"MinusCurve"))
    minusScaleHist.Add(minusScaleHistp100)

    plusScaleHist.SetLineColor(r.kBlue)
    plusScaleHist.SetLineWidth(2)
    plusScaleHist.SetLineStyle(2)

    minusScaleHist.SetLineColor(r.kRed)
    minusScaleHist.SetLineWidth(2)
    minusScaleHist.SetLineStyle(2)
    
    compScaleHist = plusScaleHist.Clone("%s_compScaleHist"%(histName))
    compScaleHist.Add(minusScaleHist)
    compScaleHist.SetLineColor(r.kBlue)
    compScaleHist.SetLineWidth(2)


    ### Draw the plotas
    r.gStyle.SetOptStat(11111111)
    mycan.cd(1)
    plusClosureHist = setMinPT(plusClosureHist,totalbins,minpt/1000.,True,True)
    plusClosureHist.Rebin(25)
    minusClosureHist = setMinPT(minusClosureHist,totalbins,minpt/1000.,True,True)
    minusClosureHist.Rebin(25)
    plusClosureHist.Draw("ep0")
    minusClosureHist.Draw("ep0sames")

    mycan.cd(2)
    plusScaleHist = setMinPT(plusScaleHist,totalbins,minpt/1000.,True,True)
    plusScaleHist.Rebin(25)
    minusScaleHist = setMinPT(minusScaleHist,totalbins,minpt/1000.,True,True)
    minusScaleHist.Rebin(25)
    plusScaleHist.Draw("ep0")
    minusScaleHist.Draw("ep0sames")
    
    mycan.cd(3)
    refinto = refHist.Integral()
    refHist = setMinPT(refHist,totalbins,minpt/1000.,True,True)
    refinta = refHist.Integral()
    refHist.Rebin(25)
    print "Reference histogram integral: before %d, after %d"%(refinto,refinta)

    compscaleinto = compScaleHist.Integral()
    compScaleHist = setMinPT(compScaleHist,totalbins,minpt/1000.,True,True)
    compscaleinta = compScaleHist.Integral()
    compScaleHist.Rebin(25)
    print "compScale histogram integral: before %d, after %d"%(compscaleinto,compscaleinta)
    print "Scaling factor is: %2.4f = %2.4f/%2.4f"%(refinta/compscaleinta,refinta,compscaleinta)

    refHist.Draw("ep0")
    compScaleHist.Draw("ep0sames")

    raw_input("press enter to quit")
