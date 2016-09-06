import sys,os

import ROOT as r
import numpy as np

r.gROOT.SetBatch(True)
r.gErrorIgnoreLevel = r.kFatal
jobname = "aug31_thresh04-shawn_closure_study_All"
infiles = {
    #"_rec_p50":"",
    #"_rec_p40":"",
    "_rec_p25":"",
    #"_rec_p10":"",
    "_rec_b0" :"",
    #"_rec_m10":"",
    "_rec_m25":"",
    #"_rec_m40":"",
    #"_rec_m50":"",
    }

xVals = np.zeros(len(infiles.keys()),np.dtype('float64'))
xErrs = np.zeros(len(infiles.keys()),np.dtype('float64'))
distAvgVsBias   = np.zeros(len(infiles.keys()),np.dtype('float64'))
distMeanVsBias  = np.zeros(len(infiles.keys()),np.dtype('float64'))
distSigmaVsBias = np.zeros(len(infiles.keys()),np.dtype('float64'))
distRMSVsBias   = np.zeros(len(infiles.keys()),np.dtype('float64'))
distAvgVsBiasErr   = np.zeros(len(infiles.keys()),np.dtype('float64'))
distMeanVsBiasErr  = np.zeros(len(infiles.keys()),np.dtype('float64'))
distSigmaVsBiasErr = np.zeros(len(infiles.keys()),np.dtype('float64'))
distRMSVsBiasErr   = np.zeros(len(infiles.keys()),np.dtype('float64'))

pullAvgVsBias   = []
pullMeanVsBias  = []
pullSigmaVsBias = []
pullRMSVsBias   = []
pullAvgVsBiasErr   = []
pullMeanVsBiasErr  = []
pullSigmaVsBiasErr = []
pullRMSVsBiasErr   = []

for pull in range(5):
    pullAvgVsBias.append(np.zeros(len(infiles.keys()),np.dtype('float64')))
    pullMeanVsBias.append(np.zeros(len(infiles.keys()),np.dtype('float64')))
    pullSigmaVsBias.append(np.zeros(len(infiles.keys()),np.dtype('float64')))
    pullRMSVsBias.append(np.zeros(len(infiles.keys()),np.dtype('float64')))
    pullAvgVsBiasErr.append(np.zeros(len(infiles.keys()),np.dtype('float64')))
    pullMeanVsBiasErr.append(np.zeros(len(infiles.keys()),np.dtype('float64')))
    pullSigmaVsBiasErr.append(np.zeros(len(infiles.keys()),np.dtype('float64')))
    pullRMSVsBiasErr.append(np.zeros(len(infiles.keys()),np.dtype('float64')))
    pass

print "%12s:  %12s  %12s  %12s  %12s  %12s  %12s  %12s  %12s  %12s  %12s"%("name","hist mean","mean error",
                                                                           "hist rms", "rms error",
                                                                           "fit par0","par0 err",
                                                                           "fit par1","par1 err",
                                                                           "fit par2","par2 err")
