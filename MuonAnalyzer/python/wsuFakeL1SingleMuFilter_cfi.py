import FWCore.ParameterSet.Config as cms

singleMuFilter = cms.EDFilter('FakeL1SingleMuFilter',
    l1MuonSrc       = cms.InputTag("l1extraParticles","","RECO"),
    l1SingleMuCuts  = cms.string('-2.88 < phi < -0.26 && gmtMuonCand.isFwd==0'),
    debug           = cms.int32(0),
    filterEvent     = cms.bool(False),
    newStage2       = cms.bool(False)
)

singleMuFilterStage2 = cms.EDFilter('FakeL1SingleMuFilter',
    l1MuonSrc       = cms.InputTag("gmtStage2Digis","Muon"),
    l1SingleMuCuts  = cms.string('-2.88 < phi < -0.26 && 0.0 < abs(eta) < 1.2'),
    debug           = cms.int32(0),
    filterEvent     = cms.bool(False),
    newStage2       = cms.bool(True)
)
