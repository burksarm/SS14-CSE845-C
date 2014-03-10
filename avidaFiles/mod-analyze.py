#!/usr/bin/python
import sys
import imp
import os
import subprocess

#Import the environments module
environments = imp.load_source("environments", "../scripts/environments.py")

#Generates the analyze files for doing the modularity analysis.
#We only use the competitions from which we saw survival of the flattest.

if len(sys.argv) != 3:
	print "Usage mod-analyze.py <TOP-LEVEL_COMPETITION_RESULTS_DIRECTORY> <OUTPUT_DIRECTORY>"
	quit()

#Get the input and output directory
compDir = sys.argv[1]
outDir = sys.argv[2]

#Make sure the output path exists (and each competition directory)
if not os.path.exists(outDir):
	os.makedirs(outDir)

for comp in range(1, 11):
	if not os.path.exists(os.path.join(outDir, "comp%s" %comp)):
		os.makedirs(os.path.join(outDir, "comp%s" %comp))


#First get the good competition organism names from file.
goodComps = []

inFile = open("../results/goodComps.txt", "r")

for line in inFile:
	goodComps.append(line.strip())


#Now generate the analyze file for each competiton organism
mutRates = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
tasks = {"not":0, "nand":1, "and":2, "orn":3, "or":4, "andn":5, "nor":6, "xor":7, "equ":8}


#Analyze file -> environment file
analyzeFiles = {}

for org in goodComps:
	#Get the set of tasks performed by the ancestory
	ancATasks = environments.getTasks(open("../organisms/flatPool/%s.org-A" %org))
	ancBTasks = environments.getTasks(open("../organisms/flatPool/%s.org-B" %org))

	#Get the task lists we'll use in the modularity command
	aTaskList = " ".join(sorted(["task.%s" %(tasks[task]) for task in ancATasks]))
	bTaskList = " ".join(sorted(["task.%s" %(tasks[task]) for task in ancBTasks]))


	#Create a separate file for each competition run
	for comp in range(1, 11):
		for mutRate in mutRates:
			#Create the analyze file
			fName = "mod-analyze_%s-%s_comp%s.cfg" %(org, mutRate, comp)
			analyzeFile = open(fName, "w")

			#Add the filename to the collection
			analyzeFiles[fName] = "environment_%s_comp.cfg" %org

			#Load each generation 0-50, by 5
			analyzeFile.write("#Load each generation population file.\n")
			analyzeFile.write("FORRANGE i 0 50 5\n")

			#Cleanup from previously-loaded data.
			analyzeFile.write("\t#First, cleanup from previously-loaded data.\n")
			analyzeFile.write("\tPURGE_BATCH\n\n")

			#Now load the file
			competition = "%s-comp-%s" %(org, mutRate)
			analyzeFile.write("\tLOAD %s/detail-$i.spop\n\n" %os.path.abspath(os.path.join("%s/comp%s" %(compDir, comp), competition)))

			#Filter out genotypes with numCpus < 0
			analyzeFile.write("\t#Filter out genotypes with numCpus < 0\n")
			analyzeFile.write("\tFILTER num_cpus > 0\n\n")

			#Only look at A descendants.
			analyzeFile.write("\t#Only look at A descendants\n")
			analyzeFile.write("\tFILTER lineage == 0\n\n")

			#Run RECALCULATE
			analyzeFile.write("\t#Run RECALCULATE\n")
			analyzeFile.write("\tRECALCULATE\n\n")

			#Now do the modularity stats (based on the tasks the ancestor performed)
			analyzeFile.write("\t#Now do the modularity stats\n")
			analyzeFile.write("\tAVERAGE_MODULARITY %s/comp%s/modularity-%s-$i-A.dat %s\n\n" %(outDir, comp, competition, aTaskList))

			#Now cleanup the data from A
			analyzeFile.write("\t#Now cleanup the data from A\n")
			analyzeFile.write("\tPURGE_BATCH\n\n")

			#Reload the file so we can get B descendants
			analyzeFile.write("\t#Reload the file so we can get B descendants.\n")
			analyzeFile.write("\tLOAD %s/detail-$i.spop\n\n" %os.path.abspath(os.path.join("%s/comp%s" %(compDir, comp), competition)))

			#Filter out genotypes with numCpus < 0
			analyzeFile.write("\t#Filter out genotypes with numCpus < 0\n")
			analyzeFile.write("\tFILTER num_cpus > 0\n\n")

			#Only look at B descendants.
			analyzeFile.write("\t#Only look at B descendants\n")
			analyzeFile.write("\tFILTER lineage == 1\n\n")

			#Run RECALCULATE
			analyzeFile.write("\t#Run RECALCULATE\n")
			analyzeFile.write("\tRECALCULATE\n\n")

			#Now do the modularity stats (based on the tasks the ancestor performed)
			analyzeFile.write("\t#Now do the modularity stats\n")
			analyzeFile.write("\tAVERAGE_MODULARITY %s/comp%s/modularity-%s-$i-B.dat %s\n\n" %(outDir, comp, competition, bTaskList))

			#Done
			analyzeFile.write("END\n")
			analyzeFile.close()


#Now create 10 job files with the analyze files
analyzeFileNames = analyzeFiles.keys()
numToRun = len(analyzeFileNames)/10

for i in range(10):
	jobFile = open("mod-analyze-%s.qsub" %i, "w")
	jobFile.write("#!/bin/bash -login\n")
	jobFile.write("#PBS -l walltime=06:00:00,nodes=1:ppn=1\n")
	jobFile.write("#PBS -j oe\n")
	jobFile.write("#PBS -N analyze-modularity-%s\n\n" %i)

	jobFile.write("#Change to your working directory\n")
	jobFile.write("cd /mnt/home/burksarm/Documents/CSE845/SS14-CSE845-C/avidaFiles\n\n")

	jobFile.write("#Load the avida module.\n")
	jobFile.write("module load avida\n\n")

	#Get the analyze files to run
	start = i* numToRun
	end = start+numToRun -1
	filesToRun = analyzeFileNames[start:end]

	#Just make a separate command in the job file for each run
	for fName in filesToRun:
		jobFile.write("avida -c avida_comp.cfg -set ANALYZE_FILE %s -set ENVIRONMENT_FILE %s -set EVENT_FILE events.cfg -a\n"
			%(fName, analyzeFiles[fName]))

	jobFile.close()

	#Finally submit the job file
	subprocess.call(["qsub", jobFile.name])












	
