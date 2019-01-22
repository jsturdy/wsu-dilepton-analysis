#!/usr/bin/env python

"""
This is a small script that does the equivalent of multicrab.
"""

import os
from optparse import OptionParser

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException


def getOptions():
    """
    Parse and return the arguments provided by the user.
    """
    usage = ("Usage: %prog --crabCmd CMD [--workArea WAR --crabCmdOpts OPTS]"
             "\nThe multicrab command executes 'crab CMD OPTS' for each project directory contained in WAR"
             "\nUse multicrab -h for help")

    parser = OptionParser(usage=usage)

    parser.add_option('-c', '--crabCmd',
                      dest = 'crabCmd',
                      default = '',
                      help = "crab command",
                      metavar = 'CMD')

    parser.add_option('-w', '--workArea',
                      dest = 'workArea',
                      default = '',
                      help = "work area directory (only if CMD != 'submit')",
                      metavar = 'WAR')

    parser.add_option('-j', '--lumiJSON',
                      dest = 'lumiJSON',
                      default = '',
                      help = "lumi JSON location (only if CMD != 'submit')",
                      metavar = 'LUMI')

    parser.add_option('-o', '--crabCmdOpts',
                      dest = 'crabCmdOpts',
                      default = '',
                      help = "options for crab command CMD",
                      metavar = 'OPTS')

    (options, arguments) = parser.parse_args()

    if arguments:
        parser.error("Found positional argument(s): %s." % (arguments))
    if not options.crabCmd:
        parser.error("(-c CMD, --crabCmd=CMD) option not provided.")
    if options.crabCmd != 'submit':
        if not options.workArea:
            parser.error("(-w WAR, --workArea=WAR) option not provided.")
        if not os.path.isdir(options.workArea):
            parser.error("'%s' is not a valid directory." % (options.workArea))

    return options


