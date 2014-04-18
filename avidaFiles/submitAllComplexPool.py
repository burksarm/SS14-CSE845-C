#!/usr/bin/python

#Simple utility to generate the complex pool creation job file and submit it
#for all 40 populations

#Command line argument:
	#1: the output directory

import sys
import os
import subprocess

if len(sys.argv) != 2:
	print "Usage: python submitAllComplexPool.py <OUTPUT_DIR>"
	quit()

outputDir = sys.argv[1]

if not os.path.exists(outputDir):
	os.makedirs(outputDir)

for i in range(1, 41):
	#Create the  qsub file
	jobScript = open("complex-pool%s.qsub" %i, "w")

	jobScript.write("#!/bin/bash -login\n")
	jobScript.write("#PBS -l walltime=05:40:00,nodes=1:ppn=1,mem=4gb\n")
	jobScript.write("#PBS -j oe\n")
	jobScript.write("#PBS -N complex-pool%s\n\n" %i)


	jobScript.write("#Load the Avida module\n")
	jobScript.write("module load avida\n\n")

	jobScript.write("#Change to your working directory\n")
	jobScript.write("cd %s\n" %os.path.abspath("."))

	jobScript.write("#Run the competition script\n")
	jobScript.write("python complex.py %s/tmp%s\n\n" %(outputDir, i))

	#Go ahead and copy the org over and remove the temp directory
	jobScript.write("#Copy the organism over and delete the temp dir\n")
	jobScript.write("cp %s/tmp%s/archive/*.org %s/dom-%s.org\n" %(outputDir, i, outputDir, i))
        jobScript.write("rm -rf %s/tmp%s\n" %(outputDir, i))


	jobScript.close()


	#Now submit the job script we just created
	subprocess.call(["qsub", "complex-pool%s.qsub" %i])
