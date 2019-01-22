#!/bin/bash

## usage:
## ./getendpointresults.sh sep14_thresh25 v5_b0.80_pt75_n400_sym <run period>${}

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
mcsamples2017=( 
    "all_realistic_deco_tkcosmics"
    # "all_realistic_deco_p10-100"
    # "all_realistic_deco_p100-500"
    # "all_realistic_deco_p500"
 )

samples2015=(${datasamples2015[@]} ${mcsamples2015[@]})
samples2016=(${datasamples2016[@]} ${mcsamples2016[@]})
samples2017=(${datasamples2017[@]} ${mcsamples2017[@]})

## create current variables based on the specified run period
## https://stackoverflow.com/questions/11180714/how-to-iterate-over-an-array-using-indirect-reference
datasamples="datasamples${runperiod}[@]"
# datasamples=
mcsamples="mcsamples${runperiod}[@]"
mcsamples=
samples=(${!datasamples} ${!mcsamples})

basedir=/eos/cms/store/user/${USER}/CosmicEndpoint/${runperiod}
redir=eoscms.cern.ch
# redir=cms-xrd-global.cern.ch
# redir=cmsxrootd.fnal.gov

subhost=${HOSTNAME}
echo "samples is ${samples[@]}"
echo "datasamples is ${!datasamples}"
echo "mcsamples is ${!mcsamples}"

for sample in "${samples[@]}"
do
    # if [[ $sample =~ 'run2017' ]]
    # then
    #     continue
    # fi
    ncpus=2
    extra=""
    # https://stackoverflow.com/questions/3685970/check-if-an-array-contains-a-value
    case "${!mcsamples}" in  *"${sample}"*)
        # what was this for??
        extra="_notrigger_thresh10"
        ncpus=4
        # extra="_p100"
        echo "found ${sample} in mcsamples" ;;
    esac

    sourcedir=${basedir}/output_${sample}_${jobname}${extra}_${settings}

    if ! [ -d ${sourcedir} ]
    then
        echo "Directory ${sourcedir} does not exist, continuing"
        continue
    fi
    cat <<EOF > ${sample}_${settings}${extra}.sub
executable  = hadd_${sample}_${settings}${extra}.sh
arguments   = \$(ClusterID) \$(ProcId)
output      = bsubs_${settings%*_sym}/output/${sample}_${settings}_hadd.\$(ClusterId).\$(ProcId).out
error       = bsubs_${settings%*_sym}/error/${sample}_${settings}_hadd.\$(ClusterId).\$(ProcId).err
log         = bsubs_${settings%*_sym}/logs/${sample}_${settings}_hadd.\$(ClusterId).log
+JobFlavour = "workday"
RequestCpus = ${ncpus}
queue

EOF

    cat <<EOF > hadd_${sample}_${settings}${extra}.sh
#!/bin/bash
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source \${VO_CMS_SW_DIR}/cmsset_default.sh
export X509_USER_PROXY=/afs/cern.ch/user/s/sturdy/x509up_u17329

kinit -R
aklog
klist

export VO_LCG_SW_DIR=/cvmfs/sft.cern.ch/lcg/views
source \${VO_LCG_SW_DIR}/LCG_94/x86_64-slc6-gcc8-opt/setup.sh

echo "hostname is \${HOSTNAME}"
echo "submission hostname is is ${subhost}"
export JOBDIR=${PWD}
outsubdir=${sample}_${settings}

echo \${outsubdir}

outdir=${jobname}${extra}_hadded
echo mkdir -p \${outdir}
mkdir -p \${outdir}

echo mkdir -p \${outdir}/\${outsubdir}
mkdir -p \${outdir}/\${outsubdir}

## this isn't working, why?
# if [[ " ${!datasamples} " =~ " ${sample} " ]]; then
#     extra="_p100"
#     echo "found ${sample} in datasamples"
# else
#     extra=""
#     echo "unable to find ${sample} in datasamples"
# fi

algos=( "TrackerOnly" "DYTT" "Picky" "TPFMS" "TuneP" )
algos2=( "dyt" "tuneP" "picky" "tpfms" "trackerOnly" )
ptbins=( 100 200 400 )
cuts=( "loose" "tight" )

