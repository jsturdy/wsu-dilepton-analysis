import sys,os

import ROOT as r
import numpy as np

import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()

r.gROOT.SetBatch(True)
r.gErrorIgnoreLevel = r.kFatal
infiles = {
    "_rec_p50":"",
    "_rec_p40":"",
    "_rec_p25":"",
    "_rec_p10":"",
    "_rec_b0" :"",
    "_rec_m10":"",
    "_rec_m25":"",
    "_rec_m40":"",
    "_rec_m50":"",
    }

muonLegs = [
    #"Upper",
    "Lower"
    ]
etaphibins = [
    "All",
    "EtaPlus",
    "EtaMinus",
    # "PhiPlus",
    "PhiZero",
    "PhiMinus",
    "EtaPlusPhiMinus",
    "EtaPlusPhiZero",
    "EtaPlusPhiPlus",
    "EtaMinusPhiMinus",
    "EtaMinusPhiZero",
    # "EtaMinusPhiPlus",
    ]
pmstring = [
    "",
#    "-pm"
    ]

for leg in muonLegs:
    for pm in pmstring:
        jobname = "oct17_submission_thresh04_closure_study_looseMu%sAll%s"%(leg,pm)

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
        sys.stdout.flush()

        #outfile = r.TFile("oct17_submission_thresh04_closure_study_looseMu%sAll%s_output.root"%(leg,pm),"recreate")
        outfile = r.TFile("oct17_submission_thresh04_closure_study_looseMu%sAll%s_output.root"%(leg,pm),"update")

        for filename in infiles.keys():
            infile = r.TFile("oct17_submission_thresh04/closure_study/All/%s%s.root"%(jobname,filename),"READ")
            print infile
            N_BINS = 500
            outcan = r.TCanvas("outcan","%s%s"%(jobname,filename),1280,1024)
            outcan.Divide(2,2)
            outcan.cd(1)

            minBin = 0.2-(5*abs(0.2))
            maxBin = 0.2+(5*abs(0.2))
            resBin = 2
            filesuffix = "none"

            if (filename.find("m50") > 0):
                minBin = -0.4-1.0
                maxBin = -0.4+1.0
                resBin = 0
                xVals[resBin] = -0.4
                filesuffix = "m50"

            elif (filename.find("m40") > 0):
                minBin = -0.32-1.0
                maxBin = -0.32+1.0
                resBin = 1
                xVals[resBin] = -0.32
                filesuffix = "m40"

            elif (filename.find("m25") > 0):
                minBin = -0.2-1.0
                maxBin = -0.2+1.0
                resBin = 2
                xVals[resBin] = -0.2
                filesuffix = "m25"

            elif (filename.find("m10") > 0):
                minBin = -0.2-1.0
                maxBin = -0.2+1.0
                resBin = 3
                xVals[resBin] = -0.08
                filesuffix = "m10"

            elif (filename.find("b0") > 0):
                minBin = -1.0
                maxBin =  1.0
                resBin = 4
                xVals[resBin] = 0.0
                filesuffix = "b0"

            elif (filename.find("p10") > 0):
                minBin = 0.2-1.0
                maxBin = 0.2+1.0
                resBin = 5
                xVals[resBin] = 0.08
                filesuffix = "p10"

            elif (filename.find("p25") > 0):
                minBin = 0.2-1.0
                maxBin = 0.2+1.0
                resBin = 6
                xVals[resBin] = 0.2
                filesuffix = "p25"

            elif (filename.find("p40") > 0):
                minBin = 0.32-1.0
                maxBin = 0.32+1.0
                resBin = 7
                xVals[resBin] = 0.32
                filesuffix = "p40"

            elif (filename.find("p50") > 0):
                minBin = 0.4-1.0
                maxBin = 0.4+1.0
                resBin = 8
                xVals[resBin] = 0.4
                filesuffix = "p50"

            else:
                print "Unknown input file"
                continue
            print filename,resBin
            sys.stdout.flush()

            preFitDist = r.TH1D("%s_preFitDist"%(filesuffix), "pre-fit",500, minBin, maxBin)
            preFitDist.Sumw2()
            #chi2Pull1 = r.TH1D("%s_chi2Pull1"%(filesuffix),"#Delta#kappa_{inj} - #Delta#kappa_{meas}",200, -1.0, 1.0)
            #chi2Pull1.Sumw2()

            for cbin in range(N_BINS):
                graphname  = "chi2_looseMu%sAll_closureBin%03d"%(leg,cbin)
                prefitname = "preFitPoly_looseMu%sAll_closureBin%03d"%(leg,cbin)
                fitname    = "fitPoly_looseMu%sAll_closureBin%03d"%(leg,cbin)
                graph  = infile.Get(graphname)
                prefit = infile.Get(prefitname)
                fit    = infile.Get(fitname)
                if graph:
                    graph.SetName("%s_%s"%(filesuffix,graphname))
                    prefit.SetName("%s_%s"%(filesuffix,prefitname))
                    fit.SetName("%s_%s"%(filesuffix,fitname))

                    outfile.cd()
                    graph.Write()
                    prefit.Write()
                    fit.Write()

                    if cbin == 0:
                        if graph:
                            graph.Draw("AP")
                            preFitDist.Fill(prefit.GetMinimumX(-0.8,0.8))
                            # chi2Pull1.Fill(xVals[resBin] - fit.GetMinimumX(-0.8,0.8))
                            pass
                        pass
                    else:
                        if graph:
                            graph.Draw("PSAME")
                            preFitDist.Fill(prefit.GetMinimumX(-0.8,0.8))
                            # chi2Pull1.Fill(xVals[resBin] - fit.GetMinimumX(-0.8,0.8))
                            pass
                        pass
                    pass
                pass

            fitFunc = []
            fitFunc.append(r.TF1("%s_fitFunc"%(filesuffix),"gaus",minBin/2,maxBin/2))
            fitFunc[0].SetParameters(0,0)
            outcan.cd(2)
            chi2Dist = infile.Get("chi2Dist")
            chi2Dist.SetName("%s_chi2Dist"%(filesuffix))
            chi2Dist.Rebin(10)
            chi2Dist.SetTitle("#chi^{2} minimized #Delta#kappa_{B}^{rec.} distribution")
            chi2Dist.GetXaxis().SetTitle("#Delta#kappa_{rec.} c/TeV")
            chi2Dist.GetYaxis().SetTitle("Pseudoexperiments per %2.2f c/TeV"%(chi2Dist.GetBinWidth(2)))
            chi2Dist.Draw()
            fitFunc[0].SetParameters(0,0)
            chi2Dist.Fit("%s_fitFunc"%(filesuffix),"QEMIPR")
            print "%12s:  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e"%(
                "chi2Dist",chi2Dist.GetMean(),chi2Dist.GetMeanError(),
                chi2Dist.GetRMS(),chi2Dist.GetRMSError(),
                fitFunc[0].GetParameter(0),fitFunc[0].GetParError(0),
                fitFunc[0].GetParameter(1),fitFunc[0].GetParError(1),
                fitFunc[0].GetParameter(2),fitFunc[0].GetParError(2))
            sys.stdout.flush()
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
            chi2Dist.Write()
            preFitDist.Write()
            fitFunc[0].Write()

            outcan.cd(3)
            chi2Min = infile.Get("chi2Min")
            chi2Min.SetName("%s_chi2Min"%(filesuffix))
            chi2Min.Rebin(2)
            chi2Min.SetStats(r.kFALSE)
            chi2Min.SetTitle("#chi^{2} minimum distribution")
            chi2Min.Draw()
            chi2Min.Write()

            outcan.cd(4)
            chi2Width = infile.Get("chi2Width")
            chi2Width.SetName("%s_chi2Width"%(filesuffix))
            chi2Width.Rebin(2)
            chi2Width.SetStats(r.kFALSE)
            chi2Width.SetTitle("#chi^{2} minimization width distribution")
            chi2Width.Draw()
            chi2Width.Write()
            outcan.Update()

            #raw_input("press enter to continue")

            pullcan = r.TCanvas("pullcan","%s%s"%(jobname,filename),1280,1024)
            pullcan.Divide(2,3)
            for pull in range(5):
                singlepullcan = r.TCanvas("singlepullcan","%s%s"%(jobname,filename),1280,1024)
                idx = pull + 1
                pullcan.cd(idx)
                chi2Pull = infile.Get("chi2Pull%d"%(idx))
                chi2Pull.SetName("%s_chi2Pull%d"%(filesuffix,idx))
                chi2Pull.SetMarkerColor(r.kBlack)
                chi2Pull.SetMarkerStyle(r.kFullDiamond)
                chi2Pull.SetLineColor(r.kBlack)
                chi2Pull.SetLineStyle(1)
                chi2Pull.SetLineWidth(2)
                chi2Pull.Rebin(4)
                chi2Pull.Draw()
                if pull < 1:
                    fitFunc.append(r.TF1("%s_fitFunc%d"%(filesuffix,idx),"gaus",-0.25,0.25))
                elif pull < 2:
                    fitFunc.append(r.TF1("%s_fitFunc%d"%(filesuffix,idx),"gaus",-1.25,1.25))
                else:
                    fitFunc.append(r.TF1("%s_fitFunc%d"%(filesuffix,idx),"gaus",-2.5,2.5))
                    pass
                fitFunc[idx].SetParameters(0,0)
                chi2Pull.Fit("%s_fitFunc%d"%(filesuffix,idx),"QEMIPR")
                print "%12s:  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e  %12.4e"%(
                    "chi2Pull%d"%(idx),chi2Pull.GetMean(),chi2Pull.GetMeanError(),
                    chi2Pull.GetRMS(),chi2Pull.GetRMSError(),
                    fitFunc[idx].GetParameter(0),fitFunc[idx].GetParError(0),
                    fitFunc[idx].GetParameter(1),fitFunc[idx].GetParError(1),
                    fitFunc[idx].GetParameter(2),fitFunc[idx].GetParError(2))
                sys.stdout.flush()
                pullAvgVsBias[pull][resBin]   = chi2Pull.GetMean()
                pullRMSVsBias[pull][resBin]   = chi2Pull.GetRMS()
                pullMeanVsBias[pull][resBin]  = fitFunc[idx].GetParameter(1)
                pullSigmaVsBias[pull][resBin] = fitFunc[idx].GetParameter(2)
                pullAvgVsBiasErr[pull][resBin]   = chi2Pull.GetMeanError()
                pullRMSVsBiasErr[pull][resBin]   = chi2Pull.GetRMSError()
                pullMeanVsBiasErr[pull][resBin]  = fitFunc[idx].GetParError(1)
                pullSigmaVsBiasErr[pull][resBin] = fitFunc[idx].GetParError(2)
                
                r.gPad.Update()
                st2 = r.gPad.GetPrimitive("stats")
                st2.SetOptFit(1111)
                # st2.SetOptStat(112210)
                st2.SetX1NDC(0.65)
                st2.SetX2NDC(0.9)
                st2.SetY1NDC(0.6)
                st2.SetY2NDC(0.9)
                r.gPad.Update()
                chi2Pull.Write()
                fitFunc[idx].Write()
                pass # done looping over pulls

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

        lastcan = r.TCanvas("lastcan","%s"%("Canvas"),1440,900)
        lastcan.Divide(6,2)
        lastcan.cd(1)
        distAvgVsBiasGraph = r.TGraphErrors(len(infiles.keys()),xVals,distAvgVsBias,xErrs,distAvgVsBiasErr)
        distAvgVsBiasGraph.SetMarkerColor(r.kRed)
        distAvgVsBiasGraph.SetMarkerStyle(r.kFullDiamond)
        distAvgVsBiasGraph.SetMarkerSize(1.5)
        distAvgVsBiasGraph.SetLineColor(r.kRed)
        distMeanVsBiasGraph = r.TGraphErrors(len(infiles.keys()),xVals,distMeanVsBias,xErrs,distMeanVsBiasErr)
        distMeanVsBiasGraph.SetMarkerColor(r.kBlack)
        distMeanVsBiasGraph.SetMarkerStyle(r.kFullCircle)
        distMeanVsBiasGraph.SetMarkerSize(1)
        distMeanVsBiasGraph.SetLineColor(r.kBlack)
        distRMSVsBiasGraph = r.TGraphErrors(len(infiles.keys()),xVals,distRMSVsBias,xErrs,distRMSVsBiasErr)
        distRMSVsBiasGraph.SetMarkerColor(r.kRed)
        distRMSVsBiasGraph.SetMarkerStyle(r.kFullDiamond)
        distRMSVsBiasGraph.SetMarkerSize(1.5)
        distRMSVsBiasGraph.SetLineColor(r.kRed)
        distSigmaVsBiasGraph = r.TGraphErrors(len(infiles.keys()),xVals,distSigmaVsBias,xErrs,distSigmaVsBiasErr)
        distSigmaVsBiasGraph.SetMarkerColor(r.kBlack)
        distSigmaVsBiasGraph.SetMarkerStyle(r.kFullCircle)
        distSigmaVsBiasGraph.SetMarkerSize(1)
        distSigmaVsBiasGraph.SetLineColor(r.kBlack)
        distAvgVsBiasGraph.SetTitle("Mean recovered vs. injected bias")
        distAvgVsBiasGraph.GetXaxis().SetTitle("#Delta#kappa_{inj} c/TeV")
        distAvgVsBiasGraph.GetYaxis().SetTitle("Mean #Delta#kappa_{rec} c/TeV")
        distAvgVsBiasGraph.Draw("AP")
        distMeanVsBiasGraph.Draw("PSAME")
        r.gPad.Update()
        r.gPad.SetGridx(r.kTRUE)
        r.gPad.SetGridy(r.kTRUE)
        lastcan.cd(7)

        distRMSVsBiasGraph.SetTitle("Sigma recovered vs. injected bias")
        distAvgVsBiasGraph.GetXaxis().SetTitle("#Delta#kappa_{inj} c/TeV")
        distAvgVsBiasGraph.GetYaxis().SetTitle("#sigma #Delta#kappa_{rec} c/TeV")
        distRMSVsBiasGraph.Draw("AP")
        distSigmaVsBiasGraph.Draw("PSAME")
        r.gPad.Update()
        r.gPad.SetGridx(r.kTRUE)
        r.gPad.SetGridy(r.kTRUE)

        distAvgVsBiasGraph.SetName("distAvgVsBiasGraph")
        distMeanVsBiasGraph.SetName("distMeanVsBiasGraph")
        distRMSVsBiasGraph.SetName("distRMSVsBiasGraph")
        distSigmaVsBiasGraph.SetName("distSigmaVsBiasGraph")

        outfile.cd()
        distAvgVsBiasGraph.Write()
        distMeanVsBiasGraph.Write()
        distRMSVsBiasGraph.Write()
        distSigmaVsBiasGraph.Write()

        pullAvgVsBiasGraph   = []
        pullMeanVsBiasGraph  = []
        pullSigmaVsBiasGraph = []
        pullRMSVsBiasGraph   = []

        sigmaLine = r.TLine(1.2*xVals[0], 1.0, 1.2*xVals[len(infiles.keys())-1], 1.0)
        sigmaLine.SetLineColor(r.kBlue)
        sigmaLine.SetLineWidth(2)

        meanLine  = r.TLine(1.2*xVals[0], 0.0, 1.2*xVals[len(infiles.keys())-1], 0.0)
        meanLine.SetLineColor(r.kBlue)
        meanLine.SetLineWidth(2)

        for pull in range(5):
            pullAvgVsBiasGraph.append(r.TGraphErrors(len(infiles.keys()),xVals,pullAvgVsBias[pull],xErrs,pullAvgVsBiasErr[pull]))
            pullAvgVsBiasGraph[pull].SetMarkerColor(r.kRed)
            pullAvgVsBiasGraph[pull].SetMarkerStyle(r.kFullDiamond)
            pullAvgVsBiasGraph[pull].SetMarkerSize(1.5)
            pullAvgVsBiasGraph[pull].SetLineColor(r.kRed)
            pullMeanVsBiasGraph.append(r.TGraphErrors(len(infiles.keys()),xVals,pullMeanVsBias[pull],xErrs,pullMeanVsBiasErr[pull]))
            pullMeanVsBiasGraph[pull].SetMarkerColor(r.kBlack)
            pullMeanVsBiasGraph[pull].SetMarkerStyle(r.kFullCircle)
            pullMeanVsBiasGraph[pull].SetMarkerSize(1)
            pullMeanVsBiasGraph[pull].SetLineColor(r.kBlack)
            pullRMSVsBiasGraph.append(r.TGraphErrors(len(infiles.keys()),xVals,pullRMSVsBias[pull],xErrs,pullRMSVsBiasErr[pull]))
            pullRMSVsBiasGraph[pull].SetMarkerColor(r.kRed)
            pullRMSVsBiasGraph[pull].SetMarkerStyle(r.kFullDiamond)
            pullRMSVsBiasGraph[pull].SetMarkerSize(1.5)
            pullRMSVsBiasGraph[pull].SetLineColor(r.kRed)
            pullSigmaVsBiasGraph.append(r.TGraphErrors(len(infiles.keys()),xVals,pullSigmaVsBias[pull],xErrs,pullSigmaVsBiasErr[pull]))
            pullSigmaVsBiasGraph[pull].SetMarkerColor(r.kBlack)
            pullSigmaVsBiasGraph[pull].SetMarkerStyle(r.kFullCircle)
            pullSigmaVsBiasGraph[pull].SetMarkerSize(1)
            pullSigmaVsBiasGraph[pull].SetLineColor(r.kBlack)
            lastcan.cd(pull+1+1)
            pullAvgVsBiasGraph[pull].SetTitle("Pull%d mean vs. injected bias"%(pull+1))
            pullAvgVsBiasGraph[pull].GetXaxis().SetTitle("#Delta#kappa_{inj} c/TeV")
            pullAvgVsBiasGraph[pull].GetYaxis().SetTitle("Pull Mean")
            if pull < 1:
                pullAvgVsBiasGraph[pull].GetYaxis().SetRangeUser(-0.075, 0.075)
            elif pull < 2:
                pullAvgVsBiasGraph[pull].GetYaxis().SetRangeUser(-0.25, 0.25)
            else:
                pullAvgVsBiasGraph[pull].GetYaxis().SetRangeUser(-0.25, 0.25)
                pass
            pullAvgVsBiasGraph[pull].Draw("AP")
            pullMeanVsBiasGraph[pull].Draw("PSAME")
            meanLine.Draw("same")
            r.gPad.SetGridx(r.kTRUE)
            r.gPad.SetGridy(r.kTRUE)
            r.gPad.Update()

            lastcan.cd(pull+1+7)
            pullRMSVsBiasGraph[pull].SetTitle("Pull%d width vs. injected bias"%(pull+1))
            pullRMSVsBiasGraph[pull].GetXaxis().SetTitle("#Delta#kappa_{inj} c/TeV")
            pullRMSVsBiasGraph[pull].GetYaxis().SetTitle("Pull #sigma")
            if pull < 1:
                pullRMSVsBiasGraph[pull].GetYaxis().SetRangeUser(0,1+0.05)
            elif pull < 2:
                pullRMSVsBiasGraph[pull].GetYaxis().SetRangeUser(1-0.75,1+0.05)
            else:
                pullRMSVsBiasGraph[pull].GetYaxis().SetRangeUser(1-0.2,1+0.5)
                pass
            pullRMSVsBiasGraph[pull].Draw("AP")
            pullSigmaVsBiasGraph[pull].Draw("PSAME")
            sigmaLine.Draw("same")
            r.gPad.SetGridx(r.kTRUE)
            r.gPad.SetGridy(r.kTRUE)
            r.gPad.Update()

            pullAvgVsBiasGraph[pull].SetName("pull%dAvgVsBiasGraph"%(pull+1))
            pullMeanVsBiasGraph[pull].SetName("pull%dMeanVsBiasGraph"%(pull+1))
            pullRMSVsBiasGraph[pull].SetName("pull%dRMSVsBiasGraph"%(pull+1))
            pullSigmaVsBiasGraph[pull].SetName("pull%dSigmaVsBiasGraph"%(pull+1))

            outfile.cd()
            pullAvgVsBiasGraph[pull].Write()
            pullMeanVsBiasGraph[pull].Write()
            pullRMSVsBiasGraph[pull].Write()
            pullSigmaVsBiasGraph[pull].Write()

            pass
        lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.png"%(jobname))
        lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.pdf"%(jobname))
        lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.eps"%(jobname))
        lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.C"  %(jobname))
        lastcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_results.png"%(jobname))
        #raw_input("press enter to exit")

        outfile.cd()
        outfile.Write()
        outfile.Close()
        pass
    pass

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
