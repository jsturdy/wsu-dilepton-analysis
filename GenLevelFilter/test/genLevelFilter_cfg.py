import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.register('sampleType',
                '',
                VarParsing.multiplicity.singleton,
                VarParsing.varType.string,
                "Type of sample.")

options.parseArguments()

process = cms.Process('NTUPLEPROCESS')
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

sample = options.sampleType.split('_')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('%s_ntuple.root'%(options.sampleType))
)

massBins = ["M300","M800","M1300","M2000"]
if not "ConLL" in sample[3]:
    massBins = massBins[:-1]
lowerCut = sample[1][1:]
upperCut = 1e10
try:
    val = cms.double(lowerCut)
except:
    lowerCut = 0

for i,b in enumerate(massBins):
    if lowerCut == b[1:] and i != (len(massBins)-1):
        upperCut = massBins[i+1][1:]
        continue

import cPickle as pickle
weight = 1
with open("ci_xsec_data.pkl","rb") as pkl:
    sdict = pickle.load(pkl)
    # pickle dict is:
    #  DY samples:
    #     d[sample]["M%d"%(mass)]
    #  CI samples:
    #     d[sample]["Lam%s"%(lval)][infm][heli]["M%s"%(mass)]
    # Data is structured as:
    #{
    #  'minCut': minCut,
    #  'xsec': [xs_val, xs_err, xs_unit],
    #  'maxCut': maxCut,
    #  'cutEfficiency': [n_pass, n_fail]
    #}
    sample = options.sampleType.split('_')
    if "DY" in sample[0]:
        xsdict = sdict[args.xsdict]
    elif "CI" in sample[0]:
        special = sample[3].split("TeV")
        lval   = special[0]
        infm   = special[1][:-2]
        heli   = special[1][-2:]
        mass   = sample[1][1:]
        xsdict = sdict[sample[0]]["%s"%(lval)][infm][heli]["M%s"%(mass)]
        print(sample[0],"%s"%(lval),infm,heli,"M%s"%(mass))
    if xsdict:
        weight = xsdict["xsec"][0]
    else:
        weight = 1.
    pass
print weight

from WSUDiLeptons.GenLevelFilter.genLevelFilter_cfi import genLevelFilter
process.genweightfilter = genLevelFilter.clone(
    filterevent  = cms.bool(False),
    filterPreFSR = cms.bool(False),
    debug        = cms.bool(False),
    minCut       = cms.double(lowerCut),
    sampleType   = cms.string(sample[0]),
    maxCut       = cms.double(upperCut),
    xsWeight     = cms.double(weight),
)

from WSUDiLeptons.GenLevelFilter.genFilterReader_cfi import genFilterReader
process.genweightreader = genFilterReader.clone(
    mInvCutSource       = cms.InputTag("genweightfilter","passMassCut"),
    preFSRmInvCutSource = cms.InputTag("genweightfilter","passPreFSRMassCut"),
    weightSource        = cms.InputTag("genweightfilter","xsWeight"),
)

secFiles = cms.untracked.vstring()
process.source = cms.Source ("PoolSource",
    fileNames          = cms.untracked.vstring(options.inputFiles),
    secondaryFileNames = secFiles
)

process.filt  = cms.Path(process.genweightfilter+process.genweightreader)# other processes accepting this filter)

# other paths
process.schedule = cms.Schedule(process.filt) #, other paths)
