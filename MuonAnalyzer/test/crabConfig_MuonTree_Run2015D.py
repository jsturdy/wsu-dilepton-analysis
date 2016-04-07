from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = 'MuonEfficiencyTree_Run2015D_Apr07'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'wsuMuonTree_data.py'

config.section_('Data')
config.Data.inputDataset = '/Cosmics/Run2015D-CosmicSP-20Jan2016-v1/RAW-RECO'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 75
config.Data.lumiMask = 'https://cmsdoc.cern.ch/~sturdy/Cosmics/JSON/21.03.2016/cosmics_Run2015_all_pix_strip_DT_RPC_complete.json'
config.Data.allowNonValidInputDataset = True
#config.Data.publication = True
config.Data.outLFNDirBase = '/store/user/sturdy/MuonEfficiency'
config.Data.outputDatasetTag = 'MuonEfficiencyTree_Run2015D_Apr07'

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
