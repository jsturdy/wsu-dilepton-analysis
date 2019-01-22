#!/bin/bash

#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/SPLooseMuCosmic_38T_p10/MuonEfficiencyTree_startup_peak_p10_Apr07/160407_161719/0000/   |fgrep root>& samplesLists_data/all_startup_peak_p10_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/SPLooseMuCosmic_38T_p100/MuonEfficiencyTree_startup_peak_p100_Apr07/160407_161739/0000/ |fgrep root>& samplesLists_data/all_startup_peak_p100_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/SPLooseMuCosmic_38T_p500/MuonEfficiencyTree_startup_peak_p500_Apr07/160407_161756/0000/ |fgrep root>& samplesLists_data/all_startup_peak_p500_trees_v5.txt
#
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/SPLooseMuCosmic_38T_p10/MuonEfficiencyTree_asym_deco_p10_Apr07/160407_161638/0000/   |fgrep root>& samplesLists_data/all_asymptotic_deco_p10_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/SPLooseMuCosmic_38T_p100/MuonEfficiencyTree_asym_deco_p100_Apr07/160407_161652/0000/ |fgrep root>& samplesLists_data/all_asymptotic_deco_p100_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/SPLooseMuCosmic_38T_p500/MuonEfficiencyTree_asym_deco_p500_Apr07/160407_161706/0000/ |fgrep root>& samplesLists_data/all_asymptotic_deco_p500_trees_v5.txt
#
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/MuonEfficiencyTree_CRAFT15_Apr07/160407_161538/0000/          |fgrep root>&  samplesLists_data/all_craft15_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/MuonEfficiencyTree_CRAFT15_Apr07_recovery/160410_211038/0000  |fgrep root>>& samplesLists_data/all_craft15_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/MuonEfficiencyTree_Run2015B_Apr07/160407_161250/0000/         |fgrep root>&  samplesLists_data/all_run2015b_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/MuonEfficiencyTree_Run2015C_Apr07/160407_161552/0000/         |fgrep root>&  samplesLists_data/all_run2015c_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/MuonEfficiencyTree_Run2015C_Apr07_recovery/160410_211052/0000 |fgrep root>>& samplesLists_data/all_run2015c_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/MuonEfficiencyTree_Run2015D_Apr07/160407_161606/0000/         |fgrep root>&  samplesLists_data/all_run2015d_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/MuonEfficiencyTree_Run2015D_Apr07_recovery/160410_211104/0000 |fgrep root>>& samplesLists_data/all_run2015d_trees_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/MuonEfficiencyTree_Run2015E_Apr07/160407_161622/0000/         |fgrep root>&  samplesLists_data/all_run2015e_trees_v5.txt
#
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics/MuonAnalysis_data_Apr_2016/160408_171105/0000 |fgrep root>& samplesLists_data/shawn_craft15_p100_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics/MuonAnalysis_data_Apr_2016/160407_192341/0000 |fgrep root>& samplesLists_data/shawn_run2015b_p100_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics/MuonAnalysis_data_Apr_2016/160407_192652/0000 |fgrep root>& samplesLists_data/shawn_run2015c_p100_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics/MuonAnalysis_data_Apr_2016/160407_192617/0000 |fgrep root>& samplesLists_data/shawn_run2015d_p100_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics/MuonAnalysis_data_Apr_2016/160407_192518/0000 |fgrep root>& samplesLists_data/shawn_run2015e_p100_v5.txt
#
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/SPLooseMuCosmic_38T_p500/MuonAnalysis_data_Apr_2016/160407_192453/0000 |fgrep root>& samplesLists_data/shawn_asym_deco_p500_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/SPLooseMuCosmic_38T_p500/MuonAnalysis_data_Apr_2016/160407_192241/0000 |fgrep root>& samplesLists_data/shawn_startup_peak_p500_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/SPLooseMuCosmic_38T_p100/MuonAnalysis_data_Apr_2016/160407_192222/0000 |fgrep root>& samplesLists_data/shawn_asym_deco_p100_v5.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/SPLooseMuCosmic_38T_p100/MuonAnalysis_data_Apr_2016/160407_192309/0000 |fgrep root>& samplesLists_data/shawn_startup_peak_p100_v5.txt

