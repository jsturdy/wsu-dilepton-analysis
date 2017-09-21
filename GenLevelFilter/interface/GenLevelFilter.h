#ifndef WSU_GENLEVELFILTER_H
#define WSU_GENLEVELFILTER_H

// -*- C++ -*-
//
// Package:    WSUDiLeptons/GenLevelFilter
// Class:      GenLevelFilter
//
/**\class GenLevelFilter GenLevelFilter.h WSUDiLeptons/GenLevelFilter/interface/GenLevelFilter.h

   Description: [one line class summary]

   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  Jared Sturdy
//         Created:  Fri, 15 Sep 2017 13:52:17 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

// TFile Service
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"
#include "TH1D.h"

//
// class declaration
//

class GenLevelFilter : public edm::stream::EDProducer<> {
public:
  explicit GenLevelFilter(const edm::ParameterSet&);
  ~GenLevelFilter();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginStream(edm::StreamID) override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  virtual void endStream() override;

  //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

  // ----------member data ---------------------------
  edm::InputTag  m_genParticleSource;
  edm::EDGetTokenT<reco::GenParticleCollection>  m_genParticleToken;

  TTree* m_genInfoTree;
  TH1D *h_diMuonMassPre, *h_diElectronMassPre;
  TH1D *h_diMuonMass, *h_diElectronMass;
  bool m_filter_pre, m_filter, m_debug, m_dielectron, m_dimuon;
  bool m_selection_pre, m_selection;

  int m_run, m_lumi, m_event;
  int m_nGenMu, m_nst1GenMu;
  int m_nGenEle, m_nst1GenEle;

  double m_minCut, m_maxCut, m_xsWeight;
  double m_invM_any_mu, m_invM_st1_mu;
  double m_invM_any_el, m_invM_st1_el;

  std::string m_sampleType;
};

#endif
