#!/usr/bin/python

#Simple utility to generate the analyze job file and submit it, for all 10 competitions
#Command line arguments:
	#1: the input directory containing the competition results
	#2: the output directory to store all the data

#This assumes that you have already run scripts/renameCompPopulations on all the competition directories!
import sys
import subprocess

if len(sys.argv) != 3:
	print "Usage: python submitAllAnalyze.py <COMPETITON_RESULT_POP_DIR> <OUTPUT_DIR>"
	quit()

inputDir = sys.argv[1]
outputDir = sys.argv[2]

for i in range(1, 11):
	#Create the analyze qsub file
	jobScript = open("analyze_comp%s.qsub" %i, "w")

	jobScript.write("#!/bin/bash -login\n")
	jobScript.write("#PBS -l walltime=03:59:00,nodes=1:ppn=1,mem=4gb\n")
	jobScript.write("#PBS -j oe\n")
	jobScript.write("#PBS -N analyze-competitions\n\n")


	jobScript.write("#Load the Avida module\n")
	jobScript.write("module load avida\n\n")

	jobScript.write("#Change to your working directory\n")
	jobScript.write("cd %s\n" %os.path.abspath("."))

	jobScript.write("#Run the analyze script\n")
	jobScript.write("python analyze.py %s/comp%s  %s/comp%s\n" %(inputDir, i, outputDir, i))

	jobScript.close()


	#Now submit the job script we just created
	subprocess.call(["qsub", "analyze_comp%s.qsub" %i])