#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/crab_projects_aug09_Run2016B-CosmicSP-PromptReco-v1/160809_194844/0000 |fgrep root >&  samplesLists_data/all_run2016b_v1_trees_2016_v2.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/crab_projects_aug09_Run2016B-CosmicSP-PromptReco-v1/160810_171234/0000 |fgrep root >>& samplesLists_data/all_run2016b_v1_trees_2016_v2.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/crab_projects_aug09_Run2016B-CosmicSP-PromptReco-v2/160809_194852/0000 |fgrep root >&  samplesLists_data/all_run2016b_v2_trees_2016_v2.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/crab_projects_aug09_Run2016B-CosmicSP-PromptReco-v2/160810_171000/0000 |fgrep root >>& samplesLists_data/all_run2016b_v2_trees_2016_v2.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/crab_projects_aug09_Run2016C-CosmicSP-PromptReco-v2/160809_194900/0000 |fgrep root >&  samplesLists_data/all_run2016c_v2_trees_2016_v2.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/crab_projects_aug09_Run2016D-CosmicSP-PromptReco-v2/160809_194908/0000 |fgrep root >&  samplesLists_data/all_run2016d_v2_trees_2016_v2.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/crab_projects_aug09_Run2016E-CosmicSP-PromptReco-v2/160809_194917/0000 |fgrep root >&  samplesLists_data/all_run2016e_v2_trees_2016_v2.txt
#gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonEfficiency/Cosmics/crab_projects_aug09_Run2016F-CosmicSP-PromptReco-v1/160809_194925/0000 |fgrep root >&  samplesLists_data/all_run2016f_v1_trees_2016_v2.txt

# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/SPLooseMuCosmic_38T_p10/MuonAnalysis_data_Aug_2016/160804_155948/0000 |fgrep root>& samplesLists_data/shawn_asym_deco_2016_p10_v1.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/SPLooseMuCosmic_38T_p100/MuonAnalysis_data_Aug_2016/160804_160007/0000 |fgrep root>& samplesLists_data/shawn_asym_deco_2016_p100_v1.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/SPLooseMuCosmic_38T_p500/MuonAnalysis_data_Aug_2016/160804_160041/0000 |fgrep root>& samplesLists_data/shawn_asym_deco_2016_p500_v1.txt

# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics2016/Cosmics/crab_projects_Run2016B-CosmicSP-PromptReco-v1/160801_161420/0000 |fgrep root>& samplesLists_data/shawn_shawn_run2016bv1_v1.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics2016/Cosmics/crab_projects_Run2016B-CosmicSP-PromptReco-v2/160801_161429/0000 |fgrep root>& samplesLists_data/shawn_shawn_run2016bv2_v1.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics2016/Cosmics/crab_projects_Run2016C-CosmicSP-PromptReco-v2/160801_161437/0000 |fgrep root>& samplesLists_data/shawn_shawn_run2016cv2_v1.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics2016/Cosmics/crab_projects_Run2016D-CosmicSP-PromptReco-v2/160801_161445/0000 |fgrep root>& samplesLists_data/shawn_shawn_run2016dv2_v1.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics2016/Cosmics/Cosmics/crab_projects_Sep_Run2016B-CosmicSP-PromptReco-v1/160921_192603/0000 |fgrep root>& samplesLists_data/shawn_shawn_run2016bv1_v2.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/szaleski/Cosmics2016/Cosmics/Cosmics/crab_projects_Sep_Run2016B-CosmicSP-PromptReco-v2/160921_192612/0000 |fgrep root>& samplesLists_data/shawn_shawn_run2016bv2_v2.txt

