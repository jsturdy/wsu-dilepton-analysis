// user include files
#include "WSUDiLeptons/GenLevelFilter/interface/GenLevelFilter.h"

GenLevelFilter::GenLevelFilter(const edm::ParameterSet& pset):
  m_filter_pre(false),
  m_filter_st1(false),
  m_filter_st23(false),
  m_filter_hs(false),
  m_filter(false),
  m_debug(false),
  m_dielectron(false),
  m_dimuon(false),
  m_selection_pre(false),
  m_selection_st1(false),
  m_selection_st23(false),
  m_selection_hs(false),
  m_selection(false),
  m_run(-1),
  m_lumi(-1),
  m_event(-1),
  m_nGenMu(-1),
  m_nst1GenMu(-1),
  m_nst23GenMu(-1),
  m_nhsGenMu(-1),
  m_nGenEle(-1),
  m_nst1GenEle(-1),
  m_nst23GenEle(-1),
  m_nhsGenEle(-1),
  m_minCut(-1),
  m_maxCut(1e10),
  m_xsWeight(-1.),
  m_invM_any_mu(-1.),
  m_invM_st1_mu(-1.),
  m_invM_st23_mu(-1.),
  m_invM_hs_mu(-1.),
  m_invM_any_el(-1.),
  m_invM_st1_el(-1.),
  m_invM_st23_el(-1.),
  m_invM_hs_el(-1.),
  m_sampleType("")
{
  //now do what ever initialization is needed
  m_genParticleSource = pset.getParameter<edm::InputTag>("genParticleSource");
  m_filter            = pset.getParameter<bool>(  "filterevent");
  m_filter_pre        = pset.getParameter<bool>(  "filterPreFSR");
  m_filter_st1        = pset.getParameter<bool>(  "filterST1");
  m_filter_st23       = pset.getParameter<bool>(  "filterST23");
  m_filter_hs         = pset.getParameter<bool>(  "filterHS");
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

    TH1::SetDefaultSumw2();
    h_diMuonMass         = fs->make<TH1D>("diMuonMass",         "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diElectronMass     = fs->make<TH1D>("diElectronMass",     "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diMuonMassPre      = fs->make<TH1D>("diMuonMassPre",      "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diElectronMassPre  = fs->make<TH1D>("diElectronMassPre",  "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diMuonMassST1      = fs->make<TH1D>("diMuonMassST1",      "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diElectronMassST1  = fs->make<TH1D>("diElectronMassST1",  "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diMuonMassST23     = fs->make<TH1D>("diMuonMassST23",     "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diElectronMassST23 = fs->make<TH1D>("diElectronMassST23", "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diMuonMassHS       = fs->make<TH1D>("diMuonMassHS",       "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);
    h_diElectronMassHS   = fs->make<TH1D>("diElectronMassHS",   "M_{#mu^{+}#mu^{-}}^{inv}", 1000, 0., 5000.);

    m_genInfoTree = fs->make<TTree>("genInfoTree", "GEN level info for weights and filtering");

    m_genInfoTree->Branch("run",   &m_run,   "run/I"  );
    m_genInfoTree->Branch("lumi",  &m_lumi,  "lumi/I" );
    m_genInfoTree->Branch("event", &m_event, "event/I");

    m_genInfoTree->Branch("sampleType",  &m_sampleType, "sampleType/C");

    m_genInfoTree->Branch("nGenMu",       &m_nGenMu,       "nGenMu/I" );
    m_genInfoTree->Branch("nst1GenMu",    &m_nst1GenMu,    "nst1GenMu/I" );
    m_genInfoTree->Branch("nst23GenMu",   &m_nst23GenMu,   "nst23GenMu/I" );
    m_genInfoTree->Branch("nhsGenMu",     &m_nhsGenMu,     "nhsGenMu/I" );
    m_genInfoTree->Branch("invM_any_mu",  &m_invM_any_mu,  "invM_any_mu/D");
    m_genInfoTree->Branch("invM_st1_mu",  &m_invM_st1_mu,  "invM_st1_mu/D");
    m_genInfoTree->Branch("invM_st23_mu", &m_invM_st23_mu, "invM_st23_mu/D");
    m_genInfoTree->Branch("invM_hs_mu",   &m_invM_hs_mu,   "invM_hs_mu/D");

    m_genInfoTree->Branch("nGenEle",       &m_nGenEle,       "nGenEle/I" );
    m_genInfoTree->Branch("nst1GenEle",    &m_nst1GenEle,    "nst1GenEle/I" );
    m_genInfoTree->Branch("nst23GenEle",   &m_nst23GenEle,   "nst23GenEle/I" );
    m_genInfoTree->Branch("nhsGenEle",     &m_nhsGenEle,     "nhsGenEle/I" );
    m_genInfoTree->Branch("invM_any_el",  &m_invM_any_el,  "invM_any_el/D");
    m_genInfoTree->Branch("invM_st1_el",  &m_invM_st1_el,  "invM_st1_el/D");
    m_genInfoTree->Branch("invM_st23_el", &m_invM_st23_el, "invM_st23_el/D");
    m_genInfoTree->Branch("invM_hs_el",   &m_invM_hs_el,   "invM_hs_el/D");

    m_genInfoTree->Branch("selection_pre",  &m_selection_pre,  "selection_pre/O" );
    m_genInfoTree->Branch("selection_st1",  &m_selection_st1,  "selection_st1/O" );
    m_genInfoTree->Branch("selection_st23", &m_selection_st23, "selection_st23/O");
    m_genInfoTree->Branch("selection_hs",   &m_selection_hs,   "selection_hs/O"  );
    m_genInfoTree->Branch("selection",      &m_selection,      "selection/O"     );
    m_genInfoTree->Branch("dimuon",         &m_dimuon,         "dimuon/O"        );
    m_genInfoTree->Branch("dielectron",     &m_dielectron,     "dielectron/O"    );
  }

  if (m_sampleType.rfind("2Mu") != std::string::npos)
    m_dimuon = true;
  else if (m_sampleType.rfind("2E") != std::string::npos)
    m_dielectron = true;

  std::cout << "Running gen filtering with :"   << std::endl
            << "filter: "      << m_filter      << std::endl
            << "filterPre: "   << m_filter_pre  << std::endl
            << "filterST1: "   << m_filter_st1  << std::endl
            << "filterST23: "  << m_filter_st23 << std::endl
            << "filterHS: "    << m_filter_hs   << std::endl
            << "minCut: "      << m_minCut      << std::endl
            << "maxCut: "      << m_maxCut      << std::endl
            << "xsWeight: "    << m_xsWeight    << std::endl
            << "sampleType: "  << m_sampleType  << std::endl
            << "dimuon: "      << m_dimuon      << std::endl
            << "dielectron: "  << m_dielectron  << std::endl;

  produces<bool>("passPreFSRMassCut");
  produces<bool>("passST1MassCut");
  produces<bool>("passST23MassCut");
  produces<bool>("passHSMassCut");
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

  m_selection      = false;
  m_selection_pre  = false;
  m_selection_st1  = false;
  m_selection_st23 = false;
  m_selection_hs   = false;

  ////////////////// Generic event information /////////////////////////
  m_run   = (ev.id()).run();
  m_lumi  = ev.luminosityBlock();
  m_event = (ev.id()).event();

  if (genParticles.isValid()) {
    // find the particle to cut on
    std::vector<const reco::GenParticle*> genZs;
    std::vector<const reco::GenParticle*> genMuons;
    std::vector<const reco::GenParticle*> genElectrons;
    std::vector<const reco::GenParticle*> hsMuons;
    std::vector<const reco::GenParticle*> hsElectrons;
    std::vector<const reco::GenParticle*> st1Muons;
    std::vector<const reco::GenParticle*> st1Electrons;
    std::vector<const reco::GenParticle*> st23Muons;
    std::vector<const reco::GenParticle*> st23Electrons;

    // if (m_debug)
    //   std::cout << "genParticles->size(): " << genParticles->size() << std::endl;
    for (auto gpart = genParticles->begin(); gpart != genParticles->end(); ++gpart) {
      // for (auto gpart : genParticles.product()) {
      if (m_debug)
        if ((abs(gpart->pdgId()) == 11) || (abs(gpart->pdgId()) == 13) || (abs(gpart->pdgId()) == 23)) {
          std::cout << "id: "            << gpart->pdgId()
                    << ", status: "      << gpart->status()
                    << ", pt: "          << gpart->pt()
                    << ", m:  "          << gpart->mass()
                    << ", isLastCopy:  " << gpart->isLastCopy();
          std::cout << std::endl;
          std::cout << " - nMothers:  "   << gpart->numberOfMothers()<< std::endl;
          for (size_t mom = 0; mom < gpart->numberOfMothers(); ++mom)
            std::cout << "  - id: "            << gpart->mother(mom)->pdgId()
                      << ", status: "      << gpart->mother(mom)->status()
                      << ", pt: "          << gpart->mother(mom)->pt()
                      << ", m:  "          << gpart->mother(mom)->mass()
                      << std::endl;

          std::cout << " - nDaughters:  " << gpart->numberOfDaughters()<< std::endl;
          for (size_t dau = 0; dau < gpart->numberOfDaughters(); ++dau)
            std::cout << "  - id: "            << gpart->daughter(dau)->pdgId()
                      << ", status: "      << gpart->daughter(dau)->status()
                      << ", pt: "          << gpart->daughter(dau)->pt()
                      << ", m:  "          << gpart->daughter(dau)->mass()
                      << std::endl;
          std::cout << std::endl;
        }

      if (abs(gpart->pdgId()) == 23)
        genZs.push_back(&(*gpart));

      // keep last copy and status 1, or not last copy and status 23 as "good"
      if (gpart->pt() > 10.) {  // what makes sense here?
        if (abs(gpart->pdgId()) == 11) {
          genElectrons.push_back(&(*gpart));
          if (abs(gpart->status()) == 23)
            st23Electrons.push_back(&(*gpart));
          else if (abs(gpart->status()) == 1)
            st1Electrons.push_back(&(*gpart));
        } else if (abs(gpart->pdgId()) == 13) {
          genMuons.push_back(&(*gpart));
          if (abs(gpart->status()) == 23)
            st23Muons.push_back(&(*gpart));
          else if (abs(gpart->status()) == 1)
            st1Muons.push_back(&(*gpart));
        }
      }

      // is the parentof the particle we want to cut on always a Z? even for CI?
      if (gpart->pt() > 10. && // what makes sense here?
          ((!gpart->isLastCopy() && gpart->status() == 23) ||
           (gpart->isLastCopy() && gpart->status() == 1))
          ) {
        if (abs(gpart->pdgId()) == 11) {
          hsElectrons.push_back(&(*gpart));
        } else if (abs(gpart->pdgId()) == 13) {
          hsMuons.push_back(&(*gpart));
        }
      }
    }

    if (m_debug) {
      std::cout << "Found " << genZs.size()  << " Z candidates"  << std::endl;
      std::cout << "Found " << st1Electrons.size()  << " status 1 electron candidates"  << std::endl
                << "Found " << st23Electrons.size() << " status 23 electron candidates" << std::endl
                << "Found " << hsElectrons.size()   << " HS electron candidates"        << std::endl
                << "Found " << genElectrons.size()  << " total electron candidates"     << std::endl;
      std::cout << "Found " << st1Muons.size()  << " status 1 muon candidates"  << std::endl
                << "Found " << st23Muons.size() << " status 23 muon candidates" << std::endl
                << "Found " << hsMuons.size()   << " HS muon candidates"        << std::endl
                << "Found " << genMuons.size()  << " total muon candidates"     << std::endl;
    }

    // create dilepton object
    // histogram mass
    // Status 1/final electrons
    m_nst1GenEle = st1Electrons.size();
    if (m_nst1GenEle >= 2) {
      double mass = (st1Electrons.at(0)->p4()+st1Electrons.at(1)->p4()).M();
      if (m_dielectron) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            if (m_filter_st1)
              std::cout << "Found dielectron candidate outside expected window m (st1) = " << mass << std::endl
                        << st1Electrons.at(0)->pdgId()
                        << " " << st1Electrons.at(0)->status()
                        << " " << st1Electrons.at(0)->isLastCopy() << std::endl
                        << st1Electrons.at(1)->pdgId()
                        << " " << st1Electrons.at(1)->status()
                        << " " << st1Electrons.at(1)->isLastCopy()
                        << std::endl;
        } else {
          m_selection_st1 = true;
        }
      }
      m_invM_st1_el = mass;
      if (m_debug)
        h_diElectronMassST1->Fill(mass);
    } else if (m_dielectron && m_debug) {
      std::cout << "Found fewer than 2 status 1 final state electrons: "
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
            if (m_filter_st1)
              std::cout << "Found dimuon candidate outside expected window m (st1) = " << mass << std::endl
                        << st1Muons.at(0)->pdgId()
                        << " " << st1Muons.at(0)->status()
                        << " " << st1Muons.at(0)->isLastCopy() << std::endl
                        << st1Muons.at(1)->pdgId()
                        << " " << st1Muons.at(1)->status()
                        << " " << st1Muons.at(1)->isLastCopy()
                        << std::endl;
        } else {
          m_selection_st1 = true;
        }
      }
      m_invM_st1_mu = mass;
      if (m_debug)
        h_diMuonMassST1->Fill(mass);
    } else if (m_dimuon && m_debug) {
      std::cout << "Found fewer than 2 status 1 final state muons: "
                << st1Muons.size() << std::endl;
      for (auto mu : st1Muons)
        std::cout << "id: "            << mu->pdgId()
                  << ", status: "      << mu->status()
                  << ", pt: "          << mu->pt()
                  << ", m:  "          << mu->mass()
                  << ", isLastCopy:  " << mu->isLastCopy()
                  << std::endl;
    }

    // hard process electrons
    // Status 23 electrons
    m_nst23GenEle = st23Electrons.size();
    if (m_nst23GenEle >= 2) {
      double mass = (st23Electrons.at(0)->p4()+st23Electrons.at(1)->p4()).M();
      if (m_dielectron) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            if (m_filter_st23)
              std::cout << "Found dielectron candidate outside expected window m (st23) = " << mass << std::endl
                        << st23Electrons.at(0)->pdgId()
                        << " " << st23Electrons.at(0)->status()
                        << " " << st23Electrons.at(0)->isLastCopy() << std::endl
                        << st23Electrons.at(1)->pdgId()
                        << " " << st23Electrons.at(1)->status()
                        << " " << st23Electrons.at(1)->isLastCopy()
                        << std::endl;
        } else {
          m_selection_st23 = true;
        }
      }
      m_invM_st23_el = mass;
      if (m_debug)
        h_diElectronMassST23->Fill(mass);
    } else if (m_dielectron && m_debug) {
      std::cout << "Found fewer than 2 status 23 electrons: "
                << st23Electrons.size() << std::endl;
      for (auto el : st23Electrons)
        std::cout << "id: "            << el->pdgId()
                  << ", status: "      << el->status()
                  << ", pt: "          << el->pt()
                  << ", m:  "          << el->mass()
                  << ", isLastCopy:  " << el->isLastCopy()
                  << std::endl;
    }

    // Status 23 muons
    m_nst23GenMu = st23Muons.size();
    if (st23Muons.size() >= 2) {
      double mass = (st23Muons.at(0)->p4()+st23Muons.at(1)->p4()).M();
      if (m_dimuon) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            if (m_filter_st23)
              std::cout << "Found dimuon candidate outside expected window m (st23) = " << mass << std::endl
                        << st23Muons.at(0)->pdgId()
                        << " " << st23Muons.at(0)->status()
                        << " " << st23Muons.at(0)->isLastCopy() << std::endl
                        << st23Muons.at(1)->pdgId()
                        << " " << st23Muons.at(1)->status()
                        << " " << st23Muons.at(1)->isLastCopy()
                        << std::endl;
        } else {
          m_selection_st23 = true;
        }
      }
      m_invM_st23_mu = mass;
      if (m_debug)
        h_diMuonMassST23->Fill(mass);
    } else if (m_dimuon && m_debug) {
      std::cout << "Found fewer than 2 status 23 muons: "
                << st23Muons.size() << std::endl;
      for (auto mu : st23Muons)
        std::cout << "id: "            << mu->pdgId()
                  << ", status: "      << mu->status()
                  << ", pt: "          << mu->pt()
                  << ", m:  "          << mu->mass()
                  << ", isLastCopy:  " << mu->isLastCopy()
                  << std::endl;
    }

    // hard process electrons
    // HS electrons
    m_nhsGenEle = hsElectrons.size();
    if (m_nhsGenEle >= 2) {
      double mass = (hsElectrons.at(0)->p4()+hsElectrons.at(1)->p4()).M();
      if (m_dielectron) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            if (m_filter_hs)
              std::cout << "Found dielectron candidate outside expected window m (hs) = " << mass << std::endl
                        << hsElectrons.at(0)->pdgId()
                        << " " << hsElectrons.at(0)->status()
                        << " " << hsElectrons.at(0)->isLastCopy() << std::endl
                        << hsElectrons.at(1)->pdgId()
                        << " " << hsElectrons.at(1)->status()
                        << " " << hsElectrons.at(1)->isLastCopy()
                        << std::endl;
        } else {
          m_selection_hs = true;
        }
      }
      m_invM_hs_el = mass;
      if (m_debug)
        h_diElectronMassHS->Fill(mass);
    } else if (m_dielectron && m_debug) {
      std::cout << "Found fewer than 2 HS electrons: "
                << hsElectrons.size() << std::endl;
      for (auto el : hsElectrons)
        std::cout << "id: "            << el->pdgId()
                  << ", status: "      << el->status()
                  << ", pt: "          << el->pt()
                  << ", m:  "          << el->mass()
                  << ", isLastCopy:  " << el->isLastCopy()
                  << std::endl;
    }

    // HS muons
    m_nhsGenMu = hsMuons.size();
    if (hsMuons.size() >= 2) {
      double mass = (hsMuons.at(0)->p4()+hsMuons.at(1)->p4()).M();
      if (m_dimuon) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            if (m_filter_hs)
              std::cout << "Found dimuon candidate outside expected window m (hs) = " << mass << std::endl
                        << hsMuons.at(0)->pdgId()
                        << " " << hsMuons.at(0)->status()
                        << " " << hsMuons.at(0)->isLastCopy() << std::endl
                        << hsMuons.at(1)->pdgId()
                        << " " << hsMuons.at(1)->status()
                        << " " << hsMuons.at(1)->isLastCopy()
                        << std::endl;
        } else {
          m_selection_hs = true;
        }
      }
      m_invM_hs_mu = mass;
      if (m_debug)
        h_diMuonMassHS->Fill(mass);
    } else if (m_dimuon && m_debug) {
      std::cout << "Found fewer than 2 HS muons: "
                << hsMuons.size() << std::endl;
      for (auto mu : hsMuons)
        std::cout << "id: "            << mu->pdgId()
                  << ", status: "      << mu->status()
                  << ", pt: "          << mu->pt()
                  << ", m:  "          << mu->mass()
                  << ", isLastCopy:  " << mu->isLastCopy()
                  << std::endl;
    }

    // make sure to take:
    //  - same status particles, 23 if exists, 1 otherwise
    //  - opposite sign pdgID
    m_nGenEle = genElectrons.size();
    if (genElectrons.size() >= 2) {
      double mass = (genElectrons.at(0)->p4()+genElectrons.at(1)->p4()).M();
      if (m_dielectron) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            if (m_filter_pre)
              std::cout << "Found dielectron candidate outside expected window m (preISR) = " << mass << std::endl
                        << genElectrons.at(0)->pdgId()
                        << " " << genElectrons.at(0)->status()
                        << " " << genElectrons.at(0)->isLastCopy() << std::endl
                        << genElectrons.at(1)->pdgId()
                        << " " << genElectrons.at(1)->status()
                        << " " << genElectrons.at(1)->isLastCopy()
                        << std::endl;
        } else {
          m_selection_pre = true;
        }
      }
      m_invM_any_el = mass;
      if (m_debug)
        h_diElectronMassPre->Fill(mass);
    }

    // hard process muons
    m_nGenMu = genMuons.size();
    if (genMuons.size() >= 2) {
      double mass = (genMuons.at(0)->p4()+genMuons.at(1)->p4()).M();
      if (m_dimuon) {
        if (mass < m_minCut || mass >= m_maxCut) {
          if (m_debug)
            if (m_filter_pre)
              std::cout << "Found dimuon candidate outside expected window m (preISR) = " << mass << std::endl
                        << genMuons.at(0)->pdgId()
                        << " " << genMuons.at(0)->status()
                        << " " << genMuons.at(0)->isLastCopy() << std::endl
                        << genMuons.at(1)->pdgId()
                        << " " << genMuons.at(1)->status()
                        << " " << genMuons.at(1)->isLastCopy()
                        << std::endl;
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

  std::unique_ptr<bool> fOut0(new bool(m_selection_st1));
  ev.put(std::move(fOut0),"passST1MassCut");

  std::unique_ptr<bool> fOut1(new bool(m_selection_st23));
  ev.put(std::move(fOut1),"passST23MassCut");

  std::unique_ptr<bool> fOut2(new bool(m_selection_hs));
  ev.put(std::move(fOut2),"passHSMassCut");

  // std::unique_ptr<bool> fOut3(new bool(m_selection_pre));
  std::unique_ptr<bool> fOut3(new bool(m_selection_st23));
  ev.put(std::move(fOut3),"passPreFSRMassCut");

  std::unique_ptr<bool> fOut4(new bool(m_selection));
  ev.put(std::move(fOut4),"passMassCut");

  std::unique_ptr<double> wOut(new double(m_xsWeight));
  ev.put(std::move(wOut),"xsWeight");

  if (m_filter) {
    if (m_filter_hs)
      return m_selection_hs;
    else if (m_filter_st1)
      return m_selection_st1;
    else if (m_filter_st23)
      return m_selection_st23;
    else if (m_filter_pre)
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
