#!/bin/env python

from endpointStudyClass import endpointStudy

class endpointDataMCStudy(endpointStudy):
    """
    Run the cosmic endpoint analysis using the data/MC method
    Compares the data curvature distribution to that in the MC
    normalizing MC to data as chosen by the pmScaling option
    - scale mu+ and mu- separately
    - scale the combined mu+/mu- distributions
    """

    from wsuPythonUtils import setMinPT,prettifyGraph
    from wsuPyROOTUtils import styleHistogram

    def __init__(self, infiledir, outfile, histName, etaphi, minpt,
                 maxbias=0.2, nBiasBins=40,stepsize=1,
                 nTotalBins=640, factor=1000, rebins=1,
                 algo="TuneP",runperiod="2015",
                 pmScaling=True,
                 xroot=False,
                 asymdeco=False,
                 makeLog=False,
                 debug=False) :

        endpointStudy.__init__(self, infiledir, outfile, histName, etaphi, minpt,
                               maxbias, nBiasBins,stepsize,
                               nTotalBins, factor, rebins,
                               algo,runperiod,pmScaling,xroot,
                               asymdeco,makeLog,debug)

        import ROOT as r
        import sys,os

        ## clean up this stuff, make it more flexible
        ## filenames
        self.cosmicDataInFileName = "%s/craft15_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,
                                                                                            self.maxbias,
                                                                                            self.nBiasBins,
                                                                                            self.algo)

        if self.asymdeco:
            if self.runperiod == "2016":
                self.cosmicDataInFileName = "%s/run%s_v1_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                     self.maxbias,
                                                                                                     self.nBiasBins,
                                                                                                     self.algo)
            elif self.runperiod == "2017":
                self.cosmicDataInFileName = "%s_hadded/run%s_combined_b%.02f_pt75_n%d_sym/CosmicHistOut_%s.root"%(self.infiledir,self.runperiod,
                                                                                                                  self.maxbias,
                                                                                                                  self.nBiasBins,
                                                                                                                  self.algo)
            pass

        if self.xroot:
            #/eos/cms/store/user/sturdy/CosmicEndpoint/2015/sep21_hadded/run2015c_b0.80_pt75_n400_sym
            eossrc = "root://cmseos.fnal.gov///store/user/sturdy"
            eossrc = "root://eoscms.cern.ch//eos/cms/store/user/sturdy"
            self.cosmicDataInFileName = "%s/CosmicEndpoint/%s/%s"%(eossrc,runperiod,self.cosmicDataInFileName)
            pass

        self.cosmicDataInFile = None

        if (self.cosmicDataInFileName).find("root://") > -1:
            print "using TNetXNGFile for EOS access"
            self.cosmicDataInFile = r.TNetXNGFile(self.cosmicDataInFileName,"read")
        else:
            self.cosmicDataInFile = r.TFile(self.cosmicDataInFileName,"read")
            pass

        print "file               IsOpen  IsZombie"
        print "cosmicDataInFile:  %6d  %8d"%(self.cosmicDataInFile.IsOpen(),
                                             self.cosmicDataInFile.IsZombie())
        print "p10InFile:         %6d  %8d"%(self.p10InFile.IsOpen(),
                                             self.p10InFile.IsZombie())
        print "p100InFile:        %6d  %8d"%(self.p100InFile.IsOpen(),
                                             self.p100InFile.IsZombie())
        print "p500InFile:        %6d  %8d"%(self.p500InFile.IsOpen(),
                                             self.p500InFile.IsZombie())
        print self.cosmicDataInFileName
        print self.p100InFileName
        print self.p500InFileName

        if not self.cosmicDataInFile.IsOpen() or not self.p100InFile.IsOpen() or not self.p500InFile.IsOpen():
            print "Unable to open input file"
            exit(1)

        elif self.cosmicDataInFile.IsZombie() or self.p100InFile.IsZombie() or self.p500InFile.IsZombie():
            print "Input file is zombie"
            exit(1)

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

        pass

    def runStudy(self, xvals, yvals, debug=False):
        import math
        import ROOT as r

        histPrefix = "%s%s"%(self.histName,"PlusCurve")
        histSuffix = ""

        print "Reference: %s/%s%s%s%s"%(self.etaphi,self.histName,"PlusCurve",self.etaphi,histSuffix)
        print "cosmicDataInFile",self.cosmicDataInFile
        print "p10InFile", self.p10InFile
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
        minusScaleHistp100.Scale(self.p10top500ScaleFactor)

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

if __name__ == "__main__":

    from optparse import OptionParser
    from wsuPythonUtils import *
    import numpy as np
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
    parser.add_option("--runperiod", type="string", dest="runperiod",
                      metavar="runperiod", default="2015",
                      help="[OPTIONAL] Running period (default is 2015)")
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
                                runperiod=options.runperiod,
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
