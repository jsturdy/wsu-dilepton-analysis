import FWCore.ParameterSet.Config as cms


genLevelFilter = cms.EDFilter('GenLevelFilter',
    genParticleSource = cms.InputTag('prunedGenParticles'),
    filterevent       = cms.bool(False),
    filterPreFSR      = cms.bool(False),
    filterST1         = cms.bool(False),
    filterST23        = cms.bool(False),
    filterHS          = cms.bool(False),
    debug             = cms.bool(False),
    minCut            = cms.double(-1.),
    maxCut            = cms.double(1e8),
    xsWeight          = cms.double(-1),
    sampleType        = cms.string(""),
)
