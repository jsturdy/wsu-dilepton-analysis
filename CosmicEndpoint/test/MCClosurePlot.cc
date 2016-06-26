#include "DataFormats/Math/interface/Vector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/LorentzVectorFwd.h"

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

#include "WSUDiLeptons/CosmicEndpoint/test/binFunctions.h"

void MCClosurePlot(std::string const& filelist, std::string const& outFile,
		   int etaBin_, int phiBin_,
		   int trackVal_, double minPt_, double maxBias_, int nBiasBins_,
		   double factor_=1.0, double lowpT_=-1.0, double highpT_=-1.0,
		   bool symmetric_=false, bool applyTrigger_=false, bool mcFlag_=false,
		   bool debug_=false)

{
  bool debug = debug_;

  if (debug) {
    std::cout<<"arg  1 (filelist) is:  "   << filelist   << std::endl;
    std::cout<<"arg  2 (etaBin) is:  "     << etaBin_    << std::endl;
    std::cout<<"arg  3 (phiBin) is:  "     << phiBin_    << std::endl;
    std::cout<<"arg  4 (outFile) is:  "    << outFile    << std::endl;
    std::cout<<"arg  5 (trackVal_) is:  "  << trackVal_  << std::endl;
    std::cout<<"arg  6 (minPt_) is:  "     << minPt_     << std::endl;
    std::cout<<"arg  7 (maxBias_) is:  "   << maxBias_   << std::endl;
    std::cout<<"arg  8 (nBiasBins_) is:  " << nBiasBins_ << std::endl;
    std::cout<<"arg  9 (factor_) is:  "    << factor_    << std::endl;
    std::cout<<"arg 10 (symmetric_) is:  " << symmetric_ << std::endl;
    std::cout<<"arg 11 (applyTrigger_) is:  " << applyTrigger_ << std::endl;
    std::cout<<"arg 12 (mcFlag_) is:  "       << mcFlag_       << std::endl;
    std::cout<<"arg 13 (debug_) is:  "        << debug_        << std::endl;
  }

  TFile *g;
  TChain *myChain;

  std::string trackAlgo;

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

  std::cout << "chose the track object"  << std::endl;

  std::stringstream outrootfile;
  std::cout << "checking for OUTPUTDIR " << std::endl;
  const char* envvar = std::getenv("OUTPUTDIR");
  if (envvar) {
    std::string outdir = std::string(envvar);
    outrootfile << outdir << "/" << outFile << outname;
    std::cout << "checked for found OUTPUTDIR "
	      << outdir << std::endl;
  }
  else {
    outrootfile << outFile << outname;
  }

  std::cout << "Output files "
	    << outrootfile.str() << std::endl;

  g = new TFile(TString(outrootfile.str()+".root"),"UPDATE");

  std::cout << "Processing tracks from " << trackAlgo << " algorithm" << std::endl;

  std::string name;
  std::stringstream inputfiles;

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
    newString << "root://xrootd.unl.edu//" << name;

    //Use the following line with line above commented out for running on local files.
    //newString << name;
    std::cout << newString.str() << std::endl;
    myChain->Add(TString(newString.str()));
  }
  std::cout << "Successfully opened inputfiles list!" << std::endl;
  //  myChain->Add(TString());
  //   newString << "root://xrootd.unl.edu//" << name;

  TTree *myTree = myChain;
  TTreeReader trackReader(myTree);

  float maxBias = maxBias_;
  int nBiasBins = nBiasBins_;

  // turn on Sumw2 by default
  TH1::SetDefaultSumw2();

  if (debug)
    std::cout << "setting up histograms" << std::endl;

  // all histograms separated eta/phi
  TString etaBins[2]    = {"EtaPlus","EtaMinus"};
  TString phiBins[3]    = {"PhiPlus","PhiZero","PhiMinus"};

  // for histograms separated by charge
  TString chargeBins[2] = {"Plus","Minus"};

  // control the curvature histograms
  // bin width = MAX_CURVE_RANGE/N_CURVE_BINS

  // default asymmetric binning -16.0/TeV to 16.0/TeV = 32/TeV, 32/3200 = 0.01/TeV
  // suggested for KS is 0.01/TeV
  // suggested for chi2 is 0.25/TeV to be around expected resolution, means rebinning 25 0.01 bins into one
  // symmetric binning 0/TeV to 16.0/TeV = 16.0/TeV, 16.0/1600 = 0.01/TeV
  // suggested for KS is 0.01/TeV
  // suggested for chi2 is 0.25/TeV to be around expected resolution, means rebinning 25 0.01 bins into one
  // should *never* have a bin that straddles 0, 0 should *always* be a bin boundary

  const int  N_CURVE_BINS      = 1600;
  const double MAX_CURVE_RANGE = 0.0160;

  if (debug)
    std::cout << "setting up pseudo experiments" << std::endl;
  ///// histograms for the MC closure study
  const int    N_PSEUDO = 100;
  const int    closureBin   = 25;      // injected bias bin to recover
  const double pseudoThresh = 0.0025;  // fraction of events to treat as data
  const bool recoverNegativeBias = false;
  const bool recoverPositiveBias = !recoverNegativeBias;

  TH2D *h_randvals;
  if (debug)
    std::cout << "booking randvals histogram" << std::endl;
  h_randvals = new TH2D("randvals","randvals",N_PSEUDO,-0.5,N_PSEUDO-0.5,1000,0,1);

  if (debug)
    std::cout << "setting up pseudo experiment histograms" << std::endl;
  TH1F *h_looseMuUpperCurvePseudoData[2][N_PSEUDO];
  TH1F *h_looseMuLowerCurvePseudoData[2][N_PSEUDO];
  if (debug)
    std::cout << "setting up pseudo experiment histograms2" << std::endl;
  TH1F *h_looseMuUpperCurvePlusBiasMCClosure[2][nBiasBins+1][N_PSEUDO];
  TH1F *h_looseMuLowerCurvePlusBiasMCClosure[2][nBiasBins+1][N_PSEUDO];
  if (debug)
    std::cout << "setting up pseudo experiment histograms3" << std::endl;
  TH1F *h_looseMuUpperCurveMinusBiasMCClosure[2][nBiasBins+1][N_PSEUDO];
  if (debug)
    std::cout << "setting up pseudo experiment histograms4" << std::endl;
  TH1F *h_looseMuLowerCurveMinusBiasMCClosure[2][nBiasBins+1][N_PSEUDO];

  if (debug)
    std::cout << "setting up TRandom3" << std::endl;
  TRandom3 closureRand(197351);

  if (debug)
    std::cout << "booking loose histograms" << std::endl;
  int etb = etaBin_;
  int phb = phiBin_;
  TString etaphilabel(etaBins[etb]+phiBins[phb]);
  g->cd();
  TDirectory* etaphidir = (TDirectory*)g->GetDirectory(etaphilabel);
  if (!etaphidir)
    etaphidir = (TDirectory*)g->mkdir(etaphilabel);
  etaphidir->cd();
  for (int chb = 0; chb < 2; ++chb) {
    if (debug)
      std::cout << "booking bias histograms"
		<< "chb=" << chb
		<< "etb=" << etb
		<< "phb=" << phb
		<< std::endl;
    for (int i = 0; i < nBiasBins+1; ++i) {
      std::stringstream name;
      name << std::setw(3) << std::setfill('0') << i + 1;

      std::stringstream title;
      title << "#Delta#kappa = +" << (i)*(factor_*maxBias/nBiasBins);

      for (int rab = 0; rab < N_PSEUDO; ++rab) {
	std::stringstream name2;
	name2 << std::setw(3) << std::setfill('0') << rab;
	if (i == closureBin) {
	  std::stringstream title2;
	  title2 << "pseudoexperiment " << rab;

	  title.str("");
	  title.clear();
	  title << "#Delta#kappa = "
		<< (recoverNegativeBias ? "-" : "+")
		<< (closureBin+1)*(factor_*maxBias/nBiasBins);
	  h_looseMuUpperCurvePseudoData[chb][rab] = new TH1F(TString("looseMuUpper"+chargeBins[chb]+"Curve"+etaphilabel+name.str()+"PseudoData"+name2.str()),
							     TString(title.str()+" "+title2.str()),
							     symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS, symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0., MAX_CURVE_RANGE*factor_);
	  h_looseMuLowerCurvePseudoData[chb][rab] = new TH1F(TString("looseMuLower"+chargeBins[chb]+"Curve"+etaphilabel+name.str()+"PseudoData"+name2.str()),
							     TString(title.str()+" "+title2.str()),
							     symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS, symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0., MAX_CURVE_RANGE*factor_);
	}

	std::stringstream title2;
	title2 << "pseudoexperiment " << rab;

	title.str("");
	title.clear();
	title << "#Delta#kappa = +" << (i)*(factor_*maxBias/nBiasBins);
	h_looseMuUpperCurvePlusBiasMCClosure[chb][i][rab]  = new TH1F(TString("looseMuUpper"+chargeBins[chb]+"Curve"+etaphilabel+"PlusBias"+name.str()+"MCClosure"+name2.str()),
								      TString(title.str()+" "+title2.str()),
								      symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS, symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0., MAX_CURVE_RANGE*factor_);
	h_looseMuLowerCurvePlusBiasMCClosure[chb][i][rab]  = new TH1F(TString("looseMuLower"+chargeBins[chb]+"Curve"+etaphilabel+"PlusBias"+name.str()+"MCClosure"+name2.str()),
								      TString(title.str()+" "+title2.str()),
								      symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS, symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0., MAX_CURVE_RANGE*factor_);
	title.str("");
	title.clear();
	title << "#Delta#kappa = -" << (i)*(factor_*maxBias/nBiasBins);
	h_looseMuUpperCurveMinusBiasMCClosure[chb][i][rab]  = new TH1F(TString("looseMuUpper"+chargeBins[chb]+"Curve"+etaphilabel+"MinusBias"+name.str()+"MCClosure"+name2.str()),
								       TString(title.str()+" "+title2.str()),
								       symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS, symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0., MAX_CURVE_RANGE*factor_);
	h_looseMuLowerCurveMinusBiasMCClosure[chb][i][rab]  = new TH1F(TString("looseMuLower"+chargeBins[chb]+"Curve"+etaphilabel+"MinusBias"+name.str()+"MCClosure"+name2.str()),
								       TString(title.str()+" "+title2.str()),
								       symmetric_ ? 2*N_CURVE_BINS : N_CURVE_BINS, symmetric_ ? -MAX_CURVE_RANGE*factor_ : 0., MAX_CURVE_RANGE*factor_);
      }  // end loop over pseudo experiments
    }  // end loop over bias bins
  }  // end loop over charge bins

  if (debug)
    std::cout << "saving etaphidir" << std::endl;
  etaphidir->Write();
  g->cd();
  // g->Write();

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

  TTreeReaderValue<Int_t> upTrackerPhits(                trackReader, "upperMuon_pixelHits"                   );
  TTreeReaderValue<Int_t> upTrackerThits(                trackReader, "upperMuon_trackerHits"                 );
  TTreeReaderValue<Int_t> upTrackerMhits(                trackReader, "upperMuon_muonStationHits"             );
  TTreeReaderValue<Int_t> upTrackerValidHits(            trackReader, "upperMuon_numberOfValidHits"           );
  TTreeReaderValue<Int_t> upTrackerValidMuonHits(        trackReader, "upperMuon_numberOfValidMuonHits"       );//Temporarily changed from ValidMuonHits to Valid Hits? why??
  TTreeReaderValue<Int_t> upTrackerMatchedMuonStations(  trackReader, "upperMuon_numberOfMatchedStations"     );
  TTreeReaderValue<Int_t> upTrackerLayersWithMeasurement(trackReader, "upperMuon_trackerLayersWithMeasurement");


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

  TTreeReaderValue<Int_t>    lowTrackerPhits(                trackReader, "lowerMuon_pixelHits"                   );
  TTreeReaderValue<Int_t>    lowTrackerThits(                trackReader, "lowerMuon_trackerHits"                 );
  TTreeReaderValue<Int_t>    lowTrackerMhits(                trackReader, "lowerMuon_muonStationHits"             );
  TTreeReaderValue<Int_t>    lowTrackerValidHits(            trackReader, "lowerMuon_numberOfValidHits"           );
  TTreeReaderValue<Int_t>    lowTrackerValidMuonHits(        trackReader, "lowerMuon_numberOfValidMuonHits"       );//Temporarily changed from ValidMuonHits to Valid Hits? why??
  TTreeReaderValue<Int_t>    lowTrackerMatchedMuonStations(  trackReader, "lowerMuon_numberOfMatchedStations"     );
  TTreeReaderValue<Int_t>    lowTrackerLayersWithMeasurement(trackReader, "lowerMuon_trackerLayersWithMeasurement");

  std::cout << "Made it to Histogramming!" << std::endl;
  int j = 0;

  //double maxDR = 0.15; // what is reasonable here? Aachen did dPhi < 0.1, dTheta (eta?) < 0.05

  while (trackReader.Next()) {

    Double_t *randvals = new Double_t[N_PSEUDO];
    closureRand.RndmArray(N_PSEUDO,randvals);
    for (int ri = 0; ri < N_PSEUDO; ++ri)
      h_randvals->Fill(ri,randvals[ri]);

    if (debug && j < 2)
      std::cout << "Made it into the first loop" << std::endl;
    g->cd();

    // apply the trigger, i.e., don't process if the trigger didn't fire
    if (applyTrigger_ && !(*fakeL1SingleMu))
      continue;

    // make combination of samples easy
    if (*nSimTracks > 0) {
      if ((simTrackpT[0] >= highpT_) || (simTrackpT[0] < lowpT_))
	continue;
    }

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
	bool up_superpointing = ((std::fabs(*upTrackerDxy) < 10) && (std::fabs(*upTrackerDz)  < 50))
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

	if ((j % 100) == 0)
	  std::cout << "upper leg"    << std::endl
		    << "mu pt  = "    << std::setw(8) << std::setprecision(2) << std::fixed << upTrackerMuonP4->pt()
		    << " - eta = "    << std::setw(6) << std::setprecision(2) << std::fixed << upTrackerMuonP4->eta()
		    << " - phi = "    << std::setw(6) << std::setprecision(2) << std::fixed << upTrackerMuonP4->phi()
		    << std::endl

		    << "trk pt = "    << std::setw(8) << std::setprecision(2) << std::fixed << sqrt(upTrackerTrack->perp2())
		    << " - eta = "    << std::setw(6) << std::setprecision(2) << std::fixed << upTrackerTrack->eta()
		    << " - phi = "    << std::setw(6) << std::setprecision(2) << std::fixed << upTrackerTrack->phi()
		    << std::endl;

	int etabin    = getEtaBin(upTrackerTrack->eta());
	int phibin    = getPhiBin(upTrackerTrack->phi());
	int chargebin = getChargeBin(*upTrackerCharge);

	if (etabin == etaBin_ && phibin == phiBin_) {
	  if (up_superpointing && up_etabar) {

	    // if a variable doesn't appear in the High-pT muon selection, then apply all the cuts
	    if (up_n1pt) {
	      for (int i = 0; i < nBiasBins+1; ++i) {
		double posBias = upperCpT+(i)*(factor_*maxBias/nBiasBins);
		double negBias = upperCpT-(i)*(factor_*maxBias/nBiasBins);

		// for the closure test, make a function?
		if (i == closureBin) {
		  for (int ri = 0; ri < N_PSEUDO; ++ri) {
		    if (!(randvals[ri] > pseudoThresh)) {
		      h_looseMuUpperCurvePseudoData[chargebin][ri]->Fill(recoverPositiveBias?posBias:negBias);
		      // h_looseMuUpperCurvePseudoData[getChargeBin(recoverPositiveBias?posBias:negBias)][ri]->Fill(recoverPositiveBias?posBias:negBias);
		    }
		  }
		}
		for (int ri = 0; ri < N_PSEUDO; ++ri) {
		  if (randvals[ri] > pseudoThresh) {
		    h_looseMuUpperCurvePlusBiasMCClosure[chargebin][i][ri]->Fill(posBias);
		    // h_looseMuUpperCurvePlusBiasMCClosure[getChargeBin(posBias)][i][ri]->Fill(posBias);
		    h_looseMuUpperCurveMinusBiasMCClosure[chargebin][i][ri]->Fill(negBias);
		    // h_looseMuUpperCurveMinusBiasMCClosure[getChargeBin(negBias)][i][ri]->Fill(negBias);
		  }
		}

		if (debug && j < 2)
		  std::cout << "Made it through the upper bias loop " << i << std::endl;
	      }
	    } // end if (up_n1pt)
	  } // end check on up_superpointing
	}  // end check on correct eta/phi bin

	/** Lower leg cosmics **/
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
	bool low_superpointing = ((std::fabs(*lowTrackerDxy) < 10) && (std::fabs(*lowTrackerDz)  < 50))
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

	if ((j % 100) == 0)
	  std::cout << "lower leg"    << std::endl
		    << "mu pt  = "    << std::setw(8) << std::setprecision(2) << std::fixed << lowTrackerMuonP4->pt()
		    << " - eta = "    << std::setw(6) << std::setprecision(2) << std::fixed << lowTrackerMuonP4->eta()
		    << " - phi = "    << std::setw(6) << std::setprecision(2) << std::fixed << lowTrackerMuonP4->phi()
		    << std::endl

		    << "trk pt = "    << std::setw(8) << std::setprecision(2) << std::fixed << sqrt(lowTrackerTrack->perp2())
		    << " - eta = "    << std::setw(6) << std::setprecision(2) << std::fixed << lowTrackerTrack->eta()
		    << " - phi = "    << std::setw(6) << std::setprecision(2) << std::fixed << lowTrackerTrack->phi()
		    << std::endl;

	etabin    = getEtaBin(lowTrackerTrack->eta());
	phibin    = getPhiBin(lowTrackerTrack->phi());
	chargebin = getChargeBin(*lowTrackerCharge);

	if (etabin == etaBin_ && phibin == phiBin_) {
	  // fill the counters histogram for the lower leg muons passing the super-pointing selection
	  if (low_superpointing && low_etabar) {
	    // if a variable doesn't appear in the High-pT muon selection, then apply all the cuts
	    if (low_n1pt) {
	      for (int i = 0; i < nBiasBins+1; ++i) {
		double posBias = lowerCpT+(i)*(factor_*maxBias/nBiasBins);
		double negBias = lowerCpT-(i)*(factor_*maxBias/nBiasBins);

		// for the closure test, make a function?
		if (i == closureBin) {
		  for (int ri = 0; ri < N_PSEUDO; ++ri) {
		    if (randvals[ri] > pseudoThresh) {
		      h_looseMuLowerCurvePseudoData[chargebin][ri]->Fill(recoverPositiveBias?posBias:negBias);
		      // h_looseMuLowerCurvePseudoData[getChargeBin(recoverPositiveBias?posBias:negBias)][ri]->Fill(recoverPositiveBias?posBias:negBias);
		    }
		  }
		}

		for (int ri = 0; ri < N_PSEUDO; ++ri) {
		  if (randvals[ri] > pseudoThresh) {
		    h_looseMuLowerCurvePlusBiasMCClosure[chargebin][i][ri]->Fill(posBias);
		    // h_looseMuLowerCurvePlusBiasMCClosure[getChargeBin(posBias)][i][ri]->Fill(posBias);
		    h_looseMuLowerCurveMinusBiasMCClosure[chargebin][i][ri]->Fill(negBias);
		    // h_looseMuLowerCurveMinusBiasMCClosure[getChargeBin(negBias)][i][ri]->Fill(negBias);
		  }
		}

		if (debug && j < 2)
		  std::cout << "Made it through the lower bias loop " << i << std::endl;
	      }
	    } // end if (low_n1pt)
	  } // end check on low_superpointing
	}  // end check on eta/phi bin
	//} // end if (sqrt(lowTrackerTrack->perp2()) > minPt_)
      } // end if (sqrt(upTrackerTrack->perp2()) > minPt_ || sqrt(lowTrackerTrack->perp2()) > minPt_)

      ++j;
      if (debug && j < 2)
	std::cout << "Made it through " << j << " sets of fills" << std::endl;
    } // closing if (*upTrackerChi2 > -1)

    delete randvals;
  } // end while loop

  if (debug)
    std::cout << std::hex << g << std::dec << std::endl;

  g->Write();
  g->Close();

  return;
}
