#!/usr/bin/python

#Simple utility to generate the competitions job file and submit it, for all 10 competitions
#Command line argument:
	#1: the input output directory to hold the 10 competion results

import sys
import subprocess

if len(sys.argv) != 2:
	print "Usage: python submitAllComps.py <OUTPUT_DIR>"
	quit()

outputDir = sys.argv[1]

for i in range(1, 11):
	#Create the competition qsub file
	jobScript = open("comp%s.qsub" %i, "w")

	jobScript.write("#!/bin/bash -login\n")
	jobScript.write("#PBS -l walltime=08:00:00,nodes=1:ppn=1,mem=4gb\n")
	jobScript.write("#PBS -j oe\n")
	jobScript.write("#PBS -N competition%s\n\n" %i)


	jobScript.write("#Load the Avida module\n")
	jobScript.write("module load avida\n\n")

	jobScript.write("#Change to your working directory\n")
	jobScript.write("cd %s\n" %os.path.abspath("."))

	jobScript.write("#Run the competition script\n")
	jobScript.write("python competitions.py %s/comp%s\n" %(outputDir, i))

	jobScript.close()


	#Now submit the job script we just created
	subprocess.call(["qsub", "comp%s.qsub" %i])