def main():

    options = getOptions()

    # The submit command needs special treatment.
    if options.crabCmd == 'submit':

        #--------------------------------------------------------
        # This is the base config:
        #--------------------------------------------------------
        from CRABClient.UserUtilities import config
        config = config()

        config.General.requestName     = None
        config.General.workArea        = options.workArea
        config.General.transferOutputs = True
        config.General.transferLogs    = False
        
        # ### TEMP FIXME BUG IN CRAB
        # config.General.instance        = 'preprod'
        ###
        config.JobType.pluginName    = 'Analysis'

        config.Data.inputDBS         = 'global'
        config.Data.inputDataset     = None
        config.Data.splitting        = None
        config.Data.outputDatasetTag = None
        config.Data.ignoreLocality   = True
        ## necessary with ignoreLocality set to true
        config.Site.whitelist        = ["T2_CH_*", "T3_US_FNALLPC"]

        ## MODIFY THIS TO POINT TO THE DESIRED OUTPUT LOCATION
        config.Data.outLFNDirBase    = '/store/user/sturdy/CosmicEndpoint/2017/Trees'

        config.Site.storageSite = 'T3_US_FNALLPC'

        # config.Site.blacklist = ['T2_EE_Estonia']
        #--------------------------------------------------------

        # Will submit one task for each of these input datasets.
        # pass in datasets as a dict {datasetname,mc/data}
        certFile = options.lumiJSON
        inputDatasetMap = {
            "MC": [
                # ## 2016 MC
                # ['/SPLooseMuCosmic_38T_p10/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RECO', None],
                # ['/SPLooseMuCosmic_38T_p100/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RECO',None],
                # ['/SPLooseMuCosmic_38T_p500/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RECO',None],

                # ## 2017 MC SIM
                # ['/SPLooseMuCosmic_38T_p10-100/RunIISummer17CosmicGS-92X_upgrade2017cosmics_realistic_deco_v10-v1/GEN-SIM', None],
                # ['/SPLooseMuCosmic_38T_p100-500/RunIISummer17CosmicGS-92X_upgrade2017cosmics_realistic_deco_v10-v1/GEN-SIM',None],
                # ['/SPLooseMuCosmic_38T_p500/RunIISummer17CosmicGS-92X_upgrade2017cosmics_realistic_deco_v10-v1/GEN-SIM',    None],
                # ['/TKCosmics_38T/RunIISummer17CosmicGS-92X_upgrade2017cosmics_realistic_deco_v10-v1/GEN-SIM',               None],
                # ['/TKCosmics_38T/RunIISummer17CosmicGS-92X_upgrade2017cosmics_realistic_deco_v10_ext1-v2/GEN-SIM',          None],

                ## 2017 MC RECO
                ['/SPLooseMuCosmic_38T_p10-100/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM-RECO',  None],
                ['/SPLooseMuCosmic_38T_p100-500/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM-RECO', None],
                ['/SPLooseMuCosmic_38T_p500/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM-RECO',     None],
                ['/TKCosmics_38T/RunIISummer17CosmicDR-DECO_92X_upgrade2017cosmics_realistic_deco_v10-v1/GEN-SIM-RECO',     None],
                # ['/TKCosmics_38T/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM-RECO',                None],
                # ['/TKCosmics_38T/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3_ext1-v2/GEN-SIM-RECO',           None],

                # ## 2018 MC SIM
                # ['/SPLooseMuCosmic_38T_p10-100/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM',  None],
                # ['/SPLooseMuCosmic_38T_p100-500/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM', None],
                # ['/SPLooseMuCosmic_38T_p500/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM',     None],
                # ['/TKCosmics_38T/RunIISpring18CosmicGS-100X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM',               None],

                # ## 2018 MC RECO
                # ['/SPLooseMuCosmic_38T_p10-100/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM-RECO',  None],
                # ['/SPLooseMuCosmic_38T_p100-500/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM-RECO', None],
                # ['/SPLooseMuCosmic_38T_p500/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM-RECO',     None],
                # ['/TKCosmics_38T/RunIISpring18CosmicDR-DECO_100X_mc2017cosmics_realistic_deco_v3-v1/GEN-SIM-RECO', None],
                # ['/TKCosmics_38T/RunIISpring18CosmicDR-PEAK_100X_mc2017cosmics_realistic_peak_v3-v1/GEN-SIM-RECO', None],

                ],
            "DATA": [
                # ## 2015 data
                # ['/Cosmics/Commissioning2015-CosmicSP-01Mar2016-v3/RAW-RECO',certFile],
                # ['/Cosmics/Commissioning2015-CosmicSP-20Jan2016-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2015A-CosmicSP-01Mar2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015B-CosmicSP-01Mar2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015B-CosmicSP-20Jan2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015C-CosmicSP-01Mar2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015C-CosmicSP-20Jan2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015C-CosmicSP-PromptReco-v1/RAW-RECO', certFile],
                # ['/Cosmics/Run2015C-CosmicSP-PromptReco-v2/RAW-RECO', certFile],
                # ['/Cosmics/Run2015C-CosmicSP-PromptReco-v3/RAW-RECO', certFile],
                # ['/Cosmics/Run2015D-CosmicSP-01Mar2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015D-CosmicSP-20Jan2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015D-CosmicSP-PromptReco-v3/RAW-RECO', certFile],
                # ['/Cosmics/Run2015D-CosmicSP-PromptReco-v4/RAW-RECO', certFile],
                # ['/Cosmics/Run2015E-CosmicSP-01Mar2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015E-CosmicSP-20Jan2016-v1/RAW-RECO',  certFile],
                # ['/Cosmics/Run2015E-CosmicSP-PromptReco-v1/RAW-RECO', certFile],
                # ['/Cosmics/HIRun2015-CosmicSP-20Jan2016-v1/RAW-RECO', certFile],
                # ['/Cosmics/HIRun2015-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ## 2016 data
                # # ['/Cosmics/Commissioning2016-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # # ['/Cosmics/Commissioning2016-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2016A-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2016A-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2016B-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2016B-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2016C-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2016D-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2016E-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2016F-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2016G-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2016H-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2016H-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2016H-CosmicSP-PromptReco-v3/RAW-RECO',certFile],
                # # ['/Cosmics/PARun2016A-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # # ['/Cosmics/PARun2016B-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # # ['/Cosmics/PARun2016C-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # # ['/Cosmics/PARun2016D-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                ## 2017 data
                ['/Cosmics/Commissioning2017-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                ['/Cosmics/Run2017A-CosmicSP-PromptReco-v1/RAW-RECO',         certFile],
                ['/Cosmics/Run2017A-CosmicSP-PromptReco-v2/RAW-RECO',         certFile],
                ['/Cosmics/Run2017A-CosmicSP-PromptReco-v3/RAW-RECO',         certFile],
                ['/Cosmics/Run2017B-CosmicSP-PromptReco-v1/RAW-RECO',         certFile],
                ['/Cosmics/Run2017B-CosmicSP-PromptReco-v2/RAW-RECO',         certFile],
                ['/Cosmics/Run2017C-CosmicSP-PromptReco-v1/RAW-RECO',         certFile],
                ['/Cosmics/Run2017C-CosmicSP-PromptReco-v2/RAW-RECO',         certFile],
                ['/Cosmics/Run2017C-CosmicSP-PromptReco-v3/RAW-RECO',         certFile],
                ['/Cosmics/Run2017D-CosmicSP-PromptReco-v1/RAW-RECO',         certFile],
                ['/Cosmics/Run2017E-CosmicSP-PromptReco-v1/RAW-RECO',         certFile],
                ['/Cosmics/Run2017F-CosmicSP-PromptReco-v1/RAW-RECO',         certFile],
                ['/Cosmics/Run2017G-CosmicSP-PromptReco-v1/RAW-RECO',         certFile],
                ['/Cosmics/Run2017H-CosmicSP-PromptReco-v1/RAW-RECO',         certFile],
                ['/Cosmics/XeXeRun2017-CosmicSP-PromptReco-v1/RAW-RECO',      certFile],
                # ## 2018 data
                # ['/Cosmics/Commissioning2018-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2018A-CosmicSP-06Jun2018-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2018A-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2018A-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2018A-CosmicSP-PromptReco-v3/RAW-RECO',certFile],
                # ['/Cosmics/Run2018B-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2018B-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2018C-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2018C-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                # ['/Cosmics/Run2018C-CosmicSP-PromptReco-v3/RAW-RECO',certFile],
                # ['/Cosmics/Run2018D-CosmicSP-PromptReco-v1/RAW-RECO',certFile],
                # ['/Cosmics/Run2018D-CosmicSP-PromptReco-v2/RAW-RECO',certFile],
                ]
            }

        for key in inputDatasetMap.keys():
            inputDatasets = None

            if key == 'DATA':
                inputDatasets = inputDatasetMap[key]
                ## MODIFY THIS TO POINT TO THE DESIRED cmsRun python config for data
                # common options: wsuMuonTree_data_reHLT_reRECO.py, wsuMuonAnalysis_data.py
                # config.JobType.psetName = 'wsuMuonAnalyzer_data_reHLT.py'
                # config.JobType.psetName = 'wsuMuonTree_data.py'
                config.JobType.psetName = 'wsuMuonAnalyzer_data.py'

                config.Data.useParent   = False
                config.Data.splitting   = 'Automatic'
                # config.Data.splitting   = 'LumiBased'
                # config.Data.unitsPerJob = 1000

            elif key == 'MC':
                inputDatasets = inputDatasetMap[key]
                config.JobType.maxMemoryMB = 4000
                ## MODIFY THIS TO POINT TO THE DESIRED cmsRun python config for MC
                # wsuMuonTree_MC_reHLT.py, wsuMuonAnalyzer_MC_reHLT.py (for rerunning RECO/HLT)
                # config.JobType.psetName = 'wsuMuonPtScaling_MC.py'
                config.JobType.psetName = 'wsuMuonAnalyzer_MC.py'
                # config.JobType.psetName = 'wsuMuonTree_MC.py'

                # True if the GEN-SIM dataset is available and running a re-reco, false otherwise
                config.Data.useParent   = False
                config.Data.splitting   = 'Automatic'
                # config.Data.splitting   = 'FileBased'
                # config.Data.unitsPerJob = 1
                pass

            for inDS in inputDatasets:
                print "Key: %s - Creating config for for input dataset %s" % (key,inDS[0])
                # inDS is of the form /A/B/C. Since B is unique for each inDS, use this in the CRAB request name.
                if key == 'DATA':
                    config.General.requestName = inDS[0].split('/')[2]
                else:
                    config.General.requestName = "%s_%s"%(inDS[0].split('/')[2],inDS[0].split('/')[1])
                    pass
                print config.General.workArea
                print config.General.requestName
                config.Data.inputDataset = inDS[0]
                config.Data.outputDatasetTag = '%s_%s' % (config.General.workArea, config.General.requestName)
                #if key == 'DATA':
                config.Data.lumiMask = inDS[1]
                #pass
                # Submit.
                try:
                    print "Submitting for input dataset %s" % (inDS[0])
                    print config
                    crabCommand(options.crabCmd, config = config, *options.crabCmdOpts.split())
                except HTTPException as hte:
                    print "Submission for input dataset %s failed: %s" % (inDS[0], hte.headers)
                except ClientException as cle:
                    print "Submission for input dataset %s failed: %s" % (inDS[0], cle)

    # All other commands can be simply executed.
    elif options.workArea:

        for dir in os.listdir(options.workArea):
            projDir = os.path.join(options.workArea, dir)
            if not  os.path.isdir(projDir):
                continue
            # Execute the crab command.
            msg = "Executing (the equivalent of): crab %s --dir %s %s" % (options.crabCmd, projDir, options.crabCmdOpts)
            print "-"*len(msg)
            print msg
            print "-"*len(msg)
            try:
                crabCommand(options.crabCmd, dir = projDir, *options.crabCmdOpts.split())
            except HTTPException as hte:
                print "Failed executing command %s for task %s: %s" % (options.crabCmd, projDir, hte.headers)
            except ClientException as cle:
                print "Failed executing command %s for task %s: %s" % (options.crabCmd, projDir, cle)


if __name__ == '__main__':
    main()
