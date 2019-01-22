import subprocess
import math
import os,socket,errno
import shutil


## https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# copied from John Hakala's bhmacros and modified for quick use here
def callMacro(macroName,inputFile,outputFile):
    macroCommand = "%s(\"%s\", \"%s\")" % (macroName,inputFile,outputFile)
    subprocess.call(["root", "-l", "-q",macroCommand])
    return

def splitJobsForBsub(inputFile,numberOfJobs,maxBias,minPt,nBiasBins,symasym):
    samplesListsDir="samplesLists_data"
    inputFilePath = samplesListsDir+"/"+inputFile
    num_input_samples = sum(1 for line in open(inputFilePath))
    with open(inputFilePath) as inputSamplesList:
        print "number of input samples is %i" % num_input_samples
        chunksize = math.ceil(1.0*num_input_samples/numberOfJobs)
        print "chunksize is: %i" % chunksize
        fid = 1
        lineswritten = 0
        totlineswritten = 0
        f = open("%s/splitLists_b%.2f_pt%2.0f_n%d/split_%i_%s_%s"%(samplesListsDir,
								   1000*maxBias,
								   minPt,nBiasBins,
								   fid,symasym,
								   inputFile),'w')
        for i,line in enumerate(inputSamplesList):
            print "%i : \n      %s" % (i,line)
            if "root" not in line:
                print("skipping line without a root file")
                continue
            if line[0] == "#":
                print("skipping commented line")
                continue
            f.write(line)
            lineswritten+=1
            totlineswritten+=1
            # if lineswritten == chunksize and fid < numberOfJobs:
            if lineswritten == chunksize and totlineswritten != num_input_samples:
                f.close()
                fid += 1
                lineswritten = 0
                f = open("%s/splitLists_b%.2f_pt%2.0f_n%d/split_%i_%s_%s"%(samplesListsDir,
									   1000*maxBias,
									   minPt,nBiasBins,
									   fid,symasym,
									   inputFile),'w')
		pass
	    pass
        f.close()
        return fid

def bSubSplitJobs(pyScriptName,toolName,outputFile,inputFile,proxyPath,numberOfJobs,
		  runPeriod,maxBias,minPt,nBiasBins,simlow,simhigh,pseudoThresh,
		  symmetric,trigger,isMC,doClosure,debug):
    symasym = "asym"
    if symmetric:
        symasym = "sym"
	pass
    samplesListsDir="samplesLists_data"

    # if not os.path.exists("/tmp/%s/output_%s_b%.2f_pt%2.0f_n%d_%s"%(os.getlogin(),pyScriptName,
    #     							    1000*maxBias,minPt,nBiasBins,symasym)):
    mkdir_p("/tmp/%s/output_%s_b%.2f_pt%2.0f_n%d_%s"%(  os.getlogin(),pyScriptName,
								1000*maxBias,minPt,nBiasBins,symasym))
	# pass

    rootScriptDir = "bsubs_b%.2f_pt%2.0f_n%d/roots"%(1000*maxBias,minPt,nBiasBins)
    # if not os.path.exists(rootScriptDir):
    mkdir_p(rootScriptDir)
	# pass

    clearSplitLists(maxBias,minPt,nBiasBins,symasym,inputFile)
    clearBsubShellScripts(maxBias,minPt,nBiasBins,symasym,inputFile)
    nJobs = splitJobsForBsub(inputFile,numberOfJobs,maxBias,minPt,nBiasBins,symasym)
    print "Prepared %i jobs ready to be submitted to bsub." % nJobs
    for i in range (1,nJobs+1):
        splitListFile="split_%i_%s_%s" % (i,symasym,inputFile)
        rootScriptName = "root-%s-b%.2f_pt%2.0f_n%d_%s_%d.C"%(pyScriptName,1000*maxBias,minPt,nBiasBins,symasym,i)
        with open("%s/%s"%(rootScriptDir,rootScriptName),"w") as f:
            f.write("{\n")
            # f.write("  gROOT->ProcessLine(\" .L %s/%s.so\");\n"%(os.getcwd()))
            inputFileList = samplesListsDir + "/splitLists_b%.2f_pt%2.0f_n%d/"%(1000*maxBias,minPt,nBiasBins) + splitListFile
            f.write("  gROOT->ProcessLine(\" .L %s.so\");\n"%(toolName))
            if (toolName=="Plot" and isMC and doClosure):
                f.write("  gROOT->ProcessLine(\" .L MCClosurePlot.so\");\n")
                pass
            ## the first execution seems to clear the proxy error
            f.write("  %s(\"%s\", \"%s_%s_%d_\", %d, %.2f, %.5f, %d, %.2f, %.2f, %.2f, %d, %d, %d, %d);\n"%(toolName,inputFileList,
                                                                                                            symasym,outputFile,i,
                                                                                                            1,
                                                                                                            minPt,maxBias,nBiasBins,
                                                                                                            1000.,simlow,simhigh,
                                                                                                            symmetric,trigger,isMC,debug))
            for tk in range(5):
                if debug and tk < 4:
                    continue
                f.write("  %s(\"%s\", \"%s_%s_%d_\", %d, %.2f, %.5f, %d, %.2f, %.2f, %.2f, %d, %d, %d, %d);\n"%(toolName,inputFileList,
                                                                                                                symasym,outputFile,i,
                                                                                                                tk+1,
                                                                                                                minPt,maxBias,nBiasBins,
                                                                                                                1000.,simlow,simhigh,
                                                                                                                symmetric,trigger,isMC,debug))
                if (toolName=="Plot" and isMC and doClosure and tk==4):
                    if debug:
                        f.write("  for (int etb = 0; etb < 1; ++etb)\n")
                        f.write("    for (int phb = 0; phb < 1; ++phb) {\n")
                    else:
                        f.write("  for (int etb = 0; etb < 2; ++etb)\n")
                        f.write("    for (int phb = 0; phb < 2; ++phb) {\n")
                        pass
                    for seed in range(25):
                        f.write("      MCClosurePlot(\"%s\", \"%s_%s_%d_\", etb, phb, %d, %.2f, %.5f, %d, %.2f, %.2f, %.2f, %.5f, %d, %d, %d, %d, %d);\n"%(inputFileList,
                                                                                                                                                           symasym,outputFile,i,
                                                                                                                                                           tk+1,
                                                                                                                                                           minPt,maxBias,nBiasBins/4,
                                                                                                                                                           1000.,simlow,simhigh,pseudoThresh,seed+1,
                                                                                                                                                           symmetric,trigger,isMC,debug))
                        pass
                    f.write("    }\n")
                    pass ## end if (toolName=="Plot")
                pass ## end for tk in range(5)
            f.write("}\n")
        # root -x -b -q  put this in the shell script
        pyCommand = "%s"%(rootScriptName)
        makeBsubShellScript(pyCommand,toolName,rootScriptDir,"%s/splitLists_b%.2f_pt%2.0f_n%d/%s"%(samplesListsDir,1000*maxBias,
                                                                                                   minPt,nBiasBins,splitListFile),
                            pyScriptName,i,proxyPath,runPeriod,maxBias,minPt,nBiasBins,symasym,outputFile,isMC,doClosure,debug)
        pass
    return


