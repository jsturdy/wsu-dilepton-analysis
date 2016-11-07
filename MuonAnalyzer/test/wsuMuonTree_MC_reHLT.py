import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('MuonAnalysis',eras.Run2_25ns,eras.Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContentCosmics_cff')
process.load('SimGeneral.MixingModule.mixCosmics_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1EmulatorRepack_FullMC_cff')
process.load('HLTrigger.Configuration.HLT_25ns10e33_v2_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(
    wantSummary      = cms.untracked.bool(True),
    #allowUnscheduled = cms.untracked.bool(True)
    )

# load conditions from the global tag, what to use here?
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '') ## default = ?
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2cosmics_asymptotic_deco_v0', '') ## from McM reHLT example

# for reHLT need to update:
## from 2016 data MuonTriggerKeys
## RPC:LHC10_BOTTOM, but tag doesn't exist in DB
## and 
## uGMT:UGMT_bottomOnly, not sure where this should go?

# L1TUtmTriggerMenuRcd   L1Menu_Collisions2016_v4_xml
# L1RPCBxOrConfigRcd     L1RPCBxOrConfig_LHC9_BOTTOM_mc
# L1RPCConeDefinitionRcd L1RPCConeDefinition_LHC9_BOTTOM_mc
# L1RPCConfigRcd         L1RPCConfig_LHC9_BOTTOM_mc
# L1RPCHsbConfigRcd      L1RPCHsbConfig_LHC9_BOTTOM_mc

from CondCore.DBCommon.CondDBSetup_cfi import *
process.cosmicTrigger = cms.ESSource("PoolDBESSource",CondDBSetup,
    connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string("L1TUtmTriggerMenuRcd"),
            #tag = cms.string("L1Menu_Collisions2016_v4_xml")
            tag = cms.string("L1Menu_Collisions2016_v6r5_ugt_1board_xml")
            ),
        cms.PSet(
            record = cms.string("L1RPCBxOrConfigRcd"),
            tag = cms.string("L1RPCBxOrConfig_LHC9_BOTTOM_mc")
            ),
        cms.PSet(
            record = cms.string("L1RPCConeDefinitionRcd"),
            tag = cms.string("L1RPCConeDefinition_LHC9_BOTTOM_mc")
            ),
        cms.PSet(
            record = cms.string("L1RPCConfigRcd"),
            tag = cms.string("L1RPCConfig_LHC9_BOTTOM_mc")
            ),
        cms.PSet(
            record = cms.string("L1RPCHsbConfigRcd"),
            tag = cms.string("L1RPCHsbConfig_LHC9_BOTTOM_mc")
            )

        )
)
process.es_prefer_cosmicTrigger = cms.ESPrefer("PoolDBESSource","cosmicTrigger")

process.load('L1Trigger.Configuration.L1TRawToDigi_cff')
process.load('L1Trigger.Configuration.L1Extra_cff')

l1path = 'L1_SingleMuOpen'
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
process.trigFilter = triggerResultsFilter.clone()
process.trigFilter.triggerConditions = cms.vstring('HLT_L1SingleMuOpen*')
process.trigFilter.l1tResults        = cms.InputTag('gtDigis','','')
process.trigFilter.hltResults        = cms.InputTag('TriggerResults','','')

from WSUDiLeptons.MuonAnalyzer.inputfiles import *

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        mcfilespt100asym
        ),
    secondaryFileNames = cms.untracked.vstring(
        mcfilespt100asymraw
        ),
)

process.source.inputCommands = cms.untracked.vstring(
    'keep *',
    'drop *_TriggerResults_*_HLT', 
    'drop *_hltTriggerSummaryAOD_*_HLT', 
    'drop *_hltGtStage2ObjectMap_*_HLT', 
    'drop *_l1extraParticles_*_RECO', 
    'drop L1GlobalTriggerReadoutRecord_gtDigis_*_RECO', 
    'drop *_cscSegments_*_RECO', 
    'drop *_dt4DSegments_*_RECO', 
    'drop *_rpcRecHits_*_RECO'
    #'drop FEDRawDataCollection_rawDataCollector_*_*',
    #'drop *_cosmicDCTracks_*_*',
    #'drop *_hltGtStage2ObjectMap_*_*',
)
process.source.dropDescendantsOfDroppedBranches = cms.untracked.bool(False)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500) )

process.load('WSUDiLeptons.MuonAnalyzer.wsuMuonCollections_cfi')
process.load('WSUDiLeptons.MuonAnalyzer.wsuTrackCollections_cfi')
process.COSMICoutput.fileName = cms.untracked.string('CosmicTree_MC_CosmicSP_80X.root')

from WSUDiLeptons.MuonAnalyzer.wsuTrackCollections_cfi import COSMICTrackoutput
process.COSMICoutput.outputCommands.append(COSMICTrackoutput)

