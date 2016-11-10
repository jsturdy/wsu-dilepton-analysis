# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: reco -s RAW2DIGI,RECO,SKIM:CosmicSP --era Run2_25ns,Run2_2016 --data --scenario cosmics --filein dbs:/Cosmics/Run2016G-CosmicSP-PromptReco-v1/RAW-RECO --fileout cosmic_data_reRECO_SKIM.root --conditions 80X_dataRun2_2016SeptRepro_v4 --python_filename cosmic_data_reRECO_SKIM_RAWRECO.py --no_exec

import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('MuonAnalysis',eras.Run2_25ns,eras.Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContentCosmics_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.ReconstructionCosmics_cff')
process.load('Configuration.StandardSequences.SkimsCosmics_cff')
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
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_2016SeptRepro_v4', '')

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

# from CondCore.DBCommon.CondDBSetup_cfi import *
# process.cosmicTrigger = cms.ESSource('PoolDBESSource',CondDBSetup,
#     connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
#     toGet = cms.VPSet(
#         cms.PSet(
#             record = cms.string('L1TUtmTriggerMenuRcd'),
#             #tag = cms.string('L1Menu_Collisions2016_v4_xml')
#             tag = cms.string('L1Menu_Collisions2016_v6r5_ugt_1board_xml')
#             ),
#         cms.PSet(
#             record = cms.string('L1RPCBxOrConfigRcd'),
#             tag = cms.string('L1RPCBxOrConfig_LHC9_BOTTOM_mc')
#             ),
#         cms.PSet(
#             record = cms.string('L1RPCConeDefinitionRcd'),
#             tag = cms.string('L1RPCConeDefinition_LHC9_BOTTOM_mc')
#             ),
#         cms.PSet(
#             record = cms.string('L1RPCConfigRcd'),
#             tag = cms.string('L1RPCConfig_LHC9_BOTTOM_mc')
#             ),
#         cms.PSet(
#             record = cms.string('L1RPCHsbConfigRcd'),
#             tag = cms.string('L1RPCHsbConfig_LHC9_BOTTOM_mc')
#             )

#         )
# )
# process.es_prefer_cosmicTrigger = cms.ESPrefer('PoolDBESSource','cosmicTrigger')

process.load('L1Trigger.Configuration.L1TRawToDigi_cff')
process.load('L1Trigger.Configuration.L1Extra_cff')

l1path = 'L1_SingleMuOpen'
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
process.trigFilter = triggerResultsFilter.clone()
process.trigFilter.triggerConditions = cms.vstring('HLT_L1SingleMuOpen*')
process.trigFilter.l1tResults        = cms.InputTag('gtDigis','','')
process.trigFilter.hltResults        = cms.InputTag('TriggerResults','','')

from WSUDiLeptons.MuonAnalyzer.inputfiles import *
from WSUDiLeptons.MuonAnalyzer.cosmics2016bv1 import *

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        cosmics16bv1reco
        ),
    # secondaryFileNames = cms.untracked.vstring(
    #     cosmics16bv1raw
    # )
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
process.COSMICoutput.fileName = cms.untracked.string('CosmicSP_80X_dataRun2_2016SeptRepro_v4.root')

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
    hltTrigCut      = cms.string('L1SingleMuOpen'),
    #fakeL1SingleMuSrc = cms.InputTag('singleMuFilter'),
    isGen           = cms.bool(False)
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
    hltTrigCut      = cms.string('L1SingleMuOpen'),
    #fakeL1SingleMuSrc = cms.InputTag('singleMuFilter'),
    isGen           = cms.bool(False)
)

process.TFileService = cms.Service('TFileService',
    fileName = cms.string('CosmicMuonTree_data_80X_wSKIM.root')
)

process.muonSPFilter.src = cms.InputTag('zprimeMuons')

