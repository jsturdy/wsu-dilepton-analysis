#include "DataFormats/Math/interface/Vector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/LorentzVectorFwd.h"

#include <time.h>
#include <chrono>

#include "TLorentzVector.h"
#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TBrowser.h"
#include "TH2.h"
#include "TRandom.h"
#include "TRandom3.h"
#include "TTreeReader.h"
#include "TCanvas.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"
#include "TVector2.h"
#include "TVector3.h"
#include "TPad.h"
#include "TPaveStats.h"
#include "TString.h"
#include "TChain.h"
#include <memory>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <sstream>
#include <math.h>
#include <cmath>

#include <TStopwatch.h>

#include "WSUDiLeptons/CosmicEndpoint/test/binFunctions.h"

typedef std::chrono::high_resolution_clock Clock;
typedef std::chrono::milliseconds milliseconds;
typedef std::chrono::seconds seconds;

void Plot(std::string const& filelist, std::string const& outFile,
	  int trackVal_, double minPt_, double maxBias_, int nBiasBins_,
	  double factor_=1.0, double lowpT_=-1.0, double highpT_=-1.0,
	  bool symmetric_=false, bool applyTrigger_=false, bool mcFlag_=false,
	  bool debug_=false)

{
  Clock::time_point tstart = Clock::now();

  bool debug = debug_;

  if (debug) {
    std::cout<<"arg  1 (filelist) is:  "   << filelist   << std::endl;
    std::cout<<"arg  2 (outFile) is:  "    << outFile    << std::endl;
    std::cout<<"arg  3 (trackVal_) is:  "  << trackVal_  << std::endl;
    std::cout<<"arg  4 (minPt_) is:  "     << minPt_     << std::endl;
    std::cout<<"arg  5 (maxBias_) is:  "   << maxBias_   << std::endl;
    std::cout<<"arg  6 (nBiasBins_) is:  " << nBiasBins_ << std::endl;
    std::cout<<"arg  7 (factor_) is:  "    << factor_    << std::endl;
    std::cout<<"arg  8 (lowpT_) is:  "     << lowpT_     << std::endl;
    std::cout<<"arg  9 (highpT_) is:  "    << highpT_    << std::endl;
    std::cout<<"arg 10 (symmetric_) is:  " << symmetric_ << std::endl;
    std::cout<<"arg 11 (applyTrigger_) is:  " << applyTrigger_ << std::endl;
    std::cout<<"arg 12 (mcFlag_) is:  "       << mcFlag_       << std::endl;
    std::cout<<"arg 13 (debug_) is:  "        << debug_        << std::endl;
  }

  TFile *g;
  TChain *myChain;

  std::string trackAlgo;
  std::ofstream lumiFileOut100_loose;
  std::ofstream lumiFileOut200_loose;
  std::ofstream lumiFileOut400_loose;
  std::ofstream lumiFileOut100_tight;
  std::ofstream lumiFileOut200_tight;
  std::ofstream lumiFileOut400_tight;

  std::string outname;

  bool istrackerp = false;
  bool istunep    = false;

  if (trackVal_== 1) {
    myChain   = new TChain(TString("analysisTrackerMuons/MuonTree"));
    outname   = "TrackerOnly";
    trackAlgo = "trackerOnly";
    // if using TrackerOnly, should *not* apply muon system cuts
    istrackerp = true;
  }
  else if (trackVal_== 2) {
    myChain   = new TChain(TString("analysisTPFMSMuons/MuonTree"));
    outname   = "TPFMS";
    trackAlgo = "tpfms";
  }
  else if (trackVal_== 3) {
    myChain   = new TChain(TString("analysisDYTMuons/MuonTree"));
    outname   = "DYTT";
    trackAlgo = "dyt";
  }
  else if (trackVal_== 4) {
    myChain   = new TChain(TString("analysisPickyMuons/MuonTree"));
    outname   = "Picky";
    trackAlgo = "picky";
  }
  else if (trackVal_== 5) {
    myChain   = new TChain(TString("analysisTunePMuons/MuonTree"));
    outname   = "TuneP";
    trackAlgo = "tuneP";
    // if using TuneP and pT < 200, should *not* apply muon system cuts
    istrackerp = true;
    istunep    = true;
  }
  else {
    std::cout << "INVALID TRACK SPECIFIED! Choose a value between [1, 5]" << std::endl;
    return;
  }

  if (debug)
    std::cout << "chose the track object"  << std::endl;

  std::stringstream outrootfile, outlumifile;
  if (debug)
    std::cout << "checking for OUTPUTDIR " << std::endl;
  const char* envvar = std::getenv("OUTPUTDIR");
  if (envvar) {
    std::string outdir = std::string(envvar);
    outrootfile << outdir << "/" << outFile << outname;
    outlumifile << outdir << "/" << outFile << trackAlgo;
    std::cout << "OUTPUTDIR " << outdir << std::endl;
  }
  else {
    outrootfile << outFile << outname;
    outlumifile << outFile << trackAlgo;
  }

  std::cout << "Output files "
	    << outrootfile.str() << std::endl
	    << outlumifile.str() << std::endl;

  g = new TFile(TString(outrootfile.str()+".root"),"RECREATE");

  lumiFileOut100_loose.open(outlumifile.str()+"_pt100_loose.txt");
  lumiFileOut200_loose.open(outlumifile.str()+"_pt200_loose.txt");
  lumiFileOut400_loose.open(outlumifile.str()+"_pt400_loose.txt");

  lumiFileOut100_tight.open(outlumifile.str()+"_pt100_tight.txt");
  lumiFileOut200_tight.open(outlumifile.str()+"_pt200_tight.txt");
  lumiFileOut400_tight.open(outlumifile.str()+"_pt400_tight.txt");

  std::cout << "Processing tracks from " << trackAlgo << " algorithm" << std::endl;

  std::string name;
  std::stringstream inputfiles;

  if (debug)
    std::cout << "checking for AFSJOBDIR " << std::endl;
  const char* afsvar = std::getenv("AFSJOBDIR");
  if (afsvar) {
    std::string jobdir = std::string(afsvar);
    inputfiles << jobdir << "/" << filelist;
  }
  else {
    // what if AFSJOBDIR is not set, then just assume current working directory
    inputfiles << "./" << filelist;
  }

  std::ifstream file(inputfiles.str());
  std:: cout << "opening input file list "
	     << inputfiles.str() << std::hex << "  " << file << std::dec << std::endl;

  while (std::getline(file,name)) {
    std::stringstream newString;
    // newString << "root://xrootd.unl.edu//" << name;
    newString << "root://cmseos.fnal.gov//" << name;

    // Use the following line with line above commented out for running on local files.
    // newString << name;
    std::cout << newString.str() << std::endl;
    myChain->Add(TString(newString.str()));
  }
  std::cout << "Successfully opened inputfiles list!" << std::endl;
  // myChain->Add(TString());
  // newString << "root://xrootd.unl.edu//" << name;

  TTree *myTree = myChain;
  TTreeReader trackReader(myTree);

  float maxBias = maxBias_;
  int nBiasBins = nBiasBins_;

  std::string counterBinLabels[55] = {
    "00 - superpointing and barrel",             // 0
    "01 - #frac{#Deltap_{T}}{p_{T}} N-1 (loose)",// 1
    "02 - N_{Trk Hits} N-1 (loose)",             // 2
    "03 - N_{Pix Hits} N-1 (loose)",             // 3
    "04 - N_{Valid #mu Hits} N-1 (loose)",       // 4
    "05 - N_{Mt. Sta. Hits} N-1 (loose)",        // 5
    "06 - D_{xy} N-1 (loose)",                   // 6
    "07 - D_{z} N-1 (loose)",                    // 7
    "08 - p_{T} N-1 (loose)",                    // 8
    "09",
    "10",

    "11 - #frac{#Deltap_{T}}{p_{T}} N-1 (w/ D_{xy})",// 11
    "12 - N_{Trk Hits} N-1 (w/ D_{xy})",             // 12
    "13 - N_{Pix Hits} N-1 (w/ D_{xy})",             // 13
    "14 - N_{Valid #mu Hits} N-1 (w/ D_{xy})",       // 14
    "15 - N_{Mt. Sta. Hits} N-1 (w/ D_{xy})",        // 15
    "16 - D_{xy} N-1 (w/ D_{xy})",                   // 16
    "17 - D_{z} N-1 (w/ D_{xy})",                    // 17
    "18 - p_{T} N-1 (w/ D_{xy})",                    // 18
    "19",
    "20",

    "21 - #frac{#Deltap_{T}}{p_{T}} N-1 (w/ D_{z})",// 21
    "22 - N_{Trk Hits} N-1 (w/ D_{z})",             // 22
    "23 - N_{Pix Hits} N-1 (w/ D_{z})",             // 23
    "24 - N_{Valid #mu Hits} N-1 (w/ D_{z})",       // 24
    "25 - N_{Mt. Sta. Hits} N-1 (w/ D_{z})",        // 25
    "26 - D_{xy} N-1 (w/ D_{z})",                   // 26
    "27 - D_{z} N-1 (w/ D_{z})",                    // 27
    "28 - p_{T} N-1 (w/ D_{z})",                    // 28
    "29",
    "30",

    "31 - #frac{#Deltap_{T}}{p_{T}} N-1 (tight)",// 31
    "32 - N_{Trk Hits} N-1 (tight)",             // 32
    "33 - N_{Pix Hits} N-1 (tight)",             // 33
    "34 - N_{Valid #mu Hits} N-1 (tight)",       // 34
    "35 - N_{Mt. Sta. Hits} N-1 (tight)",        // 35
    "36 - D_{xy} N-1 (tight)",                   // 36
    "37 - D_{z} N-1 (tight)",                    // 37
    "38 - p_{T} N-1 (tight)",                    // 38
    "39",

    "40 - p_{T} > 50",   // 40
    "41 - p_{T} > 100",  // 41
    "42 - p_{T} > 150",  // 42
    "43 - p_{T} > 200",  // 43
    "44 - p_{T} > 300",  // 44
    "45 - p_{T} > 400",  // 45
    "46 - p_{T} > 500",  // 46
    "47 - p_{T} > 1000", // 47
    "48 - p_{T} > 1500", // 48
    "49 - p_{T} > 2000", // 49
    "50 - p_{T} > 3000", // 50
    "51",
    "52 - trueL1_SingleMuOpen", // 52
    "53 - fakeL1_SingleMuOpen", // 53
    "54 - Uncut",               // 54
  };

  // turn on Sumw2 by default
  TH1::SetDefaultSumw2();

  if (debug)
    std::cout << "setting up histograms" << std::endl;
  TH1I *h_countersUpper = new TH1I("upperCounters","upperCounters",55, -0.5, 54.5);
  TH1I *h_countersLower = new TH1I("lowerCounters","lowerCounters",55, -0.5, 54.5);

  for (int b = 0; b < 55; ++b) {
    h_countersUpper->GetXaxis()->SetBinLabel(b+1,TString(counterBinLabels[b]));
    h_countersLower->GetXaxis()->SetBinLabel(b+1,TString(counterBinLabels[b]));
  }

  // all histograms separated eta/phi
  TString etaBins[2]    = {"EtaMinus","EtaPlus"};
  TString phiBins[3]    = {"PhiMinus","PhiZero","PhiPlus"};

  // for histograms separated by charge
  TString chargeBins[2] = {"Minus","Plus"};

  // control the curvature histograms
  // bin width = MAX_CURVE_RANGE/N_CURVE_BINS

  // default asymmetric binning -16.0/TeV to 16.0/TeV = 32/TeV, 32/3200 = 0.01/TeV
  // suggested for KS is 0.01/TeV
  // suggested for chi2 is 0.25/TeV to be around expected resolution, means rebinning 25 0.01 bins into one
  // symmetric binning 0/TeV to 16.0/TeV = 16.0/TeV, 16.0/1600 = 0.01/TeV
  // suggested for KS is 0.01/TeV
  // suggested for chi2 is 0.25/TeV to be around expected resolution, means rebinning 25 0.01 bins into one
  // should *never* have a bin that straddles 0, 0 should *always* be a bin boundary

  const int    N_CURVE_BINS    = 640;
  const double MAX_CURVE_RANGE = 0.0160;

  // all histograms split into charge bins (plus/minus) and eta/phi bins
  // all can be combined at a later stage for any analysis
  // histograms for upper leg muons, inclusive in charge
  TH1D *h_upperPt[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperEta[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperPhi[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperChi2[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperNdof[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperCharge[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperCurve[2][2][2];  //[3]; changed since we never have positive phi muons

  TH1D *h_upperDxy[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperDz[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperDxyError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperDzError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperTrackPt[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperTrackEta[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperTrackPhi[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperPtError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperPtRelErr[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperPixelHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperTrackerHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperMuonStationHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperValidHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperValidMuonHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperMatchedMuonStations[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_upperTrackerLayersWithMeasurement[2][2][2];  //[3]; changed since we never have positive phi muons

  // histograms for lower leg muons, inclusive in charge
  TH1D *h_lowerPt[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerEta[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerPhi[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerChi2[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerNdof[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerCharge[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerCurve[2][2][2];  //[3]; changed since we never have positive phi muons

  TH1D *h_lowerDxy[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerDz[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerDxyError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerDzError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerTrackPt[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerTrackEta[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerTrackPhi[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerPtError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerPtRelErr[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerPixelHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerTrackerHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerMuonStationHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerValidHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerValidMuonHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerMatchedMuonStations[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_lowerTrackerLayersWithMeasurement[2][2][2];  //[3]; changed since we never have positive phi muons

  if (debug)
    std::cout << "booking no cut histograms" << std::endl;
  for (int etb = 0; etb < 2; ++etb) {
    // no need for the third phi bin, since there are no positive phi muons
    for (int phb = 0; phb < 2; ++phb) {
      TString etaphilabel(etaBins[etb]+phiBins[phb]);
      g->cd();
      TDirectory* etaphidir = (TDirectory*)g->mkdir(etaphilabel);
      etaphidir->cd();
      for (int chb = 0; chb < 2; ++chb) {
	// upper leg histograms
	h_upperPt[chb][etb][phb]     = new TH1D("upper"+chargeBins[chb]+"Pt"+etaphilabel,
						"upper"+chargeBins[chb]+"Pt"+etaphilabel,
						300,   0., 3000.);
	h_upperEta[chb][etb][phb]    = new TH1D("upper"+chargeBins[chb]+"Eta"+etaphilabel,
						"upper"+chargeBins[chb]+"Eta"+etaphilabel,
						40,  -2.,    2.);
	h_upperPhi[chb][etb][phb]    = new TH1D("upper"+chargeBins[chb]+"Phi"+etaphilabel,
						"upper"+chargeBins[chb]+"Phi"+etaphilabel,
						40,  -4.,    4.);
	h_upperChi2[chb][etb][phb]   = new TH1D("upper"+chargeBins[chb]+"Chi2"+etaphilabel,
						"upper"+chargeBins[chb]+"Chi2"+etaphilabel,
						50,   0.,  150.);
	h_upperNdof[chb][etb][phb]   = new TH1D("upper"+chargeBins[chb]+"Ndof"+etaphilabel,
						"upper"+chargeBins[chb]+"Ndof"+etaphilabel,
						100, -0.5,  99.5);
	h_upperCharge[chb][etb][phb] = new TH1D("upper"+chargeBins[chb]+"Charge"+etaphilabel,
						"upper"+chargeBins[chb]+"Charge"+etaphilabel,
						3, -1.5,   1.5);
	h_upperCurve[chb][etb][phb]  = new TH1D("upper"+chargeBins[chb]+"Curve"+etaphilabel,
						"upper"+chargeBins[chb]+"Curve"+etaphilabel,
						symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS,
                                                symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0.,
                                                MAX_CURVE_RANGE*factor_);

	h_upperDxy[chb][etb][phb]             = new TH1D("upper"+chargeBins[chb]+"Dxy"+etaphilabel,
							 "upper"+chargeBins[chb]+"Dxy"+etaphilabel,
							 100, -100., 100.);
	h_upperDz[chb][etb][phb]              = new TH1D("upper"+chargeBins[chb]+"Dz"+etaphilabel,
							 "upper"+chargeBins[chb]+"Dz"+etaphilabel,
							 100, -250., 250.);
	h_upperDxyError[chb][etb][phb]        = new TH1D("upper"+chargeBins[chb]+"DxyError"+etaphilabel,
							 "upper"+chargeBins[chb]+"DxyError"+etaphilabel,
							 50, 0., 150.);
	h_upperDzError[chb][etb][phb]         = new TH1D("upper"+chargeBins[chb]+"DzError"+etaphilabel,
							 "upper"+chargeBins[chb]+"DzError"+etaphilabel,
							 50, 0., 150.);
	h_upperTrackPt[chb][etb][phb]         = new TH1D("upper"+chargeBins[chb]+"TrackPt"+etaphilabel,
							 "upper"+chargeBins[chb]+"TrackPt"+etaphilabel,
							 300, 0., 3000.);
	h_upperTrackEta[chb][etb][phb]        = new TH1D("upper"+chargeBins[chb]+"TrackEta"+etaphilabel,
							 "upper"+chargeBins[chb]+"TrackEta"+etaphilabel,
							 40, -2., 2.);
	h_upperTrackPhi[chb][etb][phb]        = new TH1D("upper"+chargeBins[chb]+"TrackPhi"+etaphilabel,
							 "upper"+chargeBins[chb]+"TrackPhi"+etaphilabel,
							 40, -4., 4.);
	h_upperPtError[chb][etb][phb]         = new TH1D("upper"+chargeBins[chb]+"PtError"+etaphilabel,
							 "upper"+chargeBins[chb]+"PtError"+etaphilabel,
							 100, 0., 600.);
	h_upperPtRelErr[chb][etb][phb]        = new TH1D("upper"+chargeBins[chb]+"PtRelErr"+etaphilabel,
							 "upper"+chargeBins[chb]+"PtRelErr"+etaphilabel,
							 100, 0., 1.);

	h_upperPixelHits[chb][etb][phb]       = new TH1D("upper"+chargeBins[chb]+"PixelHits"+etaphilabel,
							 "upper"+chargeBins[chb]+"PixelHits"+etaphilabel,
							 10, -0.5, 9.5 );
	h_upperTrackerHits[chb][etb][phb]     = new TH1D("upper"+chargeBins[chb]+"TrackerHits"+etaphilabel,
							 "upper"+chargeBins[chb]+"TrackerHits"+etaphilabel,
							 35, -0.5, 34.5);
	h_upperMuonStationHits[chb][etb][phb] = new TH1D("upper"+chargeBins[chb]+"MuonStationHits"+etaphilabel,
							 "upper"+chargeBins[chb]+"MuonStationHits"+etaphilabel,
							 10, -0.5, 9.5 );
	h_upperValidHits[chb][etb][phb]       = new TH1D("upper"+chargeBins[chb]+"ValidHits"+etaphilabel,
							 "upper"+chargeBins[chb]+"ValidHits"+etaphilabel,
							 100,-0.5, 99.5);
	h_upperValidMuonHits[chb][etb][phb]   = new TH1D("upper"+chargeBins[chb]+"ValidMuonHits"+etaphilabel,
							 "upper"+chargeBins[chb]+"ValidMuonHits"+etaphilabel,
							 75, -0.5, 74.5);
	h_upperMatchedMuonStations[chb][etb][phb] = new TH1D("upper"+chargeBins[chb]+"MatchedMuonStations"+etaphilabel,
							     "upper"+chargeBins[chb]+"MatchedMuonStations"+etaphilabel,
							     10, -0.5, 9.5 );
	h_upperTrackerLayersWithMeasurement[chb][etb][phb] = new TH1D("upper"+chargeBins[chb]+"TrackerLayersWithMeasurement"+etaphilabel,
								      "upper"+chargeBins[chb]+"TrackerLayersWithMeasurement"+etaphilabel,
								      20, -0.5, 19.5);

 	// lower leg histograms
	h_lowerPt[chb][etb][phb]     = new TH1D("lower"+chargeBins[chb]+"Pt"+etaphilabel,
						"lower"+chargeBins[chb]+"Pt"+etaphilabel,
						300,   0., 3000.);
	h_lowerEta[chb][etb][phb]    = new TH1D("lower"+chargeBins[chb]+"Eta"+etaphilabel,
						"lower"+chargeBins[chb]+"Eta"+etaphilabel,
						40,  -2.,    2.);
	h_lowerPhi[chb][etb][phb]    = new TH1D("lower"+chargeBins[chb]+"Phi"+etaphilabel,
						"lower"+chargeBins[chb]+"Phi"+etaphilabel,
						40,  -4.,    4.);
	h_lowerChi2[chb][etb][phb]   = new TH1D("lower"+chargeBins[chb]+"Chi2"+etaphilabel,
						"lower"+chargeBins[chb]+"Chi2"+etaphilabel,
						50,   0.,  150.);
	h_lowerNdof[chb][etb][phb]   = new TH1D("lower"+chargeBins[chb]+"Ndof"+etaphilabel,
						"lower"+chargeBins[chb]+"Ndof"+etaphilabel,
						100, -0.5,  99.5);
	h_lowerCharge[chb][etb][phb] = new TH1D("lower"+chargeBins[chb]+"Charge"+etaphilabel,
						"lower"+chargeBins[chb]+"Charge"+etaphilabel,
						3, -1.5,   1.5);
	h_lowerCurve[chb][etb][phb]  = new TH1D("lower"+chargeBins[chb]+"Curve"+etaphilabel,
						"lower"+chargeBins[chb]+"Curve"+etaphilabel,
						symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS, symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0., MAX_CURVE_RANGE*factor_);

	h_lowerDxy[chb][etb][phb]             = new TH1D("lower"+chargeBins[chb]+"Dxy"+etaphilabel,
							 "lower"+chargeBins[chb]+"Dxy"+etaphilabel,
							 100, -100., 100.);
	h_lowerDz[chb][etb][phb]              = new TH1D("lower"+chargeBins[chb]+"Dz"+etaphilabel,
							 "lower"+chargeBins[chb]+"Dz"+etaphilabel,
							 100, -250., 250.);
	h_lowerDxyError[chb][etb][phb]        = new TH1D("lower"+chargeBins[chb]+"DxyError"+etaphilabel,
							 "lower"+chargeBins[chb]+"DxyError"+etaphilabel,
							 50, 0., 150.);
	h_lowerDzError[chb][etb][phb]         = new TH1D("lower"+chargeBins[chb]+"DzError"+etaphilabel,
							 "lower"+chargeBins[chb]+"DzError"+etaphilabel,
							 50, 0., 150.);
	h_lowerTrackPt[chb][etb][phb]         = new TH1D("lower"+chargeBins[chb]+"TrackPt"+etaphilabel,
							 "lower"+chargeBins[chb]+"TrackPt"+etaphilabel,
							 300, 0., 3000.);
	h_lowerTrackEta[chb][etb][phb]        = new TH1D("lower"+chargeBins[chb]+"TrackEta"+etaphilabel,
							 "lower"+chargeBins[chb]+"TrackEta"+etaphilabel,
							 40, -2., 2.);
	h_lowerTrackPhi[chb][etb][phb]        = new TH1D("lower"+chargeBins[chb]+"TrackPhi"+etaphilabel,
							 "lower"+chargeBins[chb]+"TrackPhi"+etaphilabel,
							 40, -4., 4.);
	h_lowerPtError[chb][etb][phb]         = new TH1D("lower"+chargeBins[chb]+"PtError"+etaphilabel,
							 "lower"+chargeBins[chb]+"PtError"+etaphilabel,
							 100, 0., 600.);
	h_lowerPtRelErr[chb][etb][phb]        = new TH1D("lower"+chargeBins[chb]+"PtRelErr"+etaphilabel,
							 "lower"+chargeBins[chb]+"PtRelErr"+etaphilabel,
							 100, 0., 1.);

	h_lowerPixelHits[chb][etb][phb]       = new TH1D("lower"+chargeBins[chb]+"PixelHits"+etaphilabel,
							 "lower"+chargeBins[chb]+"PixelHits"+etaphilabel,
							 10, -0.5, 9.5 );
	h_lowerTrackerHits[chb][etb][phb]     = new TH1D("lower"+chargeBins[chb]+"TrackerHits"+etaphilabel,
							 "lower"+chargeBins[chb]+"TrackerHits"+etaphilabel,
							 35, -0.5, 34.5);
	h_lowerMuonStationHits[chb][etb][phb] = new TH1D("lower"+chargeBins[chb]+"MuonStationHits"+etaphilabel,
							 "lower"+chargeBins[chb]+"MuonStationHits"+etaphilabel,
							 10, -0.5, 9.5 );
	h_lowerValidHits[chb][etb][phb]       = new TH1D("lower"+chargeBins[chb]+"ValidHits"+etaphilabel,
							 "lower"+chargeBins[chb]+"ValidHits"+etaphilabel,
							 100,-0.5, 99.5);
	h_lowerValidMuonHits[chb][etb][phb]   = new TH1D("lower"+chargeBins[chb]+"ValidMuonHits"+etaphilabel,
							 "lower"+chargeBins[chb]+"ValidMuonHits"+etaphilabel,
							 75, -0.5, 74.5);
	h_lowerMatchedMuonStations[chb][etb][phb] = new TH1D("lower"+chargeBins[chb]+"MatchedMuonStations"+etaphilabel,
							     "lower"+chargeBins[chb]+"MatchedMuonStations"+etaphilabel,
							     10, -0.5, 9.5 );
	h_lowerTrackerLayersWithMeasurement[chb][etb][phb] = new TH1D("lower"+chargeBins[chb]+"TrackerLayersWithMeasurement"+etaphilabel,
								      "lower"+chargeBins[chb]+"TrackerLayersWithMeasurement"+etaphilabel,
								      20, -0.5, 19.5);
      }

      if (debug)
	std::cout << "saving etaphidir" << std::endl;
      etaphidir->Write();
      g->cd();
      // g->Write();
    }  // end loop over phi bins
  }  // end loop over eta bins

  if (debug)
    std::cout << "setting up loose histograms" << std::endl;
  // all histograms split into charge bins (plus/minus) and eta/phi bins
  // all can be combined at a later stage for any analysis
  // histograms for loose cuts (not applying the Dxy/Dz cuts)
  TH1D *h_looseMuUpperPt[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperEta[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperPhi[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperChi2[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperNdof[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperCharge[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperCurve[2][2][2];  //[3]; changed since we never have positive phi muons

  if (debug)
    std::cout << "setting up loose histograms2" << std::endl;
  TH1D *h_looseMuUpperDxy[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperDz[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperDxyError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperDzError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperTrackPt[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperTrackEta[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperTrackPhi[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperPtError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperPtRelErr[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperPixelHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperTrackerHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperMuonStationHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperValidHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperValidMuonHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperMatchedMuonStations[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperTrackerLayersWithMeasurement[2][2][2];  //[3]; changed since we never have positive phi muons

  if (debug)
    std::cout << "setting up loose histograms2" << std::endl;
  TH1D *h_looseMuUpperCurvePlusBias[2][2][2][nBiasBins];  //[3][nBiasBins]; changed since we never have positive phi muons
  TH1D *h_looseMuUpperCurveMinusBias[2][2][2][nBiasBins];  //[3][nBiasBins]; changed since we never have positive phi muons

  if (debug)
    std::cout << "setting up loose histograms2" << std::endl;
  // histograms for lower leg muons, inclusive in charge
  TH1D *h_looseMuLowerPt[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerEta[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerPhi[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerChi2[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerNdof[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerCharge[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerCurve[2][2][2];  //[3]; changed since we never have positive phi muons

  if (debug)
    std::cout << "setting up loose histograms2" << std::endl;
  TH1D *h_looseMuLowerDxy[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerDz[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerDxyError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerDzError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerTrackPt[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerTrackEta[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerTrackPhi[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerPtError[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerPtRelErr[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerPixelHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerTrackerHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerMuonStationHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerValidHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerValidMuonHits[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerMatchedMuonStations[2][2][2];  //[3]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerTrackerLayersWithMeasurement[2][2][2];  //[3]; changed since we never have positive phi muons

  if (debug)
    std::cout << "setting up loose histograms2" << std::endl;
  TH1D *h_looseMuLowerCurvePlusBias[2][2][2][nBiasBins];  //[3][nBiasBins]; changed since we never have positive phi muons
  TH1D *h_looseMuLowerCurveMinusBias[2][2][2][nBiasBins];  //[3][nBiasBins]; changed since we never have positive phi muons

  if (debug)
    std::cout << "booking loose histograms" << std::endl;
  for (int etb = 0; etb < 2; ++etb) {
    // no need for the third phi bin, since there are no positive phi muons
    for (int phb = 0; phb < 2; ++phb) {
      TString etaphilabel(etaBins[etb]+phiBins[phb]);
      g->cd();
      TDirectory* etaphidir = (TDirectory*)g->GetDirectory(etaphilabel);
      if (!etaphidir)
	etaphidir = (TDirectory*)g->mkdir(etaphilabel);
      etaphidir->cd();
      for (int chb = 0; chb < 2; ++chb) {

	// upper leg histograms
	h_looseMuUpperPt[chb][etb][phb]     = new TH1D("looseMuUpper"+chargeBins[chb]+"Pt"+etaphilabel,
						       "looseMuUpper"+chargeBins[chb]+"Pt"+etaphilabel,
						       300,   0., 3000.);
	h_looseMuUpperEta[chb][etb][phb]    = new TH1D("looseMuUpper"+chargeBins[chb]+"Eta"+etaphilabel,
						       "looseMuUpper"+chargeBins[chb]+"Eta"+etaphilabel,
						       40,  -2.,    2.);
	h_looseMuUpperPhi[chb][etb][phb]    = new TH1D("looseMuUpper"+chargeBins[chb]+"Phi"+etaphilabel,
						       "looseMuUpper"+chargeBins[chb]+"Phi"+etaphilabel,
						       40,  -4.,    4.);
	h_looseMuUpperChi2[chb][etb][phb]   = new TH1D("looseMuUpper"+chargeBins[chb]+"Chi2"+etaphilabel,
						       "looseMuUpper"+chargeBins[chb]+"Chi2"+etaphilabel,
						       50,   0.,  150.);
	h_looseMuUpperNdof[chb][etb][phb]   = new TH1D("looseMuUpper"+chargeBins[chb]+"Ndof"+etaphilabel,
						       "looseMuUpper"+chargeBins[chb]+"Ndof"+etaphilabel,
						       100, -0.5,  99.5);
	h_looseMuUpperCharge[chb][etb][phb] = new TH1D("looseMuUpper"+chargeBins[chb]+"Charge"+etaphilabel,
						       "looseMuUpper"+chargeBins[chb]+"Charge"+etaphilabel,
						       3, -1.5,   1.5);
	h_looseMuUpperCurve[chb][etb][phb]  = new TH1D("looseMuUpper"+chargeBins[chb]+"Curve"+etaphilabel,
						       "looseMuUpper"+chargeBins[chb]+"Curve"+etaphilabel,
						       symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS,
                                                       symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0.,
                                                       MAX_CURVE_RANGE*factor_);

	h_looseMuUpperDxy[chb][etb][phb]             = new TH1D("looseMuUpper"+chargeBins[chb]+"Dxy"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"Dxy"+etaphilabel,
								100, -100., 100.);
	h_looseMuUpperDz[chb][etb][phb]              = new TH1D("looseMuUpper"+chargeBins[chb]+"Dz"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"Dz"+etaphilabel,
								100, -250., 250.);
	h_looseMuUpperDxyError[chb][etb][phb]        = new TH1D("looseMuUpper"+chargeBins[chb]+"DxyError"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"DxyError"+etaphilabel,
								50, 0., 150.);
	h_looseMuUpperDzError[chb][etb][phb]         = new TH1D("looseMuUpper"+chargeBins[chb]+"DzError"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"DzError"+etaphilabel,
								50, 0., 150.);
	h_looseMuUpperTrackPt[chb][etb][phb]         = new TH1D("looseMuUpper"+chargeBins[chb]+"TrackPt"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"TrackPt"+etaphilabel,
								300, 0., 3000.);
	h_looseMuUpperTrackEta[chb][etb][phb]        = new TH1D("looseMuUpper"+chargeBins[chb]+"TrackEta"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"TrackEta"+etaphilabel,
								40, -2., 2.);
	h_looseMuUpperTrackPhi[chb][etb][phb]        = new TH1D("looseMuUpper"+chargeBins[chb]+"TrackPhi"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"TrackPhi"+etaphilabel,
								40, -4., 4.);
	h_looseMuUpperPtError[chb][etb][phb]         = new TH1D("looseMuUpper"+chargeBins[chb]+"PtError"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"PtError"+etaphilabel,
								100, 0., 600.);
	h_looseMuUpperPtRelErr[chb][etb][phb]        = new TH1D("looseMuUpper"+chargeBins[chb]+"PtRelErr"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"PtRelErr"+etaphilabel,
								100, 0., 1.);

	h_looseMuUpperPixelHits[chb][etb][phb]       = new TH1D("looseMuUpper"+chargeBins[chb]+"PixelHits"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"PixelHits"+etaphilabel,
								10, -0.5, 9.5 );
	h_looseMuUpperTrackerHits[chb][etb][phb]     = new TH1D("looseMuUpper"+chargeBins[chb]+"TrackerHits"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"TrackerHits"+etaphilabel,
								35, -0.5, 34.5);
	h_looseMuUpperMuonStationHits[chb][etb][phb] = new TH1D("looseMuUpper"+chargeBins[chb]+"MuonStationHits"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"MuonStationHits"+etaphilabel,
								10, -0.5, 9.5 );
	h_looseMuUpperValidHits[chb][etb][phb]       = new TH1D("looseMuUpper"+chargeBins[chb]+"ValidHits"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"ValidHits"+etaphilabel,
								100,-0.5, 99.5);
	h_looseMuUpperValidMuonHits[chb][etb][phb]   = new TH1D("looseMuUpper"+chargeBins[chb]+"ValidMuonHits"+etaphilabel,
								"looseMuUpper"+chargeBins[chb]+"ValidMuonHits"+etaphilabel,
								75, -0.5, 74.5);
	h_looseMuUpperMatchedMuonStations[chb][etb][phb] = new TH1D("looseMuUpper"+chargeBins[chb]+"MatchedMuonStations"+etaphilabel,
								    "looseMuUpper"+chargeBins[chb]+"MatchedMuonStations"+etaphilabel,
								    10, -0.5, 9.5 );
	h_looseMuUpperTrackerLayersWithMeasurement[chb][etb][phb] = new TH1D("looseMuUpper"+chargeBins[chb]+"TrackerLayersWithMeasurement"+etaphilabel,
									     "looseMuUpper"+chargeBins[chb]+"TrackerLayersWithMeasurement"+etaphilabel,
									     20, -0.5, 19.5);

	// lower leg histograms
	h_looseMuLowerPt[chb][etb][phb]     = new TH1D("looseMuLower"+chargeBins[chb]+"Pt"+etaphilabel,
						       "looseMuLower"+chargeBins[chb]+"Pt"+etaphilabel,
						       300,   0., 3000.);
	h_looseMuLowerEta[chb][etb][phb]    = new TH1D("looseMuLower"+chargeBins[chb]+"Eta"+etaphilabel,
						       "looseMuLower"+chargeBins[chb]+"Eta"+etaphilabel,
						       40,  -2.,    2.);
	h_looseMuLowerPhi[chb][etb][phb]    = new TH1D("looseMuLower"+chargeBins[chb]+"Phi"+etaphilabel,
						       "looseMuLower"+chargeBins[chb]+"Phi"+etaphilabel,
						       40,  -4.,    4.);
	h_looseMuLowerChi2[chb][etb][phb]   = new TH1D("looseMuLower"+chargeBins[chb]+"Chi2"+etaphilabel,
						       "looseMuLower"+chargeBins[chb]+"Chi2"+etaphilabel,
						       50,   0.,  150.);
	h_looseMuLowerNdof[chb][etb][phb]   = new TH1D("looseMuLower"+chargeBins[chb]+"Ndof"+etaphilabel,
						       "looseMuLower"+chargeBins[chb]+"Ndof"+etaphilabel,
						       100, -0.5,  99.5);
	h_looseMuLowerCharge[chb][etb][phb] = new TH1D("looseMuLower"+chargeBins[chb]+"Charge"+etaphilabel,
						       "looseMuLower"+chargeBins[chb]+"Charge"+etaphilabel,
						       3, -1.5,   1.5);
	h_looseMuLowerCurve[chb][etb][phb]  = new TH1D("looseMuLower"+chargeBins[chb]+"Curve"+etaphilabel,
						       "looseMuLower"+chargeBins[chb]+"Curve"+etaphilabel,
						       symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS,
                                                       symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0.,
                                                       MAX_CURVE_RANGE*factor_);

	h_looseMuLowerDxy[chb][etb][phb]             = new TH1D("looseMuLower"+chargeBins[chb]+"Dxy"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"Dxy"+etaphilabel,
								100, -100., 100.);
	h_looseMuLowerDz[chb][etb][phb]              = new TH1D("looseMuLower"+chargeBins[chb]+"Dz"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"Dz"+etaphilabel,
								100, -250., 250.);
	h_looseMuLowerDxyError[chb][etb][phb]        = new TH1D("looseMuLower"+chargeBins[chb]+"DxyError"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"DxyError"+etaphilabel,
								50, 0., 150.);
	h_looseMuLowerDzError[chb][etb][phb]         = new TH1D("looseMuLower"+chargeBins[chb]+"DzError"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"DzError"+etaphilabel,
								50, 0., 150.);
	h_looseMuLowerTrackPt[chb][etb][phb]         = new TH1D("looseMuLower"+chargeBins[chb]+"TrackPt"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"TrackPt"+etaphilabel,
								300, 0., 3000.);
	h_looseMuLowerTrackEta[chb][etb][phb]        = new TH1D("looseMuLower"+chargeBins[chb]+"TrackEta"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"TrackEta"+etaphilabel,
								40, -2., 2.);
	h_looseMuLowerTrackPhi[chb][etb][phb]        = new TH1D("looseMuLower"+chargeBins[chb]+"TrackPhi"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"TrackPhi"+etaphilabel,
								40, -4., 4.);
	h_looseMuLowerPtError[chb][etb][phb]         = new TH1D("looseMuLower"+chargeBins[chb]+"PtError"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"PtError"+etaphilabel,
								100, 0., 600.);
	h_looseMuLowerPtRelErr[chb][etb][phb]        = new TH1D("looseMuLower"+chargeBins[chb]+"PtRelErr"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"PtRelErr"+etaphilabel,
								100, 0., 1.);

	h_looseMuLowerPixelHits[chb][etb][phb]       = new TH1D("looseMuLower"+chargeBins[chb]+"PixelHits"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"PixelHits"+etaphilabel,
								10, -0.5, 9.5 );
	h_looseMuLowerTrackerHits[chb][etb][phb]     = new TH1D("looseMuLower"+chargeBins[chb]+"TrackerHits"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"TrackerHits"+etaphilabel,
								35, -0.5, 34.5);
	h_looseMuLowerMuonStationHits[chb][etb][phb] = new TH1D("looseMuLower"+chargeBins[chb]+"MuonStationHits"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"MuonStationHits"+etaphilabel,
								10, -0.5, 9.5 );
	h_looseMuLowerValidHits[chb][etb][phb]       = new TH1D("looseMuLower"+chargeBins[chb]+"ValidHits"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"ValidHits"+etaphilabel,
								100,-0.5, 99.5);
	h_looseMuLowerValidMuonHits[chb][etb][phb]   = new TH1D("looseMuLower"+chargeBins[chb]+"ValidMuonHits"+etaphilabel,
								"looseMuLower"+chargeBins[chb]+"ValidMuonHits"+etaphilabel,
								75, -0.5, 74.5);
	h_looseMuLowerMatchedMuonStations[chb][etb][phb] = new TH1D("looseMuLower"+chargeBins[chb]+"MatchedMuonStations"+etaphilabel,
								    "looseMuLower"+chargeBins[chb]+"MatchedMuonStations"+etaphilabel,
								    10, -0.5, 9.5 );
	h_looseMuLowerTrackerLayersWithMeasurement[chb][etb][phb] = new TH1D("looseMuLower"+chargeBins[chb]+"TrackerLayersWithMeasurement"+etaphilabel,
									     "looseMuLower"+chargeBins[chb]+"TrackerLayersWithMeasurement"+etaphilabel,
									     20, -0.5, 19.5);

	if (debug)
	  std::cout << "booking bias histograms"
		    << "chb=" << chb
		    << "etb=" << etb
		    << "phb=" << phb
		    << std::endl;
	for (int i = 0; i < nBiasBins; ++i) {
	  std::stringstream name;
	  name << std::setw(3) << std::setfill('0') << i + 1;

	  std::stringstream title;
	  title << "#Delta#kappa = +" << (i+1)*(factor_*maxBias/nBiasBins);
	  h_looseMuUpperCurvePlusBias[chb][etb][phb][i] = new TH1D(TString("looseMuUpper"+chargeBins[chb]+"Curve"+etaphilabel+"PlusBias"+name.str()),
								   TString(title.str()),
								   symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS,
                                                                   symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0.,
                                                                   MAX_CURVE_RANGE*factor_);
	  h_looseMuLowerCurvePlusBias[chb][etb][phb][i] = new TH1D(TString("looseMuLower"+chargeBins[chb]+"Curve"+etaphilabel+"PlusBias"+name.str()),
								   TString(title.str()),
								   symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS,
                                                                   symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0.,
                                                                   MAX_CURVE_RANGE*factor_);

	  title.str("");
	  title.clear();
	  title << "#Delta#kappa = -" << (i+1)*(factor_*maxBias/nBiasBins);
	  h_looseMuUpperCurveMinusBias[chb][etb][phb][i] = new TH1D(TString("looseMuUpper"+chargeBins[chb]+"Curve"+etaphilabel+"MinusBias"+name.str()),
								    TString(title.str()),
								    symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS,
                                                                    symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0.,
                                                                    MAX_CURVE_RANGE*factor_);
	  h_looseMuLowerCurveMinusBias[chb][etb][phb][i] = new TH1D(TString("looseMuLower"+chargeBins[chb]+"Curve"+etaphilabel+"MinusBias"+name.str()),
								    TString(title.str()),
								    symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS,
                                                                    symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0.,
                                                                    MAX_CURVE_RANGE*factor_);
	}  // end loop over bias bins
      }  // end loop over charge bins

      if (debug)
	std::cout << "saving etaphidir" << std::endl;
      etaphidir->Write();
      g->cd();
      // g->Write();
    }  // end loop over phi bins
  }  // end loop over eta bins

  if (debug)
    std::cout << "Creating upper muMinus TTreeReaderValues" << std::endl;
  TTreeReaderValue<Int_t>    run(  trackReader, "muonRunNumber"  );
  TTreeReaderValue<Int_t>    lumi( trackReader, "muonLumiBlock"  );
  TTreeReaderValue<Int_t>    event(trackReader, "muonEventNumber");

  TTreeReaderValue<Int_t> trueL1SingleMu(trackReader, "l1SingleMu");
  TTreeReaderValue<Int_t> fakeL1SingleMu(trackReader, "fakeL1SingleMu");
  TTreeReaderValue<Int_t> nSimTracks( trackReader,    "nSimTracks");
  TTreeReaderArray<double> simTrackpT(trackReader,    "simTrackpT" );


  TTreeReaderValue<math::XYZTLorentzVector> upTrackerMuonP4(trackReader,"upperMuon_P4"      );
  TTreeReaderValue<math::XYZVector>         upTrackerTrack( trackReader,"upperMuon_trackVec");
  TTreeReaderValue<Double_t> upTrackerPt(      trackReader, "upperMuon_trackPt" );
  TTreeReaderValue<Int_t>    upTrackerCharge(  trackReader, "upperMuon_charge"  );
  TTreeReaderValue<Double_t> upTrackerChi2(    trackReader, "upperMuon_chi2"    );
  TTreeReaderValue<Int_t>    upTrackerNdof(    trackReader, "upperMuon_ndof"    );
  TTreeReaderValue<Double_t> upTrackerDxy(     trackReader, "upperMuon_dxy"     );
  TTreeReaderValue<Double_t> upTrackerDz(      trackReader, "upperMuon_dz"      );
  TTreeReaderValue<Double_t> upTrackerDxyError(trackReader, "upperMuon_dxyError");
  TTreeReaderValue<Double_t> upTrackerDzError( trackReader, "upperMuon_dzError" );
  TTreeReaderValue<Double_t> upTrackerPtError( trackReader, "upperMuon_ptError" );

  TTreeReaderValue<Int_t> upTrackerFirstPixel(           trackReader, "upperMuon_firstPixel"                  );
  TTreeReaderValue<Int_t> upTrackerPhits(                trackReader, "upperMuon_pixelHits"                   );
  TTreeReaderValue<Int_t> upTrackerThits(                trackReader, "upperMuon_trackerHits"                 );
  TTreeReaderValue<Int_t> upTrackerMhits(                trackReader, "upperMuon_muonStationHits"             );
  TTreeReaderValue<Int_t> upTrackerValidHits(            trackReader, "upperMuon_numberOfValidHits"           );
  TTreeReaderValue<Int_t> upTrackerValidMuonHits(        trackReader, "upperMuon_numberOfValidMuonHits"       );//Temporarily changed from ValidMuonHits to Valid Hits? why??
  TTreeReaderValue<Int_t> upTrackerMatchedMuonStations(  trackReader, "upperMuon_numberOfMatchedStations"     );
  TTreeReaderValue<Int_t> upTrackerLayersWithMeasurement(trackReader, "upperMuon_trackerLayersWithMeasurement");


  if (debug)
    std::cout << "Creating lower muMinus TTreeReaderValues" << std::endl;
  TTreeReaderValue<math::XYZTLorentzVector> lowTrackerMuonP4(trackReader,"lowerMuon_P4"      );
  TTreeReaderValue<math::XYZVector>         lowTrackerTrack( trackReader,"lowerMuon_trackVec");
  TTreeReaderValue<Double_t> lowTrackerPt(      trackReader, "lowerMuon_trackPt" );
  TTreeReaderValue<Int_t>    lowTrackerCharge(  trackReader, "lowerMuon_charge"  );
  TTreeReaderValue<Double_t> lowTrackerChi2(    trackReader, "lowerMuon_chi2"    );
  TTreeReaderValue<Int_t>    lowTrackerNdof(    trackReader, "lowerMuon_ndof"    );
  TTreeReaderValue<Double_t> lowTrackerDxy(     trackReader, "lowerMuon_dxy"     );
  TTreeReaderValue<Double_t> lowTrackerDz(      trackReader, "lowerMuon_dz"      );
  TTreeReaderValue<Double_t> lowTrackerDxyError(trackReader, "lowerMuon_dxyError");
  TTreeReaderValue<Double_t> lowTrackerDzError( trackReader, "lowerMuon_dzError" );
  TTreeReaderValue<Double_t> lowTrackerPtError( trackReader, "lowerMuon_ptError" );

  TTreeReaderValue<Int_t>    lowTrackerFirstPixel(           trackReader, "lowerMuon_firstPixel"                  );
  TTreeReaderValue<Int_t>    lowTrackerPhits(                trackReader, "lowerMuon_pixelHits"                   );
  TTreeReaderValue<Int_t>    lowTrackerThits(                trackReader, "lowerMuon_trackerHits"                 );
  TTreeReaderValue<Int_t>    lowTrackerMhits(                trackReader, "lowerMuon_muonStationHits"             );
  TTreeReaderValue<Int_t>    lowTrackerValidHits(            trackReader, "lowerMuon_numberOfValidHits"           );
  TTreeReaderValue<Int_t>    lowTrackerValidMuonHits(        trackReader, "lowerMuon_numberOfValidMuonHits"       );//Temporarily changed from ValidMuonHits to Valid Hits? why??
  TTreeReaderValue<Int_t>    lowTrackerMatchedMuonStations(  trackReader, "lowerMuon_numberOfMatchedStations"     );
  TTreeReaderValue<Int_t>    lowTrackerLayersWithMeasurement(trackReader, "lowerMuon_trackerLayersWithMeasurement");

  if (debug)
    std::cout << "Made it to Histogramming!" << std::endl;

  int j = 0;
  int k = 0;

  //double maxDR = 0.15; // what is reasonable here? Aachen did dPhi < 0.1, dTheta (eta?) < 0.05

  TStopwatch tsw;
  //int tenthpcount(1);
  int onepcount(1);
  int tenpcount(1);
  Long64_t nentries = myChain->GetEntries();

  Clock::time_point loopStart = Clock::now();

  while (trackReader.Next()) {
    //Timing information
    if ( k==0) {
      tsw.Start();
      std::cout << "." << std::flush;
    }

    if ((k*10)/nentries == tenpcount ) {
      tsw.Stop();
      Double_t time = tsw.RealTime();
      tsw.Start(kFALSE);
      Double_t finTime(0.);
      Double_t frac = (k*1.0)/(nentries*1.0);
      if (frac>0) finTime = time / frac - time;
      Double_t finMin = finTime / 60.;
      std::cout << std::setprecision(3) << std::fixed << tenpcount*10 << "% done.  "
		<< "t = " << std::setw(7) << time
		<< " projected finish =" << std::setw(7) << finTime << " s ("
		<< std::setprecision(1)
		<< finMin << " min).   "
		<< std::endl;
      tenpcount++;
    } else if ( (k*100)/nentries == onepcount ) {
      std::cout << ".";
      std::cout << std::flush;
      onepcount++;
    }

    if (debug && k < 1)
      std::cout << "Made it into the first loop" << std::endl;
    g->cd();

    // count events passing the trigger
    if (*trueL1SingleMu) {
      h_countersUpper->Fill(52);
      h_countersLower->Fill(52);
    }

    if (*fakeL1SingleMu) {
      h_countersUpper->Fill(53);
      h_countersLower->Fill(53);
    }

    // proper un-cut count
    h_countersUpper->Fill(54);
    h_countersLower->Fill(54);

    // apply the trigger, i.e., don't process if the trigger didn't fire
    if (applyTrigger_ && !(*fakeL1SingleMu)) {
      ++k;  // increment here to count processed events
      continue;
    }

    // make combination of samples easy
    if (mcFlag_) {
      if (*nSimTracks > 0) {
	if ((simTrackpT[0] >= highpT_) || (simTrackpT[0] < lowpT_)) {
	  ++k;  // increment here to count processed events
	  continue;
	}
      }
    }

    bool hasPt100Loose(false), hasPt200Loose(false), hasPt400Loose(false);
    bool hasPt100Tight(false), hasPt200Tight(false), hasPt400Tight(false);

    std::stringstream upperstring;
    std::stringstream lowerstring;

    // make sure we're not reading from the skipped events
    if (*upTrackerChi2 > -1) {
      // what about cases where the upper/lower muon have pT passing, but not the other leg
      // also, interest in (q/pT_up - q/pT_low)/(sqrt(2)*(q/pT_low)), relative residual
      // and possibly (q/pT_low - q/pT_up)/(sqrt(2)*(q/pT_up)), relative residual?
      // binned vs. pT (50,60,75,100,150,200,300,400,500,750,1000,1500,2000,3000,inf?
      // can't apply a tight min pT cut for these
      // should we apply a dR cut to ensure they are well matched, e.g., dR < 0.1, 0.3?

      //if (sqrt(upTrackerTrack->perp2()) > minPt_) {
      if (sqrt(upTrackerTrack->perp2()) > minPt_ || sqrt(lowTrackerTrack->perp2()) > minPt_) {
	/** ensure that the two muon tracks are indeed the same muon */
	// double deltaR = upTrackerMuonP4->DR(*lowTrackerMuonP4); // why doesn't this work?
	/*
	  double dEta = upTrackerMuonP4->eta()-lowTrackerMuonP4->eta();
	  double dPhi = upTrackerMuonP4->phi()-lowTrackerMuonP4->phi();
	  if (dPhi >= M_PI)
	  dPhi-=2*M_PI;
	  else if (dPhi < -M_PI)
	  dPhi+=2*M_PI;
	  double deltaR = sqrt((dEta*dEta) + (dPhi*dPhi));
	  if (deltaR > maxDR)
	  continue;
	*/
	double upperCpT = factor_*(*upTrackerCharge)/(sqrt(upTrackerTrack->perp2())); //(*upTrackerMuonP4).Pt();
	/*
	// make the curvature absolute value (asymmetric)
	if (!symmetric_)
	upperCpT = factor_/(sqrt(upTrackerTrack->perp2()));//upTrackerMuonP4->pt();
	*/
	double upperRelPtErr = *upTrackerPtError/(sqrt(upTrackerTrack->perp2()));//upTrackerMuonP4->pt();

	// make bool's for each cut level?
	// uint32_t upperCuts; // 1 bit per cut?

	bool up_etabar   = (fabs(upTrackerMuonP4->eta()) < 0.9) ? 1 : 0;
	bool up_tightdxy = (*upTrackerDxy < 0.2) ? 1 : 0;
	bool up_tightdz  = (*upTrackerDz  < 0.5) ? 1 : 0;
	bool up_etaBar   = (fabs(upTrackerMuonP4->eta()) < 0.9) ? 1 : 0;
	bool up_superpointing = (
                                 (std::fabs(*upTrackerDxy) < 10)
                                 && (std::fabs(*upTrackerDz) < 50)
                                 && (*upTrackerFirstPixel > 0)
                                 )
          ? 1 : 0;

	// if using TuneP or TrackerOnly and pT < 200, should *not* apply muon system cuts
	// bool upperMuStationHits = (!istrackerp || (istunep && sqrt(upTrackerTrack->perp2()) > 200)) ? *upTrackerMatchedMuonStations > 1 : 1;
	bool upperMuStationHits = *upTrackerMatchedMuonStations > 1;
	bool upperValidMuHits   = (!istrackerp || (istunep && sqrt(upTrackerTrack->perp2()) > 200)) ? *upTrackerValidMuonHits > 0 : 1;

	bool up_n1dxymax      = (upperValidMuHits        &&
				 upperMuStationHits      &&
				 (upperRelPtErr   < 0.3) &&
				 (*upTrackerPhits > 0  ) &&
				 (*upTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool up_n1dzmax       = (upperValidMuHits        &&
				 upperMuStationHits      &&
				 (upperRelPtErr   < 0.3) &&
				 (*upTrackerPhits > 0  ) &&
				 (*upTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool up_n1ptrelerr    = (upperValidMuHits      &&
				 upperMuStationHits    &&
				 (*upTrackerPhits > 0) &&
				 (*upTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool up_n1pt          = (upperValidMuHits        &&
				 upperMuStationHits      &&
				 (upperRelPtErr   < 0.3) &&
				 (*upTrackerPhits > 0  ) &&
				 (*upTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool up_n1trkhits     = (upperValidMuHits        &&
				 upperMuStationHits      &&
				 (upperRelPtErr   < 0.3) &&
				 (*upTrackerPhits > 0 ))
	  ? 1 : 0;
	bool up_n1pixhits     = (upperValidMuHits        &&
				 upperMuStationHits      &&
				 (upperRelPtErr   < 0.3) &&
				 (*upTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool up_n1vmuhits     = (upperMuStationHits      &&
				 (upperRelPtErr   < 0.3) &&
				 (*upTrackerPhits > 0  ) &&
				 (*upTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool up_n1mmustahits  = (upperValidMuHits        &&
				 (upperRelPtErr   < 0.3) &&
				 (*upTrackerPhits > 0  ) &&
				 (*upTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;

	int etabin    = getEtaBin(upTrackerTrack->eta());
	int phibin    = getPhiBin(upTrackerTrack->phi());
	int chargebin = getChargeBin(*upTrackerCharge);

	if (debug && (j % 100) == 0)
	  std::cout << "upper leg"    << std::endl
		    << "mu pt  = "    << std::setw(8) << std::setprecision(2) << std::fixed << upTrackerMuonP4->pt()
		    << " - eta = "    << std::setw(6) << std::setprecision(2) << std::fixed << upTrackerMuonP4->eta()
		    << " - phi = "    << std::setw(6) << std::setprecision(2) << std::fixed << upTrackerMuonP4->phi()
		    << std::endl

		    << "trk pt = "    << std::setw(8) << std::setprecision(2) << std::fixed << sqrt(upTrackerTrack->perp2())
		    << " - eta = "    << std::setw(6) << std::setprecision(2) << std::fixed << upTrackerTrack->eta()
		    << " - phi = "    << std::setw(6) << std::setprecision(2) << std::fixed << upTrackerTrack->phi()
		    << std::endl

		    << " - etabin = "    << etabin
		    << " - phibin = "    << phibin
		    << " - chargebin = " << chargebin
		    << std::endl;

	h_upperPt[chargebin][    etabin][phibin]->Fill(upTrackerMuonP4->pt());
	h_upperEta[chargebin][   etabin][phibin]->Fill(upTrackerMuonP4->eta());
	h_upperPhi[chargebin][   etabin][phibin]->Fill(upTrackerMuonP4->phi());
	h_upperCurve[chargebin][ etabin][phibin]->Fill(symmetric_?upperCpT:fabs(upperCpT));

	h_upperChi2[chargebin][  etabin][phibin]->Fill(*upTrackerChi2);
	h_upperNdof[chargebin][  etabin][phibin]->Fill(*upTrackerNdof);
	h_upperCharge[chargebin][etabin][phibin]->Fill(*upTrackerCharge);

	h_upperDxy[chargebin][etabin][phibin]->Fill(     *upTrackerDxy);
	h_upperDxyError[chargebin][etabin][phibin]->Fill(*upTrackerDxyError);
	h_upperDz[chargebin][etabin][phibin]->Fill(      *upTrackerDz);
	h_upperDzError[chargebin][etabin][phibin]->Fill( *upTrackerDzError);

	h_upperPtError[chargebin][etabin][phibin]->Fill( *upTrackerPtError);
	h_upperPtRelErr[chargebin][etabin][phibin]->Fill( upperRelPtErr);

	h_upperTrackPt[chargebin][etabin][phibin]->Fill(  sqrt(upTrackerTrack->perp2()));
	h_upperTrackEta[chargebin][etabin][phibin]->Fill( upTrackerTrack->eta());
	h_upperTrackPhi[chargebin][etabin][phibin]->Fill( upTrackerTrack->phi());

	h_upperPixelHits[chargebin][etabin][phibin]->Fill(                   *upTrackerPhits);
	h_upperTrackerHits[chargebin][etabin][phibin]->Fill(                 *upTrackerThits);
	h_upperValidHits[chargebin][etabin][phibin]->Fill(                   *upTrackerValidHits);
	h_upperValidMuonHits[chargebin][etabin][phibin]->Fill(               *upTrackerValidMuonHits);
	h_upperMuonStationHits[chargebin][etabin][phibin]->Fill(             *upTrackerMhits);
	h_upperMatchedMuonStations[chargebin][etabin][phibin]->Fill(         *upTrackerMatchedMuonStations);
	h_upperTrackerLayersWithMeasurement[chargebin][etabin][phibin]->Fill(*upTrackerLayersWithMeasurement);

	upperstring << "pt="      << sqrt(upTrackerTrack->perp2())
		    << ",eta="    << upTrackerTrack->eta()
		    << ",phi="    << upTrackerTrack->phi()
		    << ",charge=" << *upTrackerCharge;

	// fill the counters histogram for the upper leg muons passing the super-pointing selection, currently just fill
	if (up_superpointing && up_etabar) {
	  //if (up_superpointing || true) {

	  h_countersUpper->Fill(0);

	  if (up_n1ptrelerr)
	    h_countersUpper->Fill(1);
	  if (up_n1trkhits)
	    h_countersUpper->Fill(2);
	  if (up_n1pixhits)
	    h_countersUpper->Fill(3);
	  if (up_n1vmuhits)
	    h_countersUpper->Fill(4);
	  if (up_n1mmustahits)
	    h_countersUpper->Fill(5);
	  if (up_n1dxymax)
	    h_countersUpper->Fill(6);
	  if (up_n1dzmax)
	    h_countersUpper->Fill(7);
	  if (up_n1pt)
	    h_countersUpper->Fill(8);

	  if (up_tightdxy) {
	    if (up_n1ptrelerr)
	      h_countersUpper->Fill(11);
	    if (up_n1trkhits)
	      h_countersUpper->Fill(12);
	    if (up_n1pixhits)
	      h_countersUpper->Fill(13);
	    if (up_n1vmuhits)
	      h_countersUpper->Fill(14);
	    if (up_n1mmustahits)
	      h_countersUpper->Fill(15);
	    if (up_n1dxymax)
	      h_countersUpper->Fill(16);
	    if (up_n1dzmax)
	      h_countersUpper->Fill(17);
	    if (up_n1pt)
	      h_countersUpper->Fill(18);
	  }

	  if (up_tightdz) {
	    if (up_n1ptrelerr)
	      h_countersUpper->Fill(21);
	    if (up_n1trkhits)
	      h_countersUpper->Fill(22);
	    if (up_n1pixhits)
	      h_countersUpper->Fill(23);
	    if (up_n1vmuhits)
	      h_countersUpper->Fill(24);
	    if (up_n1mmustahits)
	      h_countersUpper->Fill(25);
	    if (up_n1dxymax)
	      h_countersUpper->Fill(26);
	    if (up_n1dzmax)
	      h_countersUpper->Fill(27);
	    if (up_n1pt)
	      h_countersUpper->Fill(28);
	  }

	  if (up_tightdxy && up_tightdz) {
	    if (up_n1ptrelerr)
	      h_countersUpper->Fill(31);
	    if (up_n1trkhits)
	      h_countersUpper->Fill(32);
	    if (up_n1pixhits)
	      h_countersUpper->Fill(33);
	    if (up_n1vmuhits)
	      h_countersUpper->Fill(34);
	    if (up_n1mmustahits)
	      h_countersUpper->Fill(35);
	    if (up_n1dxymax)
	      h_countersUpper->Fill(36);
	    if (up_n1dzmax)
	      h_countersUpper->Fill(37);
	    if (up_n1pt)
	      h_countersUpper->Fill(38);
	  }

	  if (up_n1pt) {
	    // counters of passing the loose selection binned by pT
	    if (sqrt(upTrackerTrack->perp2()) > 50)
	      h_countersUpper->Fill(40);
	    if (sqrt(upTrackerTrack->perp2()) > 100)
	      h_countersUpper->Fill(41);
	    if (sqrt(upTrackerTrack->perp2()) > 150)
	      h_countersUpper->Fill(42);
	    if (sqrt(upTrackerTrack->perp2()) > 200)
	      h_countersUpper->Fill(43);
	    if (sqrt(upTrackerTrack->perp2()) > 300)
	      h_countersUpper->Fill(44);
	    if (sqrt(upTrackerTrack->perp2()) > 400)
	      h_countersUpper->Fill(45);
	    if (sqrt(upTrackerTrack->perp2()) > 500)
	      h_countersUpper->Fill(46);
	    if (sqrt(upTrackerTrack->perp2()) > 1000)
	      h_countersUpper->Fill(47);
	    if (sqrt(upTrackerTrack->perp2()) > 1500)
	      h_countersUpper->Fill(48);
	    if (sqrt(upTrackerTrack->perp2()) > 2000)
	      h_countersUpper->Fill(49);
	    if (sqrt(upTrackerTrack->perp2()) > 3000)
	      h_countersUpper->Fill(50);
	  }

	  // if a variable doesn't appear in the High-pT muon selection, then apply all the cuts
	  if (up_n1pt) {
	    h_looseMuUpperPt[chargebin][etabin][phibin]->Fill( upTrackerMuonP4->pt());
	    h_looseMuUpperEta[chargebin][etabin][phibin]->Fill(upTrackerMuonP4->eta());
	    h_looseMuUpperPhi[chargebin][etabin][phibin]->Fill(upTrackerMuonP4->phi());
	    h_looseMuUpperCurve[chargebin][etabin][phibin]->Fill(  symmetric_?upperCpT:fabs(upperCpT));

	    h_looseMuUpperChi2[chargebin][etabin][phibin]->Fill(  *upTrackerChi2);
	    h_looseMuUpperNdof[chargebin][etabin][phibin]->Fill(  *upTrackerNdof);
	    h_looseMuUpperCharge[chargebin][etabin][phibin]->Fill(*upTrackerCharge);

	    h_looseMuUpperDxy[chargebin][etabin][phibin]->Fill(     *upTrackerDxy);
	    h_looseMuUpperDxyError[chargebin][etabin][phibin]->Fill(*upTrackerDxyError);
	    h_looseMuUpperDz[chargebin][etabin][phibin]->Fill(      *upTrackerDz);
	    h_looseMuUpperDzError[chargebin][etabin][phibin]->Fill( *upTrackerDzError);

	    h_looseMuUpperPtError[chargebin][etabin][phibin]->Fill( *upTrackerPtError);
	    h_looseMuUpperPtRelErr[chargebin][etabin][phibin]->Fill( upperRelPtErr);

	    h_looseMuUpperTrackPt[chargebin][etabin][phibin]->Fill(  sqrt(upTrackerTrack->perp2()));
	    h_looseMuUpperTrackEta[chargebin][etabin][phibin]->Fill( upTrackerTrack->eta());
	    h_looseMuUpperTrackPhi[chargebin][etabin][phibin]->Fill( upTrackerTrack->phi());

	    // should these be filled here?
	    /*
	      h_looseMuUpperPixelHits[chargebin][etabin][phibin]->Fill(                   *upTrackerPhits);
	      h_looseMuUpperTrackerHits[chargebin][etabin][phibin]->Fill(                 *upTrackerThits);
	      h_looseMuUpperValidHits[chargebin][etabin][phibin]->Fill(                   *upTrackerValidHits);
	      h_looseMuUpperValidMuonHits[chargebin][etabin][phibin]->Fill(               *upTrackerValidMuonHits);
	      h_looseMuUpperMuonStationHits[chargebin][etabin][phibin]->Fill(             *upTrackerMhits);
	      h_looseMuUpperMatchedMuonStations[chargebin][etabin][phibin]->Fill(         *upTrackerMatchedMuonStations);
	      h_looseMuUpperTrackerLayersWithMeasurement[chargebin][etabin][phibin]->Fill(*upTrackerLayersWithMeasurement);
	    */
	    for (int i = 0; i < nBiasBins; ++i) {
	      double posBias = upperCpT+(i+1)*(factor_*maxBias/nBiasBins);
	      double negBias = upperCpT-(i+1)*(factor_*maxBias/nBiasBins);

	      //h_looseMuUpperCurvePlusBias[chargebin][etabin][phibin][i]->Fill(posBias);
	      //h_looseMuUpperCurveMinusBias[chargebin][etabin][phibin][i]->Fill(negBias);

	      // properly account for cases where injecting the bias migrates the muon from
	      // positive to negative, and vice versa
	      h_looseMuUpperCurvePlusBias[getChargeBin(posBias)][etabin][phibin][i]->Fill(posBias);
	      h_looseMuUpperCurveMinusBias[getChargeBin(negBias)][etabin][phibin][i]->Fill(negBias);
	    }

	    if (sqrt(upTrackerTrack->perp2()) > 100) {
	      hasPt100Loose = true;
	      if (up_tightdxy && up_tightdz)
		hasPt100Tight = true;
	      if (sqrt(upTrackerTrack->perp2()) > 200) {
		hasPt200Loose = true;
		if (up_tightdxy && up_tightdz)
		  hasPt200Tight = true;
		if (sqrt(upTrackerTrack->perp2()) > 400) {
		  hasPt400Loose = true;
		  if (up_tightdxy && up_tightdz)
		    hasPt400Tight = true;
		}
	      }
	    }
	  } // end if (up_n1pt)

	  if (up_n1pixhits) {
	    h_looseMuUpperPixelHits[chargebin][etabin][phibin]->Fill(*upTrackerPhits);
	  }
	  if (up_n1vmuhits) {
	    h_looseMuUpperValidMuonHits[chargebin][etabin][phibin]->Fill(  *upTrackerValidMuonHits);
	    h_looseMuUpperMuonStationHits[chargebin][etabin][phibin]->Fill(*upTrackerMhits);
	  }
	  if (up_n1ptrelerr) {
	    h_looseMuUpperPtError[chargebin][etabin][phibin]->Fill(*upTrackerPtError);
	    h_looseMuUpperPtRelErr[chargebin][etabin][phibin]->Fill(upperRelPtErr);
	  }
	  if (up_n1trkhits) {
	    h_looseMuUpperTrackerHits[chargebin][etabin][phibin]->Fill(  *upTrackerThits);
	    h_looseMuUpperTrackerLayersWithMeasurement[chargebin][etabin][phibin]->Fill(*upTrackerLayersWithMeasurement);
	  }
	  if (up_n1mmustahits) {
	    h_looseMuUpperMatchedMuonStations[chargebin][etabin][phibin]->Fill(*upTrackerMatchedMuonStations);
	  }
	} // end check on up_superpointing

	  /* // commented out to include or of tracks
	     } // end if (sqrt(upTrackerTrack->perp2()) > minPt_)

	     //////// Lower muon leg ///////
	     if (sqrt(lowTrackerTrack->perp2()) > minPt_) {
	  */
	double lowerCpT = factor_*(*lowTrackerCharge)/(sqrt(lowTrackerTrack->perp2()));
	/*
	// make the curvature absolute value (asymmetric)
	if (!symmetric_)
	lowerCpT = factor_/(sqrt(lowTrackerTrack->perp2()));
	*/
	double lowerRelPtErr = *lowTrackerPtError/(sqrt(lowTrackerTrack->perp2()));

	// make bool's for each cut level?
	//uint32_t lowerCuts; // 1 bit per cut

	bool low_etabar   = (fabs(lowTrackerMuonP4->eta()) < 0.9) ? 1 : 0;
	bool low_tightdxy = (*lowTrackerDxy < 0.2) ? 1 : 0;
	bool low_tightdz  = (*lowTrackerDz  < 0.5) ? 1 : 0;
	bool low_etaBar   = (fabs(lowTrackerMuonP4->eta()) < 0.9) ? 1 : 0;
	bool low_superpointing = (
                                  (std::fabs(*lowTrackerDxy) < 10)
                                  && (std::fabs(*lowTrackerDz) < 50)
                                  && (*lowTrackerFirstPixel > 0)
                                  )
          ? 1 : 0;

	// if using TrackerOnly or TuneP and pT < 200, should *not* apply muon system cuts
	// bool lowerMuStationHits = (!istrackerp || (istunep && sqrt(lowTrackerTrack->perp2()) > 200)) ? *lowTrackerMatchedMuonStations > 1 : 1;
	bool lowerMuStationHits = *lowTrackerMatchedMuonStations > 1;
	bool lowerValidMuHits   = (!istrackerp || (istunep && sqrt(lowTrackerTrack->perp2()) > 200)) ? *lowTrackerValidMuonHits > 0 : 1;

	bool low_n1dxymax      = (lowerValidMuHits         &&
				  lowerMuStationHits       &&
				  (lowerRelPtErr   < 0.3)  &&
				  (*lowTrackerPhits > 0  ) &&
				  (*lowTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool low_n1dzmax       = (lowerValidMuHits         &&
				  lowerMuStationHits       &&
				  (lowerRelPtErr   < 0.3)  &&
				  (*lowTrackerPhits > 0  ) &&
				  (*lowTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool low_n1ptrelerr    = (lowerValidMuHits       &&
				  lowerMuStationHits     &&
				  (*lowTrackerPhits > 0) &&
				  (*lowTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool low_n1pt          = (lowerValidMuHits         &&
				  lowerMuStationHits       &&
				  (lowerRelPtErr   < 0.3)  &&
				  (*lowTrackerPhits > 0  ) &&
				  (*lowTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool low_n1trkhits     = (lowerValidMuHits        &&
				  lowerMuStationHits      &&
				  (lowerRelPtErr   < 0.3) &&
				  (*lowTrackerPhits > 0 ))
	  ? 1 : 0;
	bool low_n1pixhits     = (lowerValidMuHits        &&
				  lowerMuStationHits       &&
				  (lowerRelPtErr   < 0.3) &&
				  (*lowTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool low_n1vmuhits     = (lowerMuStationHits       &&
				  (lowerRelPtErr   < 0.3)  &&
				  (*lowTrackerPhits > 0  ) &&
				  (*lowTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;
	bool low_n1mmustahits  = (lowerValidMuHits         &&
				  (lowerRelPtErr   < 0.3)  &&
				  (*lowTrackerPhits > 0  ) &&
				  (*lowTrackerLayersWithMeasurement > 5))
	  ? 1 : 0;

	etabin    = getEtaBin(lowTrackerTrack->eta());
	phibin    = getPhiBin(lowTrackerTrack->phi());
	chargebin = getChargeBin(*lowTrackerCharge);

	if (debug && (j % 100) == 0)
	  std::cout << "lower leg"    << std::endl
		    << "mu pt  = "    << std::setw(8) << std::setprecision(2) << std::fixed << lowTrackerMuonP4->pt()
		    << " - eta = "    << std::setw(6) << std::setprecision(2) << std::fixed << lowTrackerMuonP4->eta()
		    << " - phi = "    << std::setw(6) << std::setprecision(2) << std::fixed << lowTrackerMuonP4->phi()
		    << std::endl

		    << "trk pt = "    << std::setw(8) << std::setprecision(2) << std::fixed << sqrt(lowTrackerTrack->perp2())
		    << " - eta = "    << std::setw(6) << std::setprecision(2) << std::fixed << lowTrackerTrack->eta()
		    << " - phi = "    << std::setw(6) << std::setprecision(2) << std::fixed << lowTrackerTrack->phi()
		    << std::endl

		    << " - etabin = "    << etabin
		    << " - phibin = "    << phibin
		    << " - chargebin = " << chargebin
		    << std::endl;

	h_lowerPt[chargebin][    etabin][phibin]->Fill(lowTrackerMuonP4->pt());
	h_lowerEta[chargebin][   etabin][phibin]->Fill(lowTrackerMuonP4->eta());
	h_lowerPhi[chargebin][   etabin][phibin]->Fill(lowTrackerMuonP4->phi());
	h_lowerCurve[chargebin][ etabin][phibin]->Fill(symmetric_?lowerCpT:fabs(lowerCpT));

	h_lowerChi2[chargebin][  etabin][phibin]->Fill(*lowTrackerChi2);
	h_lowerNdof[chargebin][  etabin][phibin]->Fill(*lowTrackerNdof);
	h_lowerCharge[chargebin][etabin][phibin]->Fill(*lowTrackerCharge);

	h_lowerDxy[chargebin][etabin][phibin]->Fill(     *lowTrackerDxy);
	h_lowerDxyError[chargebin][etabin][phibin]->Fill(*lowTrackerDxyError);
	h_lowerDz[chargebin][etabin][phibin]->Fill(      *lowTrackerDz);
	h_lowerDzError[chargebin][etabin][phibin]->Fill( *lowTrackerDzError);

	h_lowerPtError[chargebin][etabin][phibin]->Fill( *lowTrackerPtError);
	h_lowerPtRelErr[chargebin][etabin][phibin]->Fill( lowerRelPtErr);

	h_lowerTrackPt[chargebin][etabin][phibin]->Fill(  sqrt(lowTrackerTrack->perp2()));
	h_lowerTrackEta[chargebin][etabin][phibin]->Fill( lowTrackerTrack->eta());
	h_lowerTrackPhi[chargebin][etabin][phibin]->Fill( lowTrackerTrack->phi());

	h_lowerPixelHits[chargebin][etabin][phibin]->Fill(                   *lowTrackerPhits);
	h_lowerTrackerHits[chargebin][etabin][phibin]->Fill(                 *lowTrackerThits);
	h_lowerValidHits[chargebin][etabin][phibin]->Fill(                   *lowTrackerValidHits);
	h_lowerValidMuonHits[chargebin][etabin][phibin]->Fill(               *lowTrackerValidMuonHits);
	h_lowerMuonStationHits[chargebin][etabin][phibin]->Fill(             *lowTrackerMhits);
	h_lowerMatchedMuonStations[chargebin][etabin][phibin]->Fill(         *lowTrackerMatchedMuonStations);
	h_lowerTrackerLayersWithMeasurement[chargebin][etabin][phibin]->Fill(*upTrackerLayersWithMeasurement);

	lowerstring << "pt="      << sqrt(lowTrackerTrack->perp2())
		    << ",eta="    << lowTrackerTrack->eta()
		    << ",phi="    << lowTrackerTrack->phi()
		    << ",charge=" << *lowTrackerCharge;

	// fill the counters histogram for the lower leg muons passing the super-pointing selection
	if (low_superpointing && low_etabar) {
	  //if (low_superpointing || true) {

	  h_countersLower->Fill(0);

	  if (low_n1ptrelerr)
	    h_countersLower->Fill(1);
	  if (low_n1trkhits)
	    h_countersLower->Fill(2);
	  if (low_n1pixhits)
	    h_countersLower->Fill(3);
	  if (low_n1vmuhits)
	    h_countersLower->Fill(4);
	  if (low_n1mmustahits)
	    h_countersLower->Fill(5);
	  if (low_n1dxymax)
	    h_countersLower->Fill(6);
	  if (low_n1dzmax)
	    h_countersLower->Fill(7);
	  if (low_n1pt)
	    h_countersLower->Fill(8);

	  if (low_tightdxy) {
	    if (low_n1ptrelerr)
	      h_countersLower->Fill(11);
	    if (low_n1trkhits)
	      h_countersLower->Fill(12);
	    if (low_n1pixhits)
	      h_countersLower->Fill(13);
	    if (low_n1vmuhits)
	      h_countersLower->Fill(14);
	    if (low_n1mmustahits)
	      h_countersLower->Fill(15);
	    if (low_n1dxymax)
	      h_countersLower->Fill(16);
	    if (low_n1dzmax)
	      h_countersLower->Fill(17);
	    if (low_n1pt)
	      h_countersLower->Fill(18);
	  }

	  if (low_tightdz) {
	    if (low_n1ptrelerr)
	      h_countersLower->Fill(21);
	    if (low_n1trkhits)
	      h_countersLower->Fill(22);
	    if (low_n1pixhits)
	      h_countersLower->Fill(23);
	    if (low_n1vmuhits)
	      h_countersLower->Fill(24);
	    if (low_n1mmustahits)
	      h_countersLower->Fill(25);
	    if (low_n1dxymax)
	      h_countersLower->Fill(26);
	    if (low_n1dzmax)
	      h_countersLower->Fill(27);
	    if (low_n1pt)
	      h_countersLower->Fill(28);
	  }

	  if (low_tightdxy && low_tightdz) {
	    if (low_n1ptrelerr)
	      h_countersLower->Fill(31);
	    if (low_n1trkhits)
	      h_countersLower->Fill(32);
	    if (low_n1pixhits)
	      h_countersLower->Fill(33);
	    if (low_n1vmuhits)
	      h_countersLower->Fill(34);
	    if (low_n1mmustahits)
	      h_countersLower->Fill(35);
	    if (low_n1dxymax)
	      h_countersLower->Fill(36);
	    if (low_n1dzmax)
	      h_countersLower->Fill(37);
	    if (low_n1pt)
	      h_countersLower->Fill(38);
	  }

	  if (low_n1pt) {
	    // counters of passing the loose selection binned by pT
	    if (sqrt(lowTrackerTrack->perp2()) > 50)
	      h_countersLower->Fill(40);
	    if (sqrt(lowTrackerTrack->perp2()) > 100)
	      h_countersLower->Fill(41);
	    if (sqrt(lowTrackerTrack->perp2()) > 150)
	      h_countersLower->Fill(42);
	    if (sqrt(lowTrackerTrack->perp2()) > 200)
	      h_countersLower->Fill(43);
	    if (sqrt(lowTrackerTrack->perp2()) > 300)
	      h_countersLower->Fill(44);
	    if (sqrt(lowTrackerTrack->perp2()) > 400)
	      h_countersLower->Fill(45);
	    if (sqrt(lowTrackerTrack->perp2()) > 500)
	      h_countersLower->Fill(46);
	    if (sqrt(lowTrackerTrack->perp2()) > 1000)
	      h_countersLower->Fill(47);
	    if (sqrt(lowTrackerTrack->perp2()) > 1500)
	      h_countersLower->Fill(48);
	    if (sqrt(lowTrackerTrack->perp2()) > 2000)
	      h_countersLower->Fill(49);
	    if (sqrt(lowTrackerTrack->perp2()) > 3000)
	      h_countersLower->Fill(50);
	  }

	  // if a variable doesn't appear in the High-pT muon selection, then apply all the cuts
	  if (low_n1pt) {
	    h_looseMuLowerPt[chargebin][etabin][phibin]->Fill( lowTrackerMuonP4->pt());
	    h_looseMuLowerEta[chargebin][etabin][phibin]->Fill(lowTrackerMuonP4->eta());
	    h_looseMuLowerPhi[chargebin][etabin][phibin]->Fill(lowTrackerMuonP4->phi());
	    h_looseMuLowerCurve[chargebin][etabin][phibin]->Fill(  symmetric_?lowerCpT:fabs(lowerCpT));

	    h_looseMuLowerChi2[chargebin][etabin][phibin]->Fill(  *lowTrackerChi2);
	    h_looseMuLowerNdof[chargebin][etabin][phibin]->Fill(  *lowTrackerNdof);
	    h_looseMuLowerCharge[chargebin][etabin][phibin]->Fill(*lowTrackerCharge);

	    h_looseMuLowerDxy[chargebin][etabin][phibin]->Fill(     *lowTrackerDxy);
	    h_looseMuLowerDxyError[chargebin][etabin][phibin]->Fill(*lowTrackerDxyError);
	    h_looseMuLowerDz[chargebin][etabin][phibin]->Fill(      *lowTrackerDz);
	    h_looseMuLowerDzError[chargebin][etabin][phibin]->Fill( *lowTrackerDzError);

	    h_looseMuLowerPtError[chargebin][etabin][phibin]->Fill( *lowTrackerPtError);
	    h_looseMuLowerPtRelErr[chargebin][etabin][phibin]->Fill( lowerRelPtErr);

	    h_looseMuLowerTrackPt[chargebin][etabin][phibin]->Fill(  sqrt(lowTrackerTrack->perp2()));
	    h_looseMuLowerTrackEta[chargebin][etabin][phibin]->Fill( lowTrackerTrack->eta());
	    h_looseMuLowerTrackPhi[chargebin][etabin][phibin]->Fill( lowTrackerTrack->phi());

	    // should these be filled here?
	    /*
	      h_looseMuLowerPixelHits[chargebin][etabin][phibin]->Fill(                   *lowTrackerPhits);
	      h_looseMuLowerTrackerHits[chargebin][etabin][phibin]->Fill(                 *lowTrackerThits);
	      h_looseMuLowerValidHits[chargebin][etabin][phibin]->Fill(                   *lowTrackerValidHits);
	      h_looseMuLowerValidMuonHits[chargebin][etabin][phibin]->Fill(               *lowTrackerValidMuonHits);
	      h_looseMuLowerMuonStationHits[chargebin][etabin][phibin]->Fill(             *lowTrackerMhits);
	      h_looseMuLowerMatchedMuonStations[chargebin][etabin][phibin]->Fill(         *lowTrackerMatchedMuonStations);
	      h_looseMuLowerTrackerLayersWithMeasurement[chargebin][etabin][phibin]->Fill(*lowTrackerLayersWithMeasurement);
	    */
	    for (int i = 0; i < nBiasBins; ++i) {
	      double posBias = lowerCpT+(i+1)*(factor_*maxBias/nBiasBins);
	      double negBias = lowerCpT-(i+1)*(factor_*maxBias/nBiasBins);

	      //h_looseMuLowerCurvePlusBias[chargebin][etabin][phibin][i]->Fill(posBias);
	      //h_looseMuLowerCurveMinusBias[chargebin][etabin][phibin][i]->Fill(negBias);

	      // properly account for cases where injecting the bias migrates the muon from
	      // positive to negative, and vice versa
	      h_looseMuLowerCurvePlusBias[getChargeBin(posBias)][etabin][phibin][i]->Fill(posBias);
	      h_looseMuLowerCurveMinusBias[getChargeBin(negBias)][etabin][phibin][i]->Fill(negBias);
	    }

	    if (sqrt(lowTrackerTrack->perp2()) > 100) {
	      hasPt100Loose = true;
	      if (low_tightdxy && low_tightdz)
		hasPt100Tight = true;
	      if (sqrt(lowTrackerTrack->perp2()) > 200) {
		hasPt200Loose = true;
		if (low_tightdxy && low_tightdz)
		  hasPt200Tight = true;
		if (sqrt(lowTrackerTrack->perp2()) > 400) {
		  hasPt400Loose = true;
		  if (low_tightdxy && low_tightdz)
		    hasPt400Tight = true;
		}
	      }
	    }
	  } // end if (low_n1pt)

	  if (low_n1pixhits) {
	    h_looseMuLowerPixelHits[chargebin][etabin][phibin]->Fill(*lowTrackerPhits);
	  }
	  if (low_n1vmuhits) {
	    h_looseMuLowerValidMuonHits[chargebin][etabin][phibin]->Fill(  *lowTrackerValidMuonHits);
	    h_looseMuLowerMuonStationHits[chargebin][etabin][phibin]->Fill(*lowTrackerMhits);
	  }
	  if (low_n1ptrelerr) {
	    h_looseMuLowerPtError[chargebin][etabin][phibin]->Fill(*lowTrackerPtError);
	    h_looseMuLowerPtRelErr[chargebin][etabin][phibin]->Fill(lowerRelPtErr);
	  }
	  if (low_n1trkhits) {
	    h_looseMuLowerTrackerHits[chargebin][etabin][phibin]->Fill(*lowTrackerThits);
	    h_looseMuLowerTrackerLayersWithMeasurement[chargebin][etabin][phibin]->Fill(*lowTrackerLayersWithMeasurement);
	  }
	  if (low_n1mmustahits) {
	    h_looseMuLowerMatchedMuonStations[chargebin][etabin][phibin]->Fill(*lowTrackerMatchedMuonStations);
	  }
	} // end check on low_superpointing
	  //} // end if (sqrt(lowTrackerTrack->perp2()) > minPt_)
      } // end if (sqrt(upTrackerTrack->perp2()) > minPt_ || sqrt(lowTrackerTrack->perp2()) > minPt_)

      if (hasPt100Loose)
	lumiFileOut100_loose
	  << "\"" << *run << "\":"
	  << " [[" << *lumi << "," << *lumi << "]]"
	  << " : " << *event
	  << " (upper leg) " << upperstring.str()
	  << " (lower leg) " << lowerstring.str()
	  << std::endl;

      if (hasPt100Tight)
	lumiFileOut100_tight
	  << "\""  << *run  << "\":"
	  << " [[" << *lumi << "," << *lumi << "]]"
	  << " : " << *event
	  << " (upper leg) " << upperstring.str()
	  << " (lower leg) " << lowerstring.str()
	  << std::endl;

      if (hasPt200Loose)
	lumiFileOut200_loose
	  << "\"" << *run << "\":"
	  << " [[" << *lumi << "," << *lumi << "]]"
	  << " : " << *event
	  << " (upper leg) " << upperstring.str()
	  << " (lower leg) " << lowerstring.str()
	  << std::endl;

      if (hasPt200Tight)
	lumiFileOut200_tight
	  << "\""  << *run  << "\":"
	  << " [[" << *lumi << "," << *lumi << "]]"
	  << " : " << *event
	  << " (upper leg) " << upperstring.str()
	  << " (lower leg) " << lowerstring.str()
	  << std::endl;

      if (hasPt400Loose)
	lumiFileOut400_loose
	  << "\"" << *run << "\":"
	  << " [[" << *lumi << "," << *lumi << "]]"
	  << " : " << *event
	  << " (upper leg) " << upperstring.str()
	  << " (lower leg) " << lowerstring.str()
	  << std::endl;

      if (hasPt400Tight)
	lumiFileOut400_tight
	  << "\""  << *run  << "\":"
	  << " [[" << *lumi << "," << *lumi << "]]"
	  << " : " << *event
	  << " (upper leg) " << upperstring.str()
	  << " (lower leg) " << lowerstring.str()
	  << std::endl;

      ++j;
      if (debug && j < 1)
	std::cout << "Made it through " << j << " sets of fills" << std::endl;
    } // closing if (*upTrackerChi2 > -1)
    ++k;
    if (debug && k > 1000)
      break;
  } // end while loop

  Clock::time_point loopFinish = Clock::now();

  std::cout << "100% done, "
	    << "looping over TTree took: "
	    << (std::chrono::duration_cast<seconds>(loopFinish - loopStart)).count()
	    << "s" << std::endl;

  lumiFileOut100_loose.close();
  lumiFileOut200_loose.close();
  lumiFileOut400_loose.close();

  lumiFileOut100_tight.close();
  lumiFileOut200_tight.close();
  lumiFileOut400_tight.close();

  if (debug)
    std::cout << std::hex << g << std::dec << std::endl;

  Clock::time_point t0 = Clock::now();

  g->Write();
  Clock::time_point t1 = Clock::now();

  std::cout << "writing file took: "
	    << (std::chrono::duration_cast<seconds>(t1 - t0)).count()
	    << "s" << std::endl;
  g->Close();

  Clock::time_point t2 = Clock::now();

  std::cout << "closing file took: "
	    << (std::chrono::duration_cast<milliseconds>(t2 - t1)).count()
	    << "ms" << std::endl;

  std::cout << "file I/O took: "
	    << (std::chrono::duration_cast<seconds>(t2 - t0)).count()
	    << "s" << std::endl;

  std::cout << "total duration: "
	    << (std::chrono::duration_cast<seconds>(t2 - tstart)).count()
	    << "s" << std::endl;

  return;
}
