#!/bin/env python

class l1TrigInfo():
    def __init__(self, infile, outfile, tchain=False,debug=False) :
        import ROOT as r
        self.infile  = infile
        self.outfile = r.TFile("%s.root"%(options.outfile),"update")
        self.outdir = self.outfile.MakeDirectory("l1TrigInfo")
        self.tchain  = tchain
        self.debug   = debug
        
        self.outdir.cd()
        self.trig_info_hist = r.TH2D("trig_info","Trigger counters",
                                     6, -0.5, 5.5, 5, -0.5, 4.5)
        self.trig_info_hist.SetStats(r.kFALSE)
        self.trig_info_hist.GetXaxis().SetBinLabel(1,"all")
        self.trig_info_hist.GetXaxis().SetBinLabel(2,"-2.88 < L1 #phi < -0.26")
        self.trig_info_hist.GetXaxis().SetBinLabel(3,"HLT_L1SingleMuOpen")
        self.trig_info_hist.GetXaxis().SetBinLabel(4,"both")
        self.trig_info_hist.GetXaxis().SetBinLabel(5,"L1 #phi > -0.26")
        self.trig_info_hist.GetXaxis().SetBinLabel(6,"both2")
        self.trig_info_hist.GetXaxis().SetTitle("")
        self.trig_info_hist.GetYaxis().SetBinLabel(1,"all")
        self.trig_info_hist.GetYaxis().SetBinLabel(2,"noFwd")
        self.trig_info_hist.GetYaxis().SetBinLabel(3,"isFwd")
        self.trig_info_hist.GetYaxis().SetBinLabel(4,"noRPC")
        self.trig_info_hist.GetYaxis().SetBinLabel(5,"isRPC")
        self.trig_info_hist.GetYaxis().SetTitle("")
        self.trig_info_hist.Sumw2()

        self.trig_eff_hist = r.TH2D("trig_eff","Lower leg high-p_{T} ID to trigger efficiency",
                                    4, -0.5, 3.5, 2, -0.5, 1.5)
        self.trig_eff_hist.SetStats(r.kFALSE)
        self.trig_eff_hist.GetYaxis().SetBinLabel(1,"all")
        self.trig_eff_hist.GetYaxis().SetBinLabel(2,"-2.88 < L1 #phi < -0.26")
        self.trig_eff_hist.GetYaxis().SetTitle("")
        self.trig_eff_hist.GetXaxis().SetBinLabel(1,"High-p_{T} ID")
        self.trig_eff_hist.GetXaxis().SetBinLabel(2,"High-p_{T} ID&&firstPixel")
        self.trig_eff_hist.GetXaxis().SetBinLabel(3,"High-p_{T} ID&&D_{xy}<4&&D_{z}<10")
        self.trig_eff_hist.GetXaxis().SetBinLabel(4,"High-p_{T} ID&&D_{xy}<4&&D_{z}<10&&firstPixel")
        self.trig_eff_hist.GetXaxis().SetTitle("")
        self.trig_eff_hist.Sumw2()

        self.eta_vs_phi_hist = r.TH2D("eta_vs_phi","#eta vs. #phi",
                                      50, -2.5, 2.5, 40, -4., 4.)
        self.eta_vs_phi_hist.SetStats(r.kFALSE)
        self.eta_vs_phi_hist.GetXaxis().SetTitle("L1Muon #eta")
        self.eta_vs_phi_hist.GetYaxis().SetTitle("L1Muon #phi")
        self.eta_vs_phi_hist.Sumw2()

        self.eta_vs_qual_hist = r.TH2D("eta_vs_qual","#eta vs. Quality",
                                       50, -2.5, 2.5, 10, -0.5, 9.5)
        self.eta_vs_qual_hist.SetStats(r.kFALSE)
        self.eta_vs_qual_hist.GetXaxis().SetTitle("L1Muon #eta")
        self.eta_vs_qual_hist.GetYaxis().SetTitle("L1Muon Quality")
        self.eta_vs_qual_hist.Sumw2()

        self.eta_vs_singlemu_hist = r.TH2D("eta_vs_singlemu","#eta vs. L1SingleMuOpen",
                                           50, -2.5, 2.5, 2, -0.5, 1.5)
        self.eta_vs_singlemu_hist.SetStats(r.kFALSE)
        self.eta_vs_singlemu_hist.GetXaxis().SetTitle("L1Muon #eta")
        self.eta_vs_singlemu_hist.GetYaxis().SetTitle("L1MuonOpen")
        self.eta_vs_singlemu_hist.Sumw2()

        self.phi_vs_singlemu_hist = r.TH2D("phi_vs_singlemu","#phi vs. L1SingleMuOpen",
                                           40, -4., 4., 2, -0.5, 1.5)
        self.phi_vs_singlemu_hist.SetStats(r.kFALSE)
        self.phi_vs_singlemu_hist.GetXaxis().SetTitle("L1Muon #phi")
        self.phi_vs_singlemu_hist.GetYaxis().SetTitle("L1MuonOpen")
        self.phi_vs_singlemu_hist.Sumw2()
        
        self.pt_hist   = {"den":[],"num":[]}
        self.eta_hist  = {"den":[],"num":[]}
        self.phi_hist  = {"den":[],"num":[]}
        self.time_hist = {"den":[],"num":[]}
        
        cuts = [
            "high p_{T} ID",
            "high p_{T} ID+firstPixel",
            "high p_{T} ID+D_{xy}<4+D_{z}<10",
            "high p_{T} ID+both",
            ]
        
        for cut in range(4):
            self.pt_hist["den"].append(r.TH1D("pt_den%d_hist"%(cut), cuts[cut], 300, 0., 3000.))
            self.pt_hist["num"].append(r.TH1D("pt_num%d_hist"%(cut), cuts[cut], 300, 0., 3000.))
            self.pt_hist["den"][cut].Sumw2()
            self.pt_hist["num"][cut].Sumw2()
            
            self.eta_hist["den"].append(r.TH1D("eta_den%d_hist"%(cut), cuts[cut], 100, -1., 1.))
            self.eta_hist["num"].append(r.TH1D("eta_num%d_hist"%(cut), cuts[cut], 100, -1., 1.))
            self.eta_hist["den"][cut].Sumw2()
            self.eta_hist["num"][cut].Sumw2()
            
            self.phi_hist["den"].append(r.TH1D("phi_den%d_hist"%(cut), cuts[cut], 50, -3.2, 0.))
            self.phi_hist["num"].append(r.TH1D("phi_num%d_hist"%(cut), cuts[cut], 50, -3.2, 0.))
            self.phi_hist["den"][cut].Sumw2()
            self.phi_hist["num"][cut].Sumw2()
            
            self.time_hist["den"].append(r.TH1D("time_den%d_hist"%(cut), cuts[cut], 4000, -100., 100.))
            self.time_hist["num"].append(r.TH1D("time_num%d_hist"%(cut), cuts[cut], 4000, -100., 100.))
            self.time_hist["den"][cut].Sumw2()
            self.time_hist["num"][cut].Sumw2()
            pass
        return

    def processTree(self,tree):
        for ev in tree:
            # performance hit of creating an array every time through the event loop
            # rather than just resetting the values to false
            selections = []
            for l1mu in range(ev.nL1Muons):
                tmp1 = []
                for xbin in range(6):
                    tmp2 = []
                    for ybin in range(5):
                        tmp2.append(False)
                        pass
                    tmp1.append(tmp2)
                    pass
                selections.append(tmp1)
                pass
            
            for l1mu in range(ev.nL1Muons):
                if ev.l1MuonPhi[l1mu]>2. and ev.l1MuonIsFwd[l1mu]==0:
                    # funky.write("%d/%d/%d - %d\n"%(ev.run,ev.lumi,ev.event,ev.nL1Muons))
                    pass
                
                eta_vs_phi_hist.Fill( ev.l1MuonEta[l1mu],ev.l1MuonPhi[l1mu])
                eta_vs_qual_hist.Fill(ev.l1MuonEta[l1mu],ev.l1MuonQuality[l1mu])
                eta_vs_singlemu_hist.Fill(ev.l1MuonEta[l1mu],ev.l1SingleMu)
                phi_vs_singlemu_hist.Fill(ev.l1MuonPhi[l1mu],ev.l1SingleMu)
                
                selections[l1mu][0][0] = True
                if ev.l1MuonIsFwd[l1mu]==0:
                    selections[l1mu][0][1] = True
                    pass
                if ev.l1MuonIsFwd[l1mu]==1:
                    selections[l1mu][0][2] = True
                    pass
                if ev.l1MuonIsRPC[l1mu]==0:
                    selections[l1mu][0][3] = True
                    pass
                if ev.l1MuonIsRPC[l1mu]==1:
                    selections[l1mu][0][4] = True
                    pass
                
                if ev.l1MuonPhi[l1mu] > -2.88 and ev.l1MuonPhi[l1mu] < -0.26:
                    selections[l1mu][1][0] = True
                    if ev.l1MuonIsFwd[l1mu]==0:
                        selections[l1mu][1][1] = True
                        pass
                    if ev.l1MuonIsFwd[l1mu]==1:
                        selections[l1mu][1][2] = True
                        pass
                    if ev.l1MuonIsRPC[l1mu]==0:
                        selections[l1mu][1][3] = True
                        pass
                    if ev.l1MuonIsRPC[l1mu]==1:
                        selections[l1mu][1][4] = True
                        pass
                    
                    if ev.l1SingleMu:
                        selections[l1mu][3][0] = True
                        if ev.l1MuonIsFwd[l1mu]==0:
                            selections[l1mu][3][1] = True
                            pass
                        if ev.l1MuonIsFwd[l1mu]==1:
                            selections[l1mu][3][2] = True
                            pass
                        if ev.l1MuonIsRPC[l1mu]==0:
                            selections[l1mu][3][3] = True
                            pass
                        if ev.l1MuonIsRPC[l1mu]==1:
                            selections[l1mu][3][4] = True
                            pass
                        pass
                    pass
                elif ev.l1MuonPhi[l1mu] > -0.26:
                    selections[l1mu][4][0] = True
                    if ev.l1MuonIsFwd[l1mu]==0:
                        selections[l1mu][4][1] = True
                        pass
                    if ev.l1MuonIsFwd[l1mu]==1:
                        selections[l1mu][4][2] = True
                        pass
                    if ev.l1MuonIsRPC[l1mu]==0:
                        selections[l1mu][4][3] = True
                        pass
                    if ev.l1MuonIsRPC[l1mu]==1:
                        selections[l1mu][4][4] = True
                        pass
                    
                    if ev.l1SingleMu:
                        selections[l1mu][5][0] = True
                        if ev.l1MuonIsFwd[l1mu]==0:
                            selections[l1mu][5][1] = True
                            pass
                        if ev.l1MuonIsFwd[l1mu]==1:
                            selections[l1mu][5][2] = True
                            pass
                        if ev.l1MuonIsRPC[l1mu]==0:
                            selections[l1mu][5][3] = True
                            pass
                        if ev.l1MuonIsRPC[l1mu]==1:
                            selections[l1mu][5][4] = True
                            pass
                        pass
                    pass
                
                if ev.l1SingleMu:
                    selections[l1mu][2][0] = True
                    if ev.l1MuonIsFwd[l1mu]==0:
                        selections[l1mu][2][1] = True
                        pass
                    if ev.l1MuonIsFwd[l1mu]==1:
                        selections[l1mu][2][2] = True
                        pass
                    if ev.l1MuonIsRPC[l1mu]==0:
                        selections[l1mu][2][3] = True
                        pass
                    if ev.l1MuonIsRPC[l1mu]==1:
                        selections[l1mu][2][4] = True
                        pass
                    pass
                pass
            
            for xbin in range(6):
                for ybin in range(5):
                    result = 0;
                    for l1mu in range(ev.nL1Muons):
                        result = result + selections[l1mu][xbin][ybin]
                        pass
                    # if there is any l1muon in the event passing the given selection, we fill the histo
                    if result > 0:
                        trig_info_hist.Fill(xbin,ybin)
                        pass
                    pass
                pass
            
            matchCount = 0
            for mu in range(ev.nMuons):
                if ev.isUpper[mu]:
                    continue
                if abs(ev.trackEta[mu]) > 0.9:
                    continue
                if not passHighPtMuon(ev,mu):
                    continue
                if options.isMC and not matchSimTrack(ev,mu,0.9,0.9,options.debug) > -1:
                    continue
                
                self.trig_eff_hist.Fill(0,0)
                self.pt_hist["den"][0].Fill(ev.trackpT[mu])
                self.eta_hist["den"][0].Fill(ev.trackEta[mu])
                self.phi_hist["den"][0].Fill(ev.trackPhi[mu])
                self.time_hist["den"][0].Fill(ev.tpin[mu])
                
                matchCount = matchCount + 1
                
                if matchL1SingleMu(ev,mu,0.9,0.9,options.debug) > -1:
                    self.trig_eff_hist.Fill(0,1)
                    self.pt_hist["num"][0].Fill(ev.trackpT[mu])
                    self.eta_hist["num"][0].Fill(ev.trackEta[mu])
                    self.phi_hist["num"][0].Fill(ev.trackPhi[mu])
                    self.time_hist["num"][0].Fill(ev.tpin[mu])
                    pass
                
                # second selection with firstPixelLayer
                if passHighPtMuon(ev,mu,True):
                    self.trig_eff_hist.Fill(1,0)
                    self.pt_hist["den"][1].Fill(ev.trackpT[mu])
                    self.eta_hist["den"][1].Fill(ev.trackEta[mu])
                    self.phi_hist["den"][1].Fill(ev.trackPhi[mu])
                    self.time_hist["den"][1].Fill(ev.tpin[mu])
                    
                    if matchL1SingleMu(ev,mu,0.9,0.9,options.debug) > -1:
                        self.trig_eff_hist.Fill(1,1)
                        self.pt_hist["num"][1].Fill(ev.trackpT[mu])
                        self.eta_hist["num"][1].Fill(ev.trackEta[mu])
                        self.phi_hist["num"][1].Fill(ev.trackPhi[mu])
                        self.time_hist["num"][1].Fill(ev.tpin[mu])
                        pass
                    pass
                
                # third selection with dxy < 4, dz < 10
                if passHighPtMuon(ev,mu) and passDxyDz(ev,mu,4.,10.):
                    self.trig_eff_hist.Fill(2,0)
                    self.pt_hist["den"][2].Fill(ev.trackpT[mu])
                    self.eta_hist["den"][2].Fill(ev.trackEta[mu])
                    self.phi_hist["den"][2].Fill(ev.trackPhi[mu])
                    self.time_hist["den"][2].Fill(ev.tpin[mu])
                    
                    if matchL1SingleMu(ev,mu,0.9,0.9,options.debug) > -1:
                        self.trig_eff_hist.Fill(2,1)
                        self.pt_hist["num"][2].Fill(ev.trackpT[mu])
                        self.eta_hist["num"][2].Fill(ev.trackEta[mu])
                        self.phi_hist["num"][2].Fill(ev.trackPhi[mu])
                        self.time_hist["num"][2].Fill(ev.tpin[mu])
                        pass
                    pass
                
                # fourth selection with dxy < 4, dz < 10 and firstPixelLayer
                if passHighPtMuon(ev,mu,True) and passDxyDz(ev,mu,4.,10.):
                    self.trig_eff_hist.Fill(3,0)
                    self.pt_hist["den"][3].Fill(ev.trackpT[mu])
                    self.eta_hist["den"][3].Fill(ev.trackEta[mu])
                    self.phi_hist["den"][3].Fill(ev.trackPhi[mu])
                    self.time_hist["den"][3].Fill(ev.tpin[mu])
                    
                    if matchL1SingleMu(ev,mu,0.9,0.9,options.debug) > -1:
                        self.trig_eff_hist.Fill(3,1)
                        self.pt_hist["num"][3].Fill(ev.trackpT[mu])
                        self.eta_hist["num"][3].Fill(ev.trackEta[mu])
                        self.phi_hist["num"][3].Fill(ev.trackPhi[mu])
                        self.time_hist["num"][3].Fill(ev.tpin[mu])
                        pass
                    pass
                pass
            if matchCount > 1:
                print "found %d high-pT muons"%(matchCount)
                pass
            
            pass
        return
    
    def writeOut(self):
        self.outfile.cd()
        self.outdir.cd()

        trig_info_hist.Write()
        trig_eff_hist.Write()
        
        eta_vs_phi_hist.Write()
        eta_vs_qual_hist.Write()
        eta_vs_singlemu_hist.Write()
        phi_vs_singlemu_hist.Write()
        
        for cut in range(4):
            pt_hist["den"][cut].Write()
            pt_hist["num"][cut].Write()
            
            eta_hist["den"][cut].Write()
            eta_hist["num"][cut].Write()
            
            phi_hist["den"][cut].Write()
            phi_hist["num"][cut].Write()
            
            time_hist["den"][cut].Write()
            time_hist["num"][cut].Write()
            pass
        
        self.outdir.Write()
        self.outfile.Write()
        self.outfile.Close()
        return
    