def makeBsubShellScript(pyCommand,toolName,rootScriptDir,splitListName,pyScriptName,index,proxyPath,
			runPeriod,maxBias,minPt,nBiasBins,symasym,outputFile,isMC=False,doClosure=False,debug=False):
    basedir   = "bsubs_b{:.2f}_pt{:2.0f}_n{:d}".format(1000*maxBias,minPt,nBiasBins)
    subscript = "{:s}/scripts/bsub-{:s}-{:s}-{:d}.sh".format(basedir,pyScriptName,symasym,index)
    logfile   = "bsub-{:s}-{:s}-{:d}".format(pyScriptName,symasym,index)

    mkdir_p("{:s}/scripts".format(basedir))
    mkdir_p("{:s}/logs".format(basedir))
    mkdir_p("{:s}/output".format(basedir))
    mkdir_p("{:s}/error".format(basedir))
    subfile   = "{:s}/bsub-{:s}-{:s}-{:d}.sub".format(basedir,pyScriptName,symasym,index)
    # most jobs are quick, less than 30 minutes, so the 2 hr queue should be fine
    jobType = "longlunch"
    if isMC and doClosure:
        # MC jobs (with closure study) take a long time to write the files, the full day queue is more robust against a few long jobs
        jobType = "tomorrow"

    with open(subfile,"w") as f:
        f.write("""
executable  = {0:s}
arguments   = $(ClusterID) $(ProcId)
output      = {1:s}/output/{2:s}.$(ClusterId).$(ProcId).out
error       = {1:s}/error/{2:s}.$(ClusterId).$(ProcId).err
log         = {1:s}/logs/{2:s}.$(ClusterId).log
+JobFlavour = "{3:s}"
RequestCpus = 2
queue
""".format(subscript,basedir,logfile,jobType)
                )

    with open(subscript,"w") as f:
        f.write("""#!/bin/bash
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
export X509_USER_PROXY=%s

kinit -R
aklog
klist

echo "hostname is $HOSTNAME"
export JOBDIR=${PWD}
echo "batch job directory is ${JOBDIR}"
export OUTPUTDIR=${JOBDIR}/output_%s_b%.2f_pt%2.0f_n%d_%s
echo "output directory is ${OUTPUTDIR}"
mkdir ${OUTPUTDIR}
ls -tar

cd %s
export AFSJOBDIR=${PWD}
eval `scram runtime -sh`
cp binFunctions.h ${JOBDIR}/
cp MCClosurePlot* ${JOBDIR}/
cp %s* ${JOBDIR}/
cp %s/%s ${JOBDIR}/
cd ${JOBDIR}
root -b -x -q MCClosurePlot.cc++g
root -b -x -q Plot.cc++g
ls -tar
root -b -q -x %s
tree

# need newer ROOT version?
hadd -j -f  ${OUTPUTDIR}/%s_%s_%d_closure_TuneP.root ${OUTPUTDIR}/%s_%s_%d_*_eta?_phi?_pseudo*.root
rm ${OUTPUTDIR}/%s_%s_%d_*_eta?_phi?_pseudo*.root

export EOSOUTDIR=/eos/cms/store/user/${USER}/CosmicEndpoint/%s/output_%s_b%.2f_pt%2.0f_n%d_%s
eos mkdir -p ${EOSOUTDIR}
xrdcp -d 0 -f -r ${OUTPUTDIR}/*.root root://eoscms.cern.ch/${EOSOUTDIR}/

#echo "rsync -e \\"ssh -T -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\\" -ahu --progress ${OUTPUTDIR} ${JOBDIR}/myeos/output_%s_b%.2f_pt%2.0f_n%d_%s/ --exclude=\"*.png\" --exclude=\"*.txt\""
#rsync -e "ssh -T -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" -ahu --progress ${OUTPUTDIR} ${JOBDIR}/myeos/output_%s_b%.2f_pt%2.0f_n%d_%s/ --exclude=\"*.png\" --exclude=\"*.txt\"

echo "rsync -e \\"ssh -T -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\\" -ahu --progress ${OUTPUTDIR} %s:/tmp/${USER}/" --exclude=\"*.png\" --exclude=\"*.root\"
rsync -e "ssh -T -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" -ahu --progress ${OUTPUTDIR} %s:/tmp/${USER}/ --exclude=\"*.png\" --exclude=\"*.root\"
"""%(proxyPath,
     pyScriptName,1000*maxBias,minPt,nBiasBins,symasym,
     os.getcwd(),
     toolName,
     rootScriptDir,pyCommand,
     pyCommand,
     symasym,outputFile,index,symasym,outputFile,index,
     symasym,outputFile,index,
     runPeriod,pyScriptName,1000*maxBias,minPt,nBiasBins,symasym,
     pyScriptName,1000*maxBias,minPt,nBiasBins,symasym,
     pyScriptName,1000*maxBias,minPt,nBiasBins,symasym,
     socket.gethostname(),
     socket.gethostname()))

    os.chmod(subscript,0777)

    if not debug:
        # cmd = "bsub -q 1nd -W 620 %s"%(subfile)
        cmd = "condor_submit {:s}".format(subfile)
        print cmd
        os.system(cmd)
    else:
        # cmd = "bsub -q test -W 620 %s"%(subfile)
        cmd = "condor_submit {:s}".format(subfile)
        print cmd
	pass
    return

