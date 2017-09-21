import FWCore.ParameterSet.Config as cms


genLevelFilter = cms.EDFilter('GenLevelFilter',
    genParticleSource = cms.InputTag('prunedGenParticles'),
    filterevent       = cms.bool(False),
    debug             = cms.bool(False),
    minCut            = cms.double(-1.),
    maxCut            = cms.double(1e8),
    sampleType        = cms.string(""),
)

genLevelFilterP = cms.EDProducer('GenLevelFilter',
    genParticleSource = cms.InputTag('prunedGenParticles'),
    filterevent       = cms.bool(False),
    filterPreFSR      = cms.bool(False),
    debug             = cms.bool(False),
    minCut            = cms.double(-1.),
    maxCut            = cms.double(1e8),
    sampleType        = cms.string(""),
)
