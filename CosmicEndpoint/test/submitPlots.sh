#!/bin/bash

#./bsubSubmit.py -h
#Usage: bsubSubmit.py [options]
#
#Options:
#  -h, --help            show this help message and exit
#  -n njobs, --njobs=njobs
#                        [OPTIONAL] Number of jobs to submit (default is 10)
#  -g, --gridproxy       [OPTIONAL] Generate a GRID proxy
#  -i infiles, --infiles=infiles
#                        [REQUIRED] Text file with list of input files to
#                        process
#  -t title, --title=title
#                        [REQUIRED] Task title
#  -x tool, --tool=tool  [REQUIRED] Tool name (default is Plot)
#  -d, --debug           [OPTIONAL] Run in debug mode, i.e., don't submit jobs,
#                        just create them
#  -m maxbias, --maxbias=maxbias
#                        [OPTIONAL] Maximum bias in the curvature to inject in
#                        units of c/GeV (default = 0.0008)
#  -a, --asymmetric      [OPTIONAL] Specify whether to create asymmetric
#                        (absolute value) curvature (default = False)
#  -p minpt, --minpt=minpt
#                        [OPTIONAL] Minimum pT cut to apply to the muons
#                        (default = 50.)
#  -b nbiasbins, --nbiasbins=nbiasbins
#                        [OPTIONAL] Number of steps to vary the injected bias
#                        by (default = 200)
#  --trigger             [OPTIONAL] Apply or not the fake L1SingleMu selection
#  --mc                  [OPTIONAL] Whether or not running on MC
#  --closure             [OPTIONAL] Whether or not to produce closure histograms
#  --simlow=simlow       [OPTIONAL] Minimum pT cut to apply to the sim tracks
#                        (only for MC)
#  --simhigh=simhigh     [OPTIONAL] Maximum pT cut to apply to sim trkcs (only
#                        for MC)

#-n50 -m 0.0008 -b 200 -p 50 -t asym_p100_test -x Plot --trigger --mc --simlow 100 --simhigh 500

### Closure tests
# ./bsubSubmit.py -i shawn_startup_peak_p100_v5.txt -t oct16_thresh04 -n15 -m0.0016 -b400 -p75 --trigger --mc --closure --simlow 0   --simhigh 500000000000
# ./bsubSubmit.py -i shawn_startup_peak_p500_v5.txt -t oct16_thresh04 -n15 -m0.0016 -b400 -p75 --trigger --mc --closure --simlow 500 --simhigh -1
# ./bsubSubmit.py -i shawn_startup_peak_p100_v5.txt -t oct16_thresh10 -n15 -m0.0016 -b400 -p75 --trigger --mc --closure --simlow 0   --simhigh 500000000000 --pseudoThresh=0.1
# ./bsubSubmit.py -i shawn_startup_peak_p500_v5.txt -t oct16_thresh10 -n15 -m0.0016 -b400 -p75 --trigger --mc --closure --simlow 500 --simhigh -1           --pseudoThresh=0.1
# ./bsubSubmit.py -i shawn_startup_peak_p100_v5.txt -t sep21_thresh25 -n15 -m0.0008 -b400 -p75 --trigger --mc --closure --simlow 0   --simhigh 500000000000 --pseudoThresh=0.25
# ./bsubSubmit.py -i shawn_startup_peak_p500_v5.txt -t sep21_thresh25 -n15 -m0.0008 -b400 -p75 --trigger --mc --closure --simlow 500 --simhigh -1           --pseudoThresh=0.25

mc2016=(
    "shawn_startup_peak_p100_v5.txt"
    "shawn_startup_peak_p500_v5.txt"
    "shawn_asym_deco_p100_v5.txt"
    "shawn_asym_deco_p500_v5.txt"
)

mc2016=(
    # "asymptotic_deco_p10_2016_reRECO_endpoint.txt"
    "asymptotic_deco_p100_2016_reRECO_endpoint.txt"
    "asymptotic_deco_p500_2016_reRECO_endpoint.txt"
)

data2015=(
    "shawn_craft15_p100_v5.txt"
    "shawn_run2015b_p100_v5.txt"
    "shawn_run2015c_p100_v5.txt"
    "shawn_run2015d_p100_v5.txt"
    "shawn_run2015e_p100_v5.txt"
)

data2016=(
    "all_run2016b_v1_trees_2016_reRECO_endpoint_jan20.txt"
    "all_run2016b_v2_trees_2016_reRECO_endpoint_jan20.txt"
    "all_run2016c_v2_trees_2016_reRECO_endpoint_jan20.txt"
    "all_run2016d_v2_trees_2016_reRECO_endpoint_jan20.txt"
    "all_run2016e_v2_trees_2016_reRECO_endpoint_jan20.txt"
    "all_run2016f_v1_trees_2016_reRECO_endpoint_jan20.txt"
    "all_run2016g_v1_trees_2016_reRECO_endpoint_jan20.txt"
    "all_run2016h_v1_trees_2016_reRECO_endpoint_jan20.txt"
    "all_run2016h_v2_trees_2016_reRECO_endpoint_jan20.txt"
)

data2017=(
    "all_commissioning2017_v1_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017a_v1_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017a_v2_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017a_v3_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017b_v1_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017b_v2_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017c_v1_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017c_v2_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017c_v3_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017d_v1_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017e_v1_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017f_v1_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017g_v1_cosmicendpoint2017_trees_09jan19.txt"
    "all_run2017h_v1_cosmicendpoint2017_trees_09jan19.txt"
    # "all_run2017x_v1_cosmicendpoint2017_trees_09jan19.txt"
)