allrootfiles=\`ls -lshtar ${sourcedir}/*.root|wc -l\`
i=0
algorootfiles=()
for algo in "\${algos[@]}"
do
    # echo "i=${i}"
    algorootfiles[i]=\`ls -lshtar ${sourcedir}/*_\${algo}.root|wc -l\`
    ((i++))
done
echo "allrootfiles=\${allrootfiles}"
echo "algorootfiles=\${algorootfiles[@]}"
echo "extra is \${extra}"

for algo in "\${algos[@]}"
do
    flist=\$(ls -d -1 ${sourcedir}/*_\${algo}.root)

    if [ -n "\${flist}" ]
    then
        # flist=(\${flist//\/eos\/uscms/root:\/\/${redir}\/\/\/})
        ## change for lxplus redir...
        flist=(\${flist//\/eos\/cms/root:\/\/${redir}\/\/})
        echo "hadd -j -f \${outdir}/\${outsubdir}/CosmicHistOut_\${algo}.root \${flist[@]}"
        eval "hadd -j -f \${outdir}/\${outsubdir}/CosmicHistOut_\${algo}.root \${flist[@]} >&/dev/null"
    fi
done

echo "rsync -e \\"ssh -T -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\\" -ahu --progress ${subhost}:/tmp/\${USER}/output_${sample}_${jobname}${extra}_${settings} \${PWD}/"
rsync -e "ssh -T -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" -ahu --progress ${subhost}:/tmp/\${USER}/output_${sample}_${jobname}${extra}_${settings} \${PWD}/

for algo2 in "\${algos2[@]}"
do
    for ptbin in "\${ptbins[@]}"
    do
        for cut in "\${cuts[@]}"
        do
            echo "cat \${PWD}/output_${sample}_${jobname}${extra}_${settings}/*_\${algo2}_pt\${ptbin}_\${cut}.txt > \${outdir}/\${outsubdir}/\${algo2}_pt\${ptbin}_\${cut}.txt"
            cat \${PWD}/output_${sample}_${jobname}${extra}_${settings}/*_\${algo2}_pt\${ptbin}_\${cut}.txt > \${outdir}/\${outsubdir}/\${algo2}_pt\${ptbin}_\${cut}.txt
        done
    done
done

# eosoutdir=${basedir}/${jobname}_hadded
eosoutdir=${basedir}/\${outdir}
## do we have to create the output eos dir?
eos mkdir \${eosoutdir}
echo "xrdcp -r \${outdir} root://${redir}/\${eosoutdir}/"
xrdcp -r \${outdir} root://${redir}/\${eosoutdir}/
EOF

    chmod +x hadd_${sample}_${settings}${extra}.sh
    # echo condor_submit ${sample}_${settings}${extra}.sub
    # condor_submit ${sample}_${settings}${extra}.sub
done


ncpus=2
extra=""
cat <<EOF > run${runperiod}_combined_${settings}${extra}.sub
executable  = hadd_run${runperiod}_combined_${settings}${extra}.sh
arguments   = \$(ClusterID) \$(ProcId)
output      = bsubs_${settings%*_sym}/output/run${runperiod}_combined_${settings}_hadd.\$(ClusterId).\$(ProcId).out
error       = bsubs_${settings%*_sym}/error/run${runperiod}_combined_${settings}_hadd.\$(ClusterId).\$(ProcId).err
log         = bsubs_${settings%*_sym}/logs/run${runperiod}_combined_${settings}_hadd.\$(ClusterId).log
+JobFlavour = "workday"
RequestCpus = ${ncpus}
queue

EOF

cat <<EOF > hadd_run${runperiod}_combined_${settings}${extra}.sh
#!/bin/bash
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source \${VO_CMS_SW_DIR}/cmsset_default.sh
export X509_USER_PROXY=/afs/cern.ch/user/s/sturdy/x509up_u17329

kinit -R
aklog
klist

export VO_LCG_SW_DIR=/cvmfs/sft.cern.ch/lcg/views
source \${VO_LCG_SW_DIR}/LCG_94/x86_64-slc6-gcc8-opt/setup.sh

echo "hostname is \${HOSTNAME}"
echo "submission hostname is is ${subhost}"
export JOBDIR=${PWD}
outsubdir=run${runperiod}_combined_${settings}

echo \${outsubdir}

outdir=${jobname}${extra}_hadded
algos=( "TrackerOnly" "DYTT" "Picky" "TPFMS" "TuneP" )
algos2=( "dyt" "tuneP" "picky" "tpfms" "trackerOnly" )
ptbins=( 100 200 400 )
cuts=( "loose" "tight" )

## combine all data files into one annual run period for simplicity
outcombineddir="\${outdir}/\${outsubdir}"
echo mkdir -p \${outcombineddir}
mkdir -p \${outcombineddir}

# #exit 0

for algo in "\${algos[@]}"
do
    flist=\$(ls -d -1 ${basedir}/\${outdir}/all_run${runperiod}?_*/CosmicHistOut_\${algo}.root)

    if [ -n "\${flist}" ]
    then
        # flist=(\${flist//\/eos\/uscms/root:\/\/${redir}\/\/\/})
        ## change for lxplus redir...
        flist=(\${flist//\/eos\/cms/root:\/\/${redir}\/\/})

        echo "hadd -j -f \${outcombineddir}/CosmicHistOut_\${algo}.root  \${flist[@]}"
        eval "hadd -j -f \${outcombineddir}/CosmicHistOut_\${algo}.root  \${flist[@]} >&/dev/null"
        #debug#hadd -j -f \${outcombineddir}/CosmicHistOut_\${algo}.root  \${flist[@]} >&/dev/null
    fi
done

for algo2 in "\${algos2[@]}"
do
    for ptbin in "\${ptbins[@]}"
    do
        for cut in "\${cuts[@]}"
        do
            echo "cat ${basedir}/\${outdir}/all_run${runperiod}?_*/\${algo2}_pt\${ptbin}_\${cut}.txt > \${outcombineddir}/\${algo2}_pt\${ptbin}_\${cut}.txt"
            cat ${basedir}/\${outdir}/all_run${runperiod}?_*/\${algo2}_pt\${ptbin}_\${cut}.txt > \${outcombineddir}/\${algo2}_pt\${ptbin}_\${cut}.txt
        done
    done
done

krenew

eosoutdir=${basedir}/\${outdir}
## do we have to create the output eos dir?
eos mkdir \${eosoutdir}
echo "xrdcp -r \${outdir} root://${redir}/\${eosoutdir}/"
xrdcp -r \${outdir} root://${redir}/\${eosoutdir}/
EOF

chmod +x hadd_run${runperiod}_combined_${settings}${extra}.sh
echo condor_submit run${runperiod}_combined_${settings}${extra}.sub
condor_submit run${runperiod}_combined_${settings}${extra}.sub
