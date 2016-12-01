#include "WSUDiLeptons/MuonAnalyzer/interface/MuonTree.h"

//#include "WSUDiLeptons/MuonAnalyzer/interface/MuonHelpers.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"

// -*- C++ -*-
//
// Package:    WSUDiLeptons/MuonAnalyzer
// Class:      MuonTree
//
/**\class MuonTree MuonTree.cc WSUDiLeptons/MuonAnalyzer/plugins/MuonTree.cc

   Description: [one line class summary]

   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  Jared Sturdy
//         Created:  Wed, 25 Feb 2015 12:55:49 GMT
//
//


MuonTree::MuonTree(const edm::ParameterSet& pset)
{
  usesResource("TFileService");

  muonSrc_     = pset.getParameter<edm::InputTag>("muonSrc");
  upperLegSrc_ = pset.getParameter<edm::InputTag>("upperLegSrc");
  lowerLegSrc_ = pset.getParameter<edm::InputTag>("lowerLegSrc");

  globalTrackSrc_  = pset.getParameter<edm::InputTag>("globalTrackSrc");
  cosmicTrackSrc_  = pset.getParameter<edm::InputTag>("cosmicTrackSrc");
  trackerTrackSrc_ = pset.getParameter<edm::InputTag>("trackerTrackSrc");

  isGen_       = pset.getParameter<bool>("isGen");
  if (isGen_)
    simTrackSrc_ = pset.getParameter<edm::InputTag>("simTrackSrc");

  l1MuonSrc_           = pset.getParameter<edm::InputTag>("l1MuonSrc");
  l1MuonSrcNew_        = pset.getParameter<edm::InputTag>("l1MuonSrcNew");
  trigResultsSrc_      = pset.getParameter<edm::InputTag>("trigResultsSrc");
  fakeL1SingleMuSrc_   = pset.getParameter<edm::InputTag>("fakeL1SingleMuSrc");
  hltTrigCut_          = pset.getParameter<std::string>("hltTrigCut");

  debug_       = pset.getParameter<int>("debug");
  algoType_    = pset.getParameter<int>("algoType");

  maxDEta_ = pset.getParameter<double>("maxDEta");
  maxDPhi_ = pset.getParameter<double>("maxDPhi");
  maxDR_   = pset.getParameter<double>("maxDR");
  minPt_   = pset.getParameter<double>("minPt");

  //now do what ever initialization is needed
  muonToken_     = consumes<reco::MuonCollection>(muonSrc_);
  upperLegToken_ = consumes<reco::MuonCollection>(upperLegSrc_);
  lowerLegToken_ = consumes<reco::MuonCollection>(lowerLegSrc_);

  globalTrackToken_  = consumes<reco::TrackCollection>(globalTrackSrc_);
  cosmicTrackToken_  = consumes<reco::TrackCollection>(cosmicTrackSrc_);
  trackerTrackToken_ = consumes<reco::TrackCollection>(trackerTrackSrc_);

  if (isGen_)
    simTrackToken_ = consumes<edm::SimTrackContainer>(simTrackSrc_);

  l1MuonToken_         = consumes<std::vector<l1extra::L1MuonParticle> >(l1MuonSrc_);
  l1MuonTokenNew_      = consumes<l1t::MuonBxCollection>(l1MuonSrcNew_);
  trigResultsToken_    = consumes<edm::TriggerResults>(trigResultsSrc_);
  fakeL1SingleMuToken_ = consumes<bool>(fakeL1SingleMuSrc_);

  event = -1;
  run   = -1;
  lumi  = -1;
}


MuonTree::~MuonTree()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void MuonTree::analyze(const edm::Event& ev, const edm::EventSetup& es)
{
  using namespace ROOT::Math;
  edm::Handle<reco::MuonCollection > muonColl;
  edm::Handle<reco::MuonCollection > upperLegColl;
  edm::Handle<reco::MuonCollection > lowerLegColl;
  ev.getByToken(muonToken_,     muonColl);
  ev.getByToken(upperLegToken_, upperLegColl);
  ev.getByToken(lowerLegToken_, lowerLegColl);

  edm::Handle<reco::TrackCollection> globalTrackColl;
  edm::Handle<reco::TrackCollection> cosmicTrackColl;
  edm::Handle<reco::TrackCollection> trackerTrackColl;
  ev.getByToken(globalTrackToken_,  globalTrackColl);
  ev.getByToken(cosmicTrackToken_,  cosmicTrackColl);
  ev.getByToken(trackerTrackToken_, trackerTrackColl);

  edm::Handle<edm::SimTrackContainer > simTrackColl;
  if (isGen_)
    ev.getByToken(simTrackToken_, simTrackColl);

  edm::Handle<std::vector<l1extra::L1MuonParticle> > l1MuonColl;
  edm::Handle<l1t::MuonBxCollection>                 l1MuonCollNew;
  ev.getByToken(l1MuonToken_,    l1MuonColl);
  ev.getByToken(l1MuonTokenNew_, l1MuonCollNew);

  edm::Handle<edm::TriggerResults> triggerResults;
  ev.getByToken(trigResultsToken_, triggerResults);

  edm::Handle<bool>                   fakeL1SingleMuH;
  ev.getByToken(fakeL1SingleMuToken_, fakeL1SingleMuH);

  edm::Handle<reco::TrackCollection> tracks[3] = {globalTrackColl, cosmicTrackColl, trackerTrackColl};

  for (int idx = 0; idx < 25; ++idx) {
    // initialize muon sim track variables
    simtrack_type[idx]   = 0;
    simtrack_pt[idx]     = -1.;
    simtrack_eta[idx]    = -10.;
    simtrack_phi[idx]    = -10.;
    simtrack_charge[idx] = -10;

    // initialize l1 muon variables (l1extra collection)
    l1muon_pt[idx]       = -10.;
    l1muon_eta[idx]      = -10.;
    l1muon_phi[idx]      = -10.;
    l1muon_charge[idx]   = -10;

    l1muon_isFwd[idx]  =  -1;
    l1muon_isRPC[idx]  =  -1;

    l1muon_bx[idx]       =  -1;
    l1muon_quality[idx]  =  -1;
    l1muon_detector[idx] =  -1;

    l1muon_iso[idx]      =  -1;
    l1muon_mip[idx]      =  -1;
    l1muon_rank[idx]     =  -1;
    l1muon_idxdtcsc[idx] =  -1;
    l1muon_idxrpc[idx]   =  -1;

    // initialize l1 muon variables (gmtStage2Digi collection)
    l1muonnew_pt[idx]       = -10.;
    l1muonnew_eta[idx]      = -10.;
    l1muonnew_phi[idx]      = -10.;
    l1muonnew_charge[idx]   = -10;

    l1muonnew_isFwd[idx]  =  -1;
    l1muonnew_isRPC[idx]  =  -1;

    l1muonnew_bx[idx]       =  -1;
    l1muonnew_quality[idx]  =  -1;
    l1muonnew_detector[idx] =  -1;

    l1muonnew_iso[idx]      =  -1;
    l1muonnew_mip[idx]      =  -1;
    l1muonnew_rank[idx]     =  -1;
    l1muonnew_idxdtcsc[idx] =  -1;
    l1muonnew_idxrpc[idx]   =  -1;

    // initialize muon variables
    muon_isGlobal[    idx] = -1;
    muon_isTracker[   idx] = -1;
    muon_isStandAlone[idx] = -1;

    muon_hasGlobal[idx]   = -1;
    muon_hasInner[ idx]   = -1;
    muon_hasOuter[ idx]   = -1;
    muon_global_chi2[idx] = -1.;
    muon_global_ndof[idx] = -1;
    muon_inner_chi2[ idx] = -1.;
    muon_inner_ndof[ idx] = -1;
    muon_outer_chi2[ idx] = -1.;
    muon_outer_ndof[ idx] = -1;

    muon_isLower[   idx] = -1;
    muon_isUpper[   idx] = -1;
    muon_isLowerOld[idx] = -1;
    muon_isUpperOld[idx] = -1;

    muonP4[idx].SetXYZT(0,0,0,-1);
    muon_pT[idx]  = -1;
    muon_Eta[idx] = -10;
    muon_Phi[idx] = -10;

    muon_innerY[idx] = 0; // what's a good nonsense value for this?
    muon_outerY[idx] = 0; // what's a good nonsense value for this?
    muon_tpin[idx]   = 0; // what's a good nonsense value for this?
    muon_tpout[idx]  = 0; // what's a good nonsense value for this?

    muon_trackVec[idx].SetXYZ(0,0,0);
    muon_trackPt[idx]  = -1;
    muon_trackEta[idx] = -10;
    muon_trackPhi[idx] = -10;
    muon_ptError[idx]  = -1;

    muon_charge[idx] = -10;
    muon_chi2[  idx] = -1.;
    muon_ndof[  idx] = -1;

    muon_dxy[     idx] = -1000;
    muon_dz[      idx] = -1000;
    muon_dxyError[idx] = -1;
    muon_dzError[ idx] = -1;

    muon_firstPixel[ idx] = -1;
    muon_pixHits[    idx] = -1;
    muon_tkHits[     idx] = -1;
    muon_muonStaHits[idx] = -1;
    muon_nVHits[     idx] = -1;
    muon_nVMuHits[   idx] = -1;
    muon_nMatSta[    idx] = -1;
    muon_tkLayWMeas[ idx] = -1;

    // initialize muon track ref variables (global, outer, inner, tracker, tpfms, dyt, picky, tunep)
    for (int tk = 0; tk < 8; ++tk) {
      track_innerY[tk][idx] = 0; // what's a good nonsense value for this?
      track_outerY[tk][idx] = 0; // what's a good nonsense value for this?
      track_tpin[tk][idx]   = 0; // what's a good nonsense value for this?
      track_tpout[tk][idx]  = 0; // what's a good nonsense value for this?

      track_trackPt[tk][idx]  = -1;
      track_trackEta[tk][idx] = -10;
      track_trackPhi[tk][idx] = -10;
      track_ptError[tk][idx]  = -1;

      track_charge[tk][idx] = -10;
      track_chi2[  tk][idx] = -1;
      track_ndof[  tk][idx] = -1;

      track_isLower[   tk][idx] = -1;
      track_isUpper[   tk][idx] = -1;
      track_isLowerOld[tk][idx] = -1;
      track_isUpperOld[tk][idx] = -1;

      track_dxy[     tk][idx] = -1000;
      track_dz[      tk][idx] = -1000;
      track_dxyError[tk][idx] = -1;
      track_dzError[ tk][idx] = -1;

      track_matchedMuIdx[tk][idx] = -1;

      track_firstPixel[ tk][idx] = -1;
      track_pixHits[    tk][idx] = -1;
      track_tkHits[     tk][idx] = -1;
      track_muonStaHits[tk][idx] = -1;
      track_nVHits[     tk][idx] = -1;
      track_nVMuHits[   tk][idx] = -1;
      track_nMatSta[    tk][idx] = -1;
      track_tkLayWMeas[ tk][idx] = -1;
    }
  }

  ////////////////// Generic event information /////////////////////////
  event = (ev.id()).event();
  run   = (ev.id()).run();
  lumi  = ev.luminosityBlock();

  //type = reco::Muon::SegmentAndTrackArbitration;

  nMuons     = muonColl->size();
  nUpperLegs = upperLegColl->size();
  nLowerLegs = lowerLegColl->size();

  nGlobalTracks  = globalTrackColl->size();
  nCosmicTracks  = cosmicTrackColl->size();
  nTrackerTracks = trackerTrackColl->size();

  ////////////////// edm::SimTrack information /////////////////////////
  nSimTracks = 0;
  if (isGen_)
    if (simTrackColl->size() > 0) {
      nSimTracks = 0;
      int simIdx = 0;
      for (auto simtrack = simTrackColl->begin(); simtrack != simTrackColl->end(); ++simtrack) {
	if (fabs(simtrack->type()) == 13) {  // only consider simtracks from muons
	  if (debug_ > 2)
	    std::cout << std::setw(5) << *simtrack << std::endl;
	  if (nSimTracks > 24) {
	    nSimTracks = 25;
	    continue; // skip if there happen to be more than 25 sim Tracks
	  }

	  simtrack_charge[simIdx] = simtrack->charge();
	  simtrack_type[simIdx]   = simtrack->type();
	  simtrack_pt[simIdx]  = simtrack->trackerSurfaceMomentum().pt();
	  simtrack_eta[simIdx] = simtrack->trackerSurfaceMomentum().eta();
	  simtrack_phi[simIdx] = simtrack->trackerSurfaceMomentum().phi();
	  ++simIdx;
	  ++nSimTracks;
	}
      }
    }

  ////////////////// L1Muon information /////////////////////////
  nL1MuonsNew = 0;
  if (l1MuonCollNew.isValid()) {
    for (int ibx = l1MuonCollNew->getFirstBX(); ibx <= l1MuonCollNew->getLastBX(); ++ibx) {
      // if (trigger_bx_only && (ibx != 0))
      if (ibx != 0)
	continue;
      int l1muIdx = 0;
      nL1MuonsNew = l1MuonCollNew->size(ibx);
      // nL1MuonsNew = 0;
      for (auto l1mu = l1MuonCollNew->begin(ibx); l1mu != l1MuonCollNew->end(ibx); ++l1mu) {
	std::cout << "bx:  " << ibx << "  et:  "  << l1mu->et()
		  << "  eta:  "  << l1mu->eta()
		  << "  phi:  "  << l1mu->phi() << std::endl;
	if (l1mu->et() == 0)
	  continue; // if you don't care about L1T candidates with zero ET.
	if (nL1MuonsNew > 24) {
	  nL1MuonsNew = 25;
	  continue; // skip if there happen to be more than 25 L1 muons
	}
	l1muonnew_pt[l1muIdx]     = l1mu->pt();
	l1muonnew_eta[l1muIdx]    = l1mu->eta();
	l1muonnew_phi[l1muIdx]    = l1mu->phi();
	l1muonnew_charge[l1muIdx] = l1mu->charge();

	l1muonnew_isFwd[l1muIdx]    = l1mu->hwRank();
	l1muonnew_isRPC[l1muIdx]    = l1mu->hwRank();

	l1muonnew_bx[l1muIdx]       = ibx;
	l1muonnew_quality[l1muIdx]  = l1mu->hwQual();
	l1muonnew_detector[l1muIdx] = l1mu->hwRank();

	l1muonnew_iso[l1muIdx]      = l1mu->hwIso();
	l1muonnew_mip[l1muIdx]      = l1mu->hwRank();
	l1muonnew_rank[l1muIdx]     = l1mu->hwRank();
	l1muonnew_idxdtcsc[l1muIdx] = l1mu->hwRank();
	l1muonnew_idxrpc[l1muIdx]   = l1mu->hwRank();

	++l1muIdx;
      }
    }
  } else {
    edm::LogWarning("MissingProduct") << "L1Upgrade muon bx collection not found." << std::endl;
  }

  ///// legacy L1 muon information ///
  nL1Muons = l1MuonColl->size();
  if (l1MuonColl->size() > 0) {
    int l1muIdx = 0;
    if (debug_ > 0)
      std::cout << "Found " << nL1Muons << " L1MuonParticles: (pt/eta/phi/charge)" << std::endl;
    for (auto l1mu = l1MuonColl->begin(); l1mu != l1MuonColl->end(); ++ l1mu) {
      if (debug_ > 0) {
	std::cout << l1mu->gmtMuonCand() << " - "
		  << l1mu->pt()     << "/"
		  << l1mu->eta()    << "/"
		  << l1mu->phi()    << "/"
		  << l1mu->charge()
		  << std::endl;

      }
      // if there happen to be more than 25 L1 muons, let's only keep the first 25
      if (l1muIdx > 24) {
	nL1Muons = 25;
	continue;
      }
      l1muon_pt[l1muIdx]     = l1mu->pt();
      l1muon_eta[l1muIdx]    = l1mu->eta();
      l1muon_phi[l1muIdx]    = l1mu->phi();
      l1muon_charge[l1muIdx] = l1mu->charge();

      l1muon_isFwd[l1muIdx]  = l1mu->gmtMuonCand().isFwd();
      l1muon_isRPC[l1muIdx]  = l1mu->gmtMuonCand().isRPC();

      l1muon_bx[l1muIdx]       = l1mu->gmtMuonCand().bx();
      l1muon_quality[l1muIdx]  = l1mu->gmtMuonCand().quality();
      l1muon_detector[l1muIdx] = l1mu->gmtMuonCand().detector();

      l1muon_iso[l1muIdx]      = l1mu->isIsolated();
      l1muon_mip[l1muIdx]      = l1mu->isMip();
      l1muon_rank[l1muIdx]     = l1mu->gmtMuonCand().rank();
      l1muon_idxdtcsc[l1muIdx] = l1mu->gmtMuonCand().getDTCSCIndex();
      l1muon_idxrpc[l1muIdx]   = l1mu->gmtMuonCand().getRPCIndex();

      ++l1muIdx;
    }  // end loop over l1MuonColl
  }  // end check on l1MuonColl size

  l1SingleMu = 0;
  const edm::TriggerNames& trigNames = ev.triggerNames(*triggerResults);
  for (unsigned int trig = 0; trig < trigNames.size(); ++trig) {
    //for (auto trig = triggerNames.begin(); trig != triggerNames.end(); ++trig) {
    if (triggerResults->accept(trig)) {
      std::string pathName = trigNames.triggerName(trig);
      if (debug_ > 3)
	std::cout << "Trigger path " << pathName << " fired" << std::endl;

      if (pathName.find(hltTrigCut_) != std::string::npos) {
	if (debug_ > 2)
	  std::cout << "Trigger path " << pathName << " fired" << std::endl;
	l1SingleMu = 1;
      }
    }
  }

  fakeL1SingleMu = *fakeL1SingleMuH;

  ////////////////// reco::Muon information /////////////////////////
  // skip processing empty collection
  if ( muonColl->size() > 0 || globalTrackColl->size() > 0 || cosmicTrackColl->size() > 0 || trackerTrackColl->size() > 0)
    if (debug_ > 0) {
      std::cout << "run/lumi/event "  << run  << "/" << lumi << "/" << event << std::endl;
      std::cout << "nMuons "          << nMuons         << std::endl
		<< "nUpperLegs "      << nUpperLegs     << std::endl
		<< "nLowerLegs "      << nLowerLegs     << std::endl
		<< "nGlobalTracks "   << nGlobalTracks  << std::endl
		<< "nCosmicTracks "   << nCosmicTracks  << std::endl
		<< "nTrackerTracks "  << nTrackerTracks << std::endl
		<< "nSimTracks "      << nSimTracks     << std::endl
		<< "nL1Muons "        << nL1Muons       << std::endl
		<< "nL1MuonsNew "     << nL1MuonsNew    << std::endl;
    }

  //// reco::Muon information ////
  if ( muonColl->size() > 0) {
    if (debug_ > 0) {
      std::cout << std::endl
  		<< "found "     << nMuons     << " muons "      << std::endl
		<< "found "     << nUpperLegs << " upper legs " << std::endl
		<< "found "     << nLowerLegs << " lower legs " << std::endl
		<< "trackAlgo " << algoType_ << std::endl;
      std::cout << " muons: " << std::endl;
      for (auto muon = muonColl->begin(); muon != muonColl->end(); ++muon) {
	std::cout << (muon->outerTrack().isNonnull() ? (muon->outerTrack()->outerPosition().Y() > 0 ? "found outer upper leg" : "found outer lower leg") :
		      (fabs(muon->innerTrack()->innerPosition().Y()) > fabs(muon->innerTrack()->outerPosition().Y()) ? " found inner upper leg" :
		       "found inner lower leg"))
		  << std::endl;
	std::cout << (muon->outerTrack().isNonnull() ? muon->outerTrack()->outerPosition().Y() > 0 :
		      (fabs(muon->innerTrack()->innerPosition().Y()) > fabs(muon->innerTrack()->outerPosition().Y()))) << "u/"
		  << (muon->outerTrack().isNonnull() ? muon->outerTrack()->outerPosition().Y() < 0 :
		      (fabs(muon->innerTrack()->innerPosition().Y()) < fabs(muon->innerTrack()->outerPosition().Y()))) << "l"
		  << std::endl;
	std::cout << std::setw(5) << *muon
		  << " (" << muon->isTrackerMuon()    << "(" << muon->innerTrack().isNonnull()  << ")t"
		  << "/"  << muon->isGlobalMuon()     << "(" << muon->globalTrack().isNonnull() << ")g"
		  << "/"  << muon->isStandAloneMuon() << "(" << muon->outerTrack().isNonnull()  << ")sa"
		  << ") "
		  << std::endl
		  << "pt:" << muon->pt() << "/eta:" << muon->eta() << "/phi:" << muon->phi() << std::endl
		  << " y:"
		  << std::setw(8) << muon->tunePMuonBestTrack()->innerPosition().Y()
		  << "/"
		  << std::setw(8) << muon->tunePMuonBestTrack()->outerPosition().Y()
		  << std::endl
		  << " outer position:("  << muon->tunePMuonBestTrack()->outerPosition().Y()
		  << "tp/"                << (muon->innerTrack().isNonnull()  ? muon->innerTrack()->outerPosition().Y()  : 0.)
		  << "t/"                 << (muon->globalTrack().isNonnull() ? muon->globalTrack()->outerPosition().Y() : 0.)
		  << "g/"                 << (muon->outerTrack().isNonnull()  ? muon->outerTrack()->outerPosition().Y()  : 0.)
		  << "sa)"
		  << std::endl
		  << " inner position:("  << muon->tunePMuonBestTrack()->innerPosition().Y()
		  << "tp/"                << (muon->innerTrack().isNonnull()  ? muon->innerTrack()->innerPosition().Y()  : 0.)
		  << "t/"                 << (muon->globalTrack().isNonnull() ? muon->globalTrack()->innerPosition().Y() : 0.)
		  << "g/"                 << (muon->outerTrack().isNonnull()  ? muon->outerTrack()->innerPosition().Y()  : 0.)
		  << "sa)"
		  << std::endl
		  << " chi2:("            << muon->tunePMuonBestTrack()->chi2()
		  << "tp/"                << (muon->innerTrack().isNonnull()  ? muon->innerTrack()->chi2()  : -1.)
		  << "t/"                 << (muon->globalTrack().isNonnull() ? muon->globalTrack()->chi2() : -1.)
		  << "g/"                 << (muon->outerTrack().isNonnull()  ? muon->outerTrack()->chi2()  : -1.)
		  << "sa)"
		  << std::endl
		  << " pt:"  << muon->tunePMuonBestTrack()->pt()
		  << "/eta:" << muon->tunePMuonBestTrack()->eta()
		  << "/phi:" << muon->tunePMuonBestTrack()->phi()
		  << std::endl
		  << " dxy:"   << std::setw(8) << muon->tunePMuonBestTrack()->dxy()
		  << " dz:"    << std::setw(8) << muon->tunePMuonBestTrack()->dz()
		  << " tpin:"  << std::setw(8) << muon->time().timeAtIpInOut
		  << " tpout:" << std::setw(8) << muon->time().timeAtIpOutIn
		  << std::endl;
      }
      std::cout << " upper legs: " << std::endl;
      for (auto muon = upperLegColl->begin(); muon != upperLegColl->end(); ++muon)
	std::cout << std::setw(5) << *muon
		  << " (" << muon->isTrackerMuon()    << "t"
		  << "/"  << muon->isGlobalMuon()     << "g"
		  << "/"  << muon->isStandAloneMuon() << "sa"
		  << ") " << muon->tunePMuonBestTrack()->innerPosition().Y()
		  << std::endl;
      std::cout << " lower legs: " << std::endl;
      for (auto muon = lowerLegColl->begin(); muon != lowerLegColl->end(); ++muon)
	std::cout << std::setw(5) << *muon
		  << " (" << muon->isTrackerMuon()    << "t"
		  << "/"  << muon->isGlobalMuon()     << "g"
		  << "/"  << muon->isStandAloneMuon() << "sa"
		  << ") " << muon->tunePMuonBestTrack()->innerPosition().Y()
		  << std::endl;
    }
    std::cout.flush();

    int muIdx = 0;
    for (auto mu = muonColl->begin(); mu != muonColl->end(); ++ mu) {
      if (nMuons > 24) {
	nMuons = 25;
	continue; // skip if there happen to be more than 25 muons
      }

      //reco::TrackRef ref = wsu::dileptons::MuonHelpers::GetTrackType(algoType_, &(*mu));

      reco::TrackRef ref = GetTrackType(algoType_, &(*mu));

      muon_tpin[muIdx]   = mu->time().timeAtIpInOut;
      muon_tpout[muIdx]  = mu->time().timeAtIpOutIn;

      muon_isTracker[   muIdx] = mu->isTrackerMuon();
      muon_isGlobal[    muIdx] = mu->isGlobalMuon();
      muon_isStandAlone[muIdx] = mu->isStandAloneMuon();

      muon_isUpper[muIdx] = (mu->outerTrack().isNonnull() ? mu->outerTrack()->outerPosition().Y() > 0 :
			     (fabs(mu->innerTrack()->innerPosition().Y()) > fabs(mu->innerTrack()->outerPosition().Y())));
      muon_isLower[muIdx] =  (mu->outerTrack().isNonnull() ? mu->outerTrack()->outerPosition().Y() < 0 :
			      (fabs(mu->innerTrack()->innerPosition().Y()) < fabs(mu->innerTrack()->outerPosition().Y())));
      muon_isLowerOld[muIdx] = fabs(mu->tunePMuonBestTrack()->innerPosition().Y()) < fabs(mu->tunePMuonBestTrack()->outerPosition().Y());
      muon_isUpperOld[muIdx] = fabs(mu->tunePMuonBestTrack()->innerPosition().Y()) > fabs(mu->tunePMuonBestTrack()->outerPosition().Y());

      muonP4[       muIdx] = mu->p4();
      muon_pT[      muIdx] = mu->pt();
      muon_Eta[     muIdx] = mu->eta();
      muon_Phi[     muIdx] = mu->phi();

      if (mu->pt() > 50)
	++nMuonsPt50;
      if (mu->pt() > 100)
	++nMuonsPt100 ;
      if (mu->pt() > 200)
	++nMuonsPt200 ;
      if (mu->pt() > 300)
	++nMuonsPt300 ;
      if (mu->pt() > 400)
	++nMuonsPt400 ;
      if (mu->pt() > 500)
	++nMuonsPt500 ;
      if (mu->pt() > 750)
	++nMuonsPt750 ;
      if (mu->pt() > 1000)
	++nMuonsPt1000;
      if (mu->pt() > 1500)
	++nMuonsPt1500;

      if (ref.isNonnull()) {  // can't dereference if the desired track ref is null
	// selections are done on "best track" in high pT ID, so take the track under study
	muon_chi2[    muIdx] = ref->chi2();
	muon_ndof[    muIdx] = ref->ndof();
	muon_charge[  muIdx] = ref->charge();
	muon_dxy[     muIdx] = ref->dxy();
	muon_dz[      muIdx] = ref->dz();
	muon_ptError[ muIdx] = ref->ptError();
	muon_dxyError[muIdx] = ref->dxyError();
	muon_dzError[ muIdx] = ref->dzError();
	muon_trackPt[ muIdx] = ref->pt();
	muon_trackEta[muIdx] = ref->eta();
	muon_trackPhi[muIdx] = ref->phi();
	muon_trackVec[muIdx] = ref->momentum();
	muon_innerY[  muIdx] = ref->innerPosition().Y();
	muon_outerY[  muIdx] = ref->outerPosition().Y();
      }

      if (mu->globalTrack().isNonnull()) {
	muon_global_chi2[muIdx] = mu->globalTrack()->chi2();
	muon_global_ndof[muIdx] = mu->globalTrack()->ndof();
	muon_hasGlobal[muIdx] = 1;
      }
      if (mu->innerTrack().isNonnull()) {
	muon_inner_chi2[muIdx] = mu->innerTrack()->chi2();
	muon_inner_ndof[muIdx] = mu->innerTrack()->ndof();
	muon_hasInner[muIdx] = 1;
      }
      if (mu->outerTrack().isNonnull()) {
	muon_outer_chi2[muIdx] = mu->outerTrack()->chi2();
	muon_outer_ndof[muIdx] = mu->outerTrack()->ndof();
	muon_hasOuter[muIdx] = 1;
      }
      // take hit pattern from global track
      if (mu->globalTrack().isNonnull()) {
	muon_hasGlobal[muIdx] = 1;
	muon_firstPixel[ muIdx] = (mu->globalTrack()->hitPattern().hasValidHitInFirstPixelBarrel() ||
				   mu->globalTrack()->hitPattern().hasValidHitInFirstPixelEndcap());
	muon_pixHits[    muIdx] = mu->globalTrack()->hitPattern().numberOfValidPixelHits();
	muon_tkHits[     muIdx] = mu->globalTrack()->hitPattern().numberOfValidTrackerHits();
	muon_tkLayWMeas[ muIdx] = mu->globalTrack()->hitPattern().trackerLayersWithMeasurement();
	muon_muonStaHits[muIdx] = mu->globalTrack()->hitPattern().muonStationsWithValidHits();
	muon_nVHits[     muIdx] = mu->globalTrack()->hitPattern().numberOfValidHits();
	muon_nVMuHits[   muIdx] = mu->globalTrack()->hitPattern().numberOfValidMuonHits();
      } else {  // otherwise take hit pattern from inner/outer track separately
	if (mu->innerTrack().isNonnull()) {
	  muon_firstPixel[ muIdx] = (mu->innerTrack()->hitPattern().hasValidHitInFirstPixelBarrel() ||
				     mu->innerTrack()->hitPattern().hasValidHitInFirstPixelEndcap());
	  muon_pixHits[    muIdx] = mu->innerTrack()->hitPattern().numberOfValidPixelHits();
	  muon_tkHits[     muIdx] = mu->innerTrack()->hitPattern().numberOfValidTrackerHits();
	  muon_tkLayWMeas[ muIdx] = mu->innerTrack()->hitPattern().trackerLayersWithMeasurement();
	}
	if (mu->outerTrack().isNonnull()) {
	  muon_muonStaHits[muIdx] = mu->outerTrack()->hitPattern().muonStationsWithValidHits();
	  muon_nVHits[     muIdx] = mu->outerTrack()->hitPattern().numberOfValidHits();
	  muon_nVMuHits[   muIdx] = mu->outerTrack()->hitPattern().numberOfValidMuonHits();
	}
      }
      muon_nMatSta[muIdx] = mu->numberOfMatchedStations(reco::Muon::SegmentAndTrackArbitration);

      // get info from all track types
      for (int tref = 0; tref < 5; ++tref) {
	ref = GetTrackType(tref+1, &(*mu));

	if (ref.isNonnull()) {  // can't dereference if the desired track ref is null
	  track_isLower[   2+tref+1][muIdx] = ref->outerPosition().Y() < 0;
	  track_isUpper[   2+tref+1][muIdx] = ref->outerPosition().Y() > 0;
	  track_isLowerOld[2+tref+1][muIdx] = fabs(ref->innerPosition().Y()) < fabs(ref->outerPosition().Y());
	  track_isUpperOld[2+tref+1][muIdx] = fabs(ref->innerPosition().Y()) > fabs(ref->outerPosition().Y());
	  track_chi2[      2+tref+1][muIdx] = ref->chi2();
	  track_ndof[      2+tref+1][muIdx] = ref->ndof();
	  track_charge[    2+tref+1][muIdx] = ref->charge();
	  track_dxy[       2+tref+1][muIdx] = ref->dxy();
	  track_dz[        2+tref+1][muIdx] = ref->dz();
	  track_ptError[   2+tref+1][muIdx] = ref->ptError();
	  track_dxyError[  2+tref+1][muIdx] = ref->dxyError();
	  track_dzError[   2+tref+1][muIdx] = ref->dzError();
	  track_trackPt[   2+tref+1][muIdx] = ref->pt();
	  track_trackEta[  2+tref+1][muIdx] = ref->eta();
	  track_trackPhi[  2+tref+1][muIdx] = ref->phi();
	  track_innerY[    2+tref+1][muIdx] = ref->innerPosition().Y();
	  track_outerY[    2+tref+1][muIdx] = ref->outerPosition().Y();

	  track_firstPixel[ 2+tref+1][muIdx] = (ref->hitPattern().hasValidHitInFirstPixelBarrel() ||
						ref->hitPattern().hasValidHitInFirstPixelEndcap());
	  track_pixHits[    2+tref+1][muIdx] = ref->hitPattern().numberOfValidPixelHits();
	  track_tkHits[     2+tref+1][muIdx] = ref->hitPattern().numberOfValidTrackerHits();
	  track_tkLayWMeas[ 2+tref+1][muIdx] = ref->hitPattern().trackerLayersWithMeasurement();
	  track_muonStaHits[2+tref+1][muIdx] = ref->hitPattern().muonStationsWithValidHits();
	  track_nVHits[     2+tref+1][muIdx] = ref->hitPattern().numberOfValidHits();
	  track_nVMuHits[   2+tref+1][muIdx] = ref->hitPattern().numberOfValidMuonHits();

	  track_matchedMuIdx[2+tref+1][muIdx] = muIdx;
	  track_nMatSta[2+tref+1][muIdx] = mu->numberOfMatchedStations();

	  if (ref->pt() > 50)
	    ++nTracksPt50[2+tref+1];
	  if (ref->pt() > 100)
	    ++nTracksPt100[2+tref+1];
	  if (ref->pt() > 200)
	    ++nTracksPt200[2+tref+1];
	  if (ref->pt() > 300)
	    ++nTracksPt300[2+tref+1];
	  if (ref->pt() > 400)
	    ++nTracksPt400[2+tref+1];
	  if (ref->pt() > 500)
	    ++nTracksPt500[2+tref+1];
	  if (ref->pt() > 750)
	    ++nTracksPt750[2+tref+1];
	  if (ref->pt() > 1000)
	    ++nTracksPt1000[2+tref+1];
	  if (ref->pt() > 1500)
	    ++nTracksPt1500[2+tref+1];
	}
      }
      ++muIdx;
    }  // end loop over muons
  }  // end check on muon collection size

  ////////////////// reco::Track information /////////////////////////
  if (debug_ > 0) {
    if (globalTrackColl->size() > 0) {
      std::cout	<< "found "     << nGlobalTracks  << " global "  << std::endl;
      std::cout << " global tracks: " << std::endl;
      for (auto track = globalTrackColl->begin(); track != globalTrackColl->end(); ++track)
	std::cout << "y:"
		  << std::setw(8) << track->innerPosition().Y()
		  << "/"
		  << std::setw(8) << track->outerPosition().Y()
		  << " pt:"           << std::setw(8) << track->pt()
		  << " eta:"          << std::setw(8) << track->eta()
		  << " phi:"          << std::setw(8) << track->phi()
		  << " chi2:"         << std::setw(8) << track->chi2()
		  << " dxy:"          << std::setw(8) << track->dxy()
		  << " dz:"           << std::setw(8) << track->dz()
		  << " nPixHits:"     << std::setw(2) << track->hitPattern().numberOfValidPixelHits()
		  << " nVTkHits:"     << std::setw(2) << track->hitPattern().numberOfValidTrackerHits()
		  << " nTkLayWMeas:"  << std::setw(2) << track->hitPattern().trackerLayersWithMeasurement()
		  << " nMuStaWVHits:" << std::setw(2) << track->hitPattern().muonStationsWithValidHits()
		  << " nVHits:"       << std::setw(2) << track->hitPattern().numberOfValidHits()
		  << " nVMuHits:"     << std::setw(2) << track->hitPattern().numberOfValidMuonHits()
		  << std::endl;
    }

    if (cosmicTrackColl->size() > 0) {
      std::cout << "found "     << nCosmicTracks  << " cosmic "  << std::endl;
      std::cout << " cosmic tracks: " << std::endl;
      for (auto track = cosmicTrackColl->begin(); track != cosmicTrackColl->end(); ++track)
	std::cout << "y:"
		  << std::setw(8) << track->innerPosition().Y()
		  << "/"
		  << std::setw(8) << track->outerPosition().Y()
		  << " pt:"           << std::setw(8) << track->pt()
		  << " eta:"          << std::setw(8) << track->eta()
		  << " phi:"          << std::setw(8) << track->phi()
		  << " chi2:"         << std::setw(8) << track->chi2()
		  << " dxy:"          << std::setw(8) << track->dxy()
		  << " dz:"           << std::setw(8) << track->dz()
		  << " nPixHits:"     << std::setw(2) << track->hitPattern().numberOfValidPixelHits()
		  << " nVTkHits:"     << std::setw(2) << track->hitPattern().numberOfValidTrackerHits()
		  << " nTkLayWMeas:"  << std::setw(2) << track->hitPattern().trackerLayersWithMeasurement()
		  << " nMuStaWVHits:" << std::setw(2) << track->hitPattern().muonStationsWithValidHits()
		  << " nVHits:"       << std::setw(2) << track->hitPattern().numberOfValidHits()
		  << " nVMuHits:"     << std::setw(2) << track->hitPattern().numberOfValidMuonHits()
		  << std::endl;
    }

    if (trackerTrackColl->size() > 0) {
      std::cout	<< "found "     << nTrackerTracks  << " tracker "  << std::endl;
      std::cout << " tracker tracks: " << std::endl;
      for (auto track = trackerTrackColl->begin(); track != trackerTrackColl->end(); ++track)
	std::cout << "y:"
		  << std::setw(8) << track->innerPosition().Y()
		  << "/"
		  << std::setw(8) << track->outerPosition().Y()
		  << " pt:"           << std::setw(8) << track->pt()
		  << " eta:"          << std::setw(8) << track->eta()
		  << " phi:"          << std::setw(8) << track->phi()
		  << " chi2:"         << std::setw(8) << track->chi2()
		  << " dxy:"          << std::setw(8) << track->dxy()
		  << " dz:"           << std::setw(8) << track->dz()
		  << " nPixHits:"     << std::setw(2) << track->hitPattern().numberOfValidPixelHits()
		  << " nVTkHits:"     << std::setw(2) << track->hitPattern().numberOfValidTrackerHits()
		  << " nTkLayWMeas:"  << std::setw(2) << track->hitPattern().trackerLayersWithMeasurement()
		  << " nMuStaWVHits:" << std::setw(2) << track->hitPattern().muonStationsWithValidHits()
		  << " nVHits:"       << std::setw(2) << track->hitPattern().numberOfValidHits()
		  << " nVMuHits:"     << std::setw(2) << track->hitPattern().numberOfValidMuonHits()
		  << std::endl;
    }
  }

  for (int tk = 0; tk < 3; ++tk) {
    int tkIdx = 0;
    if (debug_ > 2)
      std::cout << "looping over track collection " << tk << std::endl;
    for (auto trk = tracks[tk]->begin(); trk != tracks[tk]->end(); ++trk,++tkIdx) {
      track_isLower[   tk][tkIdx] = trk->outerPosition().Y() < 0;
      track_isUpper[   tk][tkIdx] = trk->outerPosition().Y() > 0;
      track_isLowerOld[tk][tkIdx] = fabs(trk->innerPosition().Y()) < fabs(trk->outerPosition().Y());
      track_isUpperOld[tk][tkIdx] = fabs(trk->innerPosition().Y()) > fabs(trk->outerPosition().Y());
      track_chi2[      tk][tkIdx] = trk->chi2();
      track_ndof[      tk][tkIdx] = trk->ndof();
      track_charge[    tk][tkIdx] = trk->charge();
      track_dxy[       tk][tkIdx] = trk->dxy();
      track_dz[        tk][tkIdx] = trk->dz();
      track_ptError[   tk][tkIdx] = trk->ptError();
      track_dxyError[  tk][tkIdx] = trk->dxyError();
      track_dzError[   tk][tkIdx] = trk->dzError();
      track_trackPt[   tk][tkIdx] = trk->pt();
      track_trackEta[  tk][tkIdx] = trk->eta();
      track_trackPhi[  tk][tkIdx] = trk->phi();
      track_innerY[    tk][tkIdx] = trk->innerPosition().Y();
      track_outerY[    tk][tkIdx] = trk->outerPosition().Y();

      track_firstPixel[ tk][tkIdx] = (trk->hitPattern().hasValidHitInFirstPixelBarrel() ||
				      trk->hitPattern().hasValidHitInFirstPixelEndcap());
      track_pixHits[    tk][tkIdx] = trk->hitPattern().numberOfValidPixelHits();
      track_tkHits[     tk][tkIdx] = trk->hitPattern().numberOfValidTrackerHits();
      track_tkLayWMeas[ tk][tkIdx] = trk->hitPattern().trackerLayersWithMeasurement();
      track_muonStaHits[tk][tkIdx] = trk->hitPattern().muonStationsWithValidHits();
      track_nVHits[     tk][tkIdx] = trk->hitPattern().numberOfValidHits();
      track_nVMuHits[   tk][tkIdx] = trk->hitPattern().numberOfValidMuonHits();

      if (trk->pt() > 50)
	++nTracksPt50[tk];
      if (trk->pt() > 100)
	++nTracksPt100[tk];
      if (trk->pt() > 200)
	++nTracksPt200[tk];
      if (trk->pt() > 300)
	++nTracksPt300[tk];
      if (trk->pt() > 400)
	++nTracksPt400[tk];
      if (trk->pt() > 500)
	++nTracksPt500[tk];
      if (trk->pt() > 750)
	++nTracksPt750[tk];
      if (trk->pt() > 1000)
	++nTracksPt1000[tk];
      if (trk->pt() > 1500)
	++nTracksPt1500[tk];

      // try to match to a muon, if found, take nMatchedMuonStations from here
      // insufficient to simply match deta/dphi, what about upper/lower splitting?
      // be able to know index so we can easily get the tuneP pT/dpT

      double bestDEta = maxDEta_;
      double bestDPhi = maxDPhi_;
      double bestDR   = maxDR_;
      int muIdx = 0;
      if (debug_ > 2)
	std::cout << "looking for matching muons to track " << tkIdx << std::endl;
      for (auto muon = muonColl->begin(); muon != muonColl->end(); ++muon) {
	double tmpDEta = fabs(muon->eta()-trk->eta());
	double tmpDPhi = fabs(reco::deltaPhi(muon->phi(),trk->phi()));
	double tmpDR   = reco::deltaR(*muon,*trk);

	//double tmpTrkInY  = trk->innerPosition().Y();
	//double tmpMuInY  = muon->tunePMuonBestTrack()->innerPosition().Y();

	double tmpTrkOutY = trk->outerPosition().Y();
	double tmpMuOutY = muon->tunePMuonBestTrack()->outerPosition().Y();

	bool yCompatible = false;
	if (tmpTrkOutY > 0 && tmpMuOutY > 0)
	  yCompatible = true;
	else if (tmpTrkOutY < 0 && tmpMuOutY < 0)
	  yCompatible = true;

	if (tmpDEta < bestDEta && tmpDPhi < bestDPhi) {
	  if (debug_ > 2)
	    std::cout << " deta = " << std::setw(6) << tmpDEta
		      << " dphi = " << std::setw(6) << tmpDPhi
		      << " y-outer (mu) = "  << std::setw(8) << muon->tunePMuonBestTrack()->outerPosition().Y()
		      << " y-outer (trk) = " << std::setw(8) << trk->outerPosition().Y()
		      << " (" << std::setw(2) << (yCompatible ? "" : "in") << "compatible)"
		      << std::endl;
	  if (yCompatible) {
	    bestDEta = tmpDEta;
	    bestDPhi = tmpDPhi;
	    if (tmpDR < bestDR)
	      bestDR   = tmpDR;
	    track_matchedMuIdx[tk][tkIdx] = muIdx;
	    //track_nMatSta[tk][tkIdx] = muon->numberOfMatchedStations(reco::Muon::SegmentAndTrackArbitration);
	    track_nMatSta[tk][tkIdx] = muon->numberOfMatchedStations();
	  }  // end check on y compatibility
	}  // end check on deta/dphi
	++muIdx;
      }
    }
    if (debug_ > 2)
      std::cout << std::endl;
  }// end loop over the different track collections

  if (debug_ > 3)
    std::cout << "Filling the tree" << std::endl;
  muonTree->Fill();
}


reco::TrackRef MuonTree::GetTrackType(int algoType, reco::Muon const* muon)
{

  if (debug_ > 3)
    std::cout << "Started finding track type!" << std::endl;

  reco::TrackRef ref;

  if      (algoType == 1) ref = muon->track();
  else if (algoType == 2) ref = muon->tpfmsTrack();
  else if (algoType == 3) ref = muon->dytTrack();
  else if (algoType == 4) ref = muon->pickyTrack();
  else if (algoType == 5) ref = muon->tunePMuonBestTrack();
  else                    ref = muon->track();

  if (debug_ > 3)
    std::cout << "Returning track ref " << ref.isNonnull() << std::endl;

  return ref;
}

// ------------ method called once each job just before starting event loop  ------------
void MuonTree::beginJob()
{
  edm::Service< TFileService > fs;

  muonTree = fs->make<TTree>( "MuonTree", "Muon variables" );

  muonTree->Branch("nMuons",     &nMuons,     "nMuons/I"    );
  muonTree->Branch("nUpperLegs", &nUpperLegs, "nUpperLegs/I");
  muonTree->Branch("nLowerLegs", &nLowerLegs, "nLowerLegs/I");

  muonTree->Branch("nGlobalTracks",  &nGlobalTracks,  "nGlobalTracks/I" );
  muonTree->Branch("nCosmicTracks",  &nCosmicTracks,  "nCosmicTracks/I" );
  muonTree->Branch("nTrackerTracks", &nTrackerTracks, "nTrackerTracks/I");

  muonTree->Branch("nSimTracks", &nSimTracks,  "nSimTracks/I");
  muonTree->Branch("nL1Muons",   &nL1Muons,    "nL1Muons/I");
  muonTree->Branch("nL1MuonsNew",&nL1MuonsNew, "nL1MuonsNew/I");

  muonTree->Branch("event", &event, "event/I");
  muonTree->Branch("run",   &run,   "run/I"  );
  muonTree->Branch("lumi",  &lumi,  "lumi/I" );

  // variables per simTrack ([nSimTracks] indexed)
  if (isGen_) {
    muonTree->Branch("simTrackpT",     simtrack_pt,     "simTrackpT[nSimTracks]/D" );
    muonTree->Branch("simTrackEta",    simtrack_eta,    "simTrackEta[nSimTracks]/D");
    muonTree->Branch("simTrackPhi",    simtrack_phi,    "simTrackPhi[nSimTracks]/D");
    muonTree->Branch("simTrackCharge", simtrack_charge, "simTrackCharge[nSimTracks]/I");
    muonTree->Branch("simTrackType",   simtrack_type,   "simTrackType[nSimTracks]/I");
  }

  // trigger information
  muonTree->Branch("l1SingleMu",     &l1SingleMu,     "l1SingleMu/I");
  muonTree->Branch("fakeL1SingleMu", &fakeL1SingleMu, "fakeL1SingleMu/I");
  // variables per L1Muon ([nL1Muons] indexed, (l1extra collection))
  muonTree->Branch("l1MuonpT",       l1muon_pt,       "l1MuonpT[nL1Muons]/D" );
  muonTree->Branch("l1MuonEta",      l1muon_eta,      "l1MuonEta[nL1Muons]/D");
  muonTree->Branch("l1MuonPhi",      l1muon_phi,      "l1MuonPhi[nL1Muons]/D");
  muonTree->Branch("l1MuonCharge",   l1muon_charge,   "l1MuonCharge[nL1Muons]/I");
  muonTree->Branch("l1MuonIsFwd",    l1muon_isFwd,    "l1MuonIsFwd[nL1Muons]/I" );
  muonTree->Branch("l1MuonIsRPC",    l1muon_isRPC,    "l1MuonIsRPC[nL1Muons]/I" );
  muonTree->Branch("l1MuonQuality",  l1muon_quality,  "l1MuonQuality[nL1Muons]/I" );
  muonTree->Branch("l1MuonDetector", l1muon_detector, "l1MuonDetector[nL1Muons]/I");
  muonTree->Branch("l1MuonBX",       l1muon_bx,       "l1MuonBX[nL1Muons]/I");
  muonTree->Branch("l1MuonIso",      l1muon_iso,      "l1MuonIso[nL1Muons]/I");
  muonTree->Branch("l1MuonMIP",      l1muon_mip,      "l1MuonMIP[nL1Muons]/I");
  muonTree->Branch("l1MuonRank",     l1muon_rank,     "l1MuonRank[nL1Muons]/I");
  muonTree->Branch("l1MuonIdxDTCSC", l1muon_idxdtcsc, "l1MuonIdxDTCSC[nL1Muons]/I");
  muonTree->Branch("l1MuonIdxRPC",   l1muon_idxrpc,   "l1MuonIdxRPC[nL1Muons]/I");

  // variables per L1Muonnew ([nL1Muonnews] indexed, (l1extra collection))
  muonTree->Branch("l1MuonNewpT",       l1muonnew_pt,       "l1MuonNewpT[nL1MuonsNew]/D" );
  muonTree->Branch("l1MuonNewEta",      l1muonnew_eta,      "l1MuonNewEta[nL1MuonsNew]/D");
  muonTree->Branch("l1MuonNewPhi",      l1muonnew_phi,      "l1MuonNewPhi[nL1MuonsNew]/D");
  muonTree->Branch("l1MuonNewCharge",   l1muonnew_charge,   "l1MuonNewCharge[nL1MuonsNew]/I");
  muonTree->Branch("l1MuonNewIsFwd",    l1muonnew_isFwd,    "l1MuonNewIsFwd[nL1MuonsNew]/I" );
  muonTree->Branch("l1MuonNewIsRPC",    l1muonnew_isRPC,    "l1MuonNewIsRPC[nL1MuonsNew]/I" );
  muonTree->Branch("l1MuonNewQuality",  l1muonnew_quality,  "l1MuonNewQuality[nL1MuonsNew]/I" );
  muonTree->Branch("l1MuonNewDetector", l1muonnew_detector, "l1MuonNewDetector[nL1MuonsNew]/I");
  muonTree->Branch("l1MuonNewBX",       l1muonnew_bx,       "l1MuonNewBX[nL1MuonsNew]/I");
  muonTree->Branch("l1MuonNewIso",      l1muonnew_iso,      "l1MuonNewIso[nL1MuonsNew]/I");
  muonTree->Branch("l1MuonNewMIP",      l1muonnew_mip,      "l1MuonNewMIP[nL1MuonsNew]/I");
  muonTree->Branch("l1MuonNewRank",     l1muonnew_rank,     "l1MuonNewRank[nL1MuonsNew]/I");
  muonTree->Branch("l1MuonNewIdxDTCSC", l1muonnew_idxdtcsc, "l1MuonNewIdxDTCSC[nL1MuonsNew]/I");
  muonTree->Branch("l1MuonNewIdxRPC",   l1muonnew_idxrpc,   "l1MuonNewIdxRPC[nL1MuonsNew]/I");
  // variables per muon ([nMuons] indexed)
  muonTree->Branch("globalpT",  muon_pT,  "globalpT[nMuons]/D" );
  muonTree->Branch("globalEta", muon_Eta, "globalEta[nMuons]/D");
  muonTree->Branch("globalPhi", muon_Phi, "globalPhi[nMuons]/D");
  muonTree->Branch("muonP4",    muonP4,   10000, 99            );

  muonTree->Branch("isGlobal",     muon_isGlobal,     "isGlobal[nMuons]/I"    );
  muonTree->Branch("isTracker",    muon_isTracker,    "isTracker[nMuons]/I"   );
  muonTree->Branch("isStandAlone", muon_isStandAlone, "isStandAlone[nMuons]/I");

  muonTree->Branch("hasGlobal",  muon_hasGlobal,   "hasGlobal[nMuons]/I");
  muonTree->Branch("hasInner",   muon_hasInner,    "hasInner[nMuons]/I" );
  muonTree->Branch("hasOuter",   muon_hasOuter,    "hasOuter[nMuons]/I" );

  muonTree->Branch("globalChi2", muon_global_chi2, "globalChi2[nMuons]/D");
  muonTree->Branch("innerChi2",  muon_inner_chi2,  "innerChi2[nMuons]/D" );
  muonTree->Branch("outerChi2",  muon_outer_chi2,  "outerChi2[nMuons]/D" );
  muonTree->Branch("globalNDF",  muon_global_ndof, "globalNDF[nMuons]/I");
  muonTree->Branch("innerNDF",   muon_inner_ndof,  "innerNDF[nMuons]/I" );
  muonTree->Branch("outerNDF",   muon_outer_ndof,  "outerNDF[nMuons]/I" );

  muonTree->Branch("isLower", muon_isLower, "isLower[nMuons]/I");
  muonTree->Branch("isUpper", muon_isUpper, "isUpper[nMuons]/I");
  muonTree->Branch("isLowerOld", muon_isLowerOld, "isLowerOld[nMuons]/I");
  muonTree->Branch("isUpperOld", muon_isUpperOld, "isUpperOld[nMuons]/I");

  muonTree->Branch("innerY", muon_innerY, "innerY[nMuons]/D");
  muonTree->Branch("outerY", muon_outerY, "outerY[nMuons]/D");
  muonTree->Branch("tpin",   muon_tpin,   "tpin[nMuons]/D"  );
  muonTree->Branch("tpout",  muon_tpout,  "tpout[nMuons]/D" );

  muonTree->Branch("trackpT",  muon_trackPt,  "trackpT[nMuons]/D" );
  muonTree->Branch("trackEta", muon_trackEta, "trackEta[nMuons]/D");
  muonTree->Branch("trackPhi", muon_trackPhi, "trackPhi[nMuons]/D");
  muonTree->Branch("trackVec", muon_trackVec, 10000, 99           );
  muonTree->Branch("chi2",     muon_chi2,     "chi2[nMuons]/D"    );
  muonTree->Branch("ndof",     muon_ndof,     "ndof[nMuons]/I"    );
  muonTree->Branch("charge",   muon_charge,   "charge[nMuons]/I"  );
  muonTree->Branch("dxy",      muon_dxy,      "dxy[nMuons]/D"     );
  muonTree->Branch("dz",       muon_dz,       "dz[nMuons]/D"      );
  muonTree->Branch("ptError",  muon_ptError,  "ptError[nMuons]/D" );
  muonTree->Branch("dxyError", muon_dxyError, "dxyError[nMuons]/D");
  muonTree->Branch("dzError",  muon_dzError,  "dzError[nMuons]/D" );

  muonTree->Branch("firstPixel",       muon_firstPixel,  "firstPixel[nMuons]/I"      );
  muonTree->Branch("pixelHits",        muon_pixHits,     "pixelHits[nMuons]/I"       );
  muonTree->Branch("trackerHits",      muon_tkHits,      "trackerHits[nMuons]/I"     );
  muonTree->Branch("muonStationHits",  muon_muonStaHits, "muonStationHits[nMuons]/I" );
  muonTree->Branch("nValidHits",       muon_nVHits,      "nValidHits[nMuons]/I"      );
  muonTree->Branch("nValidMuonHits",   muon_nVMuHits,    "nValidMuonHits[nMuons]/I"  );
  muonTree->Branch("nMatchedStations", muon_nMatSta,     "nMatchedStations[nMuons]/I");
  muonTree->Branch("tkLayersWMeas",    muon_tkLayWMeas,  "tkLayersWMeas[nMuons]/I"   );

  // variables per muon ([nTracks] indexed)
  muonTree->Branch("trk_innerY",    track_innerY, "trk_innerY[8][25]/D");
  muonTree->Branch("trk_outerY",    track_outerY, "trk_outerY[8][25]/D");
  muonTree->Branch("trk_tpin",      track_tpin,   "trk_tpin[8][25]/D"  );
  muonTree->Branch("trk_tpout",     track_tpout,  "trk_tpout[8][25]/D" );

  muonTree->Branch("trk_trackpT",   track_trackPt,   "trk_trackpT[8][25]/D" );
  muonTree->Branch("trk_trackEta",  track_trackEta,  "trk_trackEta[8][25]/D");
  muonTree->Branch("trk_trackPhi",  track_trackPhi,  "trk_trackPhi[8][25]/D");
  muonTree->Branch("trk_chi2",      track_chi2,      "trk_chi2[8][25]/D"    );
  muonTree->Branch("trk_isLower",   track_isLower,   "trk_isLower[8][25]/I" );
  muonTree->Branch("trk_isUpper",   track_isUpper,   "trk_isUpper[8][25]/I" );
  muonTree->Branch("trk_isLowerOld",track_isLowerOld,"trk_isLowerOld[8][25]/I" );
  muonTree->Branch("trk_isUpperOld",track_isUpperOld,"trk_isUpperOld[8][25]/I" );
  muonTree->Branch("trk_ndof",      track_ndof,      "trk_ndof[8][25]/I"    );
  muonTree->Branch("trk_charge",    track_charge,    "trk_charge[8][25]/I"  );
  muonTree->Branch("trk_dxy",       track_dxy,       "trk_dxy[8][25]/D"     );
  muonTree->Branch("trk_dz",        track_dz,        "trk_dz[8][25]/D"      );
  muonTree->Branch("trk_ptError",   track_ptError,   "trk_ptError[8][25]/D" );
  muonTree->Branch("trk_dxyError",  track_dxyError,  "trk_dxyError[8][25]/D");
  muonTree->Branch("trk_dzError",   track_dzError,   "trk_dzError[8][25]/D" );

  muonTree->Branch("trk_matchedMuIdx",   track_matchedMuIdx,   "trk_matchedMuIdx[8][25]/I"  );

  muonTree->Branch("trk_firstPixel",       track_firstPixel,  "trk_firstPixel[8][25]/I"      );
  muonTree->Branch("trk_pixelHits",        track_pixHits,     "trk_pixelHits[8][25]/I"       );
  muonTree->Branch("trk_trackerHits",      track_tkHits,      "trk_trackerHits[8][25]/I"     );
  muonTree->Branch("trk_muonStationHits",  track_muonStaHits, "trk_muonStationHits[8][25]/I" );
  muonTree->Branch("trk_nValidHits",       track_nVHits,      "trk_nValidHits[8][25]/I"      );
  muonTree->Branch("trk_nValidMuonHits",   track_nVMuHits,    "trk_nValidMuonHits[8][25]/I"  );
  muonTree->Branch("trk_nMatchedStations", track_nMatSta,     "trk_nMatchedStations[8][25]/I");
  muonTree->Branch("trk_tkLayersWMeas",    track_tkLayWMeas,  "trk_tkLayersWMeas[8][25]/I"   );

  // per luminosity block information
  perLumiTree = fs->make<TTree>( "LumiTree", "Per lumi block variables" );

  perLumiTree->Branch("nMuonsPt50",   &nMuonsPt50,   "nMuonsPt50/I"  );
  perLumiTree->Branch("nMuonsPt100",  &nMuonsPt100,  "nMuonsPt100/I" );
  perLumiTree->Branch("nMuonsPt200",  &nMuonsPt200,  "nMuonsPt200/I" );
  perLumiTree->Branch("nMuonsPt300",  &nMuonsPt300,  "nMuonsPt300/I" );
  perLumiTree->Branch("nMuonsPt400",  &nMuonsPt400,  "nMuonsPt400/I" );
  perLumiTree->Branch("nMuonsPt500",  &nMuonsPt500,  "nMuonsPt500/I" );
  perLumiTree->Branch("nMuonsPt750",  &nMuonsPt750,  "nMuonsPt750/I" );
  perLumiTree->Branch("nMuonsPt1000", &nMuonsPt1000, "nMuonsPt1000/I");
  perLumiTree->Branch("nMuonsPt1500", &nMuonsPt1500, "nMuonsPt1500/I");

  perLumiTree->Branch("nTracksPt50",   nTracksPt50,   "nTracksPt50[8]/I"  );
  perLumiTree->Branch("nTracksPt100",  nTracksPt100,  "nTracksPt100[8]/I" );
  perLumiTree->Branch("nTracksPt200",  nTracksPt200,  "nTracksPt200[8]/I" );
  perLumiTree->Branch("nTracksPt300",  nTracksPt300,  "nTracksPt300[8]/I" );
  perLumiTree->Branch("nTracksPt400",  nTracksPt400,  "nTracksPt400[8]/I" );
  perLumiTree->Branch("nTracksPt500",  nTracksPt500,  "nTracksPt500[8]/I" );
  perLumiTree->Branch("nTracksPt750",  nTracksPt750,  "nTracksPt750[8]/I" );
  perLumiTree->Branch("nTracksPt1000", nTracksPt1000, "nTracksPt1000[8]/I");
  perLumiTree->Branch("nTracksPt1500", nTracksPt1500, "nTracksPt1500[8]/I");
}



// ------------ method called once each job just after ending the event loop  ------------
void MuonTree::endJob()
{
}

// ------------ method called when starting to processes a run  ------------
/*
  void MuonTree::beginRun(edm::Run const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when ending the processing of a run  ------------
/*
  void MuonTree::endRun(edm::Run const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when starting to processes a luminosity block  ------------
void MuonTree::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
  if (debug_ > 1)
    std::cout << "Start luminosity block, resetting per lumi counters" << std::endl;

  nMuonsPt50   = 0;
  nMuonsPt100  = 0;
  nMuonsPt200  = 0;
  nMuonsPt300  = 0;
  nMuonsPt400  = 0;
  nMuonsPt500  = 0;
  nMuonsPt750  = 0;
  nMuonsPt1000 = 0;
  nMuonsPt1500 = 0;

  for (int tk = 0; tk < 8; ++tk) {
    nTracksPt50[tk]   = 0;
    nTracksPt100[tk]  = 0;
    nTracksPt200[tk]  = 0;
    nTracksPt300[tk]  = 0;
    nTracksPt400[tk]  = 0;
    nTracksPt500[tk]  = 0;
    nTracksPt750[tk]  = 0;
    nTracksPt1000[tk] = 0;
    nTracksPt1500[tk] = 0;
  }
}

// ------------ method called when ending the processing of a luminosity block  ------------
void MuonTree::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
  if (debug_ > 1) {
    std::cout << "End luminosity block " << lumi << std::endl;

    std::cout << "nMuonsPt50   " << nMuonsPt50   << " " << std::hex << &nMuonsPt50   << std::dec << std::endl;
    std::cout << "nMuonsPt100  " << nMuonsPt100  << " " << std::hex << &nMuonsPt100  << std::dec << std::endl;
    std::cout << "nMuonsPt200  " << nMuonsPt200  << " " << std::hex << &nMuonsPt200  << std::dec << std::endl;
    std::cout << "nMuonsPt300  " << nMuonsPt300  << " " << std::hex << &nMuonsPt300  << std::dec << std::endl;
    std::cout << "nMuonsPt400  " << nMuonsPt400  << " " << std::hex << &nMuonsPt400  << std::dec << std::endl;
    std::cout << "nMuonsPt500  " << nMuonsPt500  << " " << std::hex << &nMuonsPt500  << std::dec << std::endl;
    std::cout << "nMuonsPt750  " << nMuonsPt750  << " " << std::hex << &nMuonsPt750  << std::dec << std::endl;
    std::cout << "nMuonsPt1000 " << nMuonsPt1000 << " " << std::hex << &nMuonsPt1000 << std::dec << std::endl;
    std::cout << "nMuonsPt1500 " << nMuonsPt1500 << " " << std::hex << &nMuonsPt1500 << std::dec << std::endl;

    for (int tk = 0; tk < 8; ++tk) {
      std::cout << "nTracksPt50["   << tk << "] " << nTracksPt50[tk]   << " " << std::hex << nTracksPt50   << std::dec << std::endl;
      std::cout << "nTracksPt100["  << tk << "] " << nTracksPt100[tk]  << " " << std::hex << nTracksPt100  << std::dec << std::endl;
      std::cout << "nTracksPt200["  << tk << "] " << nTracksPt200[tk]  << " " << std::hex << nTracksPt200  << std::dec << std::endl;
      std::cout << "nTracksPt300["  << tk << "] " << nTracksPt300[tk]  << " " << std::hex << nTracksPt300  << std::dec << std::endl;
      std::cout << "nTracksPt400["  << tk << "] " << nTracksPt400[tk]  << " " << std::hex << nTracksPt400  << std::dec << std::endl;
      std::cout << "nTracksPt500["  << tk << "] " << nTracksPt500[tk]  << " " << std::hex << nTracksPt500  << std::dec << std::endl;
      std::cout << "nTracksPt750["  << tk << "] " << nTracksPt750[tk]  << " " << std::hex << nTracksPt750  << std::dec << std::endl;
      std::cout << "nTracksPt1000[" << tk << "] " << nTracksPt1000[tk] << " " << std::hex << nTracksPt1000 << std::dec << std::endl;
      std::cout << "nTracksPt1500[" << tk << "] " << nTracksPt1500[tk] << " " << std::hex << nTracksPt1500 << std::dec << std::endl;
    }

    std::cout << "filling perLumiTree "
	      << std::hex << perLumiTree << std::dec
	      << std::endl;
  }

  perLumiTree->Fill();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void MuonTree::fillDescriptions(edm::ConfigurationDescriptions& descriptions)
{
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


//define this as a plug-in
DEFINE_FWK_MODULE(MuonTree);