# done #gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016B-CosmicSP-PromptReco-v1/161111_181444/0000 |fgrep root >&  samplesLists_data/all_run2016b_v1_trees_2016_reRECO.txt
# done #gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016B-CosmicSP-PromptReco-v2/161111_181501/0000 |fgrep root >&  samplesLists_data/all_run2016b_v2_trees_2016_reRECO.txt
# done #gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016C-CosmicSP-PromptReco-v2/161111_181521/0000 |fgrep root >&  samplesLists_data/all_run2016c_v2_trees_2016_reRECO.txt
# done #gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016D-CosmicSP-PromptReco-v2/161111_181530/0000 |fgrep root >&  samplesLists_data/all_run2016d_v2_trees_2016_reRECO.txt
# done #gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016E-CosmicSP-PromptReco-v2/161111_181540/0000 |fgrep root >&  samplesLists_data/all_run2016e_v2_trees_2016_reRECO.txt

# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016F-CosmicSP-PromptReco-v1/161111_181548/0000 |fgrep root >&  samplesLists_data/all_run2016f_v1_trees_2016_reRECO.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016G-CosmicSP-PromptReco-v1/161111_181557/0000 |fgrep root >&  samplesLists_data/all_run2016g_v1_trees_2016_reRECO.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016H-CosmicSP-PromptReco-v1/161111_181607/0000 |fgrep root >&  samplesLists_data/all_run2016h_v1_trees_2016_reRECO.txt
# done #gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016H-CosmicSP-PromptReco-v2/161111_181617/0000 |fgrep root >&  samplesLists_data/all_run2016h_v2_trees_2016_reRECO.txt

# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/CosmicEndpoint/2016/Trees/SPLooseMuCosmic_38T_p10/crab_projects_endpoint_nov28_CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1_SPLooseMuCosmic_38T_p10//0000  |fgrep root" > samplesLists_data/shawn_asym_deco_2016_p10_reRECO_endpoint.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/CosmicEndpoint/2016/Trees/SPLooseMuCosmic_38T_p10/crab_projects_endpoint_nov28_CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1_SPLooseMuCosmic_38T_p10//0000  |fgrep root>>& samplesLists_data/shawn_asym_deco_2016_p10_reRECO_endpoint.txt
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/CosmicEndpoint/2016/Trees/SPLooseMuCosmic_38T_p100/crab_projects_endpoint_nov28_CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1_SPLooseMuCosmic_38T_p100/161208_165535/0000 |fgrep root" > samplesLists_data/shawn_asym_deco_2016_p100_reRECO_endpoint.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/CosmicEndpoint/2016/Trees/SPLooseMuCosmic_38T_p100/crab_projects_endpoint_nov28_CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1_SPLooseMuCosmic_38T_p100/161208_165535/0000 |fgrep root>>& samplesLists_data/shawn_asym_deco_2016_p100_reRECO_endpoint.txt
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/CosmicEndpoint/2016/Trees/SPLooseMuCosmic_38T_p500/crab_projects_endpoint_nov28_CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1_SPLooseMuCosmic_38T_p500/161128_181015/0000 |fgrep root" > samplesLists_data/shawn_asym_deco_2016_p500_reRECO_endpoint.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/CosmicEndpoint/2016/Trees/SPLooseMuCosmic_38T_p500/crab_projects_endpoint_nov28_CosmicSpring16DR80-DECO_80X_mcRun2cosmics_asymptotic_deco_v0-v1_SPLooseMuCosmic_38T_p500/161128_181015/0000 |fgrep root>>& samplesLists_data/shawn_asym_deco_2016_p500_reRECO_endpoint.txt

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016B-CosmicSP-PromptReco-v1/170120_222316/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016b_v1_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016b_v1_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016b_v1_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016b_v1_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016b_v1_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016b_v1_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016b_v1_trees_2016_reRECO_endpoint_jan20.tmp

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016B-CosmicSP-PromptReco-v2/170120_222330/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016b_v2_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016b_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016b_v2_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016b_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016b_v2_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016b_v2_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016b_v2_trees_2016_reRECO_endpoint_jan20.tmp

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016C-CosmicSP-PromptReco-v2/170120_222342/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016c_v2_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016c_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016c_v2_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016c_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016c_v2_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016c_v2_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016c_v2_trees_2016_reRECO_endpoint_jan20.tmp

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016D-CosmicSP-PromptReco-v2/170120_222354/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016d_v2_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016d_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016d_v2_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016d_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016d_v2_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016d_v2_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016d_v2_trees_2016_reRECO_endpoint_jan20.tmp

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016E-CosmicSP-PromptReco-v2/170120_222404/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016e_v2_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016e_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016e_v2_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016e_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016e_v2_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016e_v2_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016e_v2_trees_2016_reRECO_endpoint_jan20.tmp

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016F-CosmicSP-PromptReco-v1/170120_222414/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016f_v1_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016f_v1_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016f_v1_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016f_v1_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016f_v1_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016f_v1_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016f_v1_trees_2016_reRECO_endpoint_jan20.tmp

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016G-CosmicSP-PromptReco-v1/170120_222423/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016g_v1_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016g_v1_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016g_v1_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016g_v1_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016g_v1_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016g_v1_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016g_v1_trees_2016_reRECO_endpoint_jan20.tmp

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016H-CosmicSP-PromptReco-v1/170120_222432/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016h_v1_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016h_v1_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016h_v1_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016h_v1_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016h_v1_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016h_v1_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016h_v1_trees_2016_reRECO_endpoint_jan20.tmp

