import FWCore.ParameterSet.Config as cms

muonPtScaling = cms.EDAnalyzer('MuonPtScaling',
    muonSrc     = cms.InputTag("muons"),
    simTrackSrc = cms.InputTag('g4SimHits'),
    isGen       = cms.bool(True),
    debug       = cms.bool(False)
)
