import sys,os

import ROOT as r
import numpy as np
import math

import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()

# keep a pointer to the original TCanvas constructor
caninit = r.TCanvas.__init__

# define a new TCanvas class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentCanvas(r.TCanvas):
  def __init__(self, *args):
    caninit(self,*args)
    r.SetOwnership(self,False)

# replace the old TCanvas class by the new one
r.TCanvas = GarbageCollectionResistentCanvas

# keep a pointer to the original TPad constructor
padinit = r.TPad.__init__

# define a new TPad class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentCanvas(r.TPad):
  def __init__(self, *args):
    padinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TPad class by the new one
r.TPad = GarbageCollectionResistentCanvas

# keep a pointer to the original TH1D constructor
th1dinit = r.TH1D.__init__

# define a new TH1D class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentH1D(r.TH1D):
  def __init__(self, *args):
    th1dinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TH1D class by the new one
r.TH1D = GarbageCollectionResistentH1D

# keep a pointer to the original TLegend constructor
leginit = r.TLegend.__init__

# define a new TLegend class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentLegend(r.TLegend):
  def __init__(self, *args):
    leginit(self,*args)
    r.SetOwnership(self,False)

# replace the old TLegend class by the new one
r.TLegend = GarbageCollectionResistentLegend

# keep a pointer to the original TFile constructor
fileinit = r.TFile.__init__

# define a new TFile class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentFile(r.TFile):
  def __init__(self, *args):
    fileinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TFile class by the new one
r.TFile = GarbageCollectionResistentFile

r.gROOT.SetBatch(True)
r.gErrorIgnoreLevel = r.kFatal

#infilename = "june30-shawn.tunep.pt100.uw.root"
#infilename = "june30-shawn.tunep.pt200.uw.root"
#infilename = "june30-shawn.tracker.pt100.uw.root"
#infilename = "june30-shawn.tracker.pt200.uw.root"
filenames = [
  # "sep21.asym.s5.pt200.b40.lower",
  # "sep21.startup.s5.pt200.b40.lower",
  # "sep26.s5.pt200.b40.lower",
  # "sep26.s5.pt200.b40.upper",
  # "sep26.s5.pt200.b20.lower",
  # "sep26.s5.pt150.b40.lower",
  # "sep26.s5.pt150.b20.lower",

  # "sep21.full.lower",
  # "sep21.full.upper",
  # "sep21.full.lower-pm",
  # "sep21.full.upper-pm",
  # "jan23.TuneP.s25.pt200.b40.lower",
  # "jan23.TrackerOnly.s25.pt200.b40.lower",
  # "jan23.Picky.s25.pt200.b40.lower",
  # "jan23.TPFMS.s25.pt200.b40.lower",
  # # "jan23.DYTT.s25.pt200.b40.lower",
  # "jan23.TuneP.s25.pt200.b40.upper",
  # "jan23.TrackerOnly.s25.pt200.b40.upper",
  # "jan23.Picky.s25.pt200.b40.upper",
  # "jan23.TPFMS.s25.pt200.b40.upper",
  # "jan23.DYTT.s25.pt200.b40.upper",

  # # "jan21.TuneP.s25.pt200.b40.lower",
  # # "jan21.TrackerOnly.s25.pt200.b40.lower",
  # # "jan21.Picky.s25.pt200.b40.lower",
  # # "jan21.TPFMS.s25.pt200.b40.lower",
  # # "jan21.DYTT.s25.pt200.b40.lower",

  # # "jan21.TuneP.s5.pt200.b40.lower",
  # # "jan21.TrackerOnly.s5.pt200.b40.lower",
  # # "jan21.Picky.s5.pt200.b40.lower",
  # # "jan21.DYTT.s5.pt200.b40.lower",

  # "dec11.s5.pt200.b40.lower",
  # "dec11.s5.pt200.b40.upper",
  # "dec11.s5.pt200.b20.lower",
  # "dec11.s5.pt150.b40.lower",
  # "dec11.s5.pt150.b20.lower",
  
  # "aug29_ptbins.TrackerOnly.s20.pt110.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt120.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt125.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt150.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt200.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt250.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt300.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt400.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt500.b40.lower",
  # "aug29_ptbins.TrackerOnly.s20.pt750.b40.lower",

  # "aug29_ptbins.TuneP.s20.pt110.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt120.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt125.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt150.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt200.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt250.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt300.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt400.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt500.b40.lower",
  # "aug29_ptbins.TuneP.s20.pt750.b40.lower",

  # "aug29_ptbins.DYTT.s20.pt110.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt120.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt125.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt150.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt200.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt250.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt300.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt400.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt500.b40.lower",
  # "aug29_ptbins.DYTT.s20.pt750.b40.lower",

  # "aug29_ptbins.Picky.s20.pt110.b40.lower",
  # "aug29_ptbins.Picky.s20.pt120.b40.lower",
  # "aug29_ptbins.Picky.s20.pt125.b40.lower",
  # "aug29_ptbins.Picky.s20.pt150.b40.lower",
  # "aug29_ptbins.Picky.s20.pt200.b40.lower",
  # "aug29_ptbins.Picky.s20.pt250.b40.lower",
  # "aug29_ptbins.Picky.s20.pt300.b40.lower",
  # "aug29_ptbins.Picky.s20.pt400.b40.lower",
  # "aug29_ptbins.Picky.s20.pt500.b40.lower",
  # "aug29_ptbins.Picky.s20.pt750.b40.lower",

  # "aug29_ptbins.TPFMS.s20.pt110.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt120.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt125.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt150.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt200.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt250.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt300.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt400.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt500.b40.lower",
  # "aug29_ptbins.TPFMS.s20.pt750.b40.lower",

  # "feb11.TuneP.s25.pt200.b40.lower",

  "oct08_ptbins.TuneP.s20.pt150.b40.lower",
  "oct08_ptbins.TuneP.s20.pt200.b40.lower"
]

