##############
CosmicEndpoint
##############

**************
Background
**************
The cosmic endpoint method is designed to quantify a bias in the pT measurement of muons using the cosmic ray muon samples collected by the CMS experiment.
This is done by comparing the curvature distributions between data and MC simulation, and stepwise adding an artificial bias to the MC until the data and MC are in agreement.
The uncertainty in this method is taken as the width of the resulting bias scan at a point where the difference from the minimum chi2 is 1.

These tools are designed to perform some additional closure studies, looking at MC only and using some of the MC as pseudodata, and validating the method by shifting the remaining MC as in the aforementioned method.

Not yet fully implemented is the comparison between mu+ and mu- for data and MC separately.

Description of the tools
========================

python tools
____________
* resultsPlotter.py
* makeGIF_asym.py
* runEndpoint.py
* efficiencyPlotter.py
* handUncertainties.py
* trackFitChi2Plotter.py
* trackToMuonEfficiency.py
* cosmicTagAndProbe.py
* efficiencyPlotter2.py
* efficiencyStudy.py
* testMCScaling.py
* testing.py
* quickResidualTest.py
* makeGIF_sym.py
* plotL1Efficiencies.py
* getScaleFactors.py
* bsubGenScaling.py
* bsubEfficiency.py
* runGenL1Studies.py
* quickCheck.py
* makePresentablePlots.py
* makeNewClosurePlots.py
* makeClosurePlots.py
* macrotools.py
* bsubSubmit.py
* bsubClosureStudy.py
* quickHistogramPlotter.py
* endpointPlusMinusStudy.py
* endpointDataMCStudy.py
* dataMCComparisonPlots.py
* makeEndpointPlots.py
* endpointClosureStudy.py

Shell scripts
_____________
* runMinimization.sh
* test.sh
* making.gifs.sh
* getoutputs.sh
* doClosureStudy.sh
* haddendpointresults.sh
* runclosuretests.sh
* countfiles.sh
* dothestudy.sh
* setup.sh
* findFailedJobs.sh
* moveToEOS.sh
* animate.sh
* getclosureresults.sh
* full.closure.study.sh
* killed.to.resub.sh
* get.full.closure.study.results.sh
* getendpointresults.sh
* submitPlots.sh
* runendpointstudy.sh
* makeFileLists.sh


**************
Usage
**************

Getting set up
==============


Running the analysis
====================

Creating the TTrees
____________________
The first step in this analysis is to create TTrees of both the data and MC simulation.
This is accomplished with the MuonAnalysis subpackage (described in MuonAnalysis.rst)
Once this has been completed the tools in the CosmicEndpoint package will be used to process these TTrees and create the shifted histograms and the pseudoexperiments (Plot and MCClosurePlot)

Creating the endpoint inputs
____________________________
The TTrees from the MuonAnalysis package are created at some storage location and must be parsed into an input list for the endpoint tools. This is currently taken care of by a bash script makeFileLists.sh

makeFileLists.sh
++++++++++++++++
makeFileLists.sh is currently set up to be modified by hand with the directory where an individual output sample is stored and will create the corresponding input file list

submitPlots.sh
++++++++++++++
submitPlots.sh is a bash script that will drive the batch submission of the endpoint histogram creation.
The arrays are defined as the input file lists created in the makeFileLists.sh step.
submitPlots.sh will execute bsubSubmit.py on each of the defined samples with the options specified in the file (again, the expectation is that this file will be modified to ensure that the correct options are used.

bsubSubmit.py
+++++++++++++
bsubSubmit.py will take the input file list and the passed options and create a set of batch jobs to split the processing of the samples into multiple jobs

.. code-block:: bash

