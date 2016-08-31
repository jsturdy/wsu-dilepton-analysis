import sys,os

import ROOT as r

infiles = {
    #"aug04-shawn-closure-test-scalep100_binm10.uw"   :"",
    #"aug04-shawn-closure-test-scalep100_binm10.uw.pm":"",
    #"aug04-shawn-closure-test-scalep100_binp10.uw"    :"",
    #"aug04-shawn-closure-test-scalep100_binp10.uw.pm":"",
    #"aug04-shawn-closure-test2-scalep100_b40_s5_binp10.uw.pm":"",
    #"aug04-shawn-closure-test2-scalep100_b20_s5_binp10.uw.pm":"",
    #"aug04-shawn-closure-test2-scalep100_b64_s5_binp10.uw.pm":"",
    #"aug24_thresh10-shawn-closure-test2-scalep100_b40_s5_binp10.uw.pm":"",
    #"aug24_thresh10-shawn-closure-test2-scalep100_b20_s5_binp10.uw.pm":"",
    #"aug24_thresh10-shawn-closure-test2-scalep100_b64_s5_binp10.uw.pm":"",
    #"aug24_thresh25-shawn-closure-test2-scalep100_b40_s5_binp10.uw.pm":"",
    #"aug24_thresh25-shawn-closure-test2-scalep100_b20_s5_binp10.uw.pm":"",
    #"aug24_thresh25-shawn-closure-test2-scalep100_b64_s5_binp10.uw.pm":"",
    "aug29_thresh04-shawn-closure-All-pm_rec_p25":"",
    "aug29_thresh04-shawn-closure-All-pm_rec_0":"",
    "aug29_thresh04-shawn-closure-All-pm_rec_m25":"",
    #"aug29_thresh04-shawn-closure-EtaMinus-pm_rec_p25":"",
    #"aug29_thresh04-shawn-closure-EtaMinus-pm_rec_0":"",
    #"aug29_thresh04-shawn-closure-EtaMinus-pm_rec_m25":"",
    }
for filename in infiles.keys():
    infile = r.TFile("%s.root"%(filename),"READ")
    N_BINS = 5
    outcan = r.TCanvas("outcan","%s"%(filename),1280,1024)
    outcan.Divide(2,2)
    outcan.cd(1)
    for cbin in range(N_BINS):
        graphname = "chi2_looseMuLowerAll_closureBin%03d"%(cbin)
        graph = infile.Get(graphname)
        if cbin == 0:
            graph.Draw("ALP")
        else:
            graph.Draw("LPSAME")
            pass
        pass
    
    outcan.cd(2)
    chi2Dist = infile.Get("chi2Dist")
    chi2Dist.Rebin(10)
    chi2Dist.Draw()
    outcan.cd(3)
    chi2Min = infile.Get("chi2Min")
    chi2Min.Rebin(2)
    chi2Min.Draw()
    outcan.cd(4)
    chi2Width = infile.Get("chi2Width")
    chi2Width.Rebin(2)
    chi2Width.Draw()
    
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s.png"%(filename))
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s.pdf"%(filename))
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s.eps"%(filename))
    outcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s.C"  %(filename))
    raw_input("press enter to continue")

    pullcan = r.TCanvas("pullcan","%s"%(filename),1280,1024)
    pullcan.Divide(2,3)
    pullcan.cd(1)
    chi2Pull1 = infile.Get("chi2Pull1")
    #chi2Pull1.Rebin(10)
    chi2Pull1.Draw()
    pullcan.cd(2)
    chi2Pull2 = infile.Get("chi2Pull2")
    #chi2Pull2.Rebin(10)
    chi2Pull2.Draw()
    pullcan.cd(3)
    chi2Pull3 = infile.Get("chi2Pull3")
    #chi2Pull3.Rebin(10)
    chi2Pull3.Draw()
    pullcan.cd(4)
    chi2Pull4 = infile.Get("chi2Pull4")
    #chi2Pull4.Rebin(10)
    chi2Pull4.Draw()
    pullcan.cd(5)
    chi2Pull5 = infile.Get("chi2Pull5")
    #chi2Pull5.Rebin(10)
    chi2Pull5.Draw()

    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_pulls.png"%(filename))
    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_pulls.pdf"%(filename))
    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_pulls.eps"%(filename))
    pullcan.SaveAs("~/public/html/Cosmics/2016/EndpointClosureStudy/%s_pulls.C"  %(filename))
    raw_input("press enter to continue")
    pass
raw_input("press enter to exit")

#chi2Pull1
#chi2Pull2
#chi2Pull3
#chi2Pull4
#chi2Pull5
