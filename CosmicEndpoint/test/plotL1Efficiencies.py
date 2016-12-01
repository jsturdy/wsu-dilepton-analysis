#!/bin/env python

import sys,os
import ROOT as r
import numpy as np

scales = {
    "asym_deco": {
        "p10" : 1.0,
        "p100": 150834./1105504,
        "p500": 7981./1028051,
        },
    "startup_peak": {
        "p10" : 1.0,
        "p100": 145496./1105504,
        "p500": 7685./882609,
        }
    }
views = r.TCanvas("pteff","High p_{T} ID to L1 eff.",1000,1000)
ptBins  = np.array([0., 50., 100., 150., 200., 300., 500., 2000.,3000])
etaBins  = np.array([0., 50., 100., 150., 200., 300., 500., 2000.,3000])
phiBins  = np.array([0., 50., 100., 150., 200., 300., 500., 2000.,3000])
timeBins = np.array([-100.,-80.,-60.,-50.,-40.,-35.,-30.,-25.,-20.,-15.,-10.,-5.,
                      0.,
                      5.,10.,15.,20.,25.,30.,35.,40.,50.,60.,80.,100])

infile = r.TFile("asym_deco_p100_v5_runGENL1Studies_v1.root","r")
hists = {"den":[None,None,None,None],
         "num":[None,None,None,None]}