# EOSDIR="/store/user/sturdy/CosmicEndpoint/2016/Trees/Cosmics/crab_projects_endpoint_jan20_Run2016H-CosmicSP-PromptReco-v2/170120_222448/0000"
# echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root >&  samplesLists_data/all_run2016h_v2_trees_2016_reRECO_endpoint_jan20.tmp
# echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_run2016h_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016h_v2_trees_2016_reRECO_endpoint_jan20.txt"
# sed "s,^,$EOSDIR/," samplesLists_data/all_run2016h_v2_trees_2016_reRECO_endpoint_jan20.tmp > samplesLists_data/all_run2016h_v2_trees_2016_reRECO_endpoint_jan20.txt
# echo "rm samplesLists_data/all_run2016h_v2_trees_2016_reRECO_endpoint_jan20.tmp"
# rm samplesLists_data/all_run2016h_v2_trees_2016_reRECO_endpoint_jan20.tmp

basedir="/store/user/sturdy/CosmicEndpoint/2017/Trees"

pds=(
    "Cosmics"
    "SPLooseMuCosmic_38T_p10-100"
    "SPLooseMuCosmic_38T_p100-500"
    "SPLooseMuCosmic_38T_p500"
)

samples=(
    "Cosmics/Commissioning2017-CosmicSP-PromptReco-v1"
    "Cosmics/Run2017A-CosmicSP-PromptReco-v1"
    "Cosmics/Run2017A-CosmicSP-PromptReco-v2"
    "Cosmics/Run2017A-CosmicSP-PromptReco-v3"
    "Cosmics/Run2017B-CosmicSP-PromptReco-v1"
    "Cosmics/Run2017B-CosmicSP-PromptReco-v2"
    "Cosmics/Run2017C-CosmicSP-PromptReco-v1"
    "Cosmics/Run2017C-CosmicSP-PromptReco-v2"
    "Cosmics/Run2017C-CosmicSP-PromptReco-v3"
    "Cosmics/Run2017D-CosmicSP-PromptReco-v1"
    "Cosmics/Run2017E-CosmicSP-PromptReco-v1"
    "Cosmics/Run2017F-CosmicSP-PromptReco-v1"
    "Cosmics/Run2017G-CosmicSP-PromptReco-v1"
    "Cosmics/Run2017H-CosmicSP-PromptReco-v1"
    "Cosmics/XeXeRun2017-CosmicSP-PromptReco-v1"
    "SPLooseMuCosmic_38T_p10-100/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1"
    "SPLooseMuCosmic_38T_p100-500/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1"
    "SPLooseMuCosmic_38T_p500/RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1"
)

request="endpoint2017_trees_10sep18"
# always prefixed by crab_projects_
crabdir="crab_projects_${request}"
# EOS dirs will be: base/PD/datadir/date/0000
# datadir will be crabdir_samplename