for filename in infiles.keys():
    print filename
    infile = r.TFile("aug31_thresh04-shawn/closure_study/All/%s%s.root"%(jobname,filename),"READ")
    N_BINS = 500
    outcan = r.TCanvas("outcan","%s%s"%(jobname,filename),1280,1024)
    outcan.Divide(2,2)
    outcan.cd(1)

    minBin = 0.2-(5*abs(0.2))
    maxBin = 0.2+(5*abs(0.2))
    resBin = 2

    if (filename.find("m50") > 0):
        minBin = -0.4-(5*abs(0.4))
        maxBin = -0.4+(5*abs(0.4))
        resBin = 0
        xVals[resBin] = -0.4

    elif (filename.find("m40") > 0):
        minBin = -0.32-(5*abs(0.32))
        maxBin = -0.32+(5*abs(0.32))
        resBin = 1
        xVals[resBin] = -0.32

    elif (filename.find("m25") > 0):
        minBin = -0.2-(5*abs(0.2))
        maxBin = -0.2+(5*abs(0.2))
        resBin = 0 #2
        xVals[resBin] = -0.2

    elif (filename.find("m10") > 0):
        minBin = -0.2-(5*abs(0.2))
        maxBin = -0.2+(5*abs(0.2))
        resBin = 3
        xVals[resBin] = -0.08

    elif (filename.find("b0") > 0):
        minBin = -0.1
        maxBin =  0.1
        resBin = 1 #4
        xVals[resBin] = 0.0

    elif (filename.find("p10") > 0):
        minBin = 0.2-(5*abs(0.2))
        maxBin = 0.2+(5*abs(0.2))
        resBin = 5
        xVals[resBin] = 0.08

    elif (filename.find("p25") > 0):
        minBin = 0.2-(5*abs(0.2))
        maxBin = 0.2+(5*abs(0.2))
        resBin = 2 #6
        xVals[resBin] = 0.2

    elif (filename.find("p40") > 0):
        minBin = 0.32-(5*abs(0.32))
        maxBin = 0.32+(5*abs(0.32))
        resBin = 7
        xVals[resBin] = 0.32

    elif (filename.find("p50") > 0):
        minBin = 0.4-(5*abs(0.4))
        maxBin = 0.4+(5*abs(0.4))
        resBin = 8
        xVals[resBin] = 0.4

    else:
        print "Unknown input file"
        continue

    preFitDist = r.TH1D("preFitDist", "pre-fit",500, minBin, maxBin)
    preFitDist.Sumw2()

    for cbin in range(N_BINS):
        graphname = "chi2_looseMuLowerAll_closureBin%03d"%(cbin)
        fitname   = "preFitPoly_looseMuLowerAll_closureBin%03d"%(cbin)
        graph = infile.Get(graphname)
        fit = infile.Get(fitname)
        if cbin == 0:
            if graph:
                graph.Draw("ALP")
                preFitDist.Fill(fit.GetMinimumX(-0.8,0.8))
                pass
        else:
            if graph:
                graph.Draw("LPSAME")
                preFitDist.Fill(fit.GetMinimumX(-0.8,0.8))
                pass
            pass
        pass

    fitFunc = []
    fitFunc.append(r.TF1("fitFunc","gaus",-3,3))
    fitFunc[0].SetParameters(0,0)
    outcan.cd(2)
    chi2Dist = infile.Get("chi2Dist")
    chi2Dist.Rebin(10)
    chi2Dist.SetName("")
    chi2Dist.SetTitle("#chi^{2} minimized #Delta#kappa_{B}^{rec.} distribution")
    chi2Dist.Draw()
    fitFunc[0].SetParameters(0,0)
    chi2Dist.Fit("fitFunc","QEMILPR")
    print "%12s:  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e"%(
        "chi2Dist",chi2Dist.GetMean(),chi2Dist.GetMeanError(),
        chi2Dist.GetRMS(),chi2Dist.GetRMSError(),
        fitFunc[0].GetParameter(0),fitFunc[0].GetParError(0),
        fitFunc[0].GetParameter(1),fitFunc[0].GetParError(1),
        fitFunc[0].GetParameter(2),fitFunc[0].GetParError(2))
    distAvgVsBias[resBin]   = chi2Dist.GetMean()
    distRMSVsBias[resBin]   = chi2Dist.GetRMS()
    distMeanVsBias[resBin]  = fitFunc[0].GetParameter(1)
    distSigmaVsBias[resBin] = fitFunc[0].GetParameter(2)
    distAvgVsBiasErr[resBin]   = chi2Dist.GetMeanError()
    distRMSVsBiasErr[resBin]   = chi2Dist.GetRMSError()
    distMeanVsBiasErr[resBin]  = fitFunc[0].GetParError(1)
    distSigmaVsBiasErr[resBin] = fitFunc[0].GetParError(2)

    preFitDist.Rebin(10)
    preFitDist.SetLineColor(r.kRed)
    preFitDist.SetMarkerColor(r.kRed)
    #preFitDist.Draw("epsames")
    #                   ksiourmen
    r.gStyle.SetOptStat(112210)
    r.gPad.Update()
    st2 = r.gPad.GetPrimitive("stats")
    st2.SetOptFit(1111)
    #st2.SetOptStat(112210)
    st2.SetX1NDC(0.65)
    st2.SetX2NDC(0.9)
    st2.SetY1NDC(0.6)
    st2.SetY2NDC(0.9)
    r.gPad.Update()

    outcan.cd(3)
    chi2Min = infile.Get("chi2Min")
    chi2Min.Rebin(2)
    chi2Min.SetStats(r.kFALSE)
    chi2Min.SetTitle("#chi^{2} minimum distribution")
    chi2Min.Draw()
    outcan.cd(4)
    chi2Width = infile.Get("chi2Width")
    chi2Width.Rebin(2)
    chi2Width.SetStats(r.kFALSE)
    chi2Width.SetTitle("#chi^{2} minimization width distribution")
    chi2Width.Draw()
    outcan.Update()

    #raw_input("press enter to continue")

    pullcan = r.TCanvas("pullcan","%s%s"%(jobname,filename),1280,1024)
    pullcan.Divide(2,3)
    pullcan.cd(1)
    chi2Pull1 = infile.Get("chi2Pull1")
    chi2Pull1.Rebin(4)
    chi2Pull1.Draw()
    fitFunc.append(r.TF1("fitFunc1","gaus",-5,5))
    fitFunc[1].SetParameters(0,0)
    chi2Pull1.Fit("fitFunc1","QEMILPR")
    print "%12s:  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e"%(
        "chi2Pull1",chi2Pull1.GetMean(),chi2Pull1.GetMeanError(),
        chi2Pull1.GetRMS(),chi2Pull1.GetRMSError(),
        fitFunc[1].GetParameter(0),fitFunc[1].GetParError(0),
        fitFunc[1].GetParameter(1),fitFunc[1].GetParError(1),
        fitFunc[1].GetParameter(2),fitFunc[1].GetParError(2))
    pullAvgVsBias[0][resBin]   = chi2Pull1.GetMean()
    pullRMSVsBias[0][resBin]   = chi2Pull1.GetRMS()
    pullMeanVsBias[0][resBin]  = fitFunc[1].GetParameter(1)
    pullSigmaVsBias[0][resBin] = fitFunc[1].GetParameter(2)
    pullAvgVsBiasErr[0][resBin]   = chi2Pull1.GetMeanError()
    pullRMSVsBiasErr[0][resBin]   = chi2Pull1.GetRMSError()
    pullMeanVsBiasErr[0][resBin]  = fitFunc[1].GetParError(1)
    pullSigmaVsBiasErr[0][resBin] = fitFunc[1].GetParError(2)

    r.gPad.Update()
    st2 = r.gPad.GetPrimitive("stats")
    st2.SetOptFit(1111)
    #st2.SetOptStat(112210)
    st2.SetX1NDC(0.65)
    st2.SetX2NDC(0.9)
    st2.SetY1NDC(0.6)
    st2.SetY2NDC(0.9)
    r.gPad.Update()

    pullcan.cd(2)
    chi2Pull2 = infile.Get("chi2Pull2")
    chi2Pull2.Rebin(4)
    chi2Pull2.Draw()
    fitFunc.append(r.TF1("fitFunc2","gaus",-5,5))
    fitFunc[2].SetParameters(0,0)
    chi2Pull2.Fit("fitFunc2","QEMILPR")
    print "%12s:  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e"%(
        "chi2Pull2",chi2Pull2.GetMean(),chi2Pull2.GetMeanError(),
        chi2Pull2.GetRMS(),chi2Pull2.GetRMSError(),
        fitFunc[2].GetParameter(0),fitFunc[2].GetParError(0),
        fitFunc[2].GetParameter(1),fitFunc[2].GetParError(1),
        fitFunc[2].GetParameter(2),fitFunc[2].GetParError(2))
    pullAvgVsBias[1][resBin]   = chi2Pull2.GetMean()
    pullRMSVsBias[1][resBin]   = chi2Pull2.GetRMS()
    pullMeanVsBias[1][resBin]  = fitFunc[2].GetParameter(1)
    pullSigmaVsBias[1][resBin] = fitFunc[2].GetParameter(2)
    pullAvgVsBiasErr[1][resBin]   = chi2Pull2.GetMeanError()
    pullRMSVsBiasErr[1][resBin]   = chi2Pull2.GetRMSError()
    pullMeanVsBiasErr[1][resBin]  = fitFunc[2].GetParError(1)
    pullSigmaVsBiasErr[1][resBin] = fitFunc[2].GetParError(2)

    r.gPad.Update()
    st2 = r.gPad.GetPrimitive("stats")
    st2.SetOptFit(1111)
    #st2.SetOptStat(112210)
    st2.SetX1NDC(0.65)
    st2.SetX2NDC(0.9)
    st2.SetY1NDC(0.6)
    st2.SetY2NDC(0.9)
    r.gPad.Update()

    pullcan.cd(3)
    chi2Pull3 = infile.Get("chi2Pull3")
    chi2Pull3.Rebin(4)
    chi2Pull3.Draw()
    fitFunc.append(r.TF1("fitFunc3","gaus",-5,5))
    fitFunc[3].SetParameters(0,0)
    chi2Pull3.Fit("fitFunc3","QEMILPR")
    print "%12s:  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e"%(
        "chi2Pull3",chi2Pull3.GetMean(),chi2Pull3.GetMeanError(),
        chi2Pull3.GetRMS(),chi2Pull3.GetRMSError(),
        fitFunc[3].GetParameter(0),fitFunc[3].GetParError(0),
        fitFunc[3].GetParameter(1),fitFunc[3].GetParError(1),
        fitFunc[3].GetParameter(2),fitFunc[3].GetParError(2))
    pullAvgVsBias[2][resBin]   = chi2Pull3.GetMean()
    pullRMSVsBias[2][resBin]   = chi2Pull3.GetRMS()
    pullMeanVsBias[2][resBin]  = fitFunc[3].GetParameter(1)
    pullSigmaVsBias[2][resBin] = fitFunc[3].GetParameter(2)
    pullAvgVsBiasErr[2][resBin]   = chi2Pull3.GetMeanError()
    pullRMSVsBiasErr[2][resBin]   = chi2Pull3.GetRMSError()
    pullMeanVsBiasErr[2][resBin]  = fitFunc[3].GetParError(1)
    pullSigmaVsBiasErr[2][resBin] = fitFunc[3].GetParError(2)

    r.gPad.Update()
    st2 = r.gPad.GetPrimitive("stats")
    st2.SetOptFit(1111)
    #st2.SetOptStat(112210)
    st2.SetX1NDC(0.65)
    st2.SetX2NDC(0.9)
    st2.SetY1NDC(0.6)
    st2.SetY2NDC(0.9)
    r.gPad.Update()

    pullcan.cd(4)
    chi2Pull4 = infile.Get("chi2Pull4")
    chi2Pull4.Rebin(4)
    chi2Pull4.Draw()
    fitFunc.append(r.TF1("fitFunc4","gaus",-5,5))
    fitFunc[4].SetParameters(0,0)
    chi2Pull4.Fit("fitFunc4","QEMILPR")
    print "%12s:  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e"%(
        "chi2Pull4",chi2Pull4.GetMean(),chi2Pull4.GetMeanError(),
        chi2Pull4.GetRMS(),chi2Pull4.GetRMSError(),
        fitFunc[4].GetParameter(0),fitFunc[4].GetParError(0),
        fitFunc[4].GetParameter(1),fitFunc[4].GetParError(1),
        fitFunc[4].GetParameter(2),fitFunc[4].GetParError(2))
    pullAvgVsBias[3][resBin]   = chi2Pull4.GetMean()
    pullRMSVsBias[3][resBin]   = chi2Pull4.GetRMS()
    pullMeanVsBias[3][resBin]  = fitFunc[4].GetParameter(1)
    pullSigmaVsBias[3][resBin] = fitFunc[4].GetParameter(2)
    pullAvgVsBiasErr[3][resBin]   = chi2Pull4.GetMeanError()
    pullRMSVsBiasErr[3][resBin]   = chi2Pull4.GetRMSError()
    pullMeanVsBiasErr[3][resBin]  = fitFunc[4].GetParError(1)
    pullSigmaVsBiasErr[3][resBin] = fitFunc[4].GetParError(2)

    r.gPad.Update()
    st2 = r.gPad.GetPrimitive("stats")
    st2.SetOptFit(1111)
    #st2.SetOptStat(112210)
    st2.SetX1NDC(0.65)
    st2.SetX2NDC(0.9)
    st2.SetY1NDC(0.6)
    st2.SetY2NDC(0.9)
    r.gPad.Update()

    pullcan.cd(5)
    chi2Pull5 = infile.Get("chi2Pull5")
    chi2Pull5.Rebin(4)
    chi2Pull5.Draw()
    fitFunc.append(r.TF1("fitFunc5","gaus",-5,5))
    fitFunc[5].SetParameters(0,0)
    chi2Pull5.Fit("fitFunc5","QEMILPR")
    print "%12s:  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e"%(
        "chi2Pull5",chi2Pull5.GetMean(),chi2Pull5.GetMeanError(),
        chi2Pull5.GetRMS(),chi2Pull5.GetRMSError(),
        fitFunc[5].GetParameter(0),fitFunc[5].GetParError(0),
        fitFunc[5].GetParameter(1),fitFunc[5].GetParError(1),
        fitFunc[5].GetParameter(2),fitFunc[5].GetParError(2))
    pullAvgVsBias[4][resBin]   = chi2Pull5.GetMean()
    pullRMSVsBias[4][resBin]   = chi2Pull5.GetRMS()
    pullMeanVsBias[4][resBin]  = fitFunc[5].GetParameter(1)
    pullSigmaVsBias[4][resBin] = fitFunc[5].GetParameter(2)
    pullAvgVsBiasErr[4][resBin]   = chi2Pull5.GetMeanError()
    pullRMSVsBiasErr[4][resBin]   = chi2Pull5.GetRMSError()
    pullMeanVsBiasErr[4][resBin]  = fitFunc[5].GetParError(1)
    pullSigmaVsBiasErr[4][resBin] = fitFunc[5].GetParError(2)

    r.gPad.Update()
    st2 = r.gPad.GetPrimitive("stats")
    st2.SetOptFit(1111)
    #st2.SetOptStat(112210)
    st2.SetX1NDC(0.65)
    st2.SetX2NDC(0.9)
    st2.SetY1NDC(0.6)
    st2.SetY2NDC(0.9)
    r.gPad.Update()
    pullcan.Update()

    #raw_input("press enter to continue")
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s.png"%(jobname,filename))
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s.pdf"%(jobname,filename))
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s.eps"%(jobname,filename))
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s.C"  %(jobname,filename))
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s.png"%(jobname,filename))

    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s_pulls.png"%(jobname,filename))
    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s_pulls.pdf"%(jobname,filename))
    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s_pulls.eps"%(jobname,filename))
    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s_pulls.C"  %(jobname,filename))
    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s%s_pulls.png"%(jobname,filename))
    pass

