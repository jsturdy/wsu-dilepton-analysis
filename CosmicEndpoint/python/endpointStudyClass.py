#!/bin/env python

import ROOT as r
import sys,os
import numpy as np

from wsuPythonUtils import *
from wsuPyROOTUtils import *

class endpointStudy(object):
    """
    Generic class for cosmic endpoint studies
    """

    # import ROOT as r
    # import sys,os
    # import numpy as np

    from wsuPythonUtils import setMinPT,prettifyGraph
    from wsuPyROOTUtils import styleHistogram

    etaphiexclusivebins = [
        "EtaPlusPhiMinus","EtaPlusPhiZero","EtaPlusPhiPlus",
        "EtaMinusPhiMinus","EtaMinusPhiZero","EtaMinusPhiPlus"
        ]

    etaphiinclusivebins = {
        "All":     etaphiexclusivebins,
        "EtaPlus": etaphiexclusivebins[0:2],
        "EtaMinus":etaphiexclusivebins[3:5],
        # "PhiPlus":etaphiexclusivebins[2:3]+etaphiexclusivebins[5:6],
        "PhiZero" :etaphiexclusivebins[1:2]+etaphiexclusivebins[4:5],
        "PhiMinus":etaphiexclusivebins[0:1]+etaphiexclusivebins[3:4],
        }

    etaphibins = {
        "All"             :etaphiexclusivebins[0:2]+etaphiexclusivebins[3:5],
        "EtaPlus"         :etaphiexclusivebins[0:2], #fix for removal of phi plus
        "EtaMinus"        :etaphiexclusivebins[3:5],
        # "PhiPlus"         :etaphiexclusivebins[2:3]+etaphiexclusivebins[5:6],
        "PhiZero"         :etaphiexclusivebins[1:2]+etaphiexclusivebins[4:5],
        "PhiMinus"        :etaphiexclusivebins[0:1]+etaphiexclusivebins[3:4],
        "EtaPlusPhiMinus" :etaphiexclusivebins[0:1],
        "EtaPlusPhiZero"  :etaphiexclusivebins[1:2],
        #"EtaPlusPhiPlus"  :etaphiexclusivebins[2:3],
        "EtaMinusPhiMinus":etaphiexclusivebins[3:4],
        "EtaMinusPhiZero" :etaphiexclusivebins[4:5],
        #"EtaMinusPhiPlus" :etaphiexclusivebins[5:6]
        }

    def __init__(self, infiledir, outfile, histName, etaphi, minpt,
                 maxbias=0.2, nBiasBins=40,stepsize=1,
                 nTotalBins=640, factor=1000, rebins=1,
                 algo="TuneP",runperiod="2015",
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
        self.muonleg     = "Lower"
        if histName.find("ower") > 0:
            self.muonleg     = "Lower"
        elif histName.find("pper") > 0:
            self.muonleg     = "Upper"
            pass
        self.etaphi      = etaphi
        self.minpt       = minpt
        self.maxbias     = maxbias
        self.stepsize    = stepsize
        self.nBiasBins   = nBiasBins
        self.nTotalBins  = nTotalBins
        self.factor      = factor
        self.rebins      = rebins
        self.algo        = algo
        self.runperiod   = runperiod
        self.trackAlgos = ["TrackerOnly","TuneP","DYT","DYTT","TPFMS","Picky"]
        if self.algo not in self.trackAlgos:
            errmsg = "Invalid track algo specified: %s.  Allowed options are:\n"%(self.algo)
            # errmsg += self.trackAlgos
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

        self.cosmicDataInFileName = "%s/craft15_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                            self.maxbias,
                                                                                            self.nBiasBins,
                                                                                            self.algo)
        self.p10InFileName = "%s/startup_peak_%s_p10_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                    self.maxbias,
                                                                                                    self.nBiasBins,
                                                                                                    self.algo)
        self.p100InFileName = "%s/startup_peak_%s_p100_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                      self.maxbias,
                                                                                                      self.nBiasBins,
                                                                                                      self.algo)
        self.p500InFileName = "%s/startup_peak_%s_p500_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                      self.maxbias,
                                                                                                      self.nBiasBins,
                                                                                                      self.algo)

        if self.asymdeco:
            if self.runperiod == "2016":
                self.cosmicDataInFileName = "%s/run%s_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                     self.maxbias,
                                                                                                     self.nBiasBins,
                                                                                                     self.algo)
                self.p10InFileName = "%s/asym_deco_%s_p10_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                         self.maxbias,
                                                                                                         self.nBiasBins,
                                                                                                         self.algo)
                self.p100InFileName = "%s/asym_deco_%s_p100_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                           self.maxbias,
                                                                                                           self.nBiasBins,
                                                                                                           self.algo)
                self.p500InFileName = "%s/asym_deco_%s_p500_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                           self.maxbias,
                                                                                                           self.nBiasBins,
                                                                                                           self.algo)
            elif self.runperiod == "2017":
                self.cosmicDataInFileName = "%s_hadded/run%s_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                            self.maxbias,
                                                                                                            self.nBiasBins,
                                                                                                            self.algo)
                self.p10InFileName = "%s_notrigger_thresh10_hadded/all_realistic_deco_p10-100_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                                                                          self.maxbias,
                                                                                                                                          self.nBiasBins,
                                                                                                                                          self.algo)
                self.p100InFileName = "%s_notrigger_thresh10_hadded/all_realistic_deco_p100-500_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                                                                            self.maxbias,
                                                                                                                                            self.nBiasBins,
                                                                                                                                            self.algo)
                self.p500InFileName = "%s_notrigger_thresh10_hadded/all_realistic_deco_p500_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                                                                        self.maxbias,
                                                                                                                                        self.nBiasBins,
                                                                                                                                        self.algo)
                pass
            pass

        if self.xroot:
            #/eos/cms/store/user/sturdy/CosmicEndpoint/2015/sep21_hadded/run2015c_b0.80_pt75_n400_sym
            eossrc = "root://cmseos.fnal.gov///store/user/sturdy"
            eossrc = "root://eoscms.cern.ch//eos/cms/store/user/sturdy"
            self.cosmicDataInFileName = "%s/CosmicEndpoint/%s/%s"%(eossrc,runperiod,self.cosmicDataInFileName)
            self.p10InFileName  = "%s/CosmicEndpoint/%s/%s"%(eossrc,runperiod,self.p10InFileName)
            self.p100InFileName = "%s/CosmicEndpoint/%s/%s"%(eossrc,runperiod,self.p100InFileName)
            self.p500InFileName = "%s/CosmicEndpoint/%s/%s"%(eossrc,runperiod,self.p500InFileName)
            pass

        self.cosmicDataInFile = None
        self.p10InFile = None
        self.p100InFile = None
        self.p500InFile = None

        if (self.cosmicDataInFileName).find("root://") > -1:
            print "using TNetXNGFile for EOS access"
            self.cosmicDataInFile = r.TNetXNGFile(self.cosmicDataInFileName,"read")
            self.p10InFile  = r.TNetXNGFile(self.p10InFileName,"read")
            self.p100InFile = r.TNetXNGFile(self.p100InFileName,"read")
            self.p500InFile = r.TNetXNGFile(self.p500InFileName,"read")
        else:
            self.cosmicDataInFile = r.TFile(self.cosmicDataInFileName,"read")
            self.p10InFile  = r.TFile(self.p10InFileName,"read")
            self.p100InFile = r.TFile(self.p100InFileName,"read")
            self.p500InFile = r.TFile(self.p500InFileName,"read")
            pass

        # print "file               address  IsOpen  IsZombie"
        # print "cosmicDataInFile: 0x%08x  %6d  %8d"%(self.cosmicDataInFile,
        #                                             self.cosmicDataInFile.IsOpen(),
        #                                             self.cosmicDataInFile.IsZombie())
        # print "p10InFile:        0x%08x  %6d  %8d"%(self.p10InFile,
        #                                             self.p10InFile.IsOpen(),
        #                                             self.p10InFile.IsZombie()
        # print "p100InFile:       0x%08x  %6d  %8d"%(self.p100InFile,
        #                                             self.p100InFile.IsOpen(),
        #                                             self.p100InFile.IsZombie()
        # print "p500InFile:       0x%08x  %6d  %8d"%(self.p500InFile.IsOpen(),
        #                                             self.p500InFile.IsOpen(),
        #                                             self.p500InFile.IsZombie()

        # if not self.cosmicDataInFile or not self.p10InFile or not self.p100InFile or not self.p500InFile:
        if not self.cosmicDataInFile or not self.p100InFile or not self.p500InFile:
            print "input files invalid"
            exit(1)

        ## Need to be able to combine multiple MC samples together
        # - p10, p100, p500
        ## these factors depend on the run period, so will have to address that
        ### exclusively binned vs. inclusively binned

        # - p10, p500: scale p10 by (1028051./58898.)
        self.p10top500ScaleFactor  = 1028051./58898.
        # - p100, p500: scale p100 by (1028051./58898.)
        self.p100top500ScaleFactor = 1028051./58898.

        """
        N10  = 1551937

        n10  = 1490125
        n100 = 1565361
        n500 = 1735026
        
        f10'  = 0.42427688752829529
        f100' = 0.079589570968409157
        f500' = 0.0049125705489333656

        f10  = f10*(n10/N10)
        f100 = f100*(n100/N10)
        f500 = f500*(n500/N10)
        """

        self.p10top500ScaleFactor  = 0.079589570968409157
        self.p100top500ScaleFactor = 0.0049125705489333656

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

        if self.etaphi not in endpointStudy.etaphibins.keys():
            errmsg = "Invalid eta/phi option specified: %s.  Allowed options are:"%(self.etaphi)
            errmsg += endpointStudy.etaphibins.keys()
            raise NameError(errmsg)

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
        self.refpinto       = None
        self.refminto       = None
        self.refinta        = None
        self.refpinta       = None
        self.refminta       = None
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
        self.refpinto       = None
        self.refminto       = None
        self.refinta        = None
        self.refpinta       = None
        self.refminta       = None
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
        for etaphibin in endpointStudy.etaphibins[etaphi]:
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
        print "p10InFile",self.p10InFile
        print "p100InFile",self.p100InFile
        print "p500InFile",self.p500InFile

        testHist = self.getHistogram(self.cosmicDataInFile,self.etaphi,histPrefix,histSuffix,"clonecosmicData",True)

        testHist = setMinPT(testHist,self.nTotalBins,self.minpt/1000.,True,debug)
        testHist.Rebin(self.rebins)
        self.refmax = testHist.GetMaximum()

        ### Set up the reference histogram(s)
        plusRefHist  = None
        minusRefHist = None

        ## use data histogram as reference
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
        plusScaleHistp10 = self.getHistogram(self.p10InFile,self.etaphi,histPrefix,histSuffix,"plusScaleHistp10",self.debug)
        #plusScaleHistp10.Scale(self.p10top500ScaleFactor)

        histPrefix = "%s%s"%(self.histName,"MinusCurve")
        minusScaleHistp10 = self.getHistogram(self.p10InFile,self.etaphi,histPrefix,histSuffix,"minusScaleHistp10",self.debug)
        #minusScaleHistp10.Scale(self.p10top500ScaleFactor)

        plusScaleHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"plusScaleHistp100",self.debug)
        #plusScaleHistp100.Scale(self.p100top500ScaleFactor)
        plusScaleHistp100.Scale(self.p10top500ScaleFactor)

        histPrefix = "%s%s"%(self.histName,"MinusCurve")
        minusScaleHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"minusScaleHistp100",self.debug)
        #minusScaleHistp100.Scale(self.p100top500ScaleFactor)
        minusScaleHistp10.Scale(self.p10top500ScaleFactor)

        histPrefix = "%s%s"%(self.histName,"PlusCurve")
        plusScaleHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"plusScaleHistp500",self.debug)
        # plusScaleHistp500.Scale(1./self.p100top500ScaleFactor)
        plusScaleHistp500.Scale(self.p100top500ScaleFactor)

        histPrefix = "%s%s"%(self.histName,"MinusCurve")
        minusScaleHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"minusScaleHistp500",self.debug)
        # minusScaleHistp500.Scale(1./self.p100top500ScaleFactor)
        minusScaleHistp500.Scale(self.p100top500ScaleFactor)

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

                histSuffix = "%sBias%03d"%(biasChange,biasBin)
                histPrefix = "%s%s"%(self.histName,"PlusCurve")
                plusHistp10 = self.getHistogram(self.p10InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

                histPrefix = "%s%s"%(self.histName,"MinusCurve")
                minusHistp10 = self.getHistogram(self.p10InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)
                #plusHistp10.Scale( self.p10top500ScaleFactor)
                #minusHistp10.Scale(self.p10top500ScaleFactor)

                histPrefix = "%s%s"%(self.histName,"PlusCurve")
                plusHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

                histPrefix = "%s%s"%(self.histName,"MinusCurve")
                minusHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)
                #plusHistp100.Scale( self.p100top500ScaleFactor)
                #minusHistp100.Scale(self.p100top500ScaleFactor)
                plusHistp100.Scale( self.p10top500ScaleFactor)
                minusHistp100.Scale(self.p10top500ScaleFactor)

                histPrefix = "%s%s"%(self.histName,"PlusCurve")
                plusHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

                histPrefix = "%s%s"%(self.histName,"MinusCurve")
                minusHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)
                # plusHistp500.Scale( 1./self.p100top500ScaleFactor)
                # minusHistp500.Scale(1./self.p100top500ScaleFactor)
                plusHistp500.Scale( self.p100top500ScaleFactor)
                minusHistp500.Scale(self.p100top500ScaleFactor)

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
            histSuffix = ""
            histPrefix = "%s%s"%(self.histName,"PlusCurve")
            plusHistp10 = self.getHistogram(self.p10InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            histPrefix = "%s%s"%(self.histName,"MinusCurve")
            minusHistp10 = self.getHistogram(self.p10InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            #plusHistp10.Scale( self.p10top500ScaleFactor)
            #minusHistp10.Scale(self.p10top500ScaleFactor)

            histPrefix = "%s%s"%(self.histName,"PlusCurve")
            plusHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            histPrefix = "%s%s"%(self.histName,"MinusCurve")
            minusHistp100 = self.getHistogram(self.p100InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            #plusHistp100.Scale( self.p100top500ScaleFactor)
            #minusHistp100.Scale(self.p100top500ScaleFactor)
            plusHistp100.Scale( self.p10top500ScaleFactor)
            minusHistp100.Scale(self.p10top500ScaleFactor)

            histPrefix = "%s%s"%(self.histName,"PlusCurve")
            plusHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            histPrefix = "%s%s"%(self.histName,"MinusCurve")
            minusHistp500 = self.getHistogram(self.p500InFile,self.etaphi,histPrefix,histSuffix,"",self.debug)

            # plusHistp500.Scale( 1./self.p100top500ScaleFactor)
            # minusHistp500.Scale(1./self.p100top500ScaleFactor)
            plusHistp500.Scale( self.p100top500ScaleFactor)
            minusHistp500.Scale(self.p100top500ScaleFactor)

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
        # compHist.GetXaxis().SetRangeUser(-1.2*(1000./self.minpt),1.2*(1000./self.minpt))
        compHist.GetXaxis().SetRangeUser(-10,10)
        compHist.SetMaximum(1.2*self.refmax)
        #compHist.SetMaximum(100)
        compHist.SetMinimum(5)
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
        # the range must match MAX_CURVE_RANGE in Plot.cc that was used for the trees
        resHist = r.TH1D("ResHist", "", len(resids), -16.0,16.0)
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
        # resHist.GetXaxis().SetRangeUser(-1.2*(1000./self.minpt),1.2*(1000./self.minpt))
        resHist.GetXaxis().SetRangeUser(-10,10)
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

        filetypes = ["eps","png","pdf","C"]
        for filetype in filetypes:
            pad.SetLogy(False)
            gifcanvas.SaveAs("%s/%s_%s_%sbiasBinm%04d_b%d_s%d_pt%d_%s.%s"%(self.gifDir, self.algo, self.muonleg,
                                                                           self.etaphi,gifBin,
                                                                           self.rebins, self.stepsize, self.minpt,
                                                                           self.pmstring,filetype))
            pad.SetLogy(True)
            r.gPad.Update()
            gifcanvas.SaveAs("%s/%s_%s_%sbiasBinm%04d_b%d_s%d_pt%d_%s_log.%s"%(self.gifDir, self.algo, self.muonleg,
                                                                               self.etaphi,gifBin,
                                                                               self.rebins, self.stepsize, self.minpt,
                                                                               self.pmstring,filetype))
            pass

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
        fitwin = 0.3
        preFitPoly = r.TF1("preFitPoly%d"%(nparams), "pol%d"%(nparams),
                           (1-fitwin)*fitrange[0], (1-fitwin)*fitrange[1])

        r.SetOwnership(preFitPoly,False)
        preFitPoly.SetParameters(0,0)
        print "fitting in range %2.4f to %2.4f"%((1-fitwin)*fitrange[0],(1-fitwin)*fitrange[1])
        chi2graph.Fit("preFitPoly%d"%(nparams), "EMFN",
                      "", (1-fitwin)*fitrange[0], (1-fitwin)*fitrange[1])
        preFitPoly.SetLineColor(r.kRed)
        preFitPoly.SetLineStyle(2)
        preFitMinBias = preFitPoly.GetMinimumX((1-fitwin)*fitrange[0], (1-fitwin)*fitrange[1])
        preFitMinChi2 = preFitPoly.GetMinimum( (1-fitwin)*fitrange[0], (1-fitwin)*fitrange[1])
        preFitLower   = preFitPoly.GetX(preFitMinChi2+deltaChi2, (1-fitwin)*fitrange[0],   preFitMinBias)
        preFitUpper   = preFitPoly.GetX(preFitMinChi2+deltaChi2, preFitMinBias, (1-fitwin)*fitrange[1])
        preFitLower2  = preFitPoly.GetX(preFitMinChi2+10*deltaChi2, (1-fitwin)*fitrange[0],   preFitMinBias)
        preFitUpper2  = preFitPoly.GetX(preFitMinChi2+10*deltaChi2, preFitMinBias, fitrange[1])
        preFitUncUp   = 5*(preFitUpper - preFitMinBias)
        preFitUncLow  = 5*(preFitMinBias - preFitLower)

        #if debug:
        print "preFitMinBias  preFitMinChi2  preFitLowVal  preFitHighVal  preFitLowVal2  preFitHighVal2  preFitLowErr  preFitHighErr"
        print "%13.3f  %13.3f  %12.3f  %13.3f  %12.3f  %13.3f  %12.3f  %13.3f"%(preFitMinBias,preFitMinChi2,
                                                                                preFitLower,preFitUpper,
                                                                                preFitLower2,preFitUpper2,
                                                                                preFitUncLow,preFitUncUp)
        #pass

        #fitRange = [preFitMinBias-preFitUncLow,preFitMinBias+preFitUncUp]
        fitRange = [preFitLower2, preFitUpper2]
        fitPoly = r.TF1("fitPoly", "pol2", fitRange[0], fitRange[1])

        r.SetOwnership(fitPoly,False)
        fitPoly.SetParameters(0,0)
        chi2graph.Fit("fitPoly", "EMFN", "", fitRange[0], fitRange[1])

        fitPoly.SetLineColor(r.kViolet)
        fitPoly.SetLineStyle(5)
        results = {}
        results["minBias"] = fitPoly.GetMinimumX(fitRange[0], fitRange[1])
        results["minChi2"] = fitPoly.GetMinimum( fitRange[0], fitRange[1])
        results["lower"]   = fitPoly.GetX(results["minChi2"]+deltaChi2, fitRange[0], results["minBias"])
        results["upper"]   = fitPoly.GetX(results["minChi2"]+deltaChi2, results["minBias"],fitRange[1])
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