mc2017=(
    # "all_realistic_deco_p10-100_cosmicendpoint2017_trees_09jan19.txt"
    # "all_realistic_deco_p100-500_cosmicendpoint2017_trees_09jan19.txt"
    # "all_realistic_deco_p500_cosmicendpoint2017_trees_09jan19.txt"
    "all_realistic_deco_tkcosmics_cosmicendpoint2017_trees_09jan19.txt"
)

### Data jobs
#### (2015 Data)
#### (2016 Data)
#### (2017 Data)
#### (2018 Data)
for sample in "${data2017[@]}"
do
    echo "./bsubSubmit.py -i ${sample} -t 19jan19 -n5 -m0.0008 -b400 -p75 --runperiod 2017"
    ./bsubSubmit.py -i ${sample} -t 19jan19 -n5 -m0.0008 -b400 -p75 --runperiod 2017
done

### MC jobs
#### (2015 MC)
#### (2016 MC)
#### (2017 MC)
#### (2018 MC)
for sample in "${mc2017[@]}"
do
    echo "./bsubSubmit.py -i ${sample} -t 19jan19_notrigger_thresh10 -n5 -m0.0008 -b400 -p75 --mc --runperiod 2017 --simlow 0 --simhigh 1e10 --closure --pseudoThresh=0.1"
    ./bsubSubmit.py -i ${sample} -t 19jan19_notrigger_thresh10 -n5 -m0.0008 -b400 -p75 --mc --runperiod 2017 --simlow 0 --simhigh 1e10 --closure --pseudoThresh=0.1

    echo "./bsubSubmit.py -i ${sample} -t 19jan19_trigger_thresh10 -n5 -m0.0008 -b400 -p75 --mc --trigger --runperiod 2017 --simlow 0 --simhigh 1e10 --closure --pseudoThresh=0.1"
    ./bsubSubmit.py -i ${sample} -t 19jan19_trigger_thresh10 -n5 -m0.0008 -b400 -p75 --mc --trigger --runperiod 2017 --simlow 0 --simhigh 1e10 --closure --pseudoThresh=0.1
done

# echo "./bsubSubmit.py -i asymptotic_deco_p10_2016_reRECO_endpoint.txt  -t dec08_notrigger -n15 -m0.0008 -b400 -p75 --mc --runperiod 2016 --simlow 0   --simhigh 100"
# ./bsubSubmit.py -i asymptotic_deco_p10_2016_reRECO_endpoint.txt  -t dec08_notrigger -n15 -m0.0008 -b400 -p75 --mc --runperiod 2016 --simlow 0   --simhigh 100
# echo "./bsubSubmit.py -i asymptotic_deco_p100_2016_reRECO_endpoint.txt -t dec08_notrigger -n15 -m0.0008 -b400 -p75 --mc --runperiod 2016 --simlow 100 --simhigh 500"
# ./bsubSubmit.py -i asymptotic_deco_p100_2016_reRECO_endpoint.txt -t dec08_notrigger -n15 -m0.0008 -b400 -p75 --mc --runperiod 2016 --simlow 100 --simhigh 500
# echo "./bsubSubmit.py -i asymptotic_deco_p500_2016_reRECO_endpoint.txt -t dec08_notrigger -n15 -m0.0008 -b400 -p75 --mc --runperiod 2016 --simlow 500 --simhigh 500000000000"
# ./bsubSubmit.py -i asymptotic_deco_p500_2016_reRECO_endpoint.txt -t dec08_notrigger -n15 -m0.0008 -b400 -p75 --mc --runperiod 2016 --simlow 500 --simhigh 500000000000

# echo "./bsubSubmit.py -i asymptotic_deco_p10_2016_reRECO_endpoint.txt  -t dec08_trigger -n15 -m0.0008 -b400 -p75 --mc --trigger --runperiod 2016 --simlow 0   --simhigh 100"
# ./bsubSubmit.py -i asymptotic_deco_p10_2016_reRECO_endpoint.txt  -t dec08_trigger -n15 -m0.0008 -b400 -p75 --mc --trigger --runperiod 2016 --simlow 0   --simhigh 100
# echo "./bsubSubmit.py -i asymptotic_deco_p100_2016_reRECO_endpoint.txt -t dec08_trigger -n15 -m0.0008 -b400 -p75 --mc --trigger --runperiod 2016 --simlow 100 --simhigh 500"
# ./bsubSubmit.py -i asymptotic_deco_p100_2016_reRECO_endpoint.txt -t dec08_trigger -n15 -m0.0008 -b400 -p75 --mc --trigger --runperiod 2016 --simlow 100 --simhigh 500
# echo "./bsubSubmit.py -i asymptotic_deco_p500_2016_reRECO_endpoint.txt -t dec08_trigger -n15 -m0.0008 -b400 -p75 --mc --trigger --runperiod 2016 --simlow 500 --simhigh 500000000000"
# ./bsubSubmit.py -i asymptotic_deco_p500_2016_reRECO_endpoint.txt -t dec08_trigger -n15 -m0.0008 -b400 -p75 --mc --trigger --runperiod 2016 --simlow 500 --simhigh 500000000000