lastcan = r.TCanvas("lastcan","%s"%("Canvas"),1280,1024)
lastcan.Divide(6,2)
lastcan.cd(1)
distAvgVsBiasGraph   = r.TGraphErrors(3,xVals,distAvgVsBias,xErrs,distAvgVsBiasErr)
distAvgVsBiasGraph.SetMarkerColor(r.kRed)
distAvgVsBiasGraph.SetLineColor(r.kRed)
distMeanVsBiasGraph  = r.TGraphErrors(3,xVals,distMeanVsBias,xErrs,distMeanVsBiasErr)
distMeanVsBiasGraph.SetMarkerColor(r.kBlack)
distMeanVsBiasGraph.SetLineColor(r.kBlack)
distRMSVsBiasGraph   = r.TGraphErrors(3,xVals,distRMSVsBias,xErrs,distRMSVsBiasErr)
distRMSVsBiasGraph.SetMarkerColor(r.kRed)
distRMSVsBiasGraph.SetLineColor(r.kRed)
distSigmaVsBiasGraph = r.TGraphErrors(3,xVals,distSigmaVsBias,xErrs,distSigmaVsBiasErr)
distSigmaVsBiasGraph.SetMarkerColor(r.kBlack)
distSigmaVsBiasGraph.SetLineColor(r.kBlack)
distAvgVsBiasGraph.SetTitle("Mean recovered vs. injected bias")
distAvgVsBiasGraph.Draw("ALP")
distMeanVsBiasGraph.Draw("LPSAME")
lastcan.cd(7)
distRMSVsBiasGraph.SetTitle("Sigma recovered vs. injected bias")
distRMSVsBiasGraph.Draw("ALP")
distSigmaVsBiasGraph.Draw("LPSAME")

