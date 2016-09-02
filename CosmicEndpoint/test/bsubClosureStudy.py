#!/bin/env python

import subprocess
import math
import sys,os,socket
import shutil

from optparse import OptionParser
from wsuPythonUtils import checkRequiredArguments

parser = OptionParser()
parser.add_option("-g", "--gridproxy", action="store_true", dest="gridproxy",
                  metavar="gridproxy",
                  help="[OPTIONAL] Generate a GRID proxy")
parser.add_option("-i", "--infiledir", type="string", dest="infiledir",
                  metavar="infiledir",
                  help="[REQUIRED] Location of the comparison input MC ROOT files")
parser.add_option("-b", "--rebins", type="int", dest="rebins",
                  metavar="rebins", default=1,
                  help="[OPTIONAL] Number of bins to combine in the q/pT plot (default is 1)")
parser.add_option("-n", "--biasbins", type="int", dest="biasbins",
                  metavar="biasbins", default=100,
                  help="[OPTIONAL] Total number of injected bias points (default is 1000)")
parser.add_option("-t", "--totalbins", type="int", dest="totalbins",
                  metavar="totalbins", default=5000,
                  help="[OPTIONAL] Total number of bins in the original curvature distribution (default is 5000)")
parser.add_option("-m", "--maxbias", type="float", dest="maxbias",
                  metavar="maxbias", default=0.1,
                  help="[OPTIONAL] Maximum injected bias (default is 0.1 c/TeV)")
parser.add_option("-s", "--stepsize", type="int", dest="stepsize",
                  metavar="stepsize", default=1,
                  help="[OPTIONAL] Step size in the GIF (default is 1)")
parser.add_option("-d", "--debug", action="store_true", dest="debug",
                  metavar="debug",
                  help="[OPTIONAL] Debug mode")
parser.add_option("--histbase", type="string", dest="histbase",
                  metavar="histbase", default="looseMuLower",
                  help="[OPTIONAL] Base name of the histogram object (default is \"looseMuLower\")")
parser.add_option("--minpt", type="float", dest="minpt",
                  metavar="minpt", default=200.,
                  help="[OPTIONAL] Minimum pT cut to apply in the curvature plots (default is 200 c/TeV)")
parser.add_option("--etaphi", type="string", dest="etaphi",
                  metavar="etaphi", default="",
                  help="[OPTIONAL] Eta/Phi bin to use")
parser.add_option("--pm", action="store_true", dest="pm",
                  metavar="pm",
                  help="[OPTIONAL] Scale plus and minus separately")
parser.add_option("--log", action="store_true", dest="log",
                  metavar="log",
                  help="[OPTIONAL] Make curvature plots in log scale")
parser.add_option("--mcbias", type="int", dest="mcbias",
                  metavar="mcbias", default=25,
                  help="[OPTIONAL] Bias bin value to recover (default is 25)")
parser.add_option("--num_pseudo", type="int", dest="num_pseudo",
                  metavar="num_pseudo", default=500,
                  help="[OPTIONAL] Number of pseudoexperiments to run (default is 500, -1 for specific pseudo experiment)")

(options, args) = parser.parse_args()
checkRequiredArguments(options, parser)

if options.gridproxy:
    os.system("voms-proxy-init --voms cms --valid 168:00")

debug = False    
if options.debug:
    debug = True
username = os.getenv("USER")
userkey  = os.getenv("KRB5CCNAME")[17:17+5] #should be the form of FILE:/tmp/krb5cc_17329_lNizN17453
print username, userkey
proxyPath = "/afs/cern.ch/user/%s/%s/x509up_u%s"%(username[0],username,userkey)
cmd = "cp /tmp/x509up_u%s  %s"%(userkey,proxyPath)
print cmd
os.system(cmd)

os.system("mkdir -p %s/%s"%("closureStudy",options.infiledir))

