#!/bin/env python

import ROOT as r
import sys,os
import numpy as np

from optparse import OptionParser
from wsuPythonUtils import *
from wsuPyROOTUtils import *

class endpointDataMCStudy():
    """
    Run the cosmic endpoint analysis
    """

    import ROOT as r
    import sys,os
    import numpy as np

    from wsuPythonUtils import setMinPT,prettifyGraph
    from wsuPyROOTUtils import styleHistogram

    def __init__(self, infiledir, outfile, histName, etaphi, minpt,
                 maxbias=0.2, nBiasBins=40,stepsize=1,
                 nTotalBins=640, factor=1000, rebins=1,
                 algo="TuneP",
                 pmScaling=True,
                 xroot=False,
                 asymdeco=False,
                 makeLog=False,
                 debug=False) :

        r.gROOT.SetBatch(not debug)
        r.gErrorIgnoreLevel = r.kFatal

        self.infiledir   = infiledir
        self.outfile     = outfile
        self.histName    = histName
        self.etaphi      = etaphi
        self.minpt       = minpt
        self.maxbias     = maxbias
        self.stepsize    = stepsize
        self.nBiasBins   = nBiasBins
        self.nTotalBins  = nTotalBins
        self.factor      = factor
        self.rebins      = rebins
        self.algo        = algo
        self.trackAlgos = ["TrackerOnly","TuneP","DYT","TPFMS","Picky"]
        if self.algo not in self.trackAlgos:
            errmsg = "Invalid track algo specified: %s.  Allowed options are:\n"%(self.algo)
            errmsg += self.trackAlgos
            #exit(1)
            raise NameError(errmsg)


        self.pmScaling   = pmScaling
        self.pmstring    = "normal"
        if self.pmScaling:
            self.pmstring    = "pm"
            pass
        self.xroot    = xroot
        self.asymdeco = asymdeco
        self.makeLog  = makeLog
        self.debug    = debug

        cosmicDataInFileName = "%s/craft15_v5_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                          self.maxbias,
                                                                                          self.nBiasBins,
                                                                                          self.algo)
        p100InFileName = "%s/startup_peak_p100_v5_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                              self.maxbias,
                                                                                              self.nBiasBins,
                                                                                              self.algo)
        p500InFileName = "%s/startup_peak_p500_v5_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                              self.maxbias,
                                                                                              self.nBiasBins,
                                                                                              self.algo)

        if self.asymdeco:
            cosmicDataInFileName = "%s/craft15_v5_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                              self.maxbias,
                                                                                              self.nBiasBins,
                                                                                              self.algo)
            p100InFileName = "%s/asym_deco_p100_v5_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                               self.maxbias,
                                                                                               self.nBiasBins,
                                                                                               self.algo)
            p500InFileName = "%s/asym_deco_p500_v5_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                               self.maxbias,
                                                                                               self.nBiasBins,
                                                                                               self.algo)
            pass

        if self.xroot:
            eossrc = "root://cmseos.fnal.gov///store/user/sturdy"
            eossrc = "root://eoscms.cern.ch//eos/cms/store/user/sturdy"
            cosmicDataInFileName = "%s/CosmicEndpoint/2015/Closure/%s"%(eossrc,cosmicDataInFileName)
            p100InFileName = "%s/CosmicEndpoint/2015/Closure/%s"%(eossrc,p100InFileName)
            p500InFileName = "%s/CosmicEndpoint/2015/Closure/%s"%(eossrc,p500InFileName)
            pass

        self.cosmicDataInFile = None
        self.p100InFile = None
        self.p500InFile = None

        if (cosmicDataInFileName).find("root://") > -1:
            print "using TNetXNGFile for EOS access"
            self.cosmicDataInFile = r.TNetXNGFile(cosmicDataInFileName,"read")
            self.p100InFile = r.TNetXNGFile(p100InFileName,"read")
            self.p500InFile = r.TNetXNGFile(p500InFileName,"read")
        else:
            self.cosmicDataInFile = r.TFile(cosmicDataInFileName,"read")
            self.p100InFile = r.TFile(p100InFileName,"read")
            self.p500InFile = r.TFile(p500InFileName,"read")
            pass

        if not self.cosmicDataInFile or not self.p100InFile or not self.p500InFile:
            print "input files invalid"
            print "cosmicDataInFile",self.cosmicDataInFile
            print "p100InFile",self.p100InFile
            print "p500InFile",self.p500InFile
            exit(1)

        ## Need to be able to combine multiple MC samples together
        # - p10, p100, p500
        # - p100, p500: scale p100 by (1028051./58898.)
        self.p100top500ScaleFactor = 1028051./58898.

        self.outfile   = r.TFile(outfile,"update")

        r.TH1.SetDefaultSumw2()

        histparams = {
            "marker":{
                "color":r.kBlack,
                "style":r.kFullDiamond
                },
            "line":{
                "color":r.kBlack,
                "style":1,
                "width":2
                },
            }

        self.etaphiexclusivebins = ["EtaPlusPhiMinus","EtaPlusPhiZero","EtaPlusPhiPlus",
                                    "EtaMinusPhiMinus","EtaMinusPhiZero","EtaMinusPhiPlus"
                                    ]
        self.etaphiinclusivebins = {"All":     self.etaphiexclusivebins,
                                    "EtaPlus": self.etaphiexclusivebins[0:2],
                                    "EtaMinus":self.etaphiexclusivebins[3:5],
                                    # "PhiPlus":self.etaphiexclusivebins[2:3]+self.etaphiexclusivebins[5:6],
                                    "PhiZero" :self.etaphiexclusivebins[1:2]+self.etaphiexclusivebins[4:5],
                                    "PhiMinus":self.etaphiexclusivebins[0:1]+self.etaphiexclusivebins[3:4],
                                    }

        self.etaphibins = {"All"             :self.etaphiexclusivebins[0:2]+self.etaphiexclusivebins[3:5],
                           "EtaPlus"         :self.etaphiexclusivebins[0:2], #fix for removal of phi plus
                           "EtaMinus"        :self.etaphiexclusivebins[3:5],
                           # "PhiPlus"         :self.etaphiexclusivebins[2:3]+self.etaphiexclusivebins[5:6],
                           "PhiZero"         :self.etaphiexclusivebins[1:2]+self.etaphiexclusivebins[4:5],
                           "PhiMinus"        :self.etaphiexclusivebins[0:1]+self.etaphiexclusivebins[3:4],
                           "EtaPlusPhiMinus" :self.etaphiexclusivebins[0:1],
                           "EtaPlusPhiZero"  :self.etaphiexclusivebins[1:2],
                           #"EtaPlusPhiPlus"  :self.etaphiexclusivebins[2:3],
                           "EtaMinusPhiMinus":self.etaphiexclusivebins[3:4],
                           "EtaMinusPhiZero" :self.etaphiexclusivebins[4:5],
                           #"EtaMinusPhiPlus" :self.etaphiexclusivebins[5:6]
                           }

        if self.etaphi not in self.etaphibins.keys():
            print "Invalid eta/phi option specified: %s.  Allowed options are:"%(self.etaphi)
            print self.etaphibins.keys()
            exit(1)

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

    def writeOut(self):
        self.outfile.cd()
        self.outfile.Close()

        return

    def getHistogram(self, sampleFile, etaphi, histPrefix, histSuffix, cloneName, debug=False):
        outHist = None
        for etaphibin in self.etaphibins[etaphi]:
            if debug:
                print "Grabbing: %s/%s%s%s"%(etaphibin,histPrefix,etaphibin,histSuffix)
            pass

            tmpHist = sampleFile.Get("%s/%s%s%s"%(etaphibin,histPrefix,etaphibin,histSuffix)).Clone("%s_%s"%(etaphibin,cloneName))
            if outHist:
                outHist.Add(tmpHist)
            else:
                outHist = tmpHist.Clone(cloneName)
                pass
            pass
        return outHist

    def runStudy(self, xvals, yvals, debug=False):
        import math

        histPrefix = "%s%s"%(self.histName,"PlusCurve")
        histSuffix = ""

        print "Reference: %s/%s%s%s%s"%(self.etaphi,self.histName,"PlusCurve",self.etaphi,histSuffix)
        print "cosmicDataInFile",self.cosmicDataInFile
        print "p100InFile",self.p100InFile
        print "p500InFile",self.p500InFile

        testHist = self.getHistogram(self.cosmicDataInFile,self.etaphi,histPrefix,histSuffix,"clonecosmicData",True)

        testHist = setMinPT(testHist,self.nTotalBins,self.minpt/1000.,True,debug)
        testHist.Rebin(self.rebins)
        self.refmax = testHist.GetMaximum()

        ### Set up the reference histogram(s)
        plusRefHist  = None
        minusRefHist = None

        ## use fixed MC bias histogram as reference
        if debug:
            print "Using %s/%s%s%s%s as reference histograms"%(self.etaphi,self.histName,"Plus[Minus]Curve",
                                                               self.etaphi,histSuffix)

        histPrefix = "%s%s"%(self.histName,"PlusCurve")
        plusRefHist = self.getHistogram(self.cosmicDataInFile,self.etaphi,histPrefix,histSuffix,"plusRefHist",self.debug)

        histPrefix = "%s%s"%(self.histName,"MinusCurve")
        minusRefHist = self.getHistogram(self.cosmicDataInFile,self.etaphi,histPrefix,histSuffix,"minusRefHist",self.debug)

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

        self.refHist      = setMinPT(refHist,     self.nTotalBins,self.minpt/1000.,True)
        self.plusRefHist  = setMinPT(plusRefHist, self.nTotalBins,self.minpt/1000.,True)
        self.minusRefHist = setMinPT(minusRefHist,self.nTotalBins,self.minpt/1000.,True)

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
        histPrefix = "%s%s"%(self.histName,"PlusCurve")
        histSuffix = ""

        print "Scaling: %s/%s%s%s"%(self.etaphi,histPrefix,self.etaphi,histSuffix)
        plusScaleHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"plusScaleHistp100",self.debug)
        #plusScaleHistp100.Scale(self.p100top500ScaleFactor)

        histPrefix = "%s%s"%(self.histName,"MinusCurve")
        minusScaleHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"minusScaleHistp100",self.debug)
        #minusScaleHistp100.Scale(self.p100top500ScaleFactor)

        histPrefix = "%s%s"%(self.histName,"PlusCurve")
        plusScaleHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"plusScaleHistp500",self.debug)
        plusScaleHistp500.Scale(1./self.p100top500ScaleFactor)

        histPrefix = "%s%s"%(self.histName,"MinusCurve")
        minusScaleHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"minusScaleHistp500",self.debug)
        minusScaleHistp500.Scale(1./self.p100top500ScaleFactor)

        plusScaleHist = plusScaleHistp500.Clone("%s%s%s_scaling"%(self.etaphi,self.histName,"PlusCurve"))
        plusScaleHist.Add(plusScaleHistp100)

        minusScaleHist = minusScaleHistp500.Clone("%s%s%s_scaling"%(self.etaphi,self.histName,"MinusCurve"))
        minusScaleHist.Add(minusScaleHistp100)

        compScaleHist = plusScaleHist.Clone("%s%s_compScaleHist"%(self.etaphi,self.histName))
        compScaleHist.Add(minusScaleHist)

        if debug:
            print "Rebinning comparison scale histograms"
        self.compscaleinto  = compScaleHist.Integral()
        self.compscalepinto = plusScaleHist.Integral()
        self.compscaleminto = minusScaleHist.Integral()

        self.compScaleHist  = setMinPT(compScaleHist, self.nTotalBins,self.minpt/1000.,True)
        self.plusScaleHist  = setMinPT(plusScaleHist, self.nTotalBins,self.minpt/1000.,True)
        self.minusScaleHist = setMinPT(minusScaleHist,self.nTotalBins,self.minpt/1000.,True)

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
        (xvals,yvals) = self.biasLoop(xvals, yvals, negativeBias=True,  zeroBias=False, debug=self.debug)
        ## plots for zero bias
        (xvals,yvals) = self.biasLoop(xvals, yvals, negativeBias=False, zeroBias=True, debug=self.debug)
        ## loop over negative bias
        (xvals,yvals) = self.biasLoop(xvals, yvals, negativeBias=False, zeroBias=False, debug=self.debug)

        graphs = self.makeGraphs(xvals, yvals, debug=self.debug)

        ## this should not be hardcoded
        funcrange = [-self.maxbias,self.maxbias]
        fitrange  = [-self.maxbias,self.maxbias]
        fitresults = self.fitCurve(graphs["chi2"], 8, funcrange, fitrange, debug=self.debug)

        self.outfile.cd()
        fitresults["preFitPoly"].SetName("preFitPoly_%s%s"%(self.histName,self.etaphi))
        fitresults["fitPoly"].SetName("fitPoly_%s%s"%(      self.histName,self.etaphi))
        fitresults["preFitPoly"].Write()
        fitresults["fitPoly"].Write()

        width = fitresults["upper"] - fitresults["lower"]

        self.reset()

        return

    def biasLoop(self, xvals, yvals, negativeBias=False, zeroBias=False, debug=False):

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
                    print "%s/%s%s%s%sBias%03d"%(self.etaphi,self.histName,"PlusCurve",
                                                              self.etaphi,biasChange,
                                                              biasBin)
                    pass

                histPrefix = "%s%s"%(self.histName,"PlusCurve")
                histSuffix = "%sBias%03d"%(biasChange,biasBin)
                plusHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

                histPrefix = "%s%s"%(self.histName,"MinusCurve")
                minusHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)
                #plusHistp100.Scale( self.p100top500ScaleFactor)
                #minusHistp100.Scale(self.p100top500ScaleFactor)

                histPrefix = "%s%s"%(self.histName,"PlusCurve")
                plusHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

                histPrefix = "%s%s"%(self.histName,"MinusCurve")
                minusHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)
                plusHistp500.Scale( 1./self.p100top500ScaleFactor)
                minusHistp500.Scale(1./self.p100top500ScaleFactor)

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
                                                        plusHist, minusHist,
                                                        zeroBias, negativeBias)

                pass
            pass
        else:
            histPrefix = "%s%s"%(self.histName,"PlusCurve")
            histSuffix = ""
            plusHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            histPrefix = "%s%s"%(self.histName,"MinusCurve")
            minusHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            #plusHistp100.Scale( self.p100top500ScaleFactor)
            #minusHistp100.Scale(self.p100top500ScaleFactor)

            histPrefix = "%s%s"%(self.histName,"PlusCurve")
            plusHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            histPrefix = "%s%s"%(self.histName,"MinusCurve")
            minusHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            plusHistp500.Scale( 1./self.p100top500ScaleFactor)
            minusHistp500.Scale(1./self.p100top500ScaleFactor)

            plusHist  = plusHistp500.Clone("%s%s_combined"%(self.histName,"PlusCurve"))
            plusHist.Add(plusHistp100)

            minusHist = minusHistp500.Clone("%s%s_combined"%(self.histName,"MinusCurve"))
            minusHist.Add(minusHistp100)

            index   = self.nBiasBins/self.stepsize
            biasBin = 0
            gifBin  = self.nBiasBins
            (xvals, yvals) = self.compareHistograms(xvals, yvals, index, biasBin, gifBin,
                                                    plusHist, minusHist,
                                                    zeroBias, negativeBias)
            pass

        return (xvals,yvals)

    def compareHistograms(self, xvals, yvals, index, biasBin, gifBin,
                          plusHist, minusHist,
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

            plusHist  = setMinPT(plusHist, self.nTotalBins,self.minpt/1000.,True)
            minusHist = setMinPT(minusHist,self.nTotalBins,self.minpt/1000.,True)

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

            compHist  = setMinPT(compHist, self.nTotalBins,self.minpt/1000.,True)
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
        #compHist.SetMaximum(1.2*self.refmax)
        compHist.SetMaximum(100)
        compHist.SetMinimum(0.1)
        self.refHist.Draw("sames")
        if (self.makeLog):
            pad.SetLogy(True)
            pass

        r.gPad.Update()

        chi2Val  = r.Double(0.) # necessary for pass-by-reference in python
        chi2ndf  = r.Long(0)    # necessary for pass-by-reference in python
        igood    = r.Long(0)    # necessary for pass-by-reference in python
        histopts = "UW,NORM" # unweighted/weighted, normalized
        resids = np.zeros(self.refHist.GetNbinsX(),np.dtype('float64')) # pointer argument, one per bin, not quite working

        prob   = self.refHist.Chi2TestX(compHist,chi2Val,chi2ndf,igood,histopts,resids)
        ksprob = self.refHist.KolmogorovTest(compHist,"")

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

        gifcanvas.SaveAs("%s/%sbiasBinm%04d_b%d_s%d_%s.png"%(self.gifDir, self.etaphi, gifBin,
                                                             self.rebins, self.stepsize,
                                                             self.pmstring))

        return (xvals, yvals)

    def makeGraphs(self, xvals, yvals, debug=False):
        """
        Make the Chi2, reduced Chi2, and KS graphs
        """
        graphs = {}
        self.outfile.cd()
        graphs["chi2ndf"] = prettifyGraph(r.TGraph(xvals.size,xvals,yvals["Chi2NDF"]),self.graphInfo["Chi2NDF"])
        graphs["chi2"]    = prettifyGraph(r.TGraph(xvals.size,xvals,yvals["Chi2"]),   self.graphInfo["Chi2"])
        graphs["ks"]      = prettifyGraph(r.TGraph(xvals.size,xvals,yvals["KS"])  ,   self.graphInfo["KS"]  )


        graphs["chi2ndf"].SetName("chi2ndf_%s%s"%(self.histName,self.etaphi))
        graphs["chi2"].SetName(   "chi2_%s%s"%(   self.histName,self.etaphi))
        graphs["ks"].SetName(     "ks_%s%s"%(     self.histName,self.etaphi))

        graphs["chi2ndf"].Write()
        graphs["chi2"].Write()
        graphs["ks"].Write()

        return graphs


    def fitCurve(self, chi2graph, nparams, funcrange, fitrange, deltaChi2=1.0, debug=False):
        """
        Fit a graph with an n-degree polynomial
        nparams   - degree of polynomial for the pre-fit
        funcrange - lower and upper bounds on the function
        fitrange  - lower and upper bounds on the fit
        """
        import math

        self.outfile.cd()

        preFitPoly = r.TF1("preFitPoly%d"%(nparams), "pol%d"%(nparams),
                           fitrange[0],fitrange[1])
                           # preFitMin-0.3,preFitMin+0.3)

        r.SetOwnership(preFitPoly,False)
        preFitPoly.SetParameters(0,0)
        chi2graph.Fit("preFitPoly%d"%(nparams), "QEMFRN", "",
                      fitrange[0],fitrange[1])
        preFitPoly.SetLineColor(r.kRed)
        preFitPoly.SetLineStyle(2)
        preFitMinBias = preFitPoly.GetMinimumX(fitrange[0], fitrange[1])
        preFitMinChi2 = preFitPoly.GetMinimum(fitrange[0], fitrange[1])
        preFitLower = preFitPoly.GetX(preFitMinChi2+deltaChi2, fitrange[0],   preFitMinBias)
        preFitUpper = preFitPoly.GetX(preFitMinChi2+deltaChi2, preFitMinBias, fitrange[1])
        preFitUncUp  = 5*(preFitUpper - preFitMinBias)
        preFitUncLow = 5*(preFitMinBias - preFitLower)

        #if debug:
        print "preFitMinBias  preFitMinChi2  preFitLowVal  preFitHighVal  preFitLowErr  preFitHighErr"
        print "%13.3f  %13.3f  %12.3f  %13.3f  %12.3f  %13.3f"%(preFitMinBias,preFitMinChi2,
                                                                preFitLower,preFitUpper,
                                                                preFitUncLow,preFitUncUp)
        #pass

        fitPoly = r.TF1("fitPoly", "pol2",
                        preFitMinBias-preFitUncLow,
                        preFitMinBias+preFitUncUp)
                        #funcrange[0],funcrange[1])
        r.SetOwnership(fitPoly,False)
        fitPoly.SetParameters(0,0)
        chi2graph.Fit("fitPoly", "QEMFRN", "",
                      preFitMinBias-preFitUncLow,
                      preFitMinBias+preFitUncUp)
                      #fitrange[0],fitrange[1])
        fitPoly.SetLineColor(r.kViolet)
        fitPoly.SetLineStyle(5)
        results = {}
        results["minBias"] = fitPoly.GetMinimumX(preFitMinBias-preFitUncLow, preFitMinBias+preFitUncUp)
        results["minChi2"] = fitPoly.GetMinimum( preFitMinBias-preFitUncLow, preFitMinBias+preFitUncUp)
        results["lower"]   = fitPoly.GetX(results["minChi2"]+deltaChi2, preFitMinBias-preFitUncLow, results["minBias"])
        results["upper"]   = fitPoly.GetX(results["minChi2"]+deltaChi2, results["minBias"],         preFitMinBias+preFitUncUp)
        results["preFitPoly"] = preFitPoly
        results["fitPoly"]    = fitPoly

        if debug:
            print "fitPoly.Derivative(min)",fitPoly.Derivative(results["minBias"])
            print "fitPoly.Derivative2(min)",fitPoly.Derivative2(results["minBias"])
            pass
        try:
            results["error"]   = math.sqrt(2./fitPoly.Derivative2(results["minBias"]))
        except:
            print "Unable to calculate the fit error, der2 = %2.2f (%2.2f)"%(fitPoly.Derivative2(results["minBias"]),
                                                                             results["minBias"])
            results["error"] = 0
            pass

        results["minos"]   = (abs(results["minBias"]-results["lower"]),
                              abs(results["minBias"]-results["upper"]))
        if debug:
            print "min chi2 = %2.4f (+%2.4f -%2.4f), chi2 min = %2.4f"%(results["minBias"],
                                                                        results["minChi2"],
                                                                        results["lower"],
                                                                        results["upper"])

            pass

        #if debug:
        print "postFitMinBias  postFitMinChi2  postFitLowVal  postFitHighVal"
        print "%14.3f  %14.3f  %13.3f  %14.3f"%(results["minBias"],results["minChi2"],
                                                results["lower"],results["upper"])
        #pass
        return results

if __name__ == "__main__":

    #import cProfile, pstats, StringIO
    #pr = cProfile.Profile()
    #pr.enable()

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
                      metavar="biasbins", default=100,
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
    parser.add_option("--algo", type="string", dest="algo",
                      metavar="algo", default="TuneP",
                      help="[OPTIONAL] Tracking algorithm to use")
    parser.add_option("--pm", action="store_true", dest="pm",
                      metavar="pm",
                      help="[OPTIONAL] Scale plus and minus separately")
    parser.add_option("--xroot", action="store_true", dest="xroot",
                      metavar="xroot",
                      help="[OPTIONAL] Access files over xrootd")
    parser.add_option("--asymdeco", action="store_true", dest="asymdeco",
                      metavar="asymdeco",
                      help="[OPTIONAL] Process the asym_deco sample")
    parser.add_option("--log", action="store_true", dest="log",
                      metavar="log",
                      help="[OPTIONAL] Make curvature plots in log scale")

    (options, args) = parser.parse_args()

    if options.debug:
        print options
        print args
        pass

    checkRequiredArguments(options, parser)

    study = endpointDataMCStudy(infiledir=options.infiledir,
                                outfile=options.outfile,
                                histName=options.histbase,
                                etaphi=options.etaphi,
                                minpt=options.minpt,
                                maxbias=options.maxbias,
                                stepsize=options.stepsize,
                                nBiasBins=options.biasbins,
                                nTotalBins=options.totalbins,
                                rebins=options.rebins,
                                algo=options.algo,
                                pmScaling=options.pm,
                                xroot=options.xroot,
                                asymdeco=options.asymdeco,
                                makeLog=options.log,
                                debug=options.debug)


    ### Create arrays to store the graph points, length = (2*nBiasBins)+1
    xVals = np.zeros(2*options.biasbins/options.stepsize+1,np.dtype('float64'))

    ### Need three Y-arrays, store them as a map
    yVals = {}

    for test in ["KS","Chi2","Chi2NDF"]:
        yVals[test] = np.zeros(2*options.biasbins/options.stepsize+1,np.dtype('float64'))
        pass

    study.runStudy(xVals, yVals, options.debug)
    study.writeOut()

    if options.debug:
        raw_input("press enter to exit")
        pass

    #pr.disable()
    #s = StringIO.StringIO()
    #sortby = 'cumulative'
    #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    #ps.print_stats()
    #print s.getvalue()
