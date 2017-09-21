// user include files
#include "WSUDiLeptons/GenLevelFilter/interface/GenLevelFilter.h"

GenLevelFilter::GenLevelFilter(const edm::ParameterSet& pset):
  m_filter_pre(false),
  m_filter(false),
  m_debug(false),
  m_dielectron(false),
  m_dimuon(false),
  m_selection_pre(false),
  m_selection(false),
  m_run(-1),
  m_lumi(-1),
  m_event(-1),
  m_nGenMu(-1),
  m_nst1GenMu(-1),
  m_nGenEle(-1),
  m_nst1GenEle(-1),
  m_minCut(-1),
  m_maxCut(1e10),
  m_xsWeight(-1.),
  m_invM_any_mu(-1.),
  m_invM_st1_mu(-1.),
  m_invM_any_el(-1.),
  m_invM_st1_el(-1.),
  m_sampleType("")
{
   //now do what ever initialization is needed
  m_genParticleSource = pset.getParameter<edm::InputTag>("genParticleSource");
  m_filter            = pset.getParameter<bool>(  "filterevent");
  m_filter_pre        = pset.getParameter<bool>(  "filterPreFSR");
  m_debug             = pset.getParameter<bool>(  "debug");
  m_minCut            = pset.getParameter<double>("minCut");
  m_maxCut            = pset.getParameter<double>("maxCut");
  m_xsWeight          = pset.getParameter<double>("xsWeight");
  m_sampleType        = pset.getParameter<std::string>("sampleType");

  m_genParticleToken = consumes<reco::GenParticleCollection, edm::InEvent>(m_genParticleSource);

  if (m_debug) {
    //now do what ever initialization is needed
    // usesResource("TFileService");

    edm::Service< TFileService > fs;

    h_diMuonMass        = fs->make<TH1D>("diMuonMass",        "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diElectronMass    = fs->make<TH1D>("diElectronMass",    "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diMuonMassPre     = fs->make<TH1D>("diMuonMassPre",     "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diElectronMassPre = fs->make<TH1D>("diElectronMassPre", "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);

    h_diMuonMass->Sumw2();
    h_diElectronMass->Sumw2();
    h_diMuonMassPre->Sumw2();
    h_diElectronMassPre->Sumw2();

    m_genInfoTree = fs->make<TTree>("genInfoTree", "GEN level info for weights and filtering");

    m_genInfoTree->Branch("run",   &m_run,   "run/I"  );
    m_genInfoTree->Branch("lumi",  &m_lumi,  "lumi/I" );
    m_genInfoTree->Branch("event", &m_event, "event/I");

    m_genInfoTree->Branch("sampleType",  &m_sampleType, "sampleType/C");

    m_genInfoTree->Branch("nGenMu",      &m_nGenMu,      "nGenMu/I" );
    m_genInfoTree->Branch("nst1GenMu",   &m_nst1GenMu,   "nst1GenMu/I" );
    m_genInfoTree->Branch("invM_any_mu", &m_invM_any_mu, "invM_any_mu/D");
    m_genInfoTree->Branch("invM_st1_mu", &m_invM_st1_mu, "invM_st1_mu/D");

    m_genInfoTree->Branch("nGenEle",     &m_nGenEle,     "nGenEle/I" );
    m_genInfoTree->Branch("nst1GenEle",  &m_nst1GenEle,  "nst1GenEle/I" );
    m_genInfoTree->Branch("invM_any_el", &m_invM_any_el, "invM_any_el/D");
    m_genInfoTree->Branch("invM_st1_el", &m_invM_st1_el, "invM_st1_el/D");

    m_genInfoTree->Branch("selection_pre", &m_selection_pre, "selection_pre/O" );
    m_genInfoTree->Branch("selection",     &m_selection,     "selection/O"     );
    m_genInfoTree->Branch("dimuon",        &m_dimuon,        "dimuon/O"     );
    m_genInfoTree->Branch("dielectron",    &m_dielectron,    "dielectron/O" );
  }
  
  if (m_sampleType.rfind("2Mu") != std::string::npos)
    m_dimuon = true;
  else if (m_sampleType.rfind("2E") != std::string::npos)
    m_dielectron = true;

  std::cout << "Running gen filtering with :"   << std::endl
            << "filter: "      << m_filter      << std::endl
            << "filterPre: "   << m_filter_pre  << std::endl
            << "minCut: "      << m_minCut      << std::endl
            << "maxCut: "      << m_maxCut      << std::endl
            << "xsWeight: "    << m_xsWeight    << std::endl
            << "sampleType: "  << m_sampleType  << std::endl
            << "dimuon: "      << m_dimuon      << std::endl
            << "dielectron: "  << m_dielectron  << std::endl;

  produces<bool>("passPreFSRMassCut");
  produces<bool>("passMassCut");
  produces<double>("xsWeight");
}


GenLevelFilter::~GenLevelFilter()
{

   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool GenLevelFilter::filter(edm::Event& ev, const edm::EventSetup& es)
{
  edm::Handle<reco::GenParticleCollection> genParticles;
  ev.getByToken(m_genParticleToken, genParticles);

  m_selection     = false;
  m_selection_pre = false;

  ////////////////// Generic event information /////////////////////////
  m_run   = (ev.id()).run();
  m_lumi  = ev.luminosityBlock();
  m_event = (ev.id()).event();

  if (genParticles.isValid()) {
    // find the particle to cut on
    std::vector<const reco::GenParticle*> genMuons;
    std::vector<const reco::GenParticle*> genElectrons;
    std::vector<const reco::GenParticle*> st1Muons;
    std::vector<const reco::GenParticle*> st1Electrons;

    // if (m_debug)
    //   std::cout << "genParticles->size(): " << genParticles->size() << std::endl;
    for (auto gpart = genParticles->begin(); gpart != genParticles->end(); ++gpart) {
      // for (auto gpart : genParticles.product()) {
      // if (m_debug)
      //   std::cout << "id: "            << gpart->pdgId()
      //             << ", status: "      << gpart->status()
      //             << ", pt: "          << gpart->pt()
      //             << ", m:  "          << gpart->mass()
      //             << ", isLastCopy:  " << gpart->isLastCopy()
      //             << std::endl;
      if (!gpart->isLastCopy()) {
        if (abs(gpart->pdgId()) == 11)
          genElectrons.push_back(&(*gpart));
        else if (abs(gpart->pdgId()) == 13)
          genMuons.push_back(&(*gpart));
      } else {
        if (abs(gpart->pdgId()) == 11)
          st1Electrons.push_back(&(*gpart));
        else if (abs(gpart->pdgId()) == 13)
          st1Muons.push_back(&(*gpart));
      }
    }

    // create dilepton object
    // histogram mass
    // Status 1/final electrons
    m_nst1GenEle = st1Electrons.size();
    if (m_nst1GenEle >= 2) {
      double mass = (st1Electrons.at(0)->p4()+st1Electrons.at(1)->p4()).M();
      // if (m_debug)
      //   std::cout << "Found dielectron candidate m = " << mass << std::endl;
      if (m_dielectron) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            std::cout << "Found dielectron candidate outside expected window m = " << mass << std::endl;
        } else {
          m_selection = true;
        }
      }
      m_invM_st1_el = mass;
      if (m_debug)
        h_diElectronMass->Fill(mass);
    } else if (m_dielectron && m_debug) {
      std::cout << "Found fewer than 2 status 1 final electrons: "
                << st1Electrons.size() << std::endl;
      for (auto el : st1Electrons)
        std::cout << "id: "            << el->pdgId()
                  << ", status: "      << el->status()
                  << ", pt: "          << el->pt()
                  << ", m:  "          << el->mass()
                  << ", isLastCopy:  " << el->isLastCopy()
                  << std::endl;
    }

    // Status 1/final muons
    m_nst1GenMu = st1Muons.size();
    if (st1Muons.size() >= 2) {
      double mass = (st1Muons.at(0)->p4()+st1Muons.at(1)->p4()).M();
      if (m_dimuon) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            std::cout << "Found dimuon candidate outside expected window m = " << mass << std::endl;
        } else {
          m_selection = true;
        }
      }
      m_invM_st1_mu = mass;
      if (m_debug)
        h_diMuonMass->Fill(mass);
    } else if (m_dimuon && m_debug) {
      std::cout << "Found fewer than 2 status 1 final muons: "
                << st1Muons.size() << std::endl;
      for (auto mu : st1Muons)
        std::cout << "id: "            << mu->pdgId()
                  << ", status: "      << mu->status()
                  << ", pt: "          << mu->pt()
                  << ", m:  "          << mu->mass()
                  << ", isLastCopy:  " << mu->isLastCopy()
                  << std::endl;
    }

    // Any status electrons
    m_nGenEle = genElectrons.size();
    if (genElectrons.size() >= 2) {
      double mass = (genElectrons.at(0)->p4()+genElectrons.at(1)->p4()).M();
      if (m_dielectron) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            std::cout << "Found dielectron candidate outside expected window m = " << mass << std::endl;
        } else {
          m_selection_pre = true;
        }
      }
      m_invM_any_el = mass;
      if (m_debug)
        h_diElectronMassPre->Fill(mass);
    }

    // Any status muons
    m_nGenEle = genMuons.size();
    if (genMuons.size() >= 2) {
      double mass = (genMuons.at(0)->p4()+genMuons.at(1)->p4()).M();
      if (m_dimuon) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            std::cout << "Found dimuon candidate outside expected window m = " << mass << std::endl;
        } else {
          m_selection_pre = true;
        }
      }
      m_invM_any_mu = mass;
      if (m_debug)
        h_diMuonMassPre->Fill(mass);
    }

    if (m_debug)
      m_genInfoTree->Fill();
  } else {
    std::cout << "genParticles is not valid!" << std::endl;
  }

   std::unique_ptr<bool> fOut0(new bool(m_selection_pre));
   ev.put(std::move(fOut0),"passPreFSRMassCut");

   std::unique_ptr<bool> fOut1(new bool(m_selection));
   ev.put(std::move(fOut1),"passMassCut");

   std::unique_ptr<double> wOut(new double(m_xsWeight));
   ev.put(std::move(wOut),"xsWeight");

   if (m_filter) {
     if (m_filter_pre)
       return m_selection_pre;
     else
       return m_selection;
   } else {
    return true;
   }
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void GenLevelFilter::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void GenLevelFilter::endStream()
{
}

// ------------ method called when starting to processes a run  ------------
/*
void GenLevelFilter::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void GenLevelFilter::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void GenLevelFilter::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void GenLevelFilter::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void GenLevelFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions)
{
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(GenLevelFilter);
