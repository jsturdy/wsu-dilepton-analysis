#!/bin/env python

import ROOT as r
import sys,os
import numpy as np

from wsuPythonUtils import *
from wsuPyROOTUtils import *

class mcSampleManager(object):
    """
    Class to provide managment of the MC sample(s) used
    Provides interface to extract necessary scaled histograms from
    * inclusively binned MC samples (2015,2016, SPCosmics)
    * exclusively binned MC samples (2017, SPCosmics)
    * inclusively binned single MC sample (TKCosmic)
    """

    # import ROOT as r
    # import sys,os
    # import numpy as np

    from wsuPythonUtils import setMinPT,prettifyGraph,getHistogram
    from wsuPyROOTUtils import styleHistogram

    modes = ['exbin', 'inbin', 'unibin']

    def __init__(self, mode, samples, runperiod, debug=False):
        """
        `mode` should be one of:
        * exbin
        * incbin
        * unibin

        `samples` should be a dict of sample name to scale factor up to 3 for the binned modes, one for the unibin mode
        ```python
        dict = {
            "file name": scaleFactor
        }
        ```

        `runperiod`

        `debug`
        """

        if mode not in mcSampleManager.modes:
            raise ValueError("Invalid mode ({0:s}) specified".format(mode))

        self.mode     = mode
        # self.samples = samples
        self.nsamples = len(samples)
        self.debug    = debug

        if self.mode in ['inbin','exbin']:
            print("Using binned samples, have {} samples to combine".format(self.nsamples))
        else:
            print("Using the unibin sample")
            if (self.nsamples > 1):
                raise ValueError("Provided more than one sample for unibin mode!")
            pass

        self.inFiles = {}
        for sample,sf in samples.items():
            if sample.find("root://") > -1:
                print "using TNetXNGFile for EOS access"
                self.inFiles[sample] = [r.TNetXNGFile(sample,"read"), sf]
            else:
                self.inFiles[sample] = [r.TFile(sample,"read"),       sf]

        for f,sf in self.inFiles.values():
            if not f.IsOpen():
                print("{:s}:  {:6d}  {:8d}".format(f.GetName(), f.IsOpen(), f.IsZombie()))
                raise Exception("Unable to open file: {:s}".format(f.GetName()))
            elif f.IsZombie():
                print("{:s}:  {:6d}  {:8d}".format(f.GetName(), f.IsOpen(), f.IsZombie()))
                raise Exception("Specified file: {:s} is a zombie".format(f.GetName()))

        if self.debug:
            print(self.inFiles)
            print(self.inFiles.items())
            print(self.inFiles.values())
        pass

    def printFileInfo(self):
        for f,sf in self.inFiles.values():
            print "{:6d}  {:8d}  {:s}".format(f.IsOpen(), f.IsZombie(), f.GetName())
        pass

    def getMCHistogram(self, etaphi, hName, hSuffix, cFmt):
        ### calculating a scale factor from the un-biased MC

        histSuffix = hSuffix
        if self.mode in ['inbin','exbin']:
            print("Using binned samples, have {} samples to combine".format(self.nsamples))
            print "Scaling: {:s}/{:s}{:s}{:s}".format(etaphi, histPrefix, etaphi, histSuffix)
            for f,sf in self.inFiles.values():
                if ("p500" in f.GetName()):
                    histPrefix = "{:s}{:s}".format(hName,"PlusCurve")
                    plusScaleHistp500 = getHistogram(f,etaphi,histPrefix,histSuffix,"plusScaleHistp500_{:s}".format(hName,"PlusCurve"),self.debug)
                    # plusScaleHistp500.Scale(1./sf)
                    plusScaleHistp500.Scale(sf)

                    histPrefix = "{:s}{:s}".format(hName,"MinusCurve")
                    minusScaleHistp500 = getHistogram(f,etaphi,histPrefix,histSuffix,"minusScaleHistp500_{:s}".format(hName,"MinusCurve"),self.debug)
                    # minusScaleHistp500.Scale(1./sf)
                    minusScaleHistp500.Scale(sf)

                    plusScaleHist  = plusScaleHistp500.Clone("{:s}{:s}".format(etaphi, cFmt.format(hName,"PlusCurve")))
                    minusScaleHist = minusScaleHistp500.Clone("{:s}{:s}".format(etaphi,cFmt.format(hName,"MinusCurve")))
                elif ("p100" in f.GetName()):
                    histPrefix = "{:s}{:s}".format(hName,"PlusCurve")
                    plusScaleHistp100 = getHistogram(f,etaphi,histPrefix,histSuffix,"plusScaleHistp100_{:s}".format(hName,"PlusCurve"),self.debug)
                    # plusScaleHistp100.Scale(sf)
                    plusScaleHistp100.Scale(sf)

                    histPrefix = "{:s}{:s}".format(hName,"MinusCurve")
                    minusScaleHistp100 = getHistogram(f,etaphi,histPrefix,histSuffix,"minusScaleHistp100_{:s}".format(hName,"MinusCurve"),self.debug)
                    # minusScaleHistp100.Scale(sf)
                    minusScaleHistp100.Scale(sf)

                    plusScaleHist.Add(plusScaleHistp100)
                    minusScaleHist.Add(minusScaleHistp100)
                elif ("p10" in f.GetName()):
                    histPrefix = "{:s}{:s}".format(hName,"PlusCurve")
                    plusScaleHistp10 = getHistogram(f,etaphi,histPrefix,histSuffix,"plusScaleHistp10_{:s}".format(hName,"PlusCurve"),self.debug)
                    # plusScaleHistp10.Scale(sf)

                    histPrefix = "{:s}{:s}".format(hName,"MinusCurve")
                    minusScaleHistp10 = getHistogram(f,etaphi,histPrefix,histSuffix,"minusScaleHistp10_{:s}".format(hName,"MinusCurve"),self.debug)
                    # minusScaleHistp10.Scale(sf)

                    plusScaleHist.Add(plusScaleHistp10)
                    minusScaleHist.Add(minusScaleHistp10)
        else:
            print("Using the unibin sample", self.inFiles.values())
            (f,sf), = self.inFiles.values()
            histPrefix = "{:s}{:s}".format(hName,"PlusCurve")
            plusScaleHistTmp = getHistogram(f, etaphi, histPrefix, histSuffix, "plusScaleHistTmp", self.debug)
            # plusScaleHistTmp.Scale(sf)
            plusScaleHistTmp.Scale(sf)

            histPrefix = "{:s}{:s}".format(hName,"MinusCurve")
            minusScaleHistTmp = getHistogram(f, etaphi, histPrefix, histSuffix, "minusScaleHistTmp", self.debug)
            # minusScaleHistTmp.Scale(sf)
            minusScaleHistTmp.Scale(sf)

            plusScaleHist  = plusScaleHistTmp.Clone("{:s}{:s}".format(etaphi, cFmt.format(hName,"PlusCurve")))
            minusScaleHist = minusScaleHistTmp.Clone("{:s}{:s}".format(etaphi,cFmt.format(hName,"MinusCurve")))
            pass

        return (plusScaleHist, minusScaleHist)
    pass
