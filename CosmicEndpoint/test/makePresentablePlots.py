import sys,os

import ROOT as r
import numpy as np

r.gROOT.SetBatch(True)
r.gErrorIgnoreLevel = r.kFatal

infiles = [
    # "aug31_thresh04",
    # "sep14_thresh10"
    "oct17_submission_thresh04",
    "oct17_submission_thresh10",
]
bins = [
"p50",
"p40",
"p25",
"p10",
"b0",
"m10",
"m25",
"m40",
"m50",
]
perbin = [
    "chi2Dist",
    "preFitDist",
    "chi2Min",
    "chi2Width",
    "chi2Pull3",
    "chi2Pull4",
    ]
summary = [
    ["distAvgVsBiasGraph",
     "distMeanVsBiasGraph"],
    ["distRMSVsBiasGraph",
     "distSigmaVsBiasGraph"],
    ["pull3AvgVsBiasGraph",
     "pull3MeanVsBiasGraph"],
    ["pull3RMSVsBiasGraph",
     "pull3SigmaVsBiasGraph"],
    ["pull4AvgVsBiasGraph",
     "pull4MeanVsBiasGraph"],
    ["pull4RMSVsBiasGraph",
    "pull4SigmaVsBiasGraph"],
    ]

outdirbase = "~/public/html/Cosmics/2016/EndpointClosureStudy/results"
for inf in infiles:
    os.system("mkdir -p %s/%s"%(outdirbase,inf))
    outdir = "%s/%s"%(outdirbase,inf)
    infile = r.TFile("%s_closure_study_looseMuLowerAll_output.root"%(inf),"read")
    print infile
    for bin in bins:
        for per in perbin:
            objname = "%s_%s"%(bin,per)
            outcan = r.TCanvas("outcan","%s%s"%(bin,per),1280,1024)
            obj = infile.Get(objname)
            if obj:
                obj.Draw()
                pass
            outcan.SaveAs("%s/%s_%s.png"%(outdir,bin,per))
            outcan.SaveAs("%s/%s_%s.pdf"%(outdir,bin,per))
            outcan.SaveAs("%s/%s_%s.png"%(outdir,bin,per))
            outcan.SaveAs("%s/%s_%s.pdf"%(outdir,bin,per))
            pass
        pass

    for sumplt in summary:
        outcan = r.TCanvas("outcan","summary",1280,1024)
        objname0 = "%s"%(sumplt[0])
        obj0 = infile.Get(objname0)
        objname1 = "%s"%(sumplt[1])
        obj1 = infile.Get(objname1)
        obj0.GetXaxis().SetTitle("#Delta#kappa_{inj} c/TeV")
        thelegend = r.TLegend(0.6,0.75,0.8,0.9)
        thelegend.SetFillColor(0)
        thelegend.SetFillStyle(3000)

        if "distAvgVsBiasGraph" in sumplt:
            thelegend.AddEntry(obj0,"Histogram mean","lp")
            thelegend.AddEntry(obj1,"Fit mean","lp")
            obj0.SetTitle("#Delta#kappa_{rec} mean vs #Delta#kappa_{inj}")
            obj0.GetYaxis().SetTitle("Mean #Delta#kappa_{rec} c/TeV")
            obj0.SetMinimum(-0.5)
            obj0.SetMaximum(0.5)
        elif "distRMSVsBiasGraph" in sumplt:
            obj0.SetTitle("#Delta#kappa_{rec} width vs #Delta#kappa_{inj}")
            thelegend.AddEntry(obj0,"Histogram RMS","lp")
            thelegend.AddEntry(obj1,"Fit sigma","lp")
            obj0.GetYaxis().SetTitle("#sigma #Delta#kappa_{rec} c/TeV")
            obj0.SetMinimum(0.0)
            obj0.SetMaximum(0.15)
        elif "pull3MeanVsBiasGraph" in sumplt:
            obj0.SetTitle("Pull mean vs #Delta#kappa_{inj}")
            thelegend.AddEntry(obj0,"Histogram mean","lp")
            thelegend.AddEntry(obj1,"Fit mean","lp")
            obj0.GetYaxis().SetTitle("Pull mean")
            obj0.SetMinimum(-0.5)
            obj0.SetMaximum(0.5)
        elif "pull3RMSVsBiasGraph" in sumplt:
            obj0.SetTitle("Pull width vs #Delta#kappa_{inj}")
            thelegend.AddEntry(obj0,"Histogram RMS","lp")
            thelegend.AddEntry(obj1,"Fit sigma","lp")
            obj0.GetYaxis().SetTitle("Pull #sigma")
            obj0.SetMinimum(0.75)
            obj0.SetMaximum(1.25)
        elif "pull4MeanVsBiasGraph" in sumplt:
            obj0.SetTitle("Pull mean vs #Delta#kappa_{inj}")
            thelegend.AddEntry(obj0,"Histogram mean","lp")
            thelegend.AddEntry(obj1,"Fit mean","lp")
            obj0.GetYaxis().SetTitle("Pull mean")
            obj0.SetMinimum(-0.5)
            obj0.SetMaximum(0.5)
        elif "pull4RMSVsBiasGraph" in sumplt:
            obj0.SetTitle("Pull width vs #Delta#kappa_{inj}")
            thelegend.AddEntry(obj0,"Histogram RMS","lp")
            thelegend.AddEntry(obj1,"Fit sigma","lp")
            obj0.GetYaxis().SetTitle("Pull #sigma")
            obj0.SetMinimum(0.75)
            obj0.SetMaximum(1.25)
            pass
        obj0.GetYaxis().SetTitleOffset(1.5)
        obj0.Draw("ap")
        obj1.Draw("psame")
        obj0.GetYaxis().SetTitle
        r.gPad.SetGridx(r.kTRUE)
        r.gPad.SetGridy(r.kTRUE)
        thelegend.Draw("same")
        outcan.SaveAs("%s/%s_summary.png"%(outdir,sumplt[0]))
        outcan.SaveAs("%s/%s_summary.pdf"%(outdir,sumplt[0]))
        outcan.SaveAs("%s/%s_summary.png"%(outdir,sumplt[0]))
        outcan.SaveAs("%s/%s_summary.pdf"%(outdir,sumplt[0]))
        pass