pullAvgVsBiasGraph   = []
pullMeanVsBiasGraph  = []
pullSigmaVsBiasGraph = []
pullRMSVsBiasGraph   = []

for pull in range(5):
    pullAvgVsBiasGraph.append(r.TGraphErrors(3,xVals,pullAvgVsBias[pull],xErrs,pullAvgVsBiasErr[pull]))
    pullAvgVsBiasGraph[pull].SetMarkerColor(r.kRed)
    pullAvgVsBiasGraph[pull].SetLineColor(r.kRed)
    pullMeanVsBiasGraph.append(r.TGraphErrors(3,xVals,pullMeanVsBias[pull],xErrs,pullMeanVsBiasErr[pull]))
    pullMeanVsBiasGraph[pull].SetMarkerColor(r.kBlack)
    pullMeanVsBiasGraph[pull].SetLineColor(r.kBlack)
    pullRMSVsBiasGraph.append(r.TGraphErrors(3,xVals,pullRMSVsBias[pull],xErrs,pullRMSVsBiasErr[pull]))
    pullRMSVsBiasGraph[pull].SetMarkerColor(r.kRed)
    pullRMSVsBiasGraph[pull].SetLineColor(r.kRed)
    pullSigmaVsBiasGraph.append(r.TGraphErrors(3,xVals,pullSigmaVsBias[pull],xErrs,pullSigmaVsBiasErr[pull]))
    pullSigmaVsBiasGraph[pull].SetMarkerColor(r.kBlack)
    pullSigmaVsBiasGraph[pull].SetLineColor(r.kBlack)
    lastcan.cd(pull+1+1)
    pullAvgVsBiasGraph[pull].SetTitle("Pull%d mean vs. injected bias"%(pull+1))
    pullAvgVsBiasGraph[pull].Draw("ALP")
    pullMeanVsBiasGraph[pull].Draw("LPSAME")

    lastcan.cd(pull+1+7)
    pullRMSVsBiasGraph[pull].SetTitle("Pull%d width vs. injected bias"%(pull+1))
    pullRMSVsBiasGraph[pull].Draw("ALP")
    pullSigmaVsBiasGraph[pull].Draw("LPSAME")
    pass
lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.png"%(jobname))
lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.pdf"%(jobname))
lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.eps"%(jobname))
lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.C"  %(jobname))
lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.png"%(jobname))
#raw_input("press enter to exit")
