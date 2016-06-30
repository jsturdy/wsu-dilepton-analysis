#!/bin/env python

import ROOT as r
import sys,os
import numpy as np

from optparse import OptionParser
from wsuPythonUtils import *

class endpointClosureStudy():
    """
    Run the cosmic endpoint analysis closure test
    """

    import ROOT as r
    import sys,os
    import numpy as np

    from wsuPythonUtils import setMinPT,prettifyGraph

    def __init__(self, infiledir, outfile, histName, etaphi, minpt,
                 maxbias=0.2, nBiasBins=40, nPseudoExp=250,
                 injBiasBin=10, stepsize=1,
                 nTotalBins=640, factor=1000, rebins=1,
                 pmScaling=True,
                 debug=False) :

        r.gROOT.SetBatch(True)
        r.gErrorIgnoreLevel = r.kFatal

        self.infiledir   = infiledir
        self.outfile     = outfile
        self.histName    = histName
        self.etaphi      = etaphi
        self.minpt       = minpt
        self.maxbias     = maxbias
        self.nPseudoExp  = nPseudoExp
        self.injBiasBin  = injBiasBin
        self.stepsize    = stepsize
        self.nBiasBins   = nBiasBins
        self.nTotalBins  = nTotalBins
        self.factor      = factor
        self.rebins      = rebins
        self.pmScaling   = pmScaling
        self.debug       = debug

        self.p100InFile = r.TFile("%s/startup_peak_p100_v5_b0.80_pt75_n200_sym/CosmicHistOut_TuneP.root"%(infiledir),"read")
        self.p500InFile = r.TFile("%s/startup_peak_p500_v5_b0.80_pt75_n200_sym/CosmicHistOut_TuneP.root"%(infiledir),"read")

        ## Need to be able to combine multiple MC samples together
        # - p10, p100, p500
        # - p100, p500: scale p100 by (1028051./58898.)
        self.p100top500ScaleFactor = 1028051./58898.

        self.outfile   = r.TFile(outfile,"recreate")
        self.chi2min   = r.TH1D("chi2Min", "", 500,  0.0, 250.)

        recoverNegative = False
        expectedBiasValue = (maxbias/nBiasBins)*injBiasBin
        if recoverNegative:
            expectedBiasValue = -(maxbias/nBiasBins)*injBiasBin
            pass

        minBin = expectedBiasValue-(0.2*expectedBiasValue)
        maxBin = expectedBiasValue+(0.2*expectedBiasValue)

        if injBiasBin == 0:
            minBin = -0.05
            maxBin =  0.05
            pass

        print "expect to recover a bias of %2.4f"%(expectedBiasValue)
        print "creating chi2 distribution histogram with range [%2.4f,%2.4f]"%(minBin,maxBin)
        self.chi2dist  = r.TH1D("chi2Dist", "",500, minBin, maxBin)

        self.chi2width = r.TH1D("chi2Width","",100,  0.05, 0.015)
        self.chi2pull1 = r.TH1D("chi2Pull1","#Delta#kappa_{inj} - #Delta#kappa_{meas}",
                                200, -0.1, 0.1)
        self.chi2pull2 = r.TH1D("chi2Pull2","(#Delta#kappa_{inj} - #Delta#kappa_{meas})/(fit_{width}(#chi^{2}_{min}+1))",
                                200, -5.0, 5.0)
        self.chi2pull3 = r.TH1D("chi2Pull3","(#Delta#kappa_{inj} - #Delta#kappa_{meas})/(#sqrt{2/fit''(#Delta#kappa_{meas})})",
                                200, -5.0, 5.0)
        self.chi2pull4 = r.TH1D("chi2Pull4","(#Delta#kappa_{inj} - #Delta#kappa_{meas})/(#sigma_{MINOS}^{lower})",
                                200, -5.0, 5.0)
        self.chi2pull5 = r.TH1D("chi2Pull5","(#Delta#kappa_{inj} - #Delta#kappa_{meas})/(#sigma_{MINOS}^{upper})",
                                200, -5.0, 5.0)

        self.etaphiexclusivebins = ["EtaPlusPhiMinus","EtaPlusPhiZero","EtaPlusPhiPlus",
                                    "EtaMinusPhiMinus","EtaMinusPhiZero","EtaMinusPhiPlus"
                                    ]
        self.etaphiinclusivebins = {"All":     self.etaphiexclusivebins,
                                    "EtaPlus": self.etaphiexclusivebins[0:3],
                                    "EtaMinus":self.etaphiexclusivebins[3:8],}
        self.etaphibins = ["", "EtaPlus", "EtaMinus",
                           "EtaPlusPhiMinus","EtaPlusPhiZero","EtaPlusPhiPlus",
                           "EtaMinusPhiMinus","EtaMinusPhiZero","EtaMinusPhiPlus"
                           ]

        self.graphInfo = {}
        self.graphInfo["KS"]   = {"color":r.kRed,"marker":r.kFullCircle,
                                  "title":"Kolmogorov test statistic",
                                  "yaxis":""}
        self.graphInfo["Chi2"] = {"color":r.kBlue, "marker":r.kFullCircle,
                                  "title":"ROOT #chi^{2}",
                                  "yaxis":""}
        self.graphInfo["Chi2NDF"] = {"color":r.kGreen, "marker":r.kFullCircle,
                                  "title":"ROOT #chi^{2}/ndf",
                                  "yaxis":""}

        self.gifDir = "sampleGIFs/%s"%(self.etaphi)
        os.system("mkdir -p %s"%(self.gifDir))

        ## common for the looping, should probably reset at the end of the loop
        self.refmax         = None
        self.refinto        = None
        self.refinta        = None
        self.plusRefHist    = None
        self.minusRefHist   = None
        self.refHist        = None
        self.plusScaleHist  = None
        self.minusScaleHist = None
        self.compScaleHist  = None
        self.compscaleinto  = None
        self.compscalepinto = None
        self.compscaleminto = None
        self.compscaleinta  = None
        self.compscalepinta = None
        self.compscaleminta = None

        pass

    def reset(self):
        self.refmax         = None
        self.refinto        = None
        self.refinta        = None
        self.plusRefHist    = None
        self.minusRefHist   = None
        self.refHist        = None
        self.plusScaleHist  = None
        self.minusScaleHist = None
        self.compScaleHist  = None
        self.compscaleinto  = None
        self.compscalepinto = None
        self.compscaleminto = None
        self.compscaleinta  = None
        self.compscalepinta = None
        self.compscaleminta = None
        return

    def loop(self):
        for pseudo in range(self.nPseudoExp):

            ### Create arrays to store the graph points, length = (2*self.nBiasBins)+1
            xVals = np.zeros(2*self.nBiasBins/self.stepsize+1,np.dtype('float64'))

            ### Need three Y-arrays, store them as a map
            yVals = {}

            for test in ["KS","Chi2","Chi2NDF"]:
                yVals[test] = np.zeros(2*self.nBiasBins/self.stepsize+1,np.dtype('float64'))
                pass

            results = self.runStudy(xVals, yVals, pseudo, debug=self.debug)
            pass


        self.outfile.cd()
        self.chi2min.Write()
        self.chi2dist.Write()
        self.chi2width.Write()
        self.chi2pull1.Write()
        self.chi2pull2.Write()
        self.chi2pull3.Write()
        self.chi2pull4.Write()
        self.chi2pull5.Write()
        self.outfile.Close()

        return

    def runStudy(self, xvals, yvals, pseudoExp, debug=False):

        mcBiasSuffix = "%03dPseudoData%03d"%(self.injBiasBin,pseudoExp)

        print "Reference: %s/%s%s%s%s"%(self.etaphi,self.histName,"PlusCurve",self.etaphi,mcBiasSuffix)
        plusClosureHistp100 = self.p100InFile.Get("%s/%s%s%s%s"%(self.etaphi,self.histName,"PlusCurve",
                                                                 self.etaphi,mcBiasSuffix)).Clone("clonep100")
        plusClosureHistp100.Scale(self.p100top500ScaleFactor)
        plusClosureHistp500 = self.p500InFile.Get("%s/%s%s%s%s"%(self.etaphi,self.histName,"PlusCurve",
                                                                 self.etaphi,mcBiasSuffix)).Clone("clonep500")

        plusClosureHist  = plusClosureHistp500.Clone("%s%s%s%s_scaling"%(self.histName,"PlusCurve",
                                                                         self.etaphi,mcBiasSuffix))
        plusClosureHist.Add(plusClosureHistp100)
        testHist = plusClosureHist.Clone("testHistogram")

        testHist = setMinPT(testHist,self.nTotalBins,self.minpt/1000.,True,debug)
        testHist.Rebin(self.rebins)
        self.refmax = testHist.GetMaximum()

        ### Set up the reference histogram(s)
        plusRefHist  = None
        minusRefHist = None

        ## use fixed MC bias histogram as reference
        if debug:
            print "Using %s/%s%s%s%s as reference histograms"%(self.etaphi,self.histName,"Plus[Minus]Curve",
                                                               self.etaphi,mcBiasSuffix)

        plusClosureHistp100 = self.p100InFile.Get("%s/%s%s%s%s"%(self.etaphi,self.histName,"PlusCurve",
                                                                 self.etaphi,mcBiasSuffix)).Clone("plusClosureHistp100")
        plusClosureHistp100.Scale(self.p100top500ScaleFactor)

        minusClosureHistp100 = self.p100InFile.Get("%s/%s%s%s%s"%(self.etaphi,self.histName,"MinusCurve",
                                                                  self.etaphi,mcBiasSuffix)).Clone("minusClosureHistp100")
        minusClosureHistp100.Scale(self.p100top500ScaleFactor)

        plusClosureHistp500  = self.p500InFile.Get("%s/%s%s%s%s"%(self.etaphi,self.histName,"PlusCurve",
                                                                  self.etaphi,mcBiasSuffix)).Clone("plusClosureHistp500")
        minusClosureHistp500 = self.p500InFile.Get("%s/%s%s%s%s"%(self.etaphi,self.histName,"MinusCurve",
                                                                  self.etaphi,mcBiasSuffix)).Clone("minusClosureHistp500")

        plusClosureHist  = plusClosureHistp500.Clone("%s%s%s_scaling"%(self.histName,"PlusCurve",mcBiasSuffix))
        plusClosureHist.Add(plusClosureHistp100)

        minusClosureHist = minusClosureHistp500.Clone("%s%s%s_scaling"%(self.histName,"MinusCurve",mcBiasSuffix))
        minusClosureHist.Add(minusClosureHistp100)

        plusRefHist  = plusClosureHist
        minusRefHist = minusClosureHist

        if debug:
            print "Minus integral %d, Plus integral %d"%(minusRefHist.Integral(),plusRefHist.Integral())
            pass

        refHist = plusRefHist.Clone("%s_refHist"%(self.histName))

        if debug:
            print "before adding minus histogram integral: %d"%(refHist.Integral())
            pass

        refHist.Add(minusRefHist)

        if debug:
            print "after adding minus histogram integral: %d"%(refHist.Integral())
            pass

        # un-cut integral
        self.refinto  = refHist.Integral()
        self.refpinto = plusRefHist.Integral()
        self.refminto = minusRefHist.Integral()

        if debug:
            print "Rebinning reference histograms"
            pass

        self.refHist      = setMinPT(refHist,     self.nTotalBins,self.minpt/1000.,True,debug)
        self.plusRefHist  = setMinPT(plusRefHist, self.nTotalBins,self.minpt/1000.,True,debug)
        self.minusRefHist = setMinPT(minusRefHist,self.nTotalBins,self.minpt/1000.,True,debug)

        self.refHist.Rebin(     self.rebins)
        self.plusRefHist.Rebin( self.rebins)
        self.minusRefHist.Rebin(self.rebins)

        # integral after applying a pT cut
        self.refinta = refHist.Integral()
        self.refpinta = plusRefHist.Integral()
        self.refminta = minusRefHist.Integral()

        self.refHist.SetLineColor(r.kBlue)
        self.refHist.SetLineWidth(2)

        ### calculating a scale factor from the un-biased MC
        print "Scaling: %s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"PlusCurve",self.etaphi,pseudoExp)
        plusScaleHistp100 = self.p100InFile.Get("%s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"PlusCurve",self.etaphi,pseudoExp)).Clone("plusScaleHistp100")
        plusScaleHistp100.Scale(self.p100top500ScaleFactor)

        minusScaleHistp100 = self.p100InFile.Get("%s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"MinusCurve",self.etaphi,pseudoExp)).Clone("minusScaleHistp100")
        minusScaleHistp100.Scale(self.p100top500ScaleFactor)

        plusScaleHistp500  = self.p500InFile.Get("%s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"PlusCurve",self.etaphi,pseudoExp)).Clone("plusScaleHistp500")
        minusScaleHistp500 = self.p500InFile.Get("%s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"MinusCurve",self.etaphi,pseudoExp)).Clone("minusScaleHistp500")

        plusScaleHist = plusScaleHistp500.Clone("%s%s%sMCClosure%03d_scaling"%(self.etaphi,self.histName,"PlusCurve",pseudoExp))
        plusScaleHist.Add(plusScaleHistp100)

        minusScaleHist = minusScaleHistp500.Clone("%s%s%sMCClosure%03d_scaling"%(self.etaphi,self.histName,"MinusCurve",pseudoExp))
        minusScaleHist.Add(minusScaleHistp100)

        compScaleHist = plusScaleHist.Clone("%s%sMCClosure%03d_compScaleHist"%(self.etaphi,self.histName,pseudoExp))
        compScaleHist.Add(minusScaleHist)

        if debug:
            print "Rebinning comparison scale histograms"
        self.compscaleinto  = compScaleHist.Integral()
        self.compscalepinto = plusScaleHist.Integral()
        self.compscaleminto = minusScaleHist.Integral()

        self.compScaleHist  = setMinPT(compScaleHist, self.nTotalBins,self.minpt/1000.,True,debug)
        self.plusScaleHist  = setMinPT(plusScaleHist, self.nTotalBins,self.minpt/1000.,True,debug)
        self.minusScaleHist = setMinPT(minusScaleHist,self.nTotalBins,self.minpt/1000.,True,debug)

        self.compScaleHist.Rebin( self.rebins)
        self.plusScaleHist.Rebin( self.rebins)
        self.minusScaleHist.Rebin(self.rebins)

        self.compscaleinta  = compScaleHist.Integral()
        self.compscalepinta = plusScaleHist.Integral()
        self.compscaleminta = minusScaleHist.Integral()

        print "Reference histogram integral: inclusive, pT > %2.2f"%(self.minpt)
        print "                    combined: %9d, %10d"%(self.refinto, self.refinta)
        print "                    mu plus : %9d, %10d"%(self.refpinto,self.refpinta)
        print "                    mu minus: %9d, %10d"%(self.refminto,self.refminta)
        print "  plus/minus asymmetry: %2.4f, %2.4f"%(self.refpinto/self.refminto,
                                                      self.refpinta/self.refminta)
        print
        print "Scaling histogram integral  :"
        print "                    combined: %9d, %10d"%(self.compscaleinto, self.compscaleinta)
        print "                    mu plus : %9d, %10d"%(self.compscalepinto,self.compscalepinta)
        print "                    mu minus: %9d, %10d"%(self.compscaleminto,self.compscaleminta)
        print "  plus/minus asymmetry: %2.4f, %2.4f"%(self.compscalepinto/self.compscaleminto,
                                                      self.compscalepinta/self.compscaleminta)
        print
        print "Pre-Scaling ref/comp factor is:"
        print "  combined: %2.4f = %8.2f/%8.2f"%(self.refinto/self.compscaleinto,  self.refinto, self.compscaleinto)
        print "  mu plus : %2.4f = %8.2f/%8.2f"%(self.refpinto/self.compscalepinto,self.refpinto,self.compscalepinto)
        print "  mu minus: %2.4f = %8.2f/%8.2f"%(self.refminto/self.compscaleminto,self.refminto,self.compscaleminto)
        print
        print "Post-Scaling factor is:"
        print "  combined: %2.4f = %8.2f/%8.2f"%(self.refinta/self.compscaleinta,  self.refinta, self.compscaleinta)
        print "  mu plus : %2.4f = %8.2f/%8.2f"%(self.refpinta/self.compscalepinta,self.refpinta,self.compscalepinta)
        print "  mu minus: %2.4f = %8.2f/%8.2f"%(self.refminta/self.compscaleminta,self.refminta,self.compscaleminta)

        ## loop over negative bias
        (xvals,yvals) = self.biasLoop(xvals, yvals, pseudoExp, negativeBias=True,  zeroBias=False, debug=self.debug)
        ## plots for zero bias
        (xvals,yvals) = self.biasLoop(xvals, yvals, pseudoExp, negativeBias=False, zeroBias=True, debug=self.debug)
        ## loop over negative bias
        (xvals,yvals) = self.biasLoop(xvals, yvals, pseudoExp, negativeBias=False, zeroBias=False, debug=self.debug)

        graphs = self.makeGraphs(xvals, yvals, pseudoExp, debug=self.debug)

        funcrange = [-0.2,0.2]
        fitrange  = [-0.2,0.2]
        fitresults = self.fitCurve(graphs["chi2"], 8, funcrange, fitrange, debug=self.debug)

        self.chi2min.Fill(fitresults["minChi2"])

        self.chi2dist.Fill(fitresults["minBias"])

        width = fitresults["upper"] - fitresults["lower"]
        self.chi2width.Fill(width)

        exp = (self.maxbias/self.nBiasBins)*self.injBiasBin

        pull = (exp - fitresults["minBias"])
        self.chi2pull1.Fill(pull)

        pull = (exp - fitresults["minBias"])/width
        self.chi2pull2.Fill(pull)

        pull = (exp - fitresults["minBias"])/fitresults["error"]
        self.chi2pull3.Fill(pull)

        pull = (exp - fitresults["minBias"])/fitresults["minos"][0]
        self.chi2pull4.Fill(pull)

        pull = (exp - fitresults["minBias"])/fitresults["minos"][1]
        self.chi2pull5.Fill(pull)

        self.reset()

        return

    def biasLoop(self, xvals, yvals, pseudoExp, negativeBias=False, zeroBias=False, debug=False):

        if not zeroBias:
            biasChange = "Plus"
            if negativeBias:
                biasChange = "Minus"

            for step in range(0,self.nBiasBins/self.stepsize):
                ### grab the histogram corresponding to the bias value
                biasBin = (1+step)*self.stepsize
                if negativeBias:
                    biasBin = self.nBiasBins-step*self.stepsize
                if debug:
                    print "%s/%s%s%s%sBias%03dMCClosure%03d"%(self.etaphi,self.histName,"PlusCurve",
                                                              self.etaphi,
                                                              biasBin,pseudoExp)
                    pass

                plusHistp100  = self.p100InFile.Get("%s/%s%s%s%sBias%03dMCClosure%03d"%(self.etaphi,self.histName,"PlusCurve",
                                                                                        self.etaphi,biasChange,
                                                                                        biasBin,pseudoExp))
                minusHistp100 = self.p100InFile.Get("%s/%s%s%s%sBias%03dMCClosure%03d"%(self.etaphi,self.histName,"MinusCurve",
                                                                                        self.etaphi,biasChange,
                                                                                        biasBin,pseudoExp))
                plusHistp100.Scale( self.p100top500ScaleFactor)
                minusHistp100.Scale(self.p100top500ScaleFactor)

                plusHistp500  = self.p500InFile.Get("%s/%s%s%s%sBias%03dMCClosure%03d"%(self.etaphi,self.histName,"PlusCurve",
                                                                                        self.etaphi,biasChange,
                                                                                        biasBin,pseudoExp))
                minusHistp500 = self.p500InFile.Get("%s/%s%s%s%sBias%03dMCClosure%03d"%(self.etaphi,self.histName,"MinusCurve",
                                                                                        self.etaphi,biasChange,
                                                                                        biasBin,pseudoExp))

                plusHist  = plusHistp500.Clone("%s%s_combined_%sBias%03d"%(self.histName,"PlusCurve",
                                                                           biasChange,
                                                                           biasBin))
                plusHist.Add(plusHistp100)

                minusHist = minusHistp500.Clone("%s%s_combined_%sBias%03d"%(self.histName,"MinusCurve",
                                                                            biasChange,
                                                                            biasBin))
                minusHist.Add(minusHistp100)


                ## for positive injected bias
                index  = self.nBiasBins/self.stepsize+1+step
                gifBin = self.nBiasBins+(1+step)*self.stepsize
                if negativeBias:
                    index = step
                    gifBin = step*self.stepsize
                    pass

                (xvals, yvals) = self.compareHistograms(xvals, yvals, index, biasBin, gifBin,
                                                        plusHist, minusHist, pseudoExp,
                                                        zeroBias, negativeBias)

                pass
            pass
        else:
            plusHistp100  = self.p100InFile.Get("%s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"PlusCurve",
                                                                                     self.etaphi,pseudoExp))
            minusHistp100 = self.p100InFile.Get("%s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"MinusCurve",
                                                                                     self.etaphi,pseudoExp))
            plusHistp100.Scale( self.p100top500ScaleFactor)
            minusHistp100.Scale(self.p100top500ScaleFactor)

            plusHistp500  = self.p500InFile.Get("%s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"PlusCurve",
                                                                                     self.etaphi,pseudoExp))
            minusHistp500 = self.p500InFile.Get("%s/%s%s%sPlusBias000MCClosure%03d"%(self.etaphi,self.histName,"MinusCurve",
                                                                                     self.etaphi,pseudoExp))

            plusHist  = plusHistp500.Clone("%s%s_combined"%(self.histName,"PlusCurve"))
            plusHist.Add(plusHistp100)

            minusHist = minusHistp500.Clone("%s%s_combined"%(self.histName,"MinusCurve"))
            minusHist.Add(minusHistp100)

            index   = self.nBiasBins/self.stepsize
            biasBin = 0
            gifBin  = self.nBiasBins
            (xvals, yvals) = self.compareHistograms(xvals, yvals, index, biasBin, gifBin,
                                                    plusHist, minusHist, pseudoExp,
                                                    zeroBias, negativeBias)
            pass

        return (xvals,yvals)

    def compareHistograms(self, xvals, yvals, index, biasBin, gifBin,
                          plusHist, minusHist, pseudoExp,
                          zeroBias=False, negativeBias=False,
                          debug=False):

        gifcanvas = r.TCanvas("gifcanvas","gifcanvas",750,750)
        r.SetOwnership(gifcanvas,False)

        ### set up the different pads, depending on plot mode
        pad = r.TPad("pad","pad",0.0,0.3,1.0,1.0)
        r.SetOwnership(pad,False)
        pad.Draw()
        gifcanvas.cd()
        resPad = r.TPad("Respad","Respad",0.0,0.0,1.0,0.3)
        r.SetOwnership(resPad,False)
        resPad.Draw()

        r.gStyle.SetOptStat(0)

        ### scope some variables for later use
        comppinto = 0
        compminto = 0
        compinto  = 0
        comppinta = 0
        compminta = 0
        compinta  = 0

        if self.pmScaling:
            if debug:
                print "before: plusRefNBins %d, plusNBins %d"%(  self.plusRefHist.GetNbinsX(), plusHist.GetNbinsX())
                print "before: minusRefNBins %d, minusNBins %d"%(self.minusRefHist.GetNbinsX(),minusHist.GetNbinsX())
                pass

            plusHist  = setMinPT(plusHist, self.nTotalBins,self.minpt/1000.,True,debug)
            minusHist = setMinPT(minusHist,self.nTotalBins,self.minpt/1000.,True,debug)

            plusHist.Rebin( self.rebins)
            minusHist.Rebin(self.rebins)

            if debug:
                print "after: plusRefNBins %d, plusNBins %d"%(  self.plusRefHist.GetNbinsX(), plusHist.GetNbinsX())
                print "after: minusRefNBins %d, minusNBins %d"%(self.minusRefHist.GetNbinsX(),minusHist.GetNbinsX())
                pass

            ### integral before scaling
            comppinto = plusHist.Integral()
            compminto = minusHist.Integral()
            compinto  = comppinto+compminto

            if (self.plusScaleHist.Integral() > 0):
                # scale to this histogram
                #plusHist.Scale(self.refHist.Integral()/plusHist.Integral())
                # scale to scale histogram
                plusHist.Scale(self.refpinta/self.compscalepinta)
            else:
                print "unable to scale plus histogram, integral is 0"
                pass

            if (self.minusScaleHist.Integral() > 0):
                # scale to this histogram
                #minusHist.Scale(refHist.Integral()/minusHist.Integral())
                # scale to scale histogram
                minusHist.Scale(self.refminta/self.compscaleminta)
            else:
                print "unable to scale minus histogram, integral is 0"
                pass

            ### if we scale plus to plus and minus to minus, have to add them here rather than before
            ## need to make this programatic though

            comppinta = plusHist.Integral()
            compminta = minusHist.Integral()
            compinta  = comppinta+compminta
            pass

        ## Add plus and minus histograms for the comparison histogram
        compHist = plusHist.Clone("%s_compHist_MinusBias%03d"%(self.histName,biasBin))
        compHist.Add(minusHist)

        ### have to scale the combined histogram if the plus/minus histograms weren't scaled previously
        if not self.pmScaling:
            if debug:
                print "before: refNBins %d, compNBins %d"%(refHist.GetNbinsX(),compHist.GetNbinsX())
                pass

            compHist  = setMinPT(compHist, self.nTotalBins,self.minpt/1000.,True,debug)
            compHist.Rebin(self.rebins)

            if debug:
                print "after: refNBins %d, compNBins %d"%(refHist.GetNbinsX(),compHist.GetNbinsX())
                pass

            ### integral before scaling
            compinto  = compHist.Integral()

            if (self.compScaleHist.Integral() > 0):
                # scale to this histogram
                #compHist.Scale(self.refHist.Integral()/compHist.Integral())
                # scale to scale histogram
                compHist.Scale(self.refinta/self.compscaleinta)
            else:
                print "unable to scale comp histogram, integral is 0"
                pass

            compinta  = compHist.Integral()
            pass

        if negativeBias:
            compHist.SetTitle("#Delta#kappa = %2.4f [c/TeV]"%(-(self.maxbias/self.nBiasBins)*biasBin))
        else:
            compHist.SetTitle("#Delta#kappa = %2.4f [c/TeV]"%((self.maxbias/self.nBiasBins)*biasBin))
            pass
        compHist.SetLineColor(r.kRed)
        compHist.SetLineWidth(2)

        pad.cd()

        compHist.Draw()
        compHist.GetXaxis().SetTitle("#kappa [c/TeV]")
        compHist.SetMaximum(1.2*self.refmax)
        compHist.SetMinimum(0.001)
        self.refHist.Draw("sames")

        r.gPad.Update()

        chi2Val  = r.Double(0.) # necessary for pass-by-reference in python
        chi2ndf  = r.Long(0)    # necessary for pass-by-reference in python
        igood    = r.Long(0)    # necessary for pass-by-reference in python
        histopts = "UU,NORM" # unweighted/weighted, normalized
        resids = np.zeros(self.refHist.GetNbinsX(),np.dtype('float64')) # pointer argument, one per bin, not quite working

        prob   = self.refHist.Chi2TestX(compHist,chi2Val,chi2ndf,igood,histopts,resids)
        ksprob = self.refHist.KolmogorovTest(compHist,"")#)

        # this needs to be low bin, high bin
        resHist = r.TH1D("ResHist", "", len(resids), -8.0,8.0)
        #r.SetOwnership(resHist,False)
        resHist.Sumw2()
        for i,res in enumerate(resids):
            if debug:
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
        resHist.GetYaxis().SetTitle("#chi^{2} residuals")
        resHist.Draw("ep0")
        resHist.SetMaximum(15.)
        resHist.SetMinimum(-15.)

        ### now set up the points in the graph
        if zeroBias:
            xvals[index] = (self.maxbias/self.nBiasBins)*biasBin
        elif negativeBias:
            xvals[index] = -(self.maxbias/self.nBiasBins)*biasBin
        else:
            xvals[index] = (self.maxbias/self.nBiasBins)*biasBin
            pass

        yvals["Chi2NDF"][index] = chi2Val/chi2ndf
        yvals["Chi2"][index]    = chi2Val
        yvals["KS"][index]      = ksprob

        thetext = r.TPaveText(0.4,0.8,0.6,0.9,"ndc")
        #r.SetOwnership(thetext,False)
        thetext.SetFillColor(0)
        thetext.SetFillStyle(3000)
        thetext.AddText("#chi^{2}/ndf = %2.2f(%2.2f/%d)"%(chi2Val/chi2ndf,chi2Val,chi2ndf))
        thetext.AddText("KS prob = %2.4e"%(ksprob))
        thelegend = r.TLegend(0.4,0.7,0.6,0.8)
        #r.SetOwnership(thelegend,False)
        thelegend.SetFillColor(0)
        thelegend.SetFillStyle(3000)

        thelegend.AddEntry(self.refHist, "data (%d,%d)"%(self.refinto,self.refinta))
        thelegend.AddEntry(compHist,"MC (%d,%d)"%(compinto,compinta))

        gifcanvas.cd()

        pad.cd()

        thetext.Draw("nb")
        thelegend.Draw()
        r.gPad.Update()

        gifcanvas.SaveAs("%s/%sbiasBin%04d_closureBin%03d.png"%(self.gifDir, self.etaphi, gifBin, pseudoExp))
        return (xvals, yvals)

    def makeGraphs(self, xvals, yvals, pseudoExp, debug=False):
        """
        Make the Chi2, reduced Chi2, and KS graphs
        """
        graphs = {}
        self.outfile.cd()
        graphs["chi2ndf"] = prettifyGraph(r.TGraph(xvals.size,xvals,yvals["Chi2NDF"]),self.graphInfo["Chi2NDF"])
        graphs["chi2"]    = prettifyGraph(r.TGraph(xvals.size,xvals,yvals["Chi2"]),   self.graphInfo["Chi2"])
        graphs["ks"]      = prettifyGraph(r.TGraph(xvals.size,xvals,yvals["KS"])  ,   self.graphInfo["KS"]  )


        graphs["chi2ndf"].SetName("chi2ndf_%s%s_closureBin%03d"%(self.histName,self.etaphi,pseudoExp))
        graphs["chi2"].SetName(   "chi2_%s%s_closureBin%03d"%(   self.histName,self.etaphi,pseudoExp))
        graphs["ks"].SetName(     "ks_%s%s_closureBin%03d"%(     self.histName,self.etaphi,pseudoExp))

        graphs["chi2ndf"].Write()
        graphs["chi2"].Write()
        graphs["ks"].Write()

        return graphs


    def fitCurve(self, chi2graph, nparams, funcrange, fitrange, deltaChi2=1.0, debug=False):
        """
        Fit a graph with an n-degree polynomial
        nparams   - degree of polynomial
        funcrange - lower and upper bounds on the function
        fitrange  - lower and upper bounds on the fit
        """
        import math

        self.outfile.cd()

        fitPoly = r.TF1("fitPoly%d"%(nparams), "pol%d"%(nparams),
                        funcrange[0],funcrange[1])
        r.SetOwnership(fitPoly,False)
        fitPoly.SetParameters(0,0)
        chi2graph.Fit("fitPoly%d"%(nparams), "QEMFRN", "",
                      fitrange[0],fitrange[1])
        results = {}
        results["minBias"] = fitPoly.GetMinimumX(fitrange[0], fitrange[1])
        results["minChi2"] = fitPoly.GetMinimum( fitrange[0], fitrange[1])
        results["lower"]   = fitPoly.GetX(results["minChi2"]+deltaChi2, fitrange[0],        results["minBias"])
        results["upper"]   = fitPoly.GetX(results["minChi2"]+deltaChi2, results["minBias"], fitrange[1])
        if debug:
            print "fitPoly.Derivative(min)",fitPoly.Derivative(results["minBias"])
            print "fitPoly.Derivative2(min)",fitPoly.Derivative2(results["minBias"])
            pass
        results["error"]   = math.sqrt(2./fitPoly.Derivative2(results["minBias"]))
        results["minos"]   = (abs(results["minBias"]-results["lower"]),
                              abs(results["minBias"]-results["upper"]))
        if debug:
            print "min chi2 = %2.4f (+%2.4f -%2.4f), chi2 min = %2.4f"%(results["minBias"],
                                                                        results["minChi2"],
                                                                        results["lower"],
                                                                        results["upper"])

            pass

        return results

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog --infiledir path/to/MC/files -o outputfile.root [-d]")
    parser.add_option("-i", "--infiledir", type="string", dest="infiledir",
                      metavar="infiledir",
                      help="[REQUIRED] Location of the comparison input MC ROOT files")
    parser.add_option("-o", "--outfile", type="string", dest="outfile",
                      metavar="outfile",
                      help="[REQUIRED] Name of the output ROOT file")
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
    parser.add_option("--minpt", type="float", dest="minpt",
                      metavar="minpt", default=200.,
                      help="[OPTIONAL] Minimum pT cut to apply in the curvature plots (default is 200 c/TeV)")
    parser.add_option("--etaphi", type="string", dest="etaphi",
                      metavar="etaphi", default="",
                      help="[OPTIONAL] Eta/Phi bin to use")
    parser.add_option("--pm", action="store_true", dest="pm",
                      metavar="mcclosure",
                      help="[OPTIONAL] Scale plus and minus separately")
    parser.add_option("--mcbias", type="int", dest="mcbias",
                      metavar="mcbias", default=10,
                      help="[OPTIONAL] Bias bin value to recover (default is 10)")
    parser.add_option("--num_pseudo", type="int", dest="num_pseudo",
                      metavar="num_pseudo", default=250,
                      help="[OPTIONAL] Number of pseudoexperiments to take results from (default is 250)")

    (options, args) = parser.parse_args()

    if options.debug:
        print options
        print args
        pass

    checkRequiredArguments(options, parser)

    closuretest = endpointClosureStudy(infiledir=options.infiledir,
                                       outfile=options.outfile,
                                       histName=options.histbase,
                                       etaphi=options.etaphi,
                                       minpt=options.minpt,
                                       maxbias=options.maxbias,
                                       nPseudoExp=options.num_pseudo,
                                       injBiasBin=options.mcbias,
                                       stepsize=options.stepsize,
                                       nBiasBins=options.biasbins,
                                       nTotalBins=options.totalbins,
                                       rebins=options.rebins,
                                       pmScaling=options.pm,
                                       debug=options.debug)

    closuretest.loop()

    if options.debug:
        raw_input("press enter to exit")
        pass

