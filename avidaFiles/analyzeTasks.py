#!/usr/bin/python
import sys
import imp
import os
import subprocess

argc = len(sys.argv)
if argc < 3:
	print "Usage analyzeTasks.py <TOP-LEVEL_COMPETITION_RESULTS_DIRECTORY> <OUTPUT_DIRECTORY> <MUT_RATES (optional. ex. .'5,3')>"
	quit()

MUT_RATES = [0.5, 3.0]

if argc == 4:
	MUT_RATES = sys.argv[3].split(",")

#Get the input and output directory
compDir = sys.argv[1]
outDir = sys.argv[2]

#Make sure the output path exists (and each competition directory)
if not os.path.exists(outDir):
	os.makedirs(outDir)

#First get the good competition organism names from file.
goodComps = []

inFile = open("../results/goodComps.txt", "r")

for line in inFile:
	goodComps.append(line.strip())


jobFiles = []
#Create an analyze file for each competition run
for comp in range(1, 11):
	analyzeFile = open("analyzeTasks%s.cfg"  %comp, "w")

	for org in goodComps:
		for mutRate in MUT_RATES:
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

			#Run RECALCULATE
			analyzeFile.write("\t#Run RECALCULATE\n")
			analyzeFile.write("\tRECALCULATE\n\n")

			#Run Detail and get the lineage label, num_cpus and whether or not 
			#each task was performed
			analyzeFile.write("\t#Get the tasks for all the A/B descendants\n")
			analyzeFile.write("\tDETAIL %s/comp%s-tasks-%s-%s-$i lineage num_cpus task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8\n" 
				%(outDir, comp, org, mutRate))

			#Done
			analyzeFile.write("END\n\n")

	analyzeFile.close()

	#Now Create and run a job file for the analyze script
	jobFile = open("analyzeTasks%s.qsub" %comp, "w")

	jobFile.write("#!/bin/bash -login\n")
	jobFile.write("#PBS -l walltime=01:00:00,nodes=1:ppn=1\n")
	jobFile.write("#PBS -j oe\n")
	jobFile.write("#PBS -N analyze-tasks-%s\n\n" %comp)

	#Change to the current directory
	jobFile.write("cd %s\n" %os.path.abspath("."))

	#Load the avida module
	jobFile.write("module load avida\n")

	#Run the analyze file
	jobFile.write("avida -a -c avida_comp.cfg -set ENVIRONMENT_FILE environment.cfg -set EVENT_FILE events.cfg -set ANALYZE_FILE %s -set DATA_DIR %s\n" 
		%(analyzeFile.name, outDir))


	jobFile.close()
	jobFiles.append(jobFile.name)


for jobFile in jobFiles:
	subprocess.call(("qsub %s" %jobFile).split())