process.load('WSUDiLeptons.MuonAnalyzer.wsuFakeL1SingleMuFilter_cfi')
process.singleMuFilter.l1MuonSrc = cms.InputTag('l1extraParticles','','')
process.singleMuFilter.l1MuonSrc   = cms.InputTag('l1extraParticles')
process.singleMuFilter.filterEvent = cms.bool(False)

from WSUDiLeptons.MuonAnalyzer.wsuMuonTree_cfi import *

process.analysisMuons = muonTree.clone(
    muonSrc         = cms.InputTag('betterSPMuons'),
    upperLegSrc     = cms.InputTag('upperMuons'),
    lowerLegSrc     = cms.InputTag('lowerMuons'),
    globalTrackSrc  = cms.InputTag('globalMuonTracks'),
    cosmicTrackSrc  = cms.InputTag('cosmicMuonTracks'),
    trackerTrackSrc = cms.InputTag('trackerMuonTracks'),
    algoType        = cms.int32(5),
    debug           = cms.int32(1),
    trigResultsSrc  = cms.InputTag('TriggerResults','',''),
    l1MuonSrc       = cms.InputTag('l1extraParticles','',''),
    hltTrigCut      = cms.string('L1SingleMuOpen'),
    fakeL1SingleMuSrc = cms.InputTag('singleMuFilter'),
    isGen           = cms.bool(True)
)

process.analysisMuonsStage2 = muonTree.clone(
    muonSrc         = cms.InputTag('betterSPMuons'),
    upperLegSrc     = cms.InputTag('upperMuons'),
    lowerLegSrc     = cms.InputTag('lowerMuons'),
    globalTrackSrc  = cms.InputTag('globalMuonTracks'),
    cosmicTrackSrc  = cms.InputTag('cosmicMuonTracks'),
    trackerTrackSrc = cms.InputTag('trackerMuonTracks'),
    algoType        = cms.int32(5),
    debug           = cms.int32(1),
    trigResultsSrc  = cms.InputTag('TriggerResults','',''),
    l1MuonSrc       = cms.InputTag('l1extraParticles','',''),
    hltTrigCut      = cms.string('L1SingleMuOpen'),
    fakeL1SingleMuSrc = cms.InputTag('singleMuFilterStage2'),
    isGen           = cms.bool(True)
)

process.analysisSPMuons = muonTree.clone(
    muonSrc         = cms.InputTag('zprimeMuons'),
    upperLegSrc     = cms.InputTag('zprimeUpperMuons'),
    lowerLegSrc     = cms.InputTag('zprimeLowerMuons'),
    globalTrackSrc  = cms.InputTag('globalSPMuonTracks'),
    cosmicTrackSrc  = cms.InputTag('cosmicSPMuonTracks'),
    trackerTrackSrc = cms.InputTag('trackerSPMuonTracks'),
    algoType        = cms.int32(5),
    debug           = cms.int32(1),
    trigResultsSrc  = cms.InputTag('TriggerResults','',''),
    l1MuonSrc       = cms.InputTag('l1extraParticles','',''),
    hltTrigCut      = cms.string('L1SingleMuOpen'),
    fakeL1SingleMuSrc = cms.InputTag('singleMuFilter'),
    isGen           = cms.bool(True)
)

process.TFileService = cms.Service('TFileService',
    fileName = cms.string('CosmicMuonTree_MC_80X.root')
)

process.muonSPFilter.src = cms.InputTag('zprimeMuons')

from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

process.l1repack = cms.Path(
    process.SimL1Emulator
    )

process.rerunl1t = cms.Path(
    process.L1TRawToDigi
    +process.L1Extra
    )
# # EDM Output definition
# process.rerunL1TOutput = cms.OutputModule('PoolOutputModule',
#     dataset = cms.untracked.PSet(
#         dataTier = cms.untracked.string('RAW-RECO'),
#         filterName = cms.untracked.string('rerunl1t')
#     ),
#     SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('rerunl1t')),
#     eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
#     fileName = cms.untracked.string('rerunL1T_output.root'),
#     outputCommands = cms.untracked.vstring('keep *')
# )

process.muonanalysis = cms.Path(
    #process.L1TRawToDigi
    #process.trigFilter
    process.singleMuFilter
    +process.singleMuFilterStage2
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
    +process.analysisMuonsStage2
    +process.analysisSPMuons
    )

# generate EDM output
process.COSMICoutput_step   = cms.EndPath(process.COSMICoutput)
#process.rerunL1TOutput_step = cms.EndPath(process.rerunL1TOutput)

# Schedule definition
process.schedule = cms.Schedule(process.l1repack)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.rerunl1t])
process.schedule.extend([process.muonanalysis])
process.schedule.extend([process.COSMICoutput_step])

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforFullSim 

#call to customisation function customizeHLTforFullSim imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforFullSim(process)

# End of customisation functions

###-- Dump config ------------------------------------------------------------
file = open('wsuMuonTree_MC_reHLT_full_cfg.py','w')
file.write(str(process.dumpPython()))
file.close()
