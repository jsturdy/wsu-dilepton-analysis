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

        config.General.requestName = None
        config.General.workArea = options.workArea
        config.General.transferOutputs = True
        config.General.transferLogs = False
                
        config.JobType.pluginName = 'Analysis'

        config.Data.inputDBS         = 'global'
        config.Data.inputDataset     = None
        config.Data.splitting        = None
        config.Data.outputDatasetTag = None

        config.Data.outLFNDirBase = '/store/user/sturdy/MuonEfficiency'

        config.Site.storageSite = 'T3_US_FNALLPC'
        #--------------------------------------------------------

        # Will submit one task for each of these input datasets.
        # pass in datasets as a dict {datasetname,mc/data}
        inputDatasetMap = {
            "MC": [
                ##'/SPLooseMuCosmic_38T_p10/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RAW',
                ##'/SPLooseMuCosmic_38T_p100/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RAW',
                ##'/SPLooseMuCosmic_38T_p500/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RAW',
                #'/SPLooseMuCosmic_38T_p10/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RECO',
                #'/SPLooseMuCosmic_38T_p100/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RECO',
                #'/SPLooseMuCosmic_38T_p500/CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1/GEN-SIM-RECO',
                ],
            "DATA": [
                ['/Cosmics/Commissioning2016-CosmicSP-PromptReco-v1/RAW-RECO','https://cmsdoc.cern.ch/~sturdy/Cosmics/JSON/Cosmics2016/cosmics_Run2016_json_pix_strip_DT_DCSOnly.json'],
                ['/Cosmics/Commissioning2016-CosmicSP-PromptReco-v2/RAW-RECO','https://cmsdoc.cern.ch/~sturdy/Cosmics/JSON/Cosmics2016/cosmics_Run2016_json_pix_strip_DT_DCSOnly.json'],
                ['/Cosmics/Run2016A-CosmicSP-PromptReco-v1/RAW-RECO','https://cmsdoc.cern.ch/~sturdy/Cosmics/JSON/Cosmics2016/cosmics_CRAFT16_json_pix_strip_DT_DCSOnly.json'],
                ['/Cosmics/Run2016A-CosmicSP-PromptReco-v2/RAW-RECO','https://cmsdoc.cern.ch/~sturdy/Cosmics/JSON/Cosmics2016/cosmics_CRAFT16_json_pix_strip_DT_DCSOnly.json'],
                ['/Cosmics/Run2016B-CosmicSP-PromptReco-v1/RAW-RECO','https://cmsdoc.cern.ch/~sturdy/Cosmics/JSON/Cosmics2016/cosmics_CRAFT16_json_pix_strip_DT_DCSOnly.json'],
                ['/Cosmics/Run2016B-CosmicSP-PromptReco-v2/RAW-RECO','https://cmsdoc.cern.ch/~sturdy/Cosmics/JSON/Cosmics2016/cosmics_CRAFT16_json_pix_strip_DT_DCSOnly.json'],
                ]
            }

        for key in inputDatasetMap.keys():
            inputDatasets = None
            
            if key == 'DATA':
                inputDatasets = inputDatasetMap[key]
                config.JobType.psetName = 'wsuMuonTree_data.py'
                
                config.Data.splitting = 'LumiBased'
                config.Data.unitsPerJob = 250

            elif key == 'MC':
                inputDatasets = inputDatasetMap[key]
                config.JobType.psetName = 'wsuMuonTree_MC.py'
                
                config.Data.splitting = 'FileBased'
                config.Data.unitsPerJob = 5
                
            for inDS in inputDatasets:
                # inDS is of the form /A/B/C. Since B is unique for each inDS, use this in the CRAB request name.
                config.General.requestName = inDS[0].split('/')[2]
                config.Data.inputDataset = inDS[0]
                config.Data.outputDatasetTag = '%s_%s' % (config.General.workArea, config.General.requestName)
                config.Data.lumiMask = inDS[1]
                # Submit.
                try:
                    print "Submitting for input dataset %s" % (inDS[0])
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
