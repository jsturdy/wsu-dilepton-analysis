import sys,os,re

def checkRequiredArguments(opts, parser):
    """From: http://stackoverflow.com/questions/4407539/python-how-to-make-an-option-to-be-required-in-optparse
    Checks whether the parser should require a given argument or not
    """

    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) == None:
            missing_options.extend(option._long_opts)
        if len(missing_options) > 0:
            parser.error('Missing REQUIRED parameters: ' + str(missing_options))
    return

def prettifyGraph(graph, graphParams):
    graph.SetLineColor(graphParams["color"])
    graph.SetLineWidth(4)
    graph.SetMarkerColor(graphParams["color"])
    graph.SetMarkerSize(0.5)
    graph.SetMarkerStyle(graphParams["marker"])
    graph.SetTitle(graphParams["title"])
    graph.GetXaxis().SetTitle("#Delta#kappa_{b} [c/TeV]")
    graph.GetYaxis().SetTitle(graphParams["yaxis"])
    return graph


def flipHist(hist, debug=False):
    import numpy as np
    if (debug):
        print "flipping the observed histogram on top of the reference"
    # loop through bins getting the contents of each bin
    # create an array
    # reverse the array
    # call obs.SetContent(array)
    hist = hist.Clone("flipper")
    obsValsX = np.zeros(hist.GetNbinsX(),np.dtype('float64'))
    obsValsY = np.zeros(hist.GetNbinsX(),np.dtype('float64'))
    obsErrsY = np.zeros(hist.GetNbinsX(),np.dtype('float64'))
    for b in range(hist.GetNbinsX()):
        obsValsX[b] = b+1
        obsValsY[b] = hist.GetBinContent(b+1)
        obsErrsY[b] = hist.GetBinError(b+1)

    obsValsYRev = np.fliplr([obsValsY])[0]
    obsErrsYRev = np.fliplr([obsErrsY])[0]
    # hist.SetContent(obsValsYRev) ## doesn't work for some reason, oh well, hack it
    for b in range(hist.GetNbinsX()):
        hist.SetBinContent(b+1,obsValsYRev[b])
        hist.SetBinError(b+1,obsErrsYRev[b])

    return hist

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

def getHistogram(sampleFile, etaphi, histPrefix, histSuffix, cloneName, debug=False):
    outHist = None
    for etaphibin in etaphibins[etaphi]:
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

def setMinPT(hist, nbins, minPt, symmetric=True, debug=False):
    """Takes an input histogram and sets the bin content to
    0 if q/pT is outside the range
    """
    nbins = hist.GetNbinsX()
    if debug:
        print "nBinsX %d"%(hist.GetNbinsX())
    if symmetric:
        thebin = hist.FindBin(-1./minPt)
        while not (hist.GetXaxis().GetBinLowEdge(thebin) < -1./minPt):
            if debug:
                print thebin, hist.GetXaxis().GetBinLowEdge(thebin), hist.GetXaxis().GetBinUpEdge(thebin)
                pass
            thebin -= 1
            if debug:
                print thebin, hist.GetXaxis().GetBinLowEdge(thebin), hist.GetXaxis().GetBinUpEdge(thebin)
                pass
            pass
        if debug:
            print "before: lower cut off %2.2f, bin %d/%d, integral (first,bin) %d"%(-1./minPt,
                                                                                      thebin,#hist.FindBin(-1./minPt),
                                                                                      hist.GetNbinsX(),
                                                                                      hist.Integral(hist.GetXaxis().GetFirst(),
                                                                                                    thebin))
            print "binlow %f, binup %f, binw %f:"%(hist.GetXaxis().GetBinLowEdge(thebin),
                                                   hist.GetXaxis().GetBinUpEdge( thebin),
                                                   hist.GetXaxis().GetBinWidth(  thebin))
            pass

        for binlow in range(0,thebin+1):
            if debug:
                print "binlow content %d"%(hist.GetBinContent(binlow))
                pass
            hist.SetBinContent(binlow,0)
            hist.SetBinError(binlow,0)
            if debug:
                print "binlow content %d"%(hist.GetBinContent(binlow))
                pass
            pass

        if debug:
            print "after: lower cut off %2.2f, bin %d, integral (first,bin) %d"%(-1./minPt,
                                                                                  hist.FindBin(-1./minPt),
                                                                                  hist.Integral(hist.GetXaxis().GetFirst(),
                                                                                                thebin))
            pass
        pass

    thebin = hist.FindBin(1./minPt)
    while not (hist.GetXaxis().GetBinUpEdge(thebin) > 1./minPt):
        if debug:
            print thebin, hist.GetXaxis().GetBinLowEdge(thebin), hist.GetXaxis().GetBinUpEdge(thebin)
            pass
        thebin += 1
        if debug:
            print thebin, hist.GetXaxis().GetBinLowEdge(thebin), hist.GetXaxis().GetBinUpEdge(thebin)
            pass
        pass

    if debug:
        print "before: upper cut off %2.2f, bin %d/%d, integral (bin,last) %d"%(1./minPt,
                                                                                thebin,#hist.FindBin(1./minPt),
                                                                                hist.GetNbinsX(),
                                                                                hist.Integral(thebin,
                                                                                              hist.GetXaxis().GetLast()))
        print "binlow %f, binup %f, binw %f:"%(hist.GetXaxis().GetBinLowEdge(thebin),
                                               hist.GetXaxis().GetBinUpEdge( thebin),
                                               hist.GetXaxis().GetBinWidth(  thebin))
        print "nbins+1 content %d"%(hist.GetBinContent(nbins+1))
        print "nbins+2 content %d"%(hist.GetBinContent(nbins+2))
        pass

    for binhigh in range(thebin,nbins+2):
        if debug:
            print "binhigh content %d"%(hist.GetBinContent(binhigh))
            pass
        hist.SetBinContent(binhigh,0)
        hist.SetBinError(binhigh,0)
        if debug:
            print "binhigh content %d"%(hist.GetBinContent(binhigh))
            pass
        pass

    if debug:
        print "nbins+1 content %d"%(hist.GetBinContent(nbins+1))
        print "nbins+2 content %d"%(hist.GetBinContent(nbins+2))

        print "after: upper cut off %2.2f, bin %d, integral (bin,last) %d"%(1./minPt,
                                                                            hist.FindBin(1./minPt),
                                                                            hist.Integral(thebin,
                                                                                          hist.GetXaxis().GetLast()))
        pass

    return hist

def makeComparisonPlot(refHist, compHist, rebins, minpt, debug=False):
    pass
