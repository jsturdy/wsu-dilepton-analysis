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
                 algo="TuneP",mcmode="exbin",runperiod="2015",
                 pmScaling=True,
                 xroot=False,
                 asymdeco=False,
                 makeLog=False,
                 debug=False) :

        endpointStudy.__init__(self, infiledir, outfile, histName, etaphi, minpt,
                               maxbias, nBiasBins,stepsize,
                               nTotalBins, factor, rebins,
                               algo, mcmode, runperiod,
                               pmScaling, xroot,
                               asymdeco, makeLog, debug)

        ## FIXME: is this derived class really even necessary??
        print "IsOpen  IsZombie  file"
        print "{:6d}  {:8d}  {:s}".format(self.cosmicDataInFile.IsOpen(), self.cosmicDataInFile.IsZombie(), self.cosmicDataInFile.GetName())
        self.mcManager.printFileInfo()

        pass

if __name__ == "__main__":

    from optparse import OptionParser
    from wsuPythonUtils import *
    import numpy as np

    # import cProfile, pstats, StringIO
    # pr = cProfile.Profile()
    # pr.enable()

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
    parser.add_option("--mcmode", type="string", dest="mcmode",
                      metavar="mcmode", default="exbin",
                      help="[OPTIONAL] MC sample generation mode")
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
                                mcmode=options.mcmode,
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

    # pr.disable()
    # s = StringIO.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print s.getvalue()
