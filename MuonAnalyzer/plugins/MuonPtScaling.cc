#include "WSUDiLeptons/MuonAnalyzer/interface/MuonPtScaling.h"
#include <iomanip>

// -*- C++ -*-
//
// Package:    WSUDiLeptons/MuonAnalyzer
// Class:      MuonPtScaling
//
/**\class MuonPtScaling MuonPtScaling.cc WSUDiLeptons/MuonAnalyzer/plugins/MuonPtScaling.cc

   Description: [one line class summary]

   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  Jared Sturdy
//         Created:  Wed, 25 Feb 2015 12:55:49 GMT
//
//




MuonPtScaling::MuonPtScaling(const edm::ParameterSet& pset)
{
  muonSrc_   = pset.getParameter<edm::InputTag>("muonSrc");
  muonToken_ = consumes<reco::MuonCollection>(muonSrc_);

  isGen_     = pset.getParameter<bool>("isGen");
  simTrackSrc_   = pset.getParameter<edm::InputTag>("simTrackSrc");

  if (isGen_) {
    simTrackToken_ = consumes<edm::SimTrackContainer>(simTrackSrc_);
  }

  debug_     = pset.getParameter<bool>("debug");
}


MuonPtScaling::~MuonPtScaling()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void MuonPtScaling::analyze(const edm::Event& ev, const edm::EventSetup& es)
{
  using namespace ROOT::Math;
  edm::Handle<reco::MuonCollection > muonColl;
  ev.getByToken(muonToken_,          muonColl);

  int event = (ev.id()).event();
  int run   = (ev.id()).run();
  int lumi  = ev.luminosityBlock();

  if ( muonColl->size() > 0) {
    if (debug_ && muonColl->size() > 1) {
      std::cout << "run/lumi/event " << run  << "/" << lumi << "/" << event << std::endl;
      std::cout << " muons: " << std::endl;
      for (auto muon = muonColl->begin(); muon != muonColl->end(); ++muon)
	std::cout << std::setw(5)
		  << *muon << " ("
		  << muon->isTrackerMuon()            << "t"
		  << "/"  << muon->isGlobalMuon()     << "g"
		  << "/"  << muon->isStandAloneMuon() << "sa"
		  << ") " << std::setw(10) << "y:"
		  << muon->tunePMuonBestTrack()->innerPosition().Y()
		  << "/"
		  << muon->tunePMuonBestTrack()->outerPosition().Y()
		  << " "  << std::setw(10) << "chi2:"  << muon->tunePMuonBestTrack()->chi2()
		  << " "  << std::setw(10) << "dxy:"   << muon->tunePMuonBestTrack()->dxy()
		  << " "  << std::setw(10) << "dz:"    << muon->tunePMuonBestTrack()->dz()
		  << " "  << std::setw(10) << "tpin:"  << muon->time().timeAtIpInOut
		  << " "  << std::setw(10) << "tpout:" << muon->time().timeAtIpOutIn
		  << std::endl;
    }

    int muIdx = 0;
    for (auto mu = muonColl->begin(); mu != muonColl->end(); ++ mu) {
      if (muIdx == 0) {
        leadingMuonP->Fill(mu->p());
        leadingMuonPt->Fill(mu->pt());
        leadingMuonEta->Fill(mu->eta());
        leadingMuonPhi->Fill(mu->phi());
        if (fabs(mu->eta()) < 0.9) {
          leadingMuonPEta09->Fill(mu->p());
          leadingMuonPtEta09->Fill(mu->pt());
          leadingMuonEtaEta09->Fill(mu->eta());
          leadingMuonPhiEta09->Fill(mu->phi());
        }
      }

      allMuonP->Fill(mu->p());
      allMuonPt->Fill(mu->pt());
      allMuonEta->Fill(mu->eta());
      allMuonPhi->Fill(mu->phi());
      if (fabs(mu->eta()) < 0.9) {
	allMuonPEta09->Fill(mu->p());
	allMuonPtEta09->Fill(mu->pt());
	allMuonEtaEta09->Fill(mu->eta());
	allMuonPhiEta09->Fill(mu->phi());
      }
      ++muIdx;
    } // end loop over muons
  } // end check on muon collection size

  if (isGen_) {
    edm::Handle<edm::SimTrackContainer > simTrackColl;
    ev.getByToken(simTrackToken_, simTrackColl);

    if (simTrackColl->size() > 0) {
      // if (debug_ > 0)
      //   std::cout << " simTracks: "   << std::endl;

      int simIdx = 0;
      for (auto simtrack = simTrackColl->begin(); simtrack != simTrackColl->end(); ++simtrack) {
	if (fabs(simtrack->type()) == 13) {  // only consider simtracks from muons

          // if (debug_ > 0) {
          //   std::cout << std::setw(5)
          //             << *simtrack << " ("
          //             << "/"  << simtrack->trackerSurfaceMomentum().pt()     << "g"
          //             << "/"  << simtrack->trackerSurfaceMomentum().eta() << "sa"
          //             << ") " << std::setw(10) << "y:"
          //             << std::endl;
          // }
          // std::cout << std::setw(5) << *simtrack << std::endl;
          if (simIdx == 0) {
            if (fabs(simtrack->type()) == 13) {  // only consider simtracks from muons
              leadingSimTrackP->Fill(simtrack->trackerSurfaceMomentum().P());
              leadingSimTrackPt->Fill(simtrack->trackerSurfaceMomentum().pt());
              leadingSimTrackEta->Fill(simtrack->trackerSurfaceMomentum().eta());
              leadingSimTrackPhi->Fill(simtrack->trackerSurfaceMomentum().phi());
              if (fabs(simtrack->trackerSurfaceMomentum().eta()) < 0.9) {
                leadingSimTrackPEta09->Fill(simtrack->trackerSurfaceMomentum().P());
                leadingSimTrackPtEta09->Fill(simtrack->trackerSurfaceMomentum().pt());
                leadingSimTrackEtaEta09->Fill(simtrack->trackerSurfaceMomentum().eta());
                leadingSimTrackPhiEta09->Fill(simtrack->trackerSurfaceMomentum().phi());
              }
            }
          }

          allSimTrackP->Fill(simtrack->trackerSurfaceMomentum().P());
          allSimTrackPt->Fill(simtrack->trackerSurfaceMomentum().pt());
          allSimTrackEta->Fill(simtrack->trackerSurfaceMomentum().eta());
          allSimTrackPhi->Fill(simtrack->trackerSurfaceMomentum().phi());
          if (fabs(simtrack->trackerSurfaceMomentum().eta()) < 0.9) {
            allSimTrackPEta09->Fill(simtrack->trackerSurfaceMomentum().P());
            allSimTrackPtEta09->Fill(simtrack->trackerSurfaceMomentum().pt());
            allSimTrackEtaEta09->Fill(simtrack->trackerSurfaceMomentum().eta());
            allSimTrackPhiEta09->Fill(simtrack->trackerSurfaceMomentum().phi());
          }
	  ++simIdx;
	}
      }
    }
  }
}


// ------------ method called once each job just before starting event loop  ------------
void MuonPtScaling::beginJob()
{
  edm::Service< TFileService > fs;
  allMuonPt          = fs->make<TH1D>( "allMuonPt",          "#mu p_{T}",         500, 0., 5000. );
  leadingMuonPt      = fs->make<TH1D>( "leadingMuonPt",      "leading #mu p_{T}", 500, 0., 5000. );
  allMuonPtEta09     = fs->make<TH1D>( "allMuonPtEta09",     "#mu p_{T}",         500, 0., 5000. );
  leadingMuonPtEta09 = fs->make<TH1D>( "leadingMuonPtEta09", "leading #mu p_{T}", 500, 0., 5000. );

  allMuonP          = fs->make<TH1D>( "allMuonP",          "#mu p",         500, 0., 5000. );
  leadingMuonP      = fs->make<TH1D>( "leadingMuonP",      "leading #mu p", 500, 0., 5000. );
  allMuonPEta09     = fs->make<TH1D>( "allMuonPEta09",     "#mu p",         500, 0., 5000. );
  leadingMuonPEta09 = fs->make<TH1D>( "leadingMuonPEta09", "leading #mu p", 500, 0., 5000. );

  allMuonEta          = fs->make<TH1D>( "allMuonEta",          "#mu #eta",         300, -2.6, 2.6 );
  leadingMuonEta      = fs->make<TH1D>( "leadingMuonEta",      "leading #mu #eta", 300, -2.6, 2.6 );
  allMuonEtaEta09     = fs->make<TH1D>( "allMuonEtaEta09",     "#mu #eta",         300, -2.6, 2.6 );
  leadingMuonEtaEta09 = fs->make<TH1D>( "leadingMuonEtaEta09", "leading #mu #eta", 300, -2.6, 2.6 );

  allMuonPhi          = fs->make<TH1D>( "allMuonPhi",          "#mu #phi",         300, -3.2, 3.2 );
  leadingMuonPhi      = fs->make<TH1D>( "leadingMuonPhi",      "leading #mu #phi", 300, -3.2, 3.2 );
  allMuonPhiEta09     = fs->make<TH1D>( "allMuonPhiEta09",     "#mu #phi",         300, -3.2, 3.2 );
  leadingMuonPhiEta09 = fs->make<TH1D>( "leadingMuonPhiEta09", "leading #mu #phi", 300, -3.2, 3.2 );

  // sim tracks
  allSimTrackPt          = fs->make<TH1D>( "allSimTrackPt",          "sim trk p_{T}",         500, 0., 5000. );
  leadingSimTrackPt      = fs->make<TH1D>( "leadingSimTrackPt",      "leading sim trk p_{T}", 500, 0., 5000. );
  allSimTrackPtEta09     = fs->make<TH1D>( "allSimTrackPtEta09",     "sim trk p_{T}",         500, 0., 5000. );
  leadingSimTrackPtEta09 = fs->make<TH1D>( "leadingSimTrackPtEta09", "leading sim trk p_{T}", 500, 0., 5000. );

  allSimTrackP          = fs->make<TH1D>( "allSimTrackP",          "sim trk p",         500, 0., 5000. );
  leadingSimTrackP      = fs->make<TH1D>( "leadingSimTrackP",      "leading sim trk p", 500, 0., 5000. );
  allSimTrackPEta09     = fs->make<TH1D>( "allSimTrackPEta09",     "sim trk p",         500, 0., 5000. );
  leadingSimTrackPEta09 = fs->make<TH1D>( "leadingSimTrackPEta09", "leading sim trk p", 500, 0., 5000. );

  allSimTrackEta          = fs->make<TH1D>( "allSimTrackEta",          "sim trk #eta",         300, -2.6, 2.6 );
  leadingSimTrackEta      = fs->make<TH1D>( "leadingSimTrackEta",      "leading sim trk #eta", 300, -2.6, 2.6 );
  allSimTrackEtaEta09     = fs->make<TH1D>( "allSimTrackEtaEta09",     "sim trk #eta",         300, -2.6, 2.6 );
  leadingSimTrackEtaEta09 = fs->make<TH1D>( "leadingSimTrackEtaEta09", "leading sim trk #eta", 300, -2.6, 2.6 );

  allSimTrackPhi          = fs->make<TH1D>( "allSimTrackPhi",          "sim trk #phi",         300, -3.2, 3.2 );
  leadingSimTrackPhi      = fs->make<TH1D>( "leadingSimTrackPhi",      "leading sim trk #phi", 300, -3.2, 3.2 );
  allSimTrackPhiEta09     = fs->make<TH1D>( "allSimTrackPhiEta09",     "sim trk #phi",         300, -3.2, 3.2 );
  leadingSimTrackPhiEta09 = fs->make<TH1D>( "leadingSimTrackPhiEta09", "leading sim trk #phi", 300, -3.2, 3.2 );
}



// ------------ method called once each job just after ending the event loop  ------------
void MuonPtScaling::endJob()
{
}


// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void MuonPtScaling::fillDescriptions(edm::ConfigurationDescriptions& descriptions)
{
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


//define this as a plug-in
DEFINE_FWK_MODULE(MuonPtScaling);
