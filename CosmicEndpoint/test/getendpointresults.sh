#!/bin/bash

## usage:
## ./getendpointresults.sh sep14_thresh25 v5_b0.80_pt75_n400_sym
echo Collecting outputs from job ${1} run with settings ${2}
#samples=( "craft15" "run2015b" "run2015c" "run2015d" "run2015e" "asym_deco_p100" "asym_deco_p500" "startup_peak_p100" "startup_peak_p500" )
samples=( 
    "all_run2016b_v1"
    "all_run2016b_v2"
    "all_run2016c_v2"
    "all_run2016d_v2"
    "all_run2016e_v2"
    "all_run2016f_v1"
    "all_run2016g_v1"
    "all_run2016h_v1"
    "all_run2016h_v2"
    # "asymptotic_deco_p100"
    # "asymptotic_deco_p500"
#    "asym_deco_2016_p10_v1"
#    "asym_deco_2016_p100_v1"
#    "asym_deco_2016_p500_v1"
)
#samples=( "asym_deco_p100" "asym_deco_p500" "startup_peak_p100" "startup_peak_p500" )
#samples=( "startup_peak_p100" "startup_peak_p500" )
#samples=( "craft15" "run2015b" "run2015c" "run2015d" "run2015e" )
datasamples=( "craft15" "run2015b" "run2015c" "run2015d" "run2015e" )
algos=("TrackerOnly" "DYTT" "Picky" "TPFMS" "TuneP")
algos2=("dyt" "tuneP" "picky" "tpfms" "trackerOnly")

#ourcedir="/tmp/sturdy"
#sourcedir=~/myeos/sturdy/CosmicEndpoint/2015
sourcedir=~/myeos/sturdy/CosmicEndpoint/2016

echo "samples is ${samples[@]}"
echo "datasamples is ${datasamples[@]}"
outdir=${1}"_hadded"
echo ${outdir}
echo mkdir -p ${outdir}
mkdir -p ${outdir}
# for sample in "${samples[@]}"
# do
#     outsubdir=${sample}_${2}
#     echo ${outsubdir}
#     echo mkdir -p ${outdir}/${outsubdir}
#     mkdir -p ${outdir}/${outsubdir}
#     extra=""
#     # https://stackoverflow.com/questions/3685970/check-if-an-array-contains-a-value
#     case "${datasamples[@]}" in  *"${sample}"*)
# 	extra="_p100"
# 	echo "found ${sample} in datasamples" ;;
#     esac

#     ## this isn't working, why?
#     # if [[ " ${datasemples[@]} " =~ " ${sample} " ]]; then
#     # 	extra="_p100"
#     # 	echo "found ${sample} in datasamples"
#     # else
#     # 	extra=""
#     # 	echo "unable to find ${sample} in datasamples"
#     # fi
#     #  ${sourcedir}/output_shawn_startup_peak_p500_v5-sep14_thresh25_b0.80_pt75_n400_sym/sym_histograms_9_TPFMS.root
#     #  ~/myeos/sturdy/CosmicEndpoint/2015/Closure/output_shawn_startup_peak_p100_v5-sep14_thresh04_b0.80_pt75_n400_sym
#     #allrootfiles=`ls -lshtar ${sourcedir}/output_shawn_${sample}${extra}_v5-${1}_${2}/*.root|wc -l`
#     #allrootfiles=`ls -lshtar ~/myeos/sturdy/CosmicEndpoint/2015/Closure/output_shawn_${sample}${extra}_v5-${1}_${2}/*.root|wc -l`
#     #allrootfiles=`ls -lshtar ~/myeos/sturdy/CosmicEndpoint/2015/output_shawn_${sample}${extra}_v5-${1}_${2}/*.root|wc -l`
#     #allrootfiles=`ls -lshtar ~/myeos/sturdy/CosmicEndpoint/2016/output_shawn_${sample}-${1}_${2}/*.root|wc -l`
#     allrootfiles=`ls -lshtar ${sourcedir}/output_${sample}_${1}_${2}/*.root|wc -l`
#     i=0
#     algorootfiles=()
#     for algo in "${algos[@]}"
#     do
# 	# echo "i=${i}"
# 	# algorootfiles[i]=`ls -lshtar ${sourcedir}/output_shawn_${sample}${extra}_v5-${1}_${2}/*_${algo}.root|wc -l`
# 	#algorootfiles[i]=`ls -lshtar ~/myeos/sturdy/CosmicEndpoint/2015/output_shawn_${sample}${extra}_v5-${1}_${2}/*_${algo}.root|wc -l`
# 	#algorootfiles[i]=`ls -lshtar ~/myeos/sturdy/CosmicEndpoint/2016/output_shawn_${sample}-${1}_${2}/*_${algo}.root|wc -l`
# 	algorootfiles[i]=`ls -lshtar ${sourcedir}/output_${sample}_${1}_${2}/*_${algo}.root|wc -l`
# 	((i++))
#     done
#     echo "allrootfiles=$allrootfiles"
#     echo "algorootfiles=${algorootfiles[@]}"
#     echo "extra is ${extra}"

