import FWCore.ParameterSet.Config as cms

basic_cut  = "pt > 25"
# restrict collections to tracks passing near the pixel
dxy_cut = "(abs(dxy) < 50.)"
dz_cut  = " && (abs(dz)  < 75.)"

dxy_sp_cut = "(abs(dxy) < 10.)"
dz_sp_cut  = " && (abs(dz)  < 50.)"

cosmicMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("cosmicMuons"),
    cut = cms.string(basic_cut+" && "+dxy_cut+dz_cut),
)

globalMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("globalCosmicMuons"),
    cut = cms.string(basic_cut+" && "+dxy_cut+dz_cut),
)

trackerMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("ctfWithMaterialTracksP5LHCNavigation"),
    cut = cms.string(basic_cut+" && "+dxy_cut+dz_cut),
)

cosmicSPMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("cosmicMuonTracks"),
    cut = cms.string(dxy_sp_cut+dz_sp_cut),
)

globalSPMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("globalMuonTracks"),
    cut = cms.string(dxy_sp_cut+dz_sp_cut),
)

trackerSPMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("trackerMuonTracks"),
    cut = cms.string(dxy_sp_cut+dz_sp_cut),
)

# how do we ensure upper/lower for cosmic reconstruction
#  - Y position: sometimes for whatever reason this isn't reliable
#  - time information: also reliability issues
upperMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("cosmicSPMuonTracks"),
    cut = cms.string("outerPosition.Y > 0"),
    #cut = cms.string("(innerPosition.Y > 0) || (innerPosition.Y < 0 && outerPosition.Y > 0)"),
    #cut = cms.string("abs(innerPosition.Y) > abs(outerPosition.Y)"),
    #cut = cms.string("(innerPosition.Y > 0) || (innerPosition.Y < 0 && outerPosition.Y > 0)"),
    #cut = cms.string("((outerPosition.Y > 0) && (time.timeAtIpOutIn < 0)) || ((outerPosition.Y < 0) && (time.timeAtIpOutIn < 0))"),
)

upperGlobalMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("globalSPMuonTracks"),
    cut = cms.string("outerPosition.Y > 0"),
    #cut = cms.string("(innerPosition.Y > 0) || (innerPosition.Y < 0 && outerPosition.Y > 0)"),
    #cut = cms.string("abs(innerPosition.Y) > abs(outerPosition.Y)"),
    #cut = cms.string("((outerPosition.Y > 0) && (time.timeAtIpOutIn < 0)) || ((outerPosition.Y < 0) && (time.timeAtIpOutIn < 0))"),
)

upperTrackerMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("trackerSPMuonTracks"),
    #cut = cms.string("outerPosition.Y > 0"),
    #cut = cms.string("(innerPosition.Y > 0) || (innerPosition.Y < 0 && outerPosition.Y > 0)"),
    cut = cms.string("abs(innerPosition.Y) > abs(outerPosition.Y)"),
    #cut = cms.string("((outerPosition.Y > 0) && (time.timeAtIpOutIn < 0)) || ((outerPosition.Y < 0) && (time.timeAtIpOutIn < 0))"),
)

lowerMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("cosmicSPMuonTracks"),
    cut = cms.string("outerPosition.Y < 0"),
    #cut = cms.string("abs(innerPosition.Y) < abs(outerPosition.Y)"),
    #cut = cms.string("((outerPosition.Y < 0) && (time.timeAtIpOutIn > 0)) || ((outerPosition.Y > 0) && (time.timeAtIpOutIn > 0))"),
)

lowerGlobalMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("globalSPMuonTracks"),
    cut = cms.string("outerPosition.Y < 0"),
    #cut = cms.string("abs(innerPosition.Y) < abs(outerPosition.Y)"),
    #cut = cms.string("((outerPosition.Y < 0) && (time.timeAtIpOutIn > 0)) || ((outerPosition.Y > 0) && (time.timeAtIpOutIn > 0))"),
)

lowerTrackerMuonTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("trackerSPMuonTracks"),
    #cut = cms.string("outerPosition.Y < 0"),
    cut = cms.string("abs(innerPosition.Y) < abs(outerPosition.Y)"),
    #cut = cms.string("((outerPosition.Y < 0) && (time.timeAtIpOutIn > 0)) || ((outerPosition.Y > 0) && (time.timeAtIpOutIn > 0))"),
)


trackerSPFilter = cms.EDFilter("TrackCountFilter",
    src = cms.InputTag("trackerSPMuonTracks"),
    minNumber = cms.uint32(1)
)

cosmicTrackSPFilter = cms.EDFilter("TrackCountFilter",
    src = cms.InputTag("cosmicSPMuonTracks"),
    minNumber = cms.uint32(1)
)

globalTrackSPFilter = cms.EDFilter("TrackCountFilter",
    src = cms.InputTag("globalSPMuonTracks"),
    minNumber = cms.uint32(1)
)

# EDM Output definition
COSMICTrackoutput = 'keep *_*MuonTracks_*_*'

