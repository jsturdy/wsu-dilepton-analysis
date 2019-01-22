import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process("MuonAnalysis",eras.Run2_25ns,eras.Run2_2017)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(
    wantSummary      = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True)
)

# load conditions from the global tag, what to use here?
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

from WSUDiLeptons.MuonAnalyzer.inputfiles import *

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        testfiles
        # cosmics16bv1reco
        ),
    # secondaryFileNames = cms.untracked.vstring(
    #     cosmics16bv1raw
    # )
)

process.source.inputCommands = cms.untracked.vstring(
    "keep *",
    # "drop FEDRawDataCollection_rawDataCollector_*_*",
    # "drop *_cosmicDCTracks_*_*",
    # "drop *_hltGtStage2ObjectMap_*_*",
)

process.source.dropDescendantsOfDroppedBranches = cms.untracked.bool(False)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load("WSUDiLeptons.MuonAnalyzer.wsuFakeL1SingleMuFilter_cfi")
process.singleMuFilter.filterEvent = cms.bool(False)

process.load("WSUDiLeptons.MuonAnalyzer.wsuMuonCollections_cfi")
process.COSMICoutput.fileName = cms.untracked.string('CosmicAnalysis_data_CosmicSP_94X.root')

from WSUDiLeptons.MuonAnalyzer.wsuMuonAnalyzer_cfi import muonAnalysis

process.analysisMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("betterMuons"),
    tagLegSrc   = cms.InputTag("betterMuons"),
    probeLegSrc = cms.InputTag("betterMuons"),
    algoType    = cms.int32(1),
    debug       = cms.int32(-1)
)
process.analysisGlobalMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalMuonsLoc"),
    tagLegSrc   = cms.InputTag("globalMuonsLoc"),
    probeLegSrc = cms.InputTag("globalMuonsLoc"),
    algoType    = cms.int32(1),
    debug       = cms.int32(-1)
)
process.analysisSPMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("betterSPMuons"),
    tagLegSrc   = cms.InputTag("betterSPMuons"),
    probeLegSrc = cms.InputTag("betterSPMuons"),
    algoType    = cms.int32(1),
    debug       = cms.int32(1)
)
process.analysisGlobalSPMuons = muonAnalysis.clone(
    muonSrc     = cms.InputTag("globalSPMuons"),
    tagLegSrc   = cms.InputTag("upperGlobalMuons"),
    probeLegSrc = cms.InputTag("lowerGlobalMuons"),
    algoType    = cms.int32(5),
    debug       = cms.int32(-1)
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
    fileName = cms.string('CosmicMuonAnalysis_data_94X.root')
)

process.muonanalysis = cms.Path(
    process.singleMuFilter
    # +process.singleMuFilterStage2
    # +process.reconstructionCosmics
    +process.betterMuons
    +process.globalMuonsLoc
    +process.betterSPMuons
    +process.globalSPMuons
    +process.upperMuons
    +process.lowerMuons
    +process.upperGlobalMuons
    +process.lowerGlobalMuons
    +process.muonSPFilter
    # +process.globalMuonSPFilter
    # +process.analysisMuons
    # +process.analysisGlobalMuons
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
   # ,process.COSMICoutput_step
)