from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('reco nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('CosmicSP_80X_dataRun2_2016SeptRepro_v4_wSKIM.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
process.SKIMStreamCosmicSP = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('cosmicMuonsBarrelOnlyPath', 
            'cosmicMuonsPath', 
            'cosmicMuons1LegPath', 
            'globalCosmicMuonsBarrelOnlyPath', 
            'cosmictrackfinderP5Path', 
            'globalCosmicMuonsPath', 
            'globalCosmicMuons1LegPath')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RAW-RECO'),
        filterName = cms.untracked.string('CosmicSP')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('CosmicSP.root'),
    outputCommands = cms.untracked.vstring( ('drop *', 
        'keep *_logErrorHarvester_*_*', 
        'drop *', 
        'keep  FEDRawDataCollection_rawDataCollector_*_*', 
        'keep  FEDRawDataCollection_source_*_*', 
        'keep *_cscTriggerPrimitiveDigis_*_*', 
        'keep *_dtTriggerPrimitiveDigis_*_*', 
        'keep *_rpcTriggerDigis_*_*', 
        'keep *_rctDigis_*_*', 
        'keep *_csctfDigis_*_*', 
        'keep *_csctfTrackDigis_*_*', 
        'keep *_dttfDigis_*_*', 
        'keep *_gctDigis_*_*', 
        'keep *_gmtDigis_*_*', 
        'keep *_gtDigis_*_*', 
        'keep *_gtEvmDigis_*_*', 
        'keep *_l1GtRecord_*_*', 
        'keep *_l1GtObjectMap_*_*', 
        'keep *_l1extraParticles_*_*', 
        'drop *_hlt*_*_*', 
        'keep FEDRawDataCollection_rawDataCollector_*_*', 
        'keep FEDRawDataCollection_source_*_*', 
        'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_*', 
        'keep edmTriggerResults_*_*_*', 
        'keep triggerTriggerEvent_*_*_*', 
        'keep PixelDigiedmDetSetVector_siPixelDigis_*_*', 
        'keep *_siStripDigis_*_*', 
        'keep *_siStripZeroSuppression_*_*', 
        'keep *_siPixelClusters_*_*', 
        'keep *_siStripClusters_*_*', 
        'keep *_siPixelRecHits_*_*', 
        'keep *_siStripRecHits_*_*', 
        'keep *_siStripMatchedRecHits_*_*', 
        'keep *_muonDTDigis_*_*', 
        'keep *_dttfDigis_*_*', 
        'keep *_dt1DRecHits_*_*', 
        'keep *_dt4DSegments_*_*', 
        'keep *_dt4DSegmentsT0Seg_*_*', 
        'keep *_csc2DRecHits_*_*', 
        'keep *_cscSegments_*_*', 
        'keep RPCDetIdRPCDigiMuonDigiCollection_*_*_*', 
        'keep *_rpcRecHits_*_*', 
        'keep *_hbhereco_*_*', 
        'keep *_hfreco_*_*', 
        'keep *_horeco_*_*', 
        'keep HBHERecHitsSorted_hbherecoMB_*_*', 
        'keep HORecHitsSorted_horecoMB_*_*', 
        'keep HFRecHitsSorted_hfrecoMB_*_*', 
        'keep ZDCDataFramesSorted_hcalDigis_*_*', 
        'keep ZDCDataFramesSorted_simHcalUnsuppressedDigis_*_*', 
        'keep ZDCRecHitsSorted_*_*_*', 
        'keep HcalUnpackerReport_castorDigis_*_*', 
        'keep HcalUnpackerReport_hcalDigis_*_*', 
        'keep *_ecalPreshowerRecHit_*_*', 
        'keep *_ecalRecHit_*_*', 
        'keep *_ecalCompactTrigPrim_*_*', 
        'keep ESDataFramesSorted_ecalPreshowerDigis_*_*', 
        'keep *_islandBasicClusters_*_*', 
        'keep *_fixedMatrixBasicClusters_*_*', 
        'keep *_hybridSuperClusters_*_*', 
        'keep *_uncleanedHybridSuperClusters_*_*', 
        'keep *_cosmicBasicClusters_*_*', 
        'keep *_cosmicSuperClusters_*_*', 
        'drop recoSuperClusters_hybridSuperClusters_*_*', 
        'keep recoSuperClusters_islandSuperClusters_islandBarrelSuperClusters_*', 
        'keep recoSuperClusters_correctedHybridSuperClusters_*_*', 
        'keep *_correctedFixedMatrixSuperClustersWithPreshower_*_*', 
        'keep recoPreshowerClusters_fixedMatrixSuperClustersWithPreshower_*_*', 
        'keep *_correctedEndcapSuperClustersWithPreshower_*_*', 
        'keep recoPreshowerClusterShapes_preshowerClusterShape_*_*', 
        'keep recoPreshowerClusterShapes_fixedMatrixPreshowerClusterShape_*_*', 
        'keep recoGsfElectronCores_gsfElectronCores_*_*', 
        'keep recoGsfElectronCores_gedGsfElectronCores_*_*', 
        'keep recoGsfElectrons_gsfElectrons_*_*', 
        'keep recoGsfElectrons_gedGsfElectrons_*_*', 
        'keep recoGsfElectronCores_uncleanedOnlyGsfElectronCores_*_*', 
        'keep recoGsfElectrons_uncleanedOnlyGsfElectrons_*_*', 
        'keep floatedmValueMap_eidRobustLoose_*_*', 
        'keep floatedmValueMap_eidRobustTight_*_*', 
        'keep floatedmValueMap_eidRobustHighEnergy_*_*', 
        'keep floatedmValueMap_eidLoose_*_*', 
        'keep floatedmValueMap_eidTight_*_*', 
        'keep *_egmGedGsfElectronPFIsolation_*_*', 
        'keep *_photonEcalPFClusterIsolationProducer_*_*', 
        'keep *_electronEcalPFClusterIsolationProducer_*_*', 
        'keep *_photonHcalPFClusterIsolationProducer_*_*', 
        'keep *_electronHcalPFClusterIsolationProducer_*_*', 
        'drop *_egmGsfElectronIDs_*_*', 
        'drop *_egmPhotonIDs_*_*', 
        'keep *_gedPhotonCore_*_*', 
        'keep *_gedPhotons_*_*', 
        'keep *_particleBasedIsolation_*_*', 
        'keep recoPhotons_mustachePhotons_*_*', 
        'keep recoPhotonCores_mustachePhotonCore_*_*', 
        'keep recoPhotons_photons_*_*', 
        'keep recoPhotonCores_photonCore_*_*', 
        'keep recoConversions_conversions_*_*', 
        'keep recoConversions_mustacheConversions_*_*', 
        'drop *_conversions_uncleanedConversions_*', 
        'drop *_gedPhotonsTmp_valMapPFEgammaCandToPhoton_*', 
        'keep recoConversions_allConversions_*_*', 
        'keep recoConversions_allConversionsOldEG_*_*', 
        'keep recoTracks_ckfOutInTracksFromConversions_*_*', 
        'keep recoTracks_ckfInOutTracksFromConversions_*_*', 
        'keep recoTrackExtras_ckfOutInTracksFromConversions_*_*', 
        'keep recoTrackExtras_ckfInOutTracksFromConversions_*_*', 
        'keep TrackingRecHitsOwned_ckfOutInTracksFromConversions_*_*', 
        'keep TrackingRecHitsOwned_ckfInOutTracksFromConversions_*_*', 
        'keep recoConversions_uncleanedOnlyAllConversions_*_*', 
        'keep recoTracks_uncleanedOnlyCkfOutInTracksFromConversions_*_*', 
        'keep recoTracks_uncleanedOnlyCkfInOutTracksFromConversions_*_*', 
        'keep recoTrackExtras_uncleanedOnlyCkfOutInTracksFromConversions_*_*', 
        'keep recoTrackExtras_uncleanedOnlyCkfInOutTracksFromConversions_*_*', 
        'keep TrackingRecHitsOwned_uncleanedOnlyCkfOutInTracksFromConversions_*_*', 
        'keep TrackingRecHitsOwned_uncleanedOnlyCkfInOutTracksFromConversions_*_*', 
        'keep *_PhotonIDProd_*_*', 
        'keep *_PhotonIDProdGED_*_*', 
        'keep recoRecoEcalCandidates_hfRecoEcalCandidate_*_*', 
        'keep *_hfEMClusters_*_*', 
        'keep *_gedGsfElectronCores_*_*', 
        'keep *_gedGsfElectrons_*_*', 
        'keep recoTracks_ctfWithMaterialTracksP5_*_*', 
        'keep recoTrackExtras_ctfWithMaterialTracksP5_*_*', 
        'keep TrackingRecHitsOwned_ctfWithMaterialTracksP5_*_*', 
        'keep recoTracks_ctfWithMaterialTracksP5LHCNavigation_*_*', 
        'keep recoTrackExtras_ctfWithMaterialTracksP5LHCNavigation_*_*', 
        'keep TrackingRecHitsOwned_ctfWithMaterialTracksP5LHCNavigation_*_*', 
        'keep recoTracks_rsWithMaterialTracksP5_*_*', 
        'keep recoTrackExtras_rsWithMaterialTracksP5_*_*', 
        'keep TrackingRecHitsOwned_rsWithMaterialTracksP5_*_*', 
        'keep recoTracks_cosmictrackfinderP5_*_*', 
        'keep recoTrackExtras_cosmictrackfinderP5_*_*', 
        'keep TrackingRecHitsOwned_cosmictrackfinderP5_*_*', 
        'keep recoTracks_beamhaloTracks_*_*', 
        'keep recoTrackExtras_beamhaloTracks_*_*', 
        'keep TrackingRecHitsOwned_beamhaloTracks_*_*', 
        'keep recoTracks_splittedTracksP5_*_*', 
        'keep recoTrackExtras_splittedTracksP5_*_*', 
        'keep TrackingRecHitsOwned_splittedTracksP5_*_*', 
        'keep recoTracks_ctfWithMaterialTracksP5Top_*_*', 
        'keep recoTrackExtras_ctfWithMaterialTracksP5Top_*_*', 
        'keep TrackingRecHitsOwned_ctfWithMaterialTracksP5Top_*_*', 
        'keep recoTracks_rsWithMaterialTracksP5Top_*_*', 
        'keep recoTrackExtras_rsWithMaterialTracksP5Top_*_*', 
        'keep TrackingRecHitsOwned_rsWithMaterialTracksP5Top_*_*', 
        'keep recoTracks_cosmictrackfinderP5Top_*_*', 
        'keep recoTrackExtras_cosmictrackfinderP5Top_*_*', 
        'keep TrackingRecHitsOwned_cosmictrackfinderP5Top_*_*', 
        'keep recoTracks_ctfWithMaterialTracksP5Bottom_*_*', 
        'keep recoTrackExtras_ctfWithMaterialTracksP5Bottom_*_*', 
        'keep TrackingRecHitsOwned_ctfWithMaterialTracksP5Bottom_*_*', 
        'keep recoTracks_rsWithMaterialTracksP5Bottom_*_*', 
        'keep recoTrackExtras_rsWithMaterialTracksP5Bottom_*_*', 
        'keep TrackingRecHitsOwned_rsWithMaterialTracksP5Bottom_*_*', 
        'keep recoTracks_cosmictrackfinderP5Bottom_*_*', 
        'keep recoTrackExtras_cosmictrackfinderP5Bottom_*_*', 
        'keep TrackingRecHitsOwned_cosmictrackfinderP5Bottom_*_*', 
        'keep recoTracks_regionalCosmicTracks_*_*', 
        'keep recoTrackExtras_regionalCosmicTracks_*_*', 
        'keep TrackingRecHitsOwned_regionalCosmicTracks_*_*', 
        'keep *_dedxTruncated40_*_*', 
        'keep *_dedxHitInfo_*_*', 
        'keep *_dedxHarmonic2_*_*', 
        'keep *_dedxTruncated40CTF_*_*', 
        'keep *_dedxHitInfoCTF_*_*', 
        'keep *_dedxHarmonic2CTF_*_*', 
        'keep *_dedxTruncated40CosmicTF_*_*', 
        'keep *_dedxHitInfoCosmicTF_*_*', 
        'keep *_dedxHarmonic2CosmicTF_*_*', 
        'keep recoTracks_cosmicDCTracks_*_*', 
        'keep recoTrackExtras_cosmicDCTracks_*_*', 
        'keep TrackingRecHitsOwned_cosmicDCTracks_*_*', 
        'keep *_ak4CaloJets_*_*', 
        'keep *_ak4PFJets_*_*', 
        'keep *_ak4PFJetsCHS_*_*', 
        'keep *_ak8PFJetsCHS_*_*', 
        'keep *_ak8PFJetsCHSSoftDrop_*_*', 
        'keep *_cmsTopTagPFJetsCHS_*_*', 
        'keep *_JetPlusTrackZSPCorJetAntiKt4_*_*', 
        'keep *_ak4TrackJets_*_*', 
        'keep recoRecoChargedRefCandidates_trackRefsForJets_*_*', 
        'keep *_caloTowers_*_*', 
        'keep *_towerMaker_*_*', 
        'keep *_CastorTowerReco_*_*', 
        'keep *_ak4JetTracksAssociatorAtVertex_*_*', 
        'keep *_ak4JetTracksAssociatorAtVertexPF_*_*', 
        'keep *_ak4JetTracksAssociatorAtCaloFace_*_*', 
        'keep *_ak4JetTracksAssociatorExplicit_*_*', 
        'keep *_ak4JetExtender_*_*', 
        'keep *_ak4JetID_*_*', 
        'keep *_ak5CastorJets_*_*', 
        'keep *_ak5CastorJetID_*_*', 
        'keep *_ak7CastorJets_*_*', 
        'keep *_ak7CastorJetID_*_*', 
        'keep *_fixedGridRhoAll_*_*', 
        'keep *_fixedGridRhoFastjetAll_*_*', 
        'keep *_fixedGridRhoFastjetAllTmp_*_*', 
        'keep *_fixedGridRhoFastjetAllCalo_*_*', 
        'keep *_fixedGridRhoFastjetCentral_*_*', 
        'keep *_fixedGridRhoFastjetCentralCalo_*_*', 
        'keep *_fixedGridRhoFastjetCentralChargedPileUp_*_*', 
        'keep *_fixedGridRhoFastjetCentralNeutral_*_*', 
        'keep *_ak8PFJetsCHSSoftDropMass_*_*', 
        'keep recoCaloMETs_caloMet_*_*', 
        'keep recoCaloMETs_caloMetBE_*_*', 
        'keep recoCaloMETs_caloMetBEFO_*_*', 
        'keep recoCaloMETs_caloMetM_*_*', 
        'keep recoPFMETs_pfMet_*_*', 
        'keep recoPFMETs_pfChMet_*_*', 
        'keep recoPFMETs_pfMetEI_*_*', 
        'keep recoMuonMETCorrectionDataedmValueMap_muonMETValueMapProducer_*_*', 
        'keep recoHcalNoiseRBXs_hcalnoise_*_*', 
        'keep HcalNoiseSummary_hcalnoise_*_*', 
        'keep recoCSCHaloData_CSCHaloData_*_*', 
        'keep recoEcalHaloData_EcalHaloData_*_*', 
        'keep recoGlobalHaloData_GlobalHaloData_*_*', 
        'keep recoHcalHaloData_HcalHaloData_*_*', 
        'keep recoBeamHaloSummary_BeamHaloSummary_*_*', 
        'keep *_CosmicMuonSeed_*_*', 
        'keep *_CosmicMuonSeedEndCapsOnly_*_*', 
        'keep *_CosmicMuonSeedWitht0Correction_*_*', 
        'keep *_ancientMuonSeed_*_*', 
        'keep recoTracks_cosmicMuons_*_*', 
        'keep recoTrackExtras_cosmicMuons_*_*', 
        'keep TrackingRecHitsOwned_cosmicMuons_*_*', 
        'keep recoTracks_globalCosmicMuons_*_*', 
        'keep recoTrackExtras_globalCosmicMuons_*_*', 
        'keep TrackingRecHitsOwned_globalCosmicMuons_*_*', 
        'keep recoTracks_tevMuons_*_*', 
        'keep recoTrackExtras_tevMuons_*_*', 
        'keep recoTracksToOnerecoTracksAssociation_tevMuons_*_*', 
        'keep recoMuons_muons_*_*', 
        'keep recoMuonTimeExtraedmValueMap_muons_*_*', 
        'keep recoCaloMuons_calomuons_*_*', 
        'keep recoTracks_globalCosmicSplitMuons_*_*', 
        'keep recoTrackExtras_globalCosmicSplitMuons_*_*', 
        'keep TrackingRecHitsOwned_globalCosmicSplitMuons_*_*', 
        'keep recoMuons_splitMuons_*_*', 
        'keep recoMuonTimeExtraedmValueMap_splitMuons_*_*', 
        'keep recoTracks_cosmicMuonsNoRPC_*_*', 
        'keep recoTrackExtras_cosmicMuonsNoRPC_*_*', 
        'keep TrackingRecHitsOwned_cosmicMuonsNoRPC_*_*', 
        'keep recoTracks_globalCosmicMuonsNoRPC_*_*', 
        'keep recoTrackExtras_globalCosmicMuonsNoRPC_*_*', 
        'keep TrackingRecHitsOwned_globalCosmicMuonsNoRPC_*_*', 
        'keep recoMuons_muonsNoRPC_*_*', 
        'keep recoTracks_cosmicMuons1Leg_*_*', 
        'keep recoTrackExtras_cosmicMuons1Leg_*_*', 
        'keep TrackingRecHitsOwned_cosmicMuons1Leg_*_*', 
        'keep recoTracks_globalCosmicMuons1Leg_*_*', 
        'keep recoTrackExtras_globalCosmicMuons1Leg_*_*', 
        'keep TrackingRecHitsOwned_globalCosmicMuons1Leg_*_*', 
        'keep recoMuons_muons1Leg_*_*', 
        'keep recoMuonTimeExtraedmValueMap_muons1Leg_*_*', 
        'keep recoTracks_cosmicMuonsWitht0Correction_*_*', 
        'keep recoTrackExtras_cosmicMuonsWitht0Correction_*_*', 
        'keep TrackingRecHitsOwned_cosmicMuonsWitht0Correction_*_*', 
        'keep recoTracks_globalCosmicMuonsWitht0Correction_*_*', 
        'keep recoTrackExtras_globalCosmicMuonsWitht0Correction_*_*', 
        'keep TrackingRecHitsOwned_globalCosmicMuonsWitht0Correction_*_*', 
        'keep recoMuons_muonsWitht0Correction_*_*', 
        'keep recoMuonTimeExtraedmValueMap_muonsWitht0Correction_*_*', 
        'keep recoTracks_cosmicMuonsEndCapsOnly_*_*', 
        'keep recoTrackExtras_cosmicMuonsEndCapsOnly_*_*', 
        'keep TrackingRecHitsOwned_cosmicMuonsEndCapsOnly_*_*', 
        'keep recoTracks_globalBeamHaloMuonEndCapslOnly_*_*', 
        'keep recoTrackExtras_globalBeamHaloMuonEndCapslOnly_*_*', 
        'keep TrackingRecHitsOwned_globalBeamHaloMuonEndCapslOnly_*_*', 
        'keep recoMuons_muonsBeamHaloEndCapsOnly_*_*', 
        'keep recoMuonTimeExtraedmValueMap_muonsBeamHaloEndCapsOnly_*_*', 
        'keep recoTracks_standAloneMuons_*_*', 
        'keep recoTrackExtras_standAloneMuons_*_*', 
        'keep TrackingRecHitsOwned_standAloneMuons_*_*', 
        'keep recoMuons_lhcSTAMuons_*_*', 
        'keep recoMuonTimeExtraedmValueMap_lhcSTAMuons_*_*', 
        'keep recoTracks_ctfWithMaterialTracksP5_*_*', 
        'keep recoTracks_ctfWithMaterialTracksBeamHaloMuon_*_*', 
        'keep recoTracks_ctfWithMaterialTracksP5LHCNavigation_*_*', 
        'keep *_muIsoDepositTk_*_*', 
        'keep *_muIsoDepositCalByAssociatorTowers_*_*', 
        'keep *_muIsoDepositCalByAssociatorHits_*_*', 
        'keep *_muIsoDepositJets_*_*', 
        'keep *_muGlobalIsoDepositCtfTk_*_*', 
        'keep *_muGlobalIsoDepositCalByAssociatorTowers_*_*', 
        'keep *_muGlobalIsoDepositCalByAssociatorHits_*_*', 
        'keep *_muGlobalIsoDepositJets_*_*', 
        'keep *_offlineBeamSpot_*_*', 
        'keep  *_offlinePrimaryVertices__*', 
        'keep *_offlinePrimaryVerticesWithBS_*_*', 
        'keep *_offlinePrimaryVerticesFromCosmicTracks_*_*', 
        'keep *_nuclearInteractionMaker_*_*', 
        'keep *_generalV0Candidates_*_*', 
        'keep *_inclusiveSecondaryVertices_*_*', 
        'keep *_cscTriggerPrimitiveDigis_*_*', 
        'keep *_dtTriggerPrimitiveDigis_*_*', 
        'keep *_rpcTriggerDigis_*_*', 
        'keep *_rctDigis_*_*', 
        'keep *_csctfDigis_*_*', 
        'keep *_csctfTrackDigis_*_*', 
        'keep *_dttfDigis_*_*', 
        'keep *_gctDigis_*_*', 
        'keep *_gmtDigis_*_*', 
        'keep *_gtDigis_*_*', 
        'keep *_gtEvmDigis_*_*', 
        'keep *_l1GtRecord_*_*', 
        'keep *_l1GtTriggerMenuLite_*_*', 
        'keep *_l1GtObjectMap_*_*', 
        'keep *_l1extraParticles_*_*', 
        'keep *_l1L1GtObjectMap_*_*', 
        'keep LumiDetails_lumiProducer_*_*', 
        'keep LumiSummary_lumiProducer_*_*', 
        'drop *_hlt*_*_*', 
        'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_*', 
        'keep edmTriggerResults_*_*_*', 
        'keep triggerTriggerEvent_*_*_*', 
        'keep L1AcceptBunchCrossings_scalersRawToDigi_*_*', 
        'keep L1TriggerScalerss_scalersRawToDigi_*_*', 
        'keep Level1TriggerScalerss_scalersRawToDigi_*_*', 
        'keep LumiScalerss_scalersRawToDigi_*_*', 
        'keep BeamSpotOnlines_scalersRawToDigi_*_*', 
        'keep DcsStatuss_scalersRawToDigi_*_*', 
        'keep DcsStatuss_hltScalersRawToDigi_*_*', 
        'drop *_MEtoEDMConverter_*_*', 
        'drop *_*_*_SKIM' ) )
)

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
    +process.analysisSPMuons
    )

# Path and EndPath definitions
process.raw2digi_step       = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstructionCosmics)
process.endjob_step         = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step  = cms.EndPath(process.RECOSIMoutput)
process.SKIMStreamCosmicSPOutPath = cms.EndPath(process.SKIMStreamCosmicSP)

# Schedule definition
process.schedule = cms.Schedule(
    process.raw2digi_step,
    process.reconstruction_step,
    process.cosmicMuonsBarrelOnlyPath,
    process.cosmicMuonsPath,
    process.cosmicMuons1LegPath,
    process.globalCosmicMuonsBarrelOnlyPath,
    process.cosmictrackfinderP5Path,
    process.globalCosmicMuonsPath,
    process.globalCosmicMuons1LegPath,
    )

process.schedule.extend([process.muonanalysis])

process.schedule.extend([
        process.endjob_step,
        process.RECOSIMoutput_step,
        process.SKIMStreamCosmicSPOutPath
        ]
)
# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

####-- Dump config ------------------------------------------------------------
#file = open('wsuMuonTree_data_reHLT_full_cfg.py','w')
#file.write(str(process.dumpPython()))
#file.close()