datadirs=(
    # "crab_projects_endpoint2017_trees_10sep18_Commissioning2017-CosmicSP-PromptReco-v1/180910_172938"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017A-CosmicSP-PromptReco-v1/180910_172955"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017A-CosmicSP-PromptReco-v2/180910_173012"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017C-CosmicSP-PromptReco-v1/180910_173130"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017F-CosmicSP-PromptReco-v1/180910_173319"

    ## crab_projects_endpoint2017_trees_10sep18
    # "crab_projects_endpoint2017_trees_10sep18_Commissioning2017-CosmicSP-PromptReco-v1/180910_172938"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017A-CosmicSP-PromptReco-v1/180910_172955"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017A-CosmicSP-PromptReco-v2/180910_173012"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017A-CosmicSP-PromptReco-v3/180913_162535"
    # # "crab_projects_endpoint2017_trees_10sep18_Run2017B-CosmicSP-PromptReco-v1/180913_162552"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017B-CosmicSP-PromptReco-v2/180913_162608"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017C-CosmicSP-PromptReco-v1/180910_173130"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017C-CosmicSP-PromptReco-v2/180913_162624"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017C-CosmicSP-PromptReco-v3/180913_162641"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017D-CosmicSP-PromptReco-v1/180913_162657"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017E-CosmicSP-PromptReco-v1/180913_162714"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017F-CosmicSP-PromptReco-v1/180910_173319"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017G-CosmicSP-PromptReco-v1/180916_084714"
    # "crab_projects_endpoint2017_trees_10sep18_Run2017H-CosmicSP-PromptReco-v1/180916_084734"

    ## crab_projects_cosmicendpoint2017_trees_09jan19
    "crab_projects_cosmicendpoint2017_trees_09jan19_Commissioning2017-CosmicSP-PromptReco-v1/190109_151604"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017A-CosmicSP-PromptReco-v1/190109_151620"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017A-CosmicSP-PromptReco-v2/190109_151635"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017A-CosmicSP-PromptReco-v3/190109_151650"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017B-CosmicSP-PromptReco-v1/190109_133759"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017B-CosmicSP-PromptReco-v2/190109_133818"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017C-CosmicSP-PromptReco-v1/190109_133833"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017C-CosmicSP-PromptReco-v2/190109_133848"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017C-CosmicSP-PromptReco-v3/190109_133903"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017D-CosmicSP-PromptReco-v1/190109_133917"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017E-CosmicSP-PromptReco-v1/190109_133932"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017F-CosmicSP-PromptReco-v1/190109_133947"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017G-CosmicSP-PromptReco-v1/190109_134002"
    "crab_projects_cosmicendpoint2017_trees_09jan19_Run2017H-CosmicSP-PromptReco-v1/190109_134017"

)
mcdirs=(
    # "crab_projects_endpoint2017_trees_10sep18_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p10-100/180910_173440"
    # "crab_projects_endpoint2017_trees_10sep18_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p100-500/180910_173458"
    # "crab_projects_endpoint2017_trees_10sep18_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p500/180910_173517"

    # "SPLooseMuCosmic_38T_p10-100/crab_projects_endpoint2017_trees_10sep18_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p10-100/180910_173440"
    # "SPLooseMuCosmic_38T_p100-500/crab_projects_endpoint2017_trees_10sep18_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p100-500/180910_173458"
    # "SPLooseMuCosmic_38T_p500/crab_projects_endpoint2017_trees_10sep18_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p500/180910_173517"

    "TKCosmics_38T/crab_projects_cosmicendpoint2017_trees_09jan19_RunIISummer17CosmicDR-DECO_92X_upgrade2017cosmics_realistic_deco_v10-v1_TKCosmics_38T/190109_134132"
    "SPLooseMuCosmic_38T_p10-100/crab_projects_cosmicendpoint2017_trees_09jan19_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p10-100/190109_134046"
    "SPLooseMuCosmic_38T_p100-500/crab_projects_cosmicendpoint2017_trees_09jan19_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p100-500/190109_134102"
    "SPLooseMuCosmic_38T_p500/crab_projects_cosmicendpoint2017_trees_09jan19_RunIISummer17CosmicDR-94X_mc2017cosmics_realistic_deco_v3-v1_SPLooseMuCosmic_38T_p500/190109_134117"
)

