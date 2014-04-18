#!/usr/bin/python
import sys
import imp
import os
import subprocess
import competitions_parentmut as compScript

#Convenience method to generate the run string, making sure the outDir exists
def generateCmd(org, ab, eventFile, outDir, targetMutRate):
	mutRate = compScript.calcMutRate("../organisms/complexPool/%s.org" %org, targetMutRate)/2.0
	outputDir = outDir + "/%s-%s-%s" %(org, ab, targetMutRate)

	#Make sure the sub-directory exists
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)

	#Generate the hideous command
	cmd = "avida -v0 -c avida_comp.cfg -set DATA_DIR %s -set EVENT_FILE %s -set ENVIRONMENT_FILE environment_%s_comp.cfg -set COPY_MUT_PROB %.10f -set PARENT_MUT_PROB %.10f" %(outputDir, eventFile, org, mutRate, mutRate)

	return cmd

#Convenience method to figure out the org's merit from the organism file
def getOrgMerit(fName):
	for line in open(fName):
		if line.startswith("# Merit"):
			return float(line.strip().split()[-1])

argc = len(sys.argv)
if argc < 3:
	print "Usage analyzeTasks.py <OUTPUT_DIRECTORY> <NUM_GENS> <MUT_RATES (optional. ex. '0.5,3.0')>"
	quit()

MUT_RATES = [0.5, 3.0]
NUM_GENS = sys.argv[2]

if argc == 4:
	MUT_RATES = [float(rate) for rate in sys.argv[2].split(",")]

#Get output directory
outDir = sys.argv[1]

#Make sure the output path exists (and each competition directory)
if not os.path.exists(outDir):
	os.makedirs(outDir)

#First get the good competition organism names from file.
goodComps = []

inFile = open("../results/goodComps.txt", "r")

for line in inFile:
	goodComps.append(line.strip())

runList = [] #Holds all the runs we'll need

#For each org, run it in isolation and collect stats on it
for org in goodComps:
	#Create an event file to run the org in isolation (A & B)
	eventFileA = open("events_%s-A_isolation.cfg" %org, "w")
	eventFileB = open("events_%s-B_isolation.cfg" %org, "w")

	#Get the initial a and b merit...
	aMerit = getOrgMerit("../organisms/flatPool/%s.org-A" %org)
	bMerit = getOrgMerit("../organisms/flatPool/%s.org-B" %org)

	#Inject the organism
	eventFileA.write("u begin Inject ../organisms/flatPool/%s.org-A 0 %.10f 0\n" %(org, aMerit))
	eventFileB.write("u begin Inject ../organisms/flatPool/%s.org-B 0 %.10f 1\n" %(org, bMerit))

	#Get the average stats for each generation
	eventFileA.write("g 0:5 PrintAverageData\n")
	eventFileB.write("g 0:5 PrintAverageData\n")

	#Tasks aren't in the average.dat file. We want them.
	eventFileA.write("g 0:5 PrintAveNumTasks\n")
	eventFileB.write("g 0:5 PrintAveNumTasks\n")

	#Stop after NUM_GENS generations
	eventFileA.write("g %s Exit\n" %NUM_GENS)
	eventFileB.write("g %s Exit\n" %NUM_GENS)
	
	#Done
	eventFileA.close()
	eventFileB.close()

	#Now get the command for this org and add it to the run list
	for mutRate in MUT_RATES:
		runList.append(generateCmd(org, "A", eventFileA.name, outDir, mutRate))
		runList.append(generateCmd(org, "B", eventFileB.name, outDir, mutRate))

#Divide the runs into a few job files
runNum = 0
jobFiles = []

for i in range(10):
	#Create a new job file
	jobFile = open("analyzeTasks-%s.qsub" %i, "w")

	jobFile.write("#!/bin/bash -login\n")
	jobFile.write("#PBS -l walltime=02:00:00,nodes=1:ppn=1\n")
	jobFile.write("#PBS -j oe\n")
	jobFile.write("#PBS -N analyze-tasks-%s\n\n" %i)

	#Change to the current directory
	jobFile.write("cd %s\n" %os.path.abspath("."))

	#Load the avida module
	jobFile.write("module load avida\n\n")
	
	#now add up to total/10 run commands
	chunk = len(runList)/10

	for run in range(runNum, runNum + chunk + 1):
		if run < len(runList):
			jobFile.write(runList[run] + "\n")
			runNum += 1


	jobFile.close()
	jobFiles.append(jobFile.name)


#Finally submit all the jobs
for jobFile in jobFiles:
	subprocess.call(("qsub %s" %jobFile).split())