def clearSplitLists(maxBias,minPt,nBiasBins,symasym,title):
    samplesListsDir="samplesLists_data"
    splitListsDir=samplesListsDir+"/splitLists_b%.2f_pt%2.0f_n%d/"%(1000*maxBias,minPt,nBiasBins)

    # if not os.path.exists(splitListsDir):
    mkdir_p(splitListsDir)
	# pass

    for the_file in os.listdir(splitListsDir):
        file_path = os.path.join(splitListsDir,the_file)
        if ((file_path.find("_"+symasym+"_") > 0) and (file_path.find(title) > 0)):
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception,e:
                print e
		pass
	    pass
	pass
    return

def clearBsubShellScripts(maxBias,minPt,nBiasBins,symasym,title):
    bSubScriptsDir="bsubs_b%.2f_pt%2.0f_n%d/"%(1000*maxBias,minPt,nBiasBins)
    # d = os.path.dirname(bSubScriptsDir)
    # if not os.path.exists(bSubScriptsDir):
    mkdir_p(bSubScriptsDir)
	# pass

    for the_file in os.listdir(bSubScriptsDir):
        file_path = os.path.join(bSubScriptsDir,the_file)
        if ((file_path.find("-"+symasym+"-") > 0) and (file_path.find(title) > 0)):
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
		    pass
            except Exception,e:
                print e
		pass
	    pass
	pass
    return
