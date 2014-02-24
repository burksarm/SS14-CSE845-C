#!/usr/bin/python
import sys
import os
import competitions #So we can steal some code
import subprocess

#Simply runs a single competition (all mut rates) on a particular organism pair
#Takes the path to the competition organism directory, the name of the organism,
#(i.e. dom-i) and the output directory

#Check command line args
if len(sys.argv) != 4:
	print "Usage: python singleComp.py <COMP_ORGANISM_DIR> <COMP_ORGANISM_NAME> <OUTPUT_DIR>"
	quit()

compOrgDir = sys.argv[1]
compOrg = sys.argv[2]
outputDir = sys.argv[3]

#Make sure the whole output path exists, otherwise avida won't actually save
if not os.path.exists(outputDir):
	os.makedirs(outputDir)

#Get the environment and events file for the competition
environmentFile = "environment_%s_comp.cfg" %compOrg
eventsFile = "events_%s_comp.cfg" %compOrg

#Get the path to one of the organisms so we can figure out the mutation rate
orgAFile = os.path.join(compOrgDir, "%s.org-A" %compOrg)

targetMutRate = 0.5
while (targetMutRate <= 3.0):
	#Calculate the copy mutation rate
	copyMutRate = (competitions.calcMutRate(orgAFile, targetMutRate))
	parentMutRate = copyMutRate

	#Generate the intermediate output directory (i.e. for the mut rate)
	dataDir = os.path.join(outputDir, "%s-comp-%s" %(compOrg, targetMutRate))

	#Generate the run command
	runCommand = \
		"avida -c avida_comp.cfg -set EVENT_FILE %s -set ENVIRONMENT_FILE %s -set DATA_DIR %s -set COPY_MUT_PROB %.10f"\
		%(eventsFile, environmentFile, dataDir, copyMutRate)

	#Print the command as a sanity check
	print runCommand
	
	#Run it
	subprocess.call(runCommand.split())
	
	targetMutRate += 0.5










