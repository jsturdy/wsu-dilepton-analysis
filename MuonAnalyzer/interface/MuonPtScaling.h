#ifndef WSUDILEPTONS_MUONPTSCALING_H
#define WSUDILEPTONS_MUONPTSCALING_H

// system include files
#include <memory>

// user include files
#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDAnalyzer.h>

#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>

#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/Candidate/interface/Candidate.h>
#include <DataFormats/MuonReco/interface/MuonCocktails.h>
#include <DataFormats/MuonReco/interface/MuonFwd.h>
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Vector3D.h"

//sim track information
#include "SimDataFormats/Track/interface/SimTrack.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"

// TFile Service
#include <FWCore/ServiceRegistry/interface/Service.h>
#include <CommonTools/UtilAlgos/interface/TFileService.h>
#include <TH1.h>
#include "TROOT.h"
#include "TFile.h"


//
// class declaration
//

class MuonPtScaling : public edm::EDAnalyzer {

 public:
  explicit MuonPtScaling(const edm::ParameterSet&);
  ~MuonPtScaling();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


 private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  // ----------member data ---------------------------
  edm::EDGetTokenT<reco::MuonCollection > muonToken_;
  edm::EDGetTokenT<edm::SimTrackContainer> simTrackToken_;
  edm::InputTag muonSrc_, simTrackSrc_;

  bool debug_;
  bool isGen_;

  edm::Service<TFileService> fs;

  TH1D *allMuonPt, *leadingMuonPt,
    *allMuonP, *leadingMuonP,
    *allMuonEta, *leadingMuonEta,
    *allMuonPhi, *leadingMuonPhi,
    *allMuonPEta09, *leadingMuonPEta09,
    *allMuonPtEta09, *leadingMuonPtEta09,
    *allMuonEtaEta09, *leadingMuonEtaEta09,
    *allMuonPhiEta09, *leadingMuonPhiEta09;

  TH1D *allSimTrackPt, *leadingSimTrackPt,
    *allSimTrackP, *leadingSimTrackP,
    *allSimTrackEta, *leadingSimTrackEta,
    *allSimTrackPhi, *leadingSimTrackPhi,
    *allSimTrackPEta09, *leadingSimTrackPEta09,
    *allSimTrackPtEta09, *leadingSimTrackPtEta09,
    *allSimTrackEtaEta09, *leadingSimTrackEtaEta09,
    *allSimTrackPhiEta09, *leadingSimTrackPhiEta09;
};

#endif
