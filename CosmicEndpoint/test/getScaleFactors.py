#!/bin/env python

import sys,os
import ROOT as r

fileNames = {
    "asym_deco": {
        "p10": "v5_runGENL1Studies_v1.root",
        "p100":"v5_runGENL1Studies_v1.root",
        "p500":"v5_runGENL1Studies_v1.root",
        },
    "startup_peak": {
        "p10":  "v5_runGENL1Studies_v1.root",
        "p100": "v5_runGENL1Studies_v1.root",
        "p500": "v5_runGENL1Studies_v1.root"
        }
    }
files = {
    "asym_deco": {
        "p10": None,
        "p100":None,
        "p500":None,
        },
    "startup_peak": {
        "p10":  None,
        "p100": None,
        "p500": None
        }
    }
scales = {
    "asym_deco": {
        "p10": 1.0,
        "p100":1.0,
        "p500":1.0,
        },
    "startup_peak": {
        "p10":  1.0,
        "p100": 1.0,
        "p500": 1.0
        }
    }
ptHisto = {
    "asym_deco": {
        "p10": None,
        "p100":None,
        "p500":None,
        },
    "startup_peak": {
        "p10":  None,
        "p100": None,
        "p500": None
        }
    }
ptHistoCut = {
    "asym_deco": {
        "p10": None,
        "p100":None,
        "p500":None,
        },
    "startup_peak": {
        "p10":  None,
        "p100": None,
        "p500": None
        }
    }
legends = {
    "asym_deco"   : [None,None],
    "startup_peak": [None,None]
    }
views = r.TCanvas("views","views",1000,1000)
views.Divide(2,2)
int10to100  = 0.
int10to500  = 0.
int100 = 0.
int500 = 0.
for i,sample in enumerate(fileNames.keys()):
    int10to100  = 0.
    int10to500  = 0.
    int100 = 0.
    int500 = 0.
    views.cd((2*i)+1)
    legends[sample][0] = r.TLegend(0.5,0.7,0.9,0.9)
    legends[sample][0].SetHeader("%s integrals"%(sample))
    legends[sample][0].SetTextSize(0.03)
    legends[sample][0].SetFillColor(0)
    legends[sample][0].SetFillStyle(3000)
    for sub in fileNames[sample].keys():
        print "opening file: %s_%s_%s"%(sample,sub,fileNames[sample][sub])
        files[sample][sub] = r.TFile("%s_%s_%s"%(sample,sub,fileNames[sample][sub]),"r")
        ptHisto[sample][sub] = files[sample][sub].Get("genMCScaleFactors/ptHisto")
        ptHistoCut[sample][sub] = files[sample][sub].Get("genMCScaleFactors/ptHistoCut")
        print ptHisto[sample][sub]
        print ptHistoCut[sample][sub]
        if sub == "p10":
            print "bin(95):%d - bin(100):%d - bin(105):%d"%(ptHisto[sample][sub].FindBin(95),ptHisto[sample][sub].FindBin(100),ptHisto[sample][sub].FindBin(105))
            print "bin(495):%d - bin(500):%d - bin(505):%d"%(ptHisto[sample][sub].FindBin(495),ptHisto[sample][sub].FindBin(500),ptHisto[sample][sub].FindBin(505))
            int10to100 = ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(100),-1)
            int10to500 = ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(500),-1)
            legends[sample][0].AddEntry(ptHisto[sample][sub],"%s: int100:%d"%(sub,int10to100))
            legends[sample][0].AddEntry(0                   ,"%s: int500:%d"%(sub,int10to500))
            scales[sample][sub] = 1.0
            ptHisto[sample][sub].SetTitle("%s sim track p_{T} raw"%(sample))
            ptHisto[sample][sub].SetLineColor(r.kRed)
            ptHisto[sample][sub].SetMarkerColor(r.kRed)
            ptHisto[sample][sub].SetStats(r.kFALSE)
            ptHisto[sample][sub].GetYaxis().SetRangeUser(0.1,100000)
            ptHisto[sample][sub].Draw("ep")
            r.gPad.SetLogy(1)
        elif sub == "p100":
            int100 = ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(100),-1)
            legends[sample][0].AddEntry(ptHisto[sample][sub],"%s: int100:%d"%(sub,int100))
            scales[sample][sub] = int10to100/int100
            ptHisto[sample][sub].SetLineColor(r.kBlue)
            ptHisto[sample][sub].SetMarkerColor(r.kBlue)
            ptHisto[sample][sub].SetStats(r.kFALSE)
            ptHisto[sample][sub].GetYaxis().SetRangeUser(0.1,100000)
            ptHisto[sample][sub].Draw("epsame")
        elif sub == "p500":
            int500 = ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(500),-1)
            legends[sample][0].AddEntry(ptHisto[sample][sub],"%s: int500:%d"%(sub,int500))
            scales[sample][sub] = int10to500/int500
            ptHisto[sample][sub].SetLineColor(r.kOrange)
            ptHisto[sample][sub].SetMarkerColor(r.kOrange)
            ptHisto[sample][sub].SetStats(r.kFALSE)
            ptHisto[sample][sub].Draw("epsame")
            ptHisto[sample][sub].GetYaxis().SetRangeUser(0.1,100000)
        legends[sample][0].Draw()
        views.Update()
        print """%s_%s integral of distribution: %d
  0 <= pT <  10: %d
 10 <= pT < 100: %d
100 <= pT < 500: %d
10  <= pT:       %d
100 <= pT:       %d
500 <= pT:       %d
"""%(sample,sub,
     ptHisto[sample][sub].Integral(),
     ptHisto[sample][sub].Integral(0                                ,ptHisto[sample][sub].FindBin(10)-1),
     ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(10) ,ptHisto[sample][sub].FindBin(100)-1),
     ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(100),ptHisto[sample][sub].FindBin(500)-1),
     ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(10) ,-1),
     ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(100),-1),
     ptHisto[sample][sub].Integral(ptHisto[sample][sub].FindBin(500),-1)
     )
    print """%s_%s integrals
pt10to100: %d
pt10to500: %d
pt100   : %d
pt500   : %d
"""%(sample,sub,
     int10to100,
     int10to500,
     int100,
     int500
     )
    legends[sample][0].Draw()
    views.Update()

