import subprocess
import math
import os,socket
import shutil

# copied from John Hakala's bhmacros and modified for quick use here
def callMacro(macroName,inputFile,outputFile):
	macroCommand = "%s(\"%s\", \"%s\")" % (macroName,inputFile,outputFile)
	subprocess.call(["root", "-l", "-q",macroCommand])

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
		f = open("%s/splitLists_b%.2f_pt%2.0f_n%d/split_%i_%s_%s"%(samplesListsDir,
									 1000*maxBias,
									 minPt,nBiasBins,
									 fid,symasym,
									 inputFile),'w')
		for i,line in enumerate(inputSamplesList):
			#print "%i : \n      %s" % (i,line)
			f.write(line)
			lineswritten+=1
			if lineswritten == chunksize:# and fid < numberOfJobs:
				f.close()
				fid += 1
				lineswritten = 0
				f = open("%s/splitLists_b%.2f_pt%2.0f_n%d/split_%i_%s_%s"%(samplesListsDir,
											 1000*maxBias,
											 minPt,nBiasBins,
											 fid,symasym,
											 inputFile),'w')
		f.close()
		return fid

def bSubSplitJobs(pyScriptName,toolName,outputFile,inputFile,proxyPath,numberOfJobs,
		  runPeriod,maxBias,minPt,nBiasBins,simlow,simhigh,pseudoThresh,
		  symmetric,trigger,isMC,doClosure,debug):
	symasym = "asym"
	if symmetric:
		symasym = "sym"

	samplesListsDir="samplesLists_data"

	if not os.path.exists("/tmp/%s/output_%s_b%.2f_pt%2.0f_n%d_%s"%(os.getlogin(),pyScriptName,
									1000*maxBias,minPt,nBiasBins,symasym)):
		os.makedirs("/tmp/%s/output_%s_b%.2f_pt%2.0f_n%d_%s"%(  os.getlogin(),pyScriptName,
									1000*maxBias,minPt,nBiasBins,symasym))

	rootScriptDir = "bsubs_b%.2f_pt%2.0f_n%d/roots"%(1000*maxBias,minPt,nBiasBins)
	if not os.path.exists(rootScriptDir):
		os.makedirs(rootScriptDir)

	clearSplitLists(maxBias,minPt,nBiasBins,symasym,inputFile)
	clearBsubShellScripts(maxBias,minPt,nBiasBins,symasym,inputFile)
	nJobs = splitJobsForBsub(inputFile,numberOfJobs,maxBias,minPt,nBiasBins,symasym)
	print "Prepared %i jobs ready to be submitted to bsub." % nJobs
	for i in range (1,nJobs+1):
		splitListFile="split_%i_%s_%s" % (i,symasym,inputFile)
		rootScriptName = "root-%s-b%.2f_pt%2.0f_n%d_%s_%d.C"%(pyScriptName,1000*maxBias,minPt,nBiasBins,symasym,i)
		f = open("%s/%s"%(rootScriptDir,rootScriptName),"w")
		f.write("{\n")
		#f.write("  gROOT->ProcessLine(\" .L %s/%s.so\");\n"%(os.getcwd()))
		inputFileList = samplesListsDir + "/splitLists_b%.2f_pt%2.0f_n%d/"%(1000*maxBias,minPt,nBiasBins) + splitListFile
		f.write("  gROOT->ProcessLine(\" .L %s.so\");\n"%(toolName))
		if (toolName=="Plot" and isMC and doClosure):
			f.write("  gROOT->ProcessLine(\" .L MCClosurePlot.so\");\n")
			pass
		##the first execution seems to clear the proxy error
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
				    pyScriptName,i,proxyPath,runPeriod,maxBias,minPt,nBiasBins,symasym,outputFile,debug)
		pass
	pass


def makeBsubShellScript(pyCommand,toolName,rootScriptDir,splitListName,pyScriptName,index,proxyPath,
			runPeriod,maxBias,minPt,nBiasBins,symasym,outputFile,debug):
	subfile = "%s/bsubs_b%.2f_pt%2.0f_n%d/bsub-%s-%s-%s.sh"%( os.getcwd(),1000*maxBias,minPt,nBiasBins,pyScriptName,symasym,index)
	logfile = "%s/bsubs_b%.2f_pt%2.0f_n%d/bsub-%s-%s-%s.log"%(os.getcwd(),1000*maxBias,minPt,nBiasBins,pyScriptName,symasym,index)
	f = open(subfile,"w")
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
ls -tar
root -b -q -x %s
tree
hadd  ${OUTPUTDIR}/%s_%s_%d_closure_TuneP.root ${OUTPUTDIR}/%s_%s_%d_*_eta?_phi?_pseudo*.root
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
	f.close()
	os.chmod(subfile,0777)
	if not debug:
		cmd = "bsub -q 1nd -W 620 %s"%(subfile)
		print cmd
		os.system(cmd)
	else:
		cmd = "bsub -q test -W 620 %s"%(subfile)
		print cmd

def clearSplitLists(maxBias,minPt,nBiasBins,symasym,title):
	samplesListsDir="samplesLists_data"
	splitListsDir=samplesListsDir+"/splitLists_b%.2f_pt%2.0f_n%d/"%(1000*maxBias,minPt,nBiasBins)

	if not os.path.exists(splitListsDir):
		os.makedirs(splitListsDir)

	for the_file in os.listdir(splitListsDir):
		file_path = os.path.join(splitListsDir,the_file)
		if ((file_path.find("_"+symasym+"_") > 0) and (file_path.find(title) > 0)):
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				# elif os.path.isdir(file_path): shutil.rmtree(file_path)
			except Exception,e:
				print e

def clearBsubShellScripts(maxBias,minPt,nBiasBins,symasym,title):
	bSubScriptsDir="bsubs_b%.2f_pt%2.0f_n%d/"%(1000*maxBias,minPt,nBiasBins)
        #d = os.path.dirname(bSubScriptsDir)
        if not os.path.exists(bSubScriptsDir):
                os.makedirs(bSubScriptsDir)

	for the_file in os.listdir(bSubScriptsDir):
		file_path = os.path.join(bSubScriptsDir,the_file)
		if ((file_path.find("-"+symasym+"-") > 0) and (file_path.find(title) > 0)):
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				# elif os.path.isdir(file_path): shutil.rmtree(file_path)
			except Exception,e:
				print e
