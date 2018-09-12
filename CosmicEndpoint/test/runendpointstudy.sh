#!/bin/bash

echo Running endpoint study on outputs from job "${1}" run with tag "${2}"
echo Optional parameters are rebins "${3}", stepsize "${4}"

if [ -z ${1+x} ]
then
    echo "No directory was specified (${1}), exiting"
    exit
fi
indir=$1
if [ -z ${2+x} ]
then
    echo "No tag was specified (${2}), exiting"
    exit
fi
tagname=$2

rebins=40
if [ -z ${3+x} ]
then
    echo "No rebin value was specified, using 40"
else
    rebins=${3}
fi

stepsize=5
if [ -z ${4+x} ]
then
    echo "No step value was specified, using 5"
else
    stepsize=${4}
fi

algos=("TuneP" "DYTT" "TrackerOnly" "Picky" "TPFMS")
etaphibins=("EtaPlus" "EtaMinus") # "PhiMinus" "PhiZero" "EtaPlusPhiMinus" "EtaPlusPhiZero" "EtaMinusPhiMinus" "EtaMinusPhiZero")
# ptbins=(110 120 125 150 200 250 300 400 500 750)
ptbins=(150 200)

for ptbin in "${ptbins[@]}"
do
    for algo in "${algos[@]}"
    do
        echo "./endpointDataMCStudy.py -i ${indir} -o ${tagname}.${algo}.s${stepsize}.pt${ptbin}.b${rebins}.lower.root -b${rebins} --minpt ${ptbin} -m 0.8 -n 400 -s${stepsize} --algo ${algo} --runperiod 2016 --asymdeco --etaphi All"
        ./endpointDataMCStudy.py -i ${indir} -o ${tagname}.${algo}.s${stepsize}.pt${ptbin}.b${rebins}.lower.root -b${rebins} --minpt ${ptbin} -m 0.8 -n 400 -s${stepsize} --algo ${algo} --runperiod 2016 --asymdeco --etaphi All

        for etaphi in "${etaphibins[@]}"
        do
            echo "./endpointDataMCStudy.py -i ${indir} -o ${tagname}.${algo}.s${stepsize}.pt${ptbin}.b${rebins}.lower.root -b${rebins} --minpt ${ptbin} -m 0.8 -n 400 -s${stepsize} --algo ${algo} --runperiod 2016 --asymdeco --etaphi ${etaphi}"
            ./endpointDataMCStudy.py -i ${indir} -o ${tagname}.${algo}.s${stepsize}.pt${ptbin}.b${rebins}.lower.root -b${rebins} --minpt ${ptbin} -m 0.8 -n 400 -s${stepsize} --algo ${algo} --runperiod 2016 --asymdeco --etaphi ${etaphi}
        done
        
        echo "./endpointDataMCStudy.py -i ${indir} -o ${tagname}.${algo}.s${stepsize}.pt${ptbin}.b${rebins}.upper.root -b${rebins} --minpt ${ptbin} -m 0.8 -n 400 -s${stepsize} --algo ${algo} --runperiod 2016 --asymdeco --histbase looseMuUpper --etaphi All"
        ./endpointDataMCStudy.py -i ${indir} -o ${tagname}.${algo}.s${stepsize}.pt${ptbin}.b${rebins}.upper.root -b${rebins} --minpt ${ptbin} -m 0.8 -n 400 -s${stepsize} --algo ${algo} --runperiod 2016 --asymdeco --histbase looseMuUpper --etaphi All
        for etaphi in "${etaphibins[@]}"
        do
            echo "./endpointDataMCStudy.py -i ${indir} -o ${tagname}.${algo}.s${stepsize}.pt${ptbin}.b${rebins}.upper.root -b${rebins} --minpt ${ptbin} -m 0.8 -n 400 -s${stepsize} --algo ${algo} --runperiod 2016 --asymdeco --histbase looseMuUpper --etaphi ${etaphi}"
            ./endpointDataMCStudy.py -i ${indir} -o ${tagname}.${algo}.s${stepsize}.pt${ptbin}.b${rebins}.upper.root -b${rebins} --minpt ${ptbin} -m 0.8 -n 400 -s${stepsize} --algo ${algo} --runperiod 2016 --asymdeco --histbase looseMuUpper --etaphi ${etaphi}
        done
    done
done