etaphibins = {
    "1All"             :[ "|#eta|      < 0.9", "$|\eta| < 0.9$",],
    "3EtaPlus"         :[ "0    < #eta < 0.9", "$0    < \eta < 0.9$",],
    "2EtaMinus"        :[ "-0.9 < #eta < 0  ", "$-0.9 < \eta < 0$",],
    # # "PhiPlus"        :[ "|#eta| < 0.9 && #pi/3 < #phi < #pi",        "$|\eta| < 0.9, \pi/3 < \phi < \pi$",],
    # "7PhiZero"         :[ "|#eta| < 0.9 && -#pi/3 < #phi < #pi/3",     "$|\eta| < 0.9, -\pi/3 < \phi < \pi/3$",],
    # "4PhiMinus"        :[ "|#eta| < 0.9 && -#pi < #phi < -#pi/3",      "$|\eta| < 0.9, -\pi < \phi < -\pi/3$",],
    # "6EtaPlusPhiMinus" :[ "0 < #eta < 0.9 && -#pi < #phi < -#pi/3",    "$0 < \eta < 0.9, -\pi < \phi < -\pi/3$",],
    # "9EtaPlusPhiZero"  :[ "0 < #eta < 0.9 && -#pi/3 < #phi < #pi/3",   "$0 < \eta < 0.9, -\pi/3 < \phi < \pi/3$",],
    # #"EtaPlusPhiPlus"  :[ "0 < #eta < 0.9 && #pi/3 < #phi < #pi",      "$0 < \eta < 0.9, \pi/3 < \phi < \pi$",],
    # "5EtaMinusPhiMinus":[ "-0.9 < #eta < 0 && -#pi < #phi < -#pi/3",   "$-0.9 < \eta < 0, -\pi < \phi < -\pi/3$",],
    # "8EtaMinusPhiZero" :[ "-0.9 < #eta < 0 && -#pi/3 < #phi < #pi/3",  "$-0.9 < \eta < 0, -\pi/3 < \phi < \pi/3$",],
    # #"EtaMinusPhiPlus" :[ "-0.9 < #eta < 0 && #pi/3 < #phi < #pi"      "$-0.9 < \eta < 0, \pi/3 < \phi < \pi$"     ],
    }

etaphiexclusivebins = {
    "EtaPlusPhiMinus" :[2,1],
    "EtaPlusPhiZero"  :[2,2],
    "EtaPlusPhiPlus"  :[2,3],
    "EtaMinusPhiMinus":[1,1],
    "EtaMinusPhiZero" :[1,2],
    "EtaMinusPhiPlus" :[1,3],
    }

outdirbase = "~/public/html/Cosmics/2017/EndpointStudy/results"
texfilename = "%s/all_results_table.tex"%(outdirbase)

