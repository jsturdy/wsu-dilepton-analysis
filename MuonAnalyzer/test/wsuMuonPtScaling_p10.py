import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process("MuonPtScaling",eras.Run2_25ns,eras.Run2_2017)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(
    wantSummary      = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True)
)

from WSUDiLeptons.MuonAnalyzer.inputfiles import *

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # mcfilespt10asym
        mc17filespt10
        # dyfiles
    )
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("WSUDiLeptons.MuonAnalyzer.wsuMuonCollections_cfi")

from WSUDiLeptons.MuonAnalyzer.wsuTrackCollections_cfi import COSMICTrackoutput
process.COSMICoutput.outputCommands.append(COSMICTrackoutput)

from WSUDiLeptons.MuonAnalyzer.wsuMuonPtScaling_cfi import *
# process.load("WSUDiLeptons.MuonAnalyzer.wsuMuonCollections_cfi")

## for comparing with standard collision data/MC
# can't get y position from AOD/AODSIM, lives in TrackExtra not stored in AOD
#process.cosmicMuonTracks.src  = cms.InputTag("standAloneMuons")
#process.globalMuonTracks.src  = cms.InputTag("globalMuons")
#process.trackerMuonTracks.src = cms.InputTag("generalTracks")

# # load conditions from the global tag, what to use here?
# process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
# from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
# process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# l1path = 'L1_SingleMuOpen'
# from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
# process.trigFilter = triggerResultsFilter.clone()
# process.trigFilter.triggerConditions = cms.vstring("HLT_L1SingleMuOpen*")
# process.trigFilter.l1tResults        = cms.InputTag('gtDigis','','HLT')
# process.trigFilter.hltResults        = cms.InputTag('TriggerResults','','HLT')

# process.analysisPtScalingLower = muonPtScaling.clone(
#     muonSrc = cms.InputTag("zprimeLowerMuons"),
#     # debug   = cms.bool(True)
# )
# process.analysisPtScaling = muonPtScaling.clone(
#     muonSrc     = cms.InputTag("zprimeMuons"),
# )
# process.analysisPtScalingUpper = muonPtScaling.clone(
#     muonSrc     = cms.InputTag("zprimeUpperMuons"),
# )

process.analysisPtScaling = muonPtScaling.clone(
    muonSrc     = cms.InputTag("muons"),
)
process.analysisPtScaling1Leg = muonPtScaling.clone(
    muonSrc     = cms.InputTag("muons1Leg"),
)
process.analysisPtScalingSplit = muonPtScaling.clone(
    muonSrc     = cms.InputTag("splitMuons"),
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('CosmicMuonPtScaling_MC_p10_2017.root')
)

# process.muonSPFilter.src = cms.InputTag("zprimeMuons")

process.muonanalysis = cms.Path(
    # process.trigFilter
    # +process.zprimeMuons
    # +process.zprimeLowerMuons
    # +process.zprimeUpperMuons
    # +process.muonSPFilter
    process.analysisPtScaling
    # +process.analysisPtScalingLower
    # +process.analysisPtScalingUpper
    +process.analysisPtScaling1Leg
    +process.analysisPtScalingSplit
)

# Schedule definition
process.schedule = cms.Schedule(
    process.muonanalysis
)