if __name__ == "__main__":
    import sys,os
    import ROOT as r
    
    import numpy as np
    from wsuPythonUtils import checkRequiredArguments
    from wsuMuonTreeUtils import *
    
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-i", "--infile", type="string", dest="infile",
                      metavar="infile", default="CosmicMuonTree_MC_76X",
                      help="[REQUIRED] Name of the input ROOT file, or list of files (for -t mode)")
    parser.add_option("-o", "--outfile", type="string", dest="outfile",
                      metavar="outfile", default="l1_trigger_info",
                      help="[REQUIRED] Name of the output ROOT file")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      metavar="debug",
                      help="[OPTIONAL] Run in debug mode")
    parser.add_option("-m", "--mc", action="store_true", dest="isMC",
                      metavar="mc",
                      help="[OPTIONAL] Processing MC, so match to sim tracks")
    parser.add_option("-t", "--tchain", action="store_true", dest="tchain",
                      metavar="tchain",
                      help="[OPTIONAL] Use a TChain rather than the raw file, must specify a list of input files as a text file to -i")

    parser.add_option("--craftfile", type="string", dest="craftfile",
                      metavar="craftfile", default="CosmicMuonTree_MC_76X",
                      help="[OPTIONAL] Name of the input CRAFT file, or list of files (for -t mode)")
    parser.add_option("--interfile", type="string", dest="interfile",
                      metavar="interfile", default="CosmicMuonTree_MC_76X",
                      help="[OPTIONAL] Name of the input Interfill file, or list of files (for -t mode)")
    parser.add_option("--startupfile", type="string", dest="startupfile",
                      metavar="startupfile", default="CosmicMuonTree_MC_76X",
                      help="[OPTIONAL] Name of the input startup MC file, or list of files (for -t mode)")
    parser.add_option("--asymfile", type="string", dest="asymfile",
                      metavar="asymfile", default="CosmicMuonTree_MC_76X",
                      help="[OPTIONAL] Name of the input asymptotic MC file, or list of files (for -t mode)")

    (options, args) = parser.parse_args()
    checkRequiredArguments(options, parser)
    r.gROOT.SetBatch(True)
    
    myfile = None    
    mytree = None    

    study = l1TrigInfo(options.infile,options.outfile,options.tchain,options.debug)
    
    if options.tchain:
        mychain = r.TChain("analysisSPMuons/MuonTree")
        for line in open("%s"%(options.infile),"r"):
            if options.debug:
                print "root://xrootd.unl.edu//%s"%(line[:-1])
                tmp = r.TNetXNGFile("root://xrootd.unl.edu//%s"%(line[:-1]),"r")
                print tmp, "%d - %d"%(tmp.IsZombie(),tmp.IsOpen())
                sys.stdout.flush()
                pass
            print "adding root://xrootd.unl.edu//%s"%(line[:-1])
            sys.stdout.flush()
            mychain.Add("root://xrootd.unl.edu//%s"%(line[:-1]))
            print "to my chain (%d)"%(mychain.GetEntries())
            sys.stdout.flush()
            pass

        mytree = mychain
        study.processTree(mytree)
        pass
    else:
        if (options.infile).find("root://") > -1:
            print "using TNetXNGFile for EOS access"
            print "%s"%(options.infile)
            myfile = r.TNetXNGFile("%s"%(options.infile),"r")
            pass 
        else:
            print "%s"%(options.infile)
            myfile = r.TFile("%s"%(options.infile),"r")
            pass
        
        mytree = myfile.Get("analysisSPMuons/MuonTree")
        study.processTree(mytree)
        pass
        #else:
        #for i,line in enumerate(open("%s"%(options.infile),"r")):
        #    if options.debug and i > 1:
        #        print "debugging, not processing more than 2 files"
        #        break
        #    myfile = r.TNetXNGFile("root://xrootd.unl.edu//%s"%(line[:-1]),"r")
        #    print myfile, "%d - %d"%(myfile.IsZombie(),myfile.IsOpen())
        #    sys.stdout.flush()
        #    
        #    mytree = myfile.Get("analysisSPMuons/MuonTree")
        #    study.processTree(mytree)
        #    #pass
        #    pass
        #pass
    
    study.writeOut()
            
    cuts = {
        "_all":"1",
        "_noFwd":"l1MuonIsFwd==0",
        "_noRPC":"l1MuonIsRPC==0",
        "_isFwd":"l1MuonIsFwd==1",
        "_isRPC":"l1MuonIsRPC==1",
        }
    