os.system("mkdir -p %s"%(outdirbase))
print os.path.expanduser(texfilename)
outtexf = open(os.path.expanduser(texfilename),'w')
# outtexf.write("""\\begin{tabular}{rcl|rl}
outtexf.write("""\\begin{tabular}{lcr|rl}
algo & $\mathrm{p}_{\mathrm{T}}$ bin & $\eta/\phi$ bin & $\delta\kappa_{b}$ min & unc \\\\
\\hline
""")

for filename in filenames:
  # infile = r.TFile("aug29.ptbins.endpoint/%s.root"%(filename),"read")
  infile = r.TFile("%s.root"%(filename),"read")
  print filename
  print infile

  summary = r.TCanvas("summary","",1440,900)
  summary.Divide(3,3)

  os.system("mkdir -p %s/%s"%(outdirbase,filename))
  outdir = "%s/%s"%(outdirbase,filename)
  texfilename = "%s/%s_results_table.tex"%(outdir,filename)
  print os.path.expanduser(texfilename)
  outtex = open(os.path.expanduser(texfilename),'w')
  outtex.write("""\\begin{tabular}{l|rl}
$\eta/\phi$ bin & $\delta\kappa_{b}$ min & unc \\\\
\\hline
""")
  resultsHist = r.TH2D("resultsHist", "#Delta#kappa_{b} map: #eta vs. #phi",
                       2, -0.9, 0.9,
                       3, -math.pi, math.pi)

  for i,etaphi in enumerate(sorted(etaphibins.keys())):
    outcan = r.TCanvas("outcan","",1440,900)
    # summary.cd(i+1)

    graphname    = "chi2_looseMuLower%s"%(etaphi[1:])
    # ksgraphname  = "ks_looseMuLower%s"%(etaphi[1:])
    prefitname   = "preFitPoly_looseMuLower%s"%(etaphi[1:])
    fitname      = "fitPoly_looseMuLower%s"%(etaphi[1:])
    legString = "lower-leg"
    gifLeg    = "Lower"
    if filename.find("upper") > 0:
      legString = "upper-leg"
      gifLeg    = "Upper"
      graphname    = "chi2_looseMuUpper%s"%(etaphi[1:])
      # ksgraphname  = "ks_looseMuUpper%s"%(etaphi[1:])
      prefitname   = "preFitPoly_looseMuUpper%s"%(etaphi[1:])
      fitname      = "fitPoly_looseMuUpper%s"%(etaphi[1:])
      pass
    graph   = infile.Get(graphname)
    # ksgraph = infile.Get(ksgraphname)
    prefit  = infile.Get(prefitname)
    fit     = infile.Get(fitname)

    print graphname
    print graph
    print # ksgraph
    print fit
    graph.SetTitle("#chi^{2} vs. #Delta#kappa_{b}: %s"%(etaphibins[etaphi][0]))
    graph.SetMarkerStyle(r.kFullCircle)
    graph.SetMarkerColor(r.kBlack)
    graph.SetMarkerSize(1.25)
    graph.SetLineColor(r.kBlack)
    graph.Draw("aep")

    # ksgraph.SetMarkerStyle(r.kFullCircle)
    # ksgraph.SetMarkerColor(r.kViolet)
    # ksgraph.SetMarkerSize(1.25)
    # ksgraph.SetLineColor(r.kViolet)
    # ksgraph.Draw("ep")
    graph.GetYaxis().SetTitle("#chi^{2}")
    graph.GetXaxis().SetTitle("#Delta#kappa_{b} [c/TeV]")
    prefit.SetLineStyle(5)
    prefit.SetLineColor(r.kBlue)
    prefit.Draw("same")
    fit.SetLineStyle(1)
    fit.SetLineColor(r.kRed)
    fit.Draw("same")
    r.gStyle.SetOptStat(112210)
    r.gPad.Update()

    # # r.gStyle.SetOptStat(112210)
    # r.gPad.Update()
    # st2 = r.gPad.GetPrimitive("stats")
    # print r.gPad.GetListOfPrimitives().Print()
    # print st2
    # st2.SetOptFit(1111)
    # # st2.SetOptStat(112210)
    # st2.SetX1NDC(0.65)
    # st2.SetX2NDC(0.9)
    # st2.SetY1NDC(0.6)
    # st2.SetY2NDC(0.9)
    r.gROOT.SetStyle("tdrStyle")
    r.gPad.Update()

    latex = r.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(r.kBlack)
    latex.SetTextFont(42)
    latex.SetTextAlign(12)
    latex.SetTextSize(0.025)
    algo = "TuneP"
    ptVal = 200
    if filename.find("pt110") > 0:
      ptVal = 110
    elif filename.find("pt120") > 0:
      ptVal = 120
    elif filename.find("pt125") > 0:
      ptVal = 125
    elif filename.find("pt150") > 0:
      ptVal = 150
    elif filename.find("pt250") > 0:
      ptVal = 250
    elif filename.find("pt300") > 0:
      ptVal = 300
    elif filename.find("pt400") > 0:
      ptVal = 400
    elif filename.find("pt500") > 0:
      ptVal = 500
    elif filename.find("pt750") > 0:
      ptVal = 750

    if filename.find("DYT") > 0:
      algo = "DY"
    elif filename.find("TPFMS") > 0:
      algo = "TPFMS"
    elif filename.find("Picky") > 0:
      algo = "Picky"
    elif filename.find("TrackerOnly") > 0:
      algo = "TrackerOnly"
    latex.DrawLatex(0.7,0.875,"%s %s p_{T} > %d"%(legString,algo,ptVal))
    latex.DrawLatex(0.7, 0.825,"%s"%(etaphibins[etaphi][0]))

    thelegend = r.TLegend(0.675,0.6,0.95,0.8, "", "NB,NDC")
    # r.gStyle.SetLegendBorderSize(0)
    thelegend.SetTextFont(42)
    thelegend.SetTextAlign(12)
    thelegend.SetTextSize(0.025)
    thelegend.SetFillColor(0)
    thelegend.SetFillStyle(3000)

    # thelegend.AddEntry(graph,"#chi^{2} values","lp")
    prefit.SetLineWidth(3)
    fit.SetLineWidth(3)
    thelegend.AddEntry(graph,   "#chi^{2} vs. #kappa_{b}", "lep")
    # thelegend.AddEntry(ksgraph, "KS test statistic vs. #kappa_{b}",       "lep")
    value   = prefit.GetMinimum(-0.5,0.5)
    minbias = prefit.GetMinimumX(-0.5,0.5)
    lowerr  = prefit.GetX(value+1.0, -0.8,   minbias)
    uperr   = prefit.GetX(value+1.0, minbias, 0.8)
    chisq   = prefit.GetChisquare()
    prob    = prefit.GetProb()
    thelegend.AddEntry(prefit,  "pre-fit (pol8, #chi^{2}:%2.4g, prob:%2.4g)"%(chisq,prob),"lp")
    thelegend.AddEntry(None,  "#kappa_{b} = %2.4g^{+%2.4g}_{-%2.4g}"%(minbias,uperr-minbias,
                                                                      minbias-lowerr),"")
    value   = fit.GetMinimum(-0.5,0.5)
    minbias = fit.GetMinimumX(-0.5,0.5)
    lowerr  = fit.GetX(value+1.0, -0.8,   minbias)
    uperr   = fit.GetX(value+1.0, minbias, 0.8)
    chisq   = fit.GetChisquare()
    prob    = fit.GetProb()
    thelegend.AddEntry(fit,     "post-fit (pol2, #chi^{2}:%2.4g, prob:%2.4g)"%(chisq,prob),"lp")
    thelegend.AddEntry(None,  "#kappa_{b} = %2.4g^{+%2.4g}_{-%2.4g}"%(minbias,uperr-minbias,
                                                                      minbias-lowerr),"")
    thelegend.Draw()

    # graph.GetYaxis().SetRangeUser(value*0.8,value+50)
    graph.GetYaxis().SetRangeUser(0,value+50)
    graph.GetXaxis().SetRangeUser(-1.0,1.0)
    r.gPad.SetGridx(r.kTRUE)
    r.gPad.SetGridy(r.kTRUE)
    r.gPad.Update()

    summary.cd(i+1)
    graph.Draw("aep")
    # # ksgraph.Draw("ep")
    graph.GetYaxis().SetTitle("#chi^{2}")
    graph.GetXaxis().SetTitle("#Delta#kappa_{b} [c/TeV]")
    prefit.SetLineStyle(1)
    prefit.SetLineColor(r.kBlue)
    prefit.Draw("same")
    fit.SetLineStyle(1)
    fit.SetLineColor(r.kRed)
    fit.Draw("same")
    r.gStyle.SetOptStat(112210)
    r.gPad.Update()
    # st2 = r.gPad.GetPrimitive("stats")
    # st2.SetOptFit(1111)
    # # st2.SetOptStat(112210)
    # st2.SetX1NDC(0.65)
    # st2.SetX2NDC(0.9)
    # st2.SetY1NDC(0.6)
    # st2.SetY2NDC(0.9)
    # r.gPad.Update()
    thelegend.Draw()
    # outtex.write("""%s & %2.4f & $^{+%2.4f}_{-%2.4f}$ \\\\