for i,sample in enumerate(fileNames.keys()):
    views.cd((2*i)+2)
    print ptHisto[sample]
    print ptHistoCut[sample]
    legends[sample][1] = r.TLegend(0.5,0.7,0.9,0.9)
    legends[sample][1].SetHeader("%s scale factors"%(sample))
    legends[sample][1].SetTextSize(0.03)
    legends[sample][1].SetFillColor(0)
    legends[sample][1].SetFillStyle(3000)
    for sub in fileNames[sample].keys():
        #print "opening file: %s_%s_%s"%(sample,sub,fileNames[sample][sub])
        #files[sample][sub] = r.TFile("%s_%s_%s"%(sample,sub,fileNames[sample][sub]),"r")
        #ptHisto = files[sample][sub].Get("genMCScaleFactors/ptHisto")
        #ptHistoCut = files[sample][sub].Get("genMCScaleFactors/ptHistoCut")
        legends[sample][1].AddEntry(ptHistoCut[sample][sub],"%s: %2.6e"%(sub,scales[sample][sub]))
        if sub == "p10":
            ptHistoCut[sample][sub].SetTitle("%s sim track p_{T} scaled"%(sample))
            ptHistoCut[sample][sub].Scale(scales[sample][sub])
            ptHistoCut[sample][sub].SetLineColor(r.kRed)
            ptHistoCut[sample][sub].SetMarkerColor(r.kRed)
            ptHistoCut[sample][sub].SetStats(r.kFALSE)
            ptHistoCut[sample][sub].Draw("ep")
            ptHistoCut[sample][sub].GetYaxis().SetRangeUser(0.0001,100000)
            r.gPad.SetLogy(1)
        elif sub == "p100":
            ptHistoCut[sample][sub].Scale(scales[sample][sub])
            ptHistoCut[sample][sub].SetLineColor(r.kBlue)
            ptHistoCut[sample][sub].SetMarkerColor(r.kBlue)
            ptHistoCut[sample][sub].SetStats(r.kFALSE)
            ptHistoCut[sample][sub].Draw("epsame")
            ptHistoCut[sample][sub].GetYaxis().SetRangeUser(0.0001,100000)
        elif sub == "p500":
            ptHistoCut[sample][sub].Scale(scales[sample][sub])
            ptHistoCut[sample][sub].SetLineColor(r.kOrange)
            ptHistoCut[sample][sub].SetMarkerColor(r.kOrange)
            ptHistoCut[sample][sub].SetStats(r.kFALSE)
            ptHistoCut[sample][sub].Draw("epsame")
            ptHistoCut[sample][sub].GetYaxis().SetRangeUser(0.0001,100000)
        views.Update()
    legends[sample][1].Draw()
    views.Update()
print scales
views.SaveAs("~/public/html/Cosmics/mcSampleScaling.png")
views.SaveAs("~/public/html/Cosmics/mcSampleScaling.pdf")
views.SaveAs("~/public/html/Cosmics/mcSampleScaling.eps")
views.SaveAs("~/public/html/Cosmics/mcSampleScaling.C")
raw_input("enter to exit")
