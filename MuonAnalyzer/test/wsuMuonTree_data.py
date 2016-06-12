import FWCore.ParameterSet.Config as cms
process = cms.Process("MuonAnalysis")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# load conditions from the global tag, what to use here?
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

l1path = 'L1_SingleMuOpen'
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
process.trigFilter = triggerResultsFilter.clone()
process.trigFilter.triggerConditions = cms.vstring("HLT_L1SingleMuOpen*")
process.trigFilter.l1tResults        = cms.InputTag('gtDigis','','HLT')
process.trigFilter.hltResults        = cms.InputTag('TriggerResults','','HLT')

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
    "drop FEDRawDataCollection_rawDataCollector_*_*",
)
process.source.dropDescendantsOfDroppedBranches = cms.untracked.bool(False)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )

process.load("WSUDiLeptons.MuonAnalyzer.wsuMuonCollections_cfi")
process.load("WSUDiLeptons.MuonAnalyzer.wsuTrackCollections_cfi")
process.COSMICoutput.fileName = cms.untracked.string('CosmicTree_data_CosmicSP_80X.root')

from WSUDiLeptons.MuonAnalyzer.wsuTrackCollections_cfi import COSMICTrackoutput
process.COSMICoutput.outputCommands.append(COSMICTrackoutput)

process.load("WSUDiLeptons.MuonAnalyzer.wsuFakeL1SingleMuFilter_cfi")
#process.singleMuFilter.l1MuonSrc   = cms.InputTag("l1extraParticles")
process.singleMuFilter.filterEvent = cms.bool(False)

from WSUDiLeptons.MuonAnalyzer.wsuMuonTree_cfi import *

process.analysisMuons = muonTree.clone(
    muonSrc         = cms.InputTag("betterSPMuons"),
    upperLegSrc     = cms.InputTag("upperMuons"),
    lowerLegSrc     = cms.InputTag("lowerMuons"),
    globalTrackSrc  = cms.InputTag("globalMuonTracks"),
    cosmicTrackSrc  = cms.InputTag("cosmicMuonTracks"),
    trackerTrackSrc = cms.InputTag("trackerMuonTracks"),
    algoType        = cms.int32(5),
    debug           = cms.int32(0),
    trigResultsSrc  = cms.InputTag('TriggerResults','','HLT'),
    hltTrigCut      = cms.string('L1SingleMuOpen'),
    #fakeL1SingleMuSrc = cms.InputTag("singleMuFilter"),
    isGen           = cms.bool(False)
)

process.analysisSPMuons = muonTree.clone(
    muonSrc         = cms.InputTag("zprimeMuons"),
    upperLegSrc     = cms.InputTag("zprimeUpperMuons"),
    lowerLegSrc     = cms.InputTag("zprimeLowerMuons"),
    globalTrackSrc  = cms.InputTag("globalSPMuonTracks"),
    cosmicTrackSrc  = cms.InputTag("cosmicSPMuonTracks"),
    trackerTrackSrc = cms.InputTag("trackerSPMuonTracks"),
    algoType        = cms.int32(5),
    debug           = cms.int32(0),
    trigResultsSrc  = cms.InputTag('TriggerResults','','HLT'),
    hltTrigCut      = cms.string('L1SingleMuOpen'),
    #fakeL1SingleMuSrc = cms.InputTag("singleMuFilter"),
    isGen           = cms.bool(False)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('CosmicMuonTree_data_80X.root')
)

process.muonSPFilter.src = cms.InputTag("zprimeMuons")

process.muonanalysis = cms.Path(
    #process.trigFilter
    process.singleMuFilter
    +process.betterMuons
    +process.betterSPMuons
    +process.lowerMuons
    +process.upperMuons
    +process.zprimeMuons
    +process.zprimeLowerMuons
    +process.zprimeUpperMuons
    +process.cosmicMuonTracks
    +process.globalMuonTracks
    +process.trackerMuonTracks
    +process.cosmicSPMuonTracks
    +process.globalSPMuonTracks
    +process.trackerSPMuonTracks
    #+process.muonSPFilter
    +process.analysisMuons
    +process.analysisSPMuons
    )

# generate EDM output
process.COSMICoutput_step = cms.EndPath(process.COSMICoutput)

# Schedule definition
process.schedule = cms.Schedule(
    process.muonanalysis
#    ,process.COSMICoutput_step
)