for plot in ["pt","eta","phi","time"]:
    extra     = ["", "&&firstPixel","&&D_{xy}<4&&D_{z}<10","&&D_{xy}<4&&D_{z}<10&&firstPixel"]
    plotPads  = [None,None,None,None]
    ratioPads = [None,None,None,None]
    legends   = [None,None,None,None]
    eff       = [None,None,None,None]
    
    views.Divide(2,2)
    plotMax = 0
    plotMin = 0
    for i in range(4):
        views.cd(i+1)
        plotPads[i]  = r.TPad("plotPad%d"%(i), "plotPad%d"%(i),0.0,0.3,1.0,1.0)
        plotPads[i].SetFillStyle(4000)
        plotPads[i].SetFrameFillStyle(4000)
        plotPads[i].SetTopMargin(0.025)
        plotPads[i].SetBottomMargin(0.06)
        plotPads[i].SetLeftMargin(0.075)
        plotPads[i].SetRightMargin(0.05)
        
        plotPads[i].Draw()
        
        views.cd(i+1)
        ratioPads[i] = r.TPad("ratioPad%d"%(i),"ratioPad%d"%(i),0.0,0.0,1.0,0.3)
        ratioPads[i].SetFillStyle(4000)
        ratioPads[i].SetFrameFillStyle(4000)
        ratioPads[i].SetTopMargin(0.03)
        ratioPads[i].SetBottomMargin(0.1)
        ratioPads[i].SetLeftMargin(0.075)
        ratioPads[i].SetRightMargin(0.05)
        ratioPads[i].Draw()
        
        if plot == "pt":
            print "setting up special plot %s"%(plot)
            hists["den"][i] = infile.Get("l1TrigInfo/%s_den%d_hist"%(plot,i)).Rebin(len(ptBins)-1,"%s_den%d_rebinned"%(plot,i),ptBins)
            hists["num"][i] = infile.Get("l1TrigInfo/%s_num%d_hist"%(plot,i)).Rebin(len(ptBins)-1,"%s_num%d_rebinned"%(plot,i),ptBins)
        elif plot == "time":
            print "setting up special plot %s"%(plot)
            hists["den"][i] = infile.Get("l1TrigInfo/%s_den%d_hist"%(plot,i)).Rebin(len(timeBins)-1,
                                                                                    "%s_den%d_rebinned"%(plot,i),timeBins)
            hists["num"][i] = infile.Get("l1TrigInfo/%s_num%d_hist"%(plot,i)).Rebin(len(timeBins)-1,
                                                                                    "%s_num%d_rebinned"%(plot,i),timeBins)
        else:
            print "setting up plot %s"%(plot)
            hists["den"][i] = infile.Get("l1TrigInfo/%s_den%d_hist"%(plot,i)).Rebin(10)
            hists["num"][i] = infile.Get("l1TrigInfo/%s_num%d_hist"%(plot,i)).Rebin(10)
        hists["den"][i].SetLineColor(r.kBlack)
        hists["den"][i].SetLineWidth(2)
        hists["num"][i].SetLineColor(r.kRed)
        hists["num"][i].SetLineWidth(2)
    
        eff[i] = r.TGraphAsymmErrors(hists["num"][i], hists["den"][i], "cl=0.683 b(1,1) mode")
    
        views.cd(i+1)
        plotPads[i].cd()
        histMin = 0.8*hists["num"][i].GetMinimum()
        if histMin == 0:
            histMin = 0.5
        if i == 0:
            histMax = 1.2*hists["den"][i].GetMaximum()

        hists["den"][i].GetYaxis().SetRangeUser(histMin,histMax)
        hists["den"][i].SetStats(0)
        hists["den"][i].SetTitle("")
        hists["den"][i].Draw("ep0")
        hists["num"][i].Draw("ep0same")

        if plot == "pt":
            print "den%d:%d"%(i,hists["den"][i].Integral(hists["den"][i].FindBin(500),hists["den"][i].FindBin(1999)))
            print "num%d:%d"%(i,hists["num"][i].Integral(hists["num"][i].FindBin(500),hists["num"][i].FindBin(1999)))
    
        plotPads[i].SetLogy(1)
        plotPads[i].SetGridy(1)
        plotPads[i].SetGridx(1)
        
        legends[i] = r.TLegend(0.3,0.8,0.9,0.95)
        legends[i].SetBorderSize(0)
        legends[i].SetTextSize(0.025)
        legends[i].SetLineWidth(0)
        legends[i].SetFillColor(0)
        legends[i].SetFillStyle(3000)
        
        legends[i].AddEntry(hists["den"][i],"#mu pass high-p_{T} ID%s"%(extra[i]))
        legends[i].AddEntry(hists["num"][i],"matched to L1MuonParticle%s"%(extra[i]))
        legends[i].Draw("nb")
    
        ratioPads[i].cd()
        eff[i].SetTitle("")
        eff[i].SetMarkerStyle(r.kFullDiamond)
        eff[i].SetMarkerSize(1)
        eff[i].SetMarkerColor(r.kBlue)
        eff[i].SetLineColor(r.kBlue)
        eff[i].SetLineWidth(2)
        eff[i].Draw("ACP+")
        #eff[i].GetXaxis().SetTitle("p_{T} [GeV]")
        eff[i].GetXaxis().SetNdivisions(510)
        eff[i].GetXaxis().SetTitleOffset(-0.75)
        eff[i].GetXaxis().SetTitleSize(0.075)
        eff[i].GetXaxis().SetLabelSize(0)
        if plot == "pt":
            print "setting up special eff plot %s"%(plot)
            eff[i].GetXaxis().SetRangeUser(ptBins[0],ptBins[-1])
        elif plot == "time":
            print "setting up special eff plot %s"%(plot)
            eff[i].GetXaxis().SetRangeUser(timeBins[0],timeBins[-1])
        else:
            print "setting up eff plot %s"%(plot)
            #eff[i].GetXaxis().SetRangeUser(ptBins[0],ptBins[-1])
            pass
        eff[i].GetYaxis().SetNdivisions(410)
        eff[i].GetYaxis().SetLabelSize(0.07)
        eff[i].GetYaxis().SetTickLength(0.02)
        if plot == "time":
            eff[i].GetYaxis().SetRangeUser(0.,1.)
        elif plot == "eta" or plot == "phi":
            eff[i].GetYaxis().SetRangeUser(0.55,1.)
        else:
            eff[i].GetYaxis().SetRangeUser(0.65,1.)
        ratioPads[i].SetGridy(1)
        ratioPads[i].SetGridx(1)
        views.Update()
    #effToID         = r.TGraphAsymmErrors(hists["num"][0], hists["den"][0], "cl=0.683 b(1,1) mode")
    #effToIDPix      = r.TGraphAsymmErrors(hists["num"][1], hists["den"][1], "cl=0.683 b(1,1) mode")
    #effToIDDxyDz    = r.TGraphAsymmErrors(hists["num"][2], hists["den"][2], "cl=0.683 b(1,1) mode")
    #effToIDDxyDzPix = r.TGraphAsymmErrors(hists["num"][3], hists["den"][3], "cl=0.683 b(1,1) mode")
    
    views.SaveAs("~/public/html/Cosmics/L1Info/asym_deco_p100_efficiency_vs_%s.png"%(plot))
    views.SaveAs("~/public/html/Cosmics/L1Info/asym_deco_p100_efficiency_vs_%s.pdf"%(plot))
    views.SaveAs("~/public/html/Cosmics/L1Info/asym_deco_p100_efficiency_vs_%s.eps"%(plot))
    views.SaveAs("~/public/html/Cosmics/L1Info/asym_deco_p100_efficiency_vs_%s.C"  %(plot))
    views.Clear()

raw_input("enter to exit")
