#!/bin/bash

## usage:
## ./getendpointresults.sh sep14_thresh25 v5_b0.80_pt75_n400_sym <run period>

echo Collecting outputs from job ${1} run with settings ${2} from run period ${3}

if [ -z ${1+x} ]
then
    echo "No job was specified (${1}), exiting"
    exit
fi
if [ -z ${2+x} ]
then
    echo "No settings were specified (${2}), exiting"
    exit
fi
if [ -z ${3+x} ]
then
    echo "No run period was specified (${3}), exiting"
    exit
fi

jobname=${1}
settings=${2}
runperiod=${3}

datasamples2015=( "craft15" "run2015b" "run2015c" "run2015d" "run2015e" )
datasamples2016=(
    "all_run2016b_v1"
    "all_run2016b_v2"
    "all_run2016c_v2"
    "all_run2016d_v2"
    "all_run2016e_v2"
    "all_run2016f_v1"
    "all_run2016g_v1"
    "all_run2016h_v1"
    "all_run2016h_v2"
)
datasamples2017=(
    "all_commissioning2017_v1"
    "all_run2017a_v1"
    "all_run2017a_v2"
    "all_run2017a_v3"
    "all_run2017b_v1"
    "all_run2017b_v2"
    "all_run2017c_v1"
    "all_run2017c_v2"
    "all_run2017c_v3"
    "all_run2017d_v1"
    "all_run2017e_v1"
    "all_run2017f_v1"
    "all_run2017g_v1"
    "all_run2017h_v1"
    "all_run2017x_v1"
)

mcsamples2015=( "asym_deco_p100" "asym_deco_p500" "startup_peak_p100" "startup_peak_p500" )
mcsamples2016=( "asym_deco_2016_p10_v1" "asym_deco_2016_p100_v1" "asym_deco_2016_p500_v1" )
mcsamples2017=( "all_realistic_deco_p10-100" "all_realistic_deco_p100-500" "all_realistic_deco_p500" )

samples2015=(${datasamples2015[@]} ${mcsamples2015[@]})
samples2016=(${datasamples2016[@]} ${mcsamples2016[@]})
samples2017=(${datasamples2017[@]} ${mcsamples2017[@]})

## create current variables based on the specified run period
## https://stackoverflow.com/questions/11180714/how-to-iterate-over-an-array-using-indirect-reference
datasamples="datasamples${runperiod}[@]"
mcsamples="mcsamples${runperiod}[@]"
samples=(${!datasamples} ${!mcsamples})

algos=( "TrackerOnly" "DYTT" "Picky" "TPFMS" "TuneP" )
algos2=( "dyt" "tuneP" "picky" "tpfms" "trackerOnly" )
ptbins=( 100 200 400 )
cuts=( "loose" "tight" )

basedir=/eos/cms/store/user/${USER}/CosmicEndpoint/${runperiod}

echo "samples is ${samples[@]}"
echo "datasamples is ${!datasamples}"
echo "mcsamples is ${!mcsamples}"

# # should be on EOS? /tmp then copied to EOS?
outdir=/tmp/${USER}/${jobname}"_hadded"
echo mkdir -p ${outdir}
# mkdir -p ${outdir}

for sample in "${samples[@]}"
do
    sourcedir=${basedir}/output_${sample}_${jobname}_${settings}

    if ! [ -d ${sourcedir} ]
    then
        echo "Directory ${sourcedir} does not exist, continuing"
        continue
    fi
    outsubdir=${sample}_${settings}
    echo ${outsubdir}
    echo mkdir -p ${outdir}/${outsubdir}
    # mkdir -p ${outdir}/${outsubdir}
    extra=""
    # https://stackoverflow.com/questions/3685970/check-if-an-array-contains-a-value
    case "${!datasamples}" in  *"${sample}"*)
	extra="_p100"
	echo "found ${sample} in datasamples" ;;
    esac


    ## this isn't working, why?
    # if [[ " ${!datasamples} " =~ " ${sample} " ]]; then
    # 	extra="_p100"
    # 	echo "found ${sample} in datasamples"
    # else
    # 	extra=""
    # 	echo "unable to find ${sample} in datasamples"
    # fi

    allrootfiles=`ls -lshtar ${sourcedir}/*.root|wc -l`
    i=0
    algorootfiles=()
    for algo in "${algos[@]}"
    do
        # echo "i=${i}"
        algorootfiles[i]=`ls -lshtar ${sourcedir}/*_${algo}.root|wc -l`
        ((i++))
    done
    echo "allrootfiles=$allrootfiles"
    echo "algorootfiles=${algorootfiles[@]}"
    echo "extra is ${extra}"

    for algo in "${algos[@]}"
    do
        flist=$(ls -d -1 ${sourcedir}/*_${algo}.root)

        if [ -n "${flist}" ]
        then
            # flist=(${flist//\/eos\/uscms/root:\/\/${redir}\/\/\/})
            ## change for lxplus redir...
            flist=(${flist//\/eos\/uscms/root:\/\/${redir}\/\/\/})
    	    echo "hadd -f ${outdir}/${outsubdir}/CosmicHistOut_${algo}.root ${flist[@]}"
    	    # eval "hadd -f ${outdir}/${outsubdir}/CosmicHistOut_${algo}.root ${flist[@]} >&/dev/null"
        fi
    done

    for algo2 in "${algos2[@]}"
    do
        for ptbin in "${ptbins[@]}"
        do
            for cut in "${cuts[@]}"
            do
    	        echo "cat /tmp/${USER}/output_${sample}_${jobname}_${settings}/*_${algo2}_pt${ptbin}_${cut}.txt > ${outdir}/${outsubdir}/${algo2}_pt${ptbin}_${cut}.txt"
    	        # cat /tmp/${USER}/output_${sample}_${jobname}_${settings}/*_${algo2}_pt${ptbin}_${cut}.txt > ${outdir}/${outsubdir}/${algo2}_pt${ptbin}_${cut}.txt
            done
        done
    done
done


## combine all data files into one annual run period for simplicity
outcombineddir="${outdir}/run${runperiod}_v1_${settings}"
echo mkdir -p ${outcombineddir}
# mkdir -p ${outcombineddir}

# #exit 0

for algo in "${algos[@]}"
do
    echo "hadd -f ${outcombineddir}/CosmicHistOut_${algo}.root ${outdir}/run${runperiod}?_*/CosmicHistOut_${algo}.root >&/dev/null"
    # hadd -f ${outcombineddir}/CosmicHistOut_${algo}.root ${outdir}/run${runperiod}?_*/CosmicHistOut_${algo}.root >&/dev/null
done

for algo2 in "${algos2[@]}"
do
    for ptbin in "${ptbins[@]}"
    do
        for cut in "${cuts[@]}"
        do
            echo "cat ${outdir}/run${runperiod}?_*/${algo2}_pt${ptbin}_${cut}.txt > ${outcombineddir}/${algo2}_pt${ptbin}_${cut}.txt"
            # cat ${outdir}/run${runperiod}?_*/${algo2}_pt${ptbin}_${cut}.txt > ${outcombineddir}/${algo2}_pt${ptbin}_${cut}.txt
        done
    done
done