#     for algo in "${algos[@]}"
#     do
#     	echo "hadd -f ${outdir}/${outsubdir}/CosmicHistOut_${algo}.root ~/myeos/sturdy/CosmicEndpoint/2016/output_${sample}_${1}_${2}/*_${algo}.root"
#     	hadd -f ${outdir}/${outsubdir}/CosmicHistOut_${algo}.root ~/myeos/sturdy/CosmicEndpoint/2016/output_${sample}_${1}_${2}/*_${algo}.root >&/dev/null
#     done

#     for algo2 in "${algos2[@]}"
#     do
#     	echo "cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt100_loose.txt > ${outdir}/${outsubdir}/${algo2}_pt100_loose.txt"
#     	cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt100_loose.txt > ${outdir}/${outsubdir}/${algo2}_pt100_loose.txt
#     	echo "cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt100_tight.txt > ${outdir}/${outsubdir}/${algo2}_pt100_tight.txt"
#     	cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt100_tight.txt > ${outdir}/${outsubdir}/${algo2}_pt100_tight.txt
#     	echo "cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt200_loose.txt > ${outdir}/${outsubdir}/${algo2}_pt200_loose.txt"
#     	cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt200_loose.txt > ${outdir}/${outsubdir}/${algo2}_pt200_loose.txt
#     	echo "cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt200_tight.txt > ${outdir}/${outsubdir}/${algo2}_pt200_tight.txt"
#     	cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt200_tight.txt > ${outdir}/${outsubdir}/${algo2}_pt200_tight.txt
#     	echo "cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt400_loose.txt > ${outdir}/${outsubdir}/${algo2}_pt400_loose.txt"
#     	cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt400_loose.txt > ${outdir}/${outsubdir}/${algo2}_pt400_loose.txt
#     	echo "cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt400_tight.txt > ${outdir}/${outsubdir}/${algo2}_pt400_tight.txt"
#     	cat /tmp/sturdy/output_${sample}_${1}_${2}/*_${algo2}_pt400_tight.txt > ${outdir}/${outsubdir}/${algo2}_pt400_tight.txt
#     done
# done

outcombineddir="${outdir}/run2016_v1_${2}"
echo mkdir -p ${outcombineddir}
mkdir -p ${outcombineddir}

#exit 0

for algo in "${algos[@]}"
do
    echo "hadd -f ${outcombineddir}/CosmicHistOut_${algo}.root ${outdir}/run2016?_*/CosmicHistOut_${algo}.root >&/dev/null"
    hadd -f ${outcombineddir}/CosmicHistOut_${algo}.root ${outdir}/run2016?_*/CosmicHistOut_${algo}.root >&/dev/null
done

for algo2 in "${algos2[@]}"
do
    echo "cat ${outdir}/run2016?_*/${algo2}_pt100_loose.txt > ${outcombineddir}/${algo2}_pt100_loose.txt"
    cat ${outdir}/run2016?_*/${algo2}_pt100_loose.txt > ${outcombineddir}/${algo2}_pt100_loose.txt
    echo "cat ${outdir}/run2016?_*/${algo2}_pt100_tight.txt > ${outcombineddir}/${algo2}_pt100_tight.txt"
    cat ${outdir}/run2016?_*/${algo2}_pt100_tight.txt > ${outcombineddir}/${algo2}_pt100_tight.txt
    echo "cat ${outdir}/run2016?_*/${algo2}_pt200_loose.txt > ${outcombineddir}/${algo2}_pt200_loose.txt"
    cat ${outdir}/run2016?_*/${algo2}_pt200_loose.txt > ${outcombineddir}/${algo2}_pt200_loose.txt
    echo "cat ${outdir}/run2016?_*/${algo2}_pt200_tight.txt > ${outcombineddir}/${algo2}_pt200_tight.txt"
    cat ${outdir}/run2016?_*/${algo2}_pt200_tight.txt > ${outcombineddir}/${algo2}_pt200_tight.txt
    echo "cat ${outdir}/run2016?_*/${algo2}_pt400_loose.txt > ${outcombineddir}/${algo2}_pt400_loose.txt"
    cat ${outdir}/run2016?_*/${algo2}_pt400_loose.txt > ${outcombineddir}/${algo2}_pt400_loose.txt
    echo "cat ${outdir}/run2016?_*/${algo2}_pt400_tight.txt > ${outcombineddir}/${algo2}_pt400_tight.txt"
    cat ${outdir}/run2016?_*/${algo2}_pt400_tight.txt > ${outcombineddir}/${algo2}_pt400_tight.txt
done