for count in range(options.num_pseudo):
    scriptname = "closureStudy/%s/bsub_closure_job_%d.sh"%(options.infiledir,count)
    script = open(scriptname,"w")
    script.write("""#!/bin/bash
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
export X509_USER_PROXY=%s

kinit -R
aklog
klist

echo "hostname is $HOSTNAME"
export JOBDIR=${PWD}
echo "batch job directory is ${JOBDIR}"
export OUTPUTDIR=${JOBDIR}/output_%s_closure_study
echo "output directory is ${OUTPUTDIR}"
mkdir ${OUTPUTDIR}
ls -tar

cd %s
export AFSJOBDIR=${PWD}
eval `scram runtime -sh`
cp ../python/wsuPythonUtils.py ${JOBDIR}/
cp ../python/wsuPyROOTUtils.py ${JOBDIR}/
cp ../python/wsuMuonTreeUtils.py ${JOBDIR}/
cp endpointClosureStudy.py ${JOBDIR}/

echo "rsync -ah --progress --relative ./%s/*startup*/*TuneP.root.xz ${JOBDIR}/"
rsync -ah --progress --relative ./%s/*startup*/*TuneP.root.xz ${JOBDIR}/

echo "decompressing ROOT files"
cd ${JOBDIR}/%s/startup_peak_p100_v5_b0.80_pt75_n400_sym
xz --decompress *.xz

cd ${JOBDIR}/%s/startup_peak_p500_v5_b0.80_pt75_n400_sym
xz --decompress *.xz

cd ${JOBDIR}

echo "Setting up path and enviornment"
export PATH=${PWD}:${PATH}
export PYTHONPATH=${PWD}:${PYTHONPATH}

ls -tar

echo "Running closure study"
./endpointClosureStudy.py -i %s -o ${OUTPUTDIR}/%s-closure-%s-pm_rec_p25_job%d.root -b40 --minpt 100 -m 0.8 --etaphi %s --num_pseudo 0 --pseudo %d -n 100 --pm
./endpointClosureStudy.py -i %s -o ${OUTPUTDIR}/%s-closure-%s-pm_rec_b0_job%d.root -b40 --minpt 100 -m 0.8 --etaphi %s --num_pseudo 0 --pseudo %d -n 100 --mcbias=0 --pm
./endpointClosureStudy.py -i %s -o ${OUTPUTDIR}/%s-closure-%s-pm_rec_m25_job%d.root -b40 --minpt 100 -m 0.8 --etaphi %s --num_pseudo 0 --pseudo %d -n 100 --mcbias=-25 --pm
./endpointClosureStudy.py -i %s -o ${OUTPUTDIR}/%s-closure-%s_rec_p25_job%d.root -b40 --minpt 100 -m 0.8 --etaphi %s --num_pseudo 0 --pseudo %d -n 100
./endpointClosureStudy.py -i %s -o ${OUTPUTDIR}/%s-closure-%s_rec_b0_job%d.root -b40 --minpt 100 -m 0.8 --etaphi %s --num_pseudo 0 --pseudo %d -n 100 --mcbias=0
./endpointClosureStudy.py -i %s -o ${OUTPUTDIR}/%s-closure-%s_rec_m25_job%d.root -b40 --minpt 100 -m 0.8 --etaphi %s --num_pseudo 0 --pseudo %d -n 100 --mcbias=-25

mv sampleGIFs ${OUTPUTDIR}/

tree

echo "rsync -e \\"ssh -T -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\\" -ahuq --progress ${OUTPUTDIR} %s:/tmp/${USER}/"
rsync -e "ssh -T -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" -ahuq --progress ${OUTPUTDIR} %s:/tmp/${USER}/
"""%(proxyPath,
     options.infiledir,
     os.getcwd(),
     options.infiledir,
     options.infiledir,
     options.infiledir,
     options.infiledir,
     options.infiledir,options.infiledir,options.etaphi,count,options.etaphi,count,
     options.infiledir,options.infiledir,options.etaphi,count,options.etaphi,count,
     options.infiledir,options.infiledir,options.etaphi,count,options.etaphi,count,
     options.infiledir,options.infiledir,options.etaphi,count,options.etaphi,count,
     options.infiledir,options.infiledir,options.etaphi,count,options.etaphi,count,
     options.infiledir,options.infiledir,options.etaphi,count,options.etaphi,count,
     socket.gethostname(),socket.gethostname()))

    script.close()
    os.chmod(scriptname,0777)

    if not debug:
        cmd = "bsub -q 8nh -W 300 %s/%s"%(os.getcwd(),scriptname)
        print cmd
        os.system(cmd)
    elif count == 3:
        cmd = "bsub -q test -W 300 %s/%s"%(os.getcwd(),scriptname)
        print cmd
        #os.system(cmd)

    count = count + 1
    pass