#"""%(etaphibins[etaphi][1],minbias,uperr-minbias,minbias-lowerr))
    outtex.write("""%s & %2.4f & $\\pm%2.4f$ \\\\
"""%(etaphibins[etaphi][1],minbias,uperr-minbias))
    outtexf.write("""%s & $\mathrm{p}_{\mathrm{T}} > %d $ & %s & %2.4f & $\\pm%2.4f$ \\\\
"""%(algo, ptVal, etaphibins[etaphi][1], minbias, uperr-minbias))

    if etaphi in etaphiexclusivebins.keys():
        resultsHist.SetBinContent(etaphiexclusivebins[etaphi][0],etaphiexclusivebins[etaphi][1],minbias)
        resultsHist.SetBinError(  etaphiexclusivebins[etaphi][0],etaphiexclusivebins[etaphi][1],uperr-minbias)
        pass

    r.gPad.Update()
    print value,minbias,lowerr,uperr
    # raw_input("press enter to continue")

    outcan.SaveAs("%s/%s_results_%s.png"%(outdir,filename,etaphi[1:]))
    outcan.SaveAs("%s/%s_results_%s.pdf"%(outdir,filename,etaphi[1:]))
    outcan.SaveAs("%s/%s_results_%s.eps"%(outdir,filename,etaphi[1:]))
    outcan.SaveAs("%s/%s_results_%s.C"%(  outdir,filename,etaphi[1:]))
    outcan.SaveAs("%s/%s_results_%s.png"%(outdir,filename,etaphi[1:]))
    pass

  summary.SaveAs("%s/%s_summary.png"%(outdir,filename))
  summary.SaveAs("%s/%s_summary.pdf"%(outdir,filename))
  summary.SaveAs("%s/%s_summary.eps"%(outdir,filename))
  summary.SaveAs("%s/%s_summary.C"%(  outdir,filename))
  summary.SaveAs("%s/%s_summary.png"%(outdir,filename))
  # raw_input("press enter to exit")
  outtex.write("""\\end{tabular}
""")
  outtex.close()

  outtexf.write("""\\hline
""")
  outcan.cd()
  resultsHist.Draw("colztexte")
  resultsHist.SetStats(r.kFALSE)
  resultsHist.GetXaxis().SetBinLabel(1,"-0.9 < #eta < 0")
  resultsHist.GetXaxis().SetBinLabel(2,"0 < #eta < 0.9")
  resultsHist.GetYaxis().SetBinLabel(1,"-#pi < #phi < -#pi/3")
  resultsHist.GetYaxis().SetBinLabel(2,"-#pi/3 < #phi < #pi/3")
  resultsHist.GetYaxis().SetBinLabel(3,"-#pi/3 < #phi < #pi")
  r.gPad.Update()
  outcan.SaveAs("%s/results_2d_map_%s.png"%(outdir,filename))
  outcan.SaveAs("%s/results_2d_map_%s.pdf"%(outdir,filename))
  outcan.SaveAs("%s/results_2d_map_%s.eps"%(outdir,filename))
  outcan.SaveAs("%s/results_2d_map_%s.C"%(  outdir,filename))
  outcan.SaveAs("%s/results_2d_map_%s.png"%(outdir,filename))
  # raw_input("press enter to exit")

  # copy some GIFs to the output location
  cmd = "rsync -aAXch --progress --partial --relative -L sampleGIFs/All/%s_%s_AllbiasBin*_b40_s20_pt200_normal*.png %s"%(algo,gifLeg,
                                                                                                                         outdir)
  os.system(cmd)
  pass

outtexf.write("""\\hline
\\end{tabular}
""")
outtexf.close()
pr.disable()
#s = StringIO.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print s.getvalue()