# procname is used for local processing and will be
# - run<year><period>_<version>_<request> for data
# - <conditions>_<pbin>_<request> for MC
procnames=(
    # run2016h_v2_trees_2016_reRECO_endpoint_jan20
    # asym_deco_2016_p500_reRECO_endpoint_jan20
    commissioning2017_v1_cosmicendpoint2017_trees_09jan19
    run2017a_v1_cosmicendpoint2017_trees_09jan19
    run2017a_v2_cosmicendpoint2017_trees_09jan19
    run2017a_v3_cosmicendpoint2017_trees_09jan19
    run2017b_v1_cosmicendpoint2017_trees_09jan19
    run2017b_v2_cosmicendpoint2017_trees_09jan19
    run2017c_v1_cosmicendpoint2017_trees_09jan19
    run2017c_v2_cosmicendpoint2017_trees_09jan19
    run2017c_v3_cosmicendpoint2017_trees_09jan19
    run2017d_v1_cosmicendpoint2017_trees_09jan19
    run2017e_v1_cosmicendpoint2017_trees_09jan19
    run2017f_v1_cosmicendpoint2017_trees_09jan19
    run2017g_v1_cosmicendpoint2017_trees_09jan19
    run2017h_v1_cosmicendpoint2017_trees_09jan19
    # run2017x_v1_cosmicendpoint2017_trees_09jan19
    realistic_deco_tkcosmics_cosmicendpoint2017_trees_09jan19
    realistic_deco_p10-100_cosmicendpoint2017_trees_09jan19
    realistic_deco_p100-500_cosmicendpoint2017_trees_09jan19
    realistic_deco_p500_cosmicendpoint2017_trees_09jan19
)

i=0

for d in ${datadirs[@]}
do
    sname=${procnames[$i]}
    EOSDIR="${basedir}/Cosmics/${d}/0000"
    echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
    gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/${EOSDIR} |fgrep root >&  samplesLists_data/all_${sname}.tmp
    echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_${sname}.tmp > samplesLists_data/all_${sname}.txt"
    sed "s,^,$EOSDIR/," samplesLists_data/all_${sname}.tmp > samplesLists_data/all_${sname}.txt
    echo "rm samplesLists_data/all_${sname}.tmp"
    rm samplesLists_data/all_${sname}.tmp
    ((i++))
done

for mc in ${mcdirs[@]}
do
    sname=${procnames[$i]}
    EOSDIR="${basedir}/${mc}/0000"
    echo "gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms${EOSDIR} |fgrep root"
    gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/${EOSDIR} |fgrep root >&  samplesLists_data/all_${sname}.tmp
    echo "sed \"s,^,$EOSDIR/,\" samplesLists_data/all_${sname}.tmp > samplesLists_data/all_${sname}.txt"
    sed "s,^,$EOSDIR/," samplesLists_data/all_${sname}.tmp > samplesLists_data/all_${sname}.txt
    echo "rm samplesLists_data/all_${sname}.tmp"
    rm samplesLists_data/all_${sname}.tmp
    ((i++))
done

# # broken as gfal-ls does not behave as lcg-ls
# #perl -pi -e 's/\/eos\/uscms\/store/\/store/g' samplesLists_data/*_2016*v?.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016G-CosmicSP-PromptReco-v1/161111_181557/0000 |fgrep root >&  samplesLists_data/all_run2016g_v1_trees_2016_reRECO.txt
# gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016H-CosmicSP-PromptReco-v1/161111_181607/0000 |fgrep root >&  samplesLists_data/all_run2016h_v1_trees_2016_reRECO.txt
# done #gfal-ls --verbose -4 srm://cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos/uscms/store/user/sturdy/MuonTrees/Cosmics/crab_projects_nov12_Run2016H-CosmicSP-PromptReco-v2/161111_181617/0000 |fgrep root >&  samplesLists_data/all_run2016h_v2_trees_2016_reRECO.txt

# broken as gfal-ls does not behave as lcg-ls
#perl -pi -e 's/\/eos\/uscms\/store/\/store/g' samplesLists_data/*_2016*v?.txt
