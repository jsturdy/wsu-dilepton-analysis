import FWCore.ParameterSet.Config as cms
process = cms.Process("MuonAnalysis")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))



from WSUDiLeptons.MuonAnalyzer.inputfiles import *


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #comm16v1
        #comm16v2
        cosmics16av1
        #cosmics16av2
        #cosmics16bv1
        #cosmics16bv2
    )
)
process.source.inputCommands = cms.untracked.vstring(
    "keep *",
   "drop FEDRawDataCollection_rawDataCollector_*_*"
)

process.source.dropDescendantsOfDroppedBranches=cms.untracked.bool(False)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )

process.load("WSUDiLeptons.MuonAnalyzer.wsuFakeL1SingleMuFilter_cfi")
process.singleMuFilter.filterEvent = cms.bool(False)


process.load("WSUDiLeptons.MuonAnalyzer.wsuMuonCollections_cfi")
process.COSMICoutput.fileName = cms.untracked.string('CosmicAnalysis_data_CosmicSP_80X.root')

from WSUDiLeptons.MuonAnalyzer.wsuMuonAnalyzer_cfi import muonAnalysis

process.analysisMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("betterMuons"),
    tagLegSrc   = cms.InputTag("betterMuons"),
    probeLegSrc = cms.InputTag("betterMuons"),
    algoType    = cms.int32(1),
    debug       = cms.int32(-1)
)
process.analysisGlobalMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalMuons"),
    tagLegSrc   = cms.InputTag("globalMuons"),
    probeLegSrc = cms.InputTag("globalMuons"),
    algoType    = cms.int32(1),
    debug       = cms.int32(1)
)
process.analysisSPMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("betterSPMuons"),
    tagLegSrc   = cms.InputTag("betterSPMuons"),
    probeLegSrc = cms.InputTag("betterSPMuons"),
    algoType    = cms.int32(1),
    debug       = cms.int32(2)
)
process.analysisGlobalSPMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalSPMuons"),
    tagLegSrc   = cms.InputTag("upperGlobalMuons"),
    probeLegSrc = cms.InputTag("lowerGlobalMuons"),
    algoType    = cms.int32(5),
    debug       = cms.int32(2)
)

process.analysisTrackerMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalSPMuons"),
    tagLegSrc   = cms.InputTag("upperGlobalMuons"),
    probeLegSrc = cms.InputTag("lowerGlobalMuons"),
    algoType    = cms.int32(1),
    debug       = cms.int32(-1)
)
process.analysisTPFMSMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalSPMuons"),
    tagLegSrc   = cms.InputTag("upperGlobalMuons"),
    probeLegSrc = cms.InputTag("lowerGlobalMuons"),
    algoType    = cms.int32(2),
    debug       = cms.int32(-1)
)
process.analysisDYTMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalSPMuons"),
    tagLegSrc   = cms.InputTag("upperGlobalMuons"),
    probeLegSrc = cms.InputTag("lowerGlobalMuons"),
    algoType    = cms.int32(3),
    debug       = cms.int32(-1)
)
process.analysisPickyMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalSPMuons"),
    tagLegSrc   = cms.InputTag("upperGlobalMuons"),
    probeLegSrc = cms.InputTag("lowerGlobalMuons"),
    algoType    = cms.int32(4),
    debug       = cms.int32(-1)
)

process.analysisTunePMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalSPMuons"),
    tagLegSrc   = cms.InputTag("upperGlobalMuons"),
    probeLegSrc = cms.InputTag("lowerGlobalMuons"),
    algoType    = cms.int32(5),
    debug       = cms.int32(1)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('CosmicMuonAnalysis_data_80X.root')
)

process.muonanalysis = cms.Path(
    process.singleMuFilter
    #process.reconstructionCosmics
    +process.betterMuons
    +process.globalMuons
    +process.betterSPMuons
    +process.globalSPMuons
    +process.upperMuons
    +process.lowerMuons
    +process.upperGlobalMuons
    +process.lowerGlobalMuons
    +process.muonSPFilter
    #+process.globalMuonSPFilter
    #+process.analysisMuons
    #+process.analysisGlobalMuons
    +process.analysisSPMuons
    +process.analysisGlobalSPMuons
    +process.analysisTrackerMuons
    +process.analysisTPFMSMuons
    +process.analysisDYTMuons
    +process.analysisPickyMuons
    +process.analysisTunePMuons
    )

# generate EDM output
process.COSMICoutput_step = cms.EndPath(process.COSMICoutput)

# Schedule definition
process.schedule = cms.Schedule(
    process.muonanalysis
#    ,process.COSMICoutput_step
)
