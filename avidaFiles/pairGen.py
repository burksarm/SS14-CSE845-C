#!/usr/bin/python
import sys
import os
import subprocess

#Check command-line arguments.
if len(sys.argv) != 3:
	print "Usage: python pairGen.py <ANCESTOR_DIRECTORY> <OUTPUT_DIRECTORY>"
	quit()

#Run the compare script to make sure we have our environments and events setup
#subprocess.call(["python", "../scripts/compare.py"])

ancestorDir = sys.argv[1]
outputDir   = sys.argv[2]

#Make sure the top-level output directory exists
if not os.path.exists(outputDir):
	os.makedirs(outputDir)


runList = [] #Holds the commands we need to run to generate the pairs

#Go through each dominant ancestor, figure out the genome-wide mutation rates for both 0.5 and 2.0
for dirname, dirs, files in os.walk(ancestorDir):
	for fname in files:
		file = open(os.path.join(ancestorDir, fname), "r")
		for line in file:
			#Find the Genome Size comment line in the file
			if line.startswith("# Genome Size"):
				size = float(line.split()[-1])
				
				#Calculate the copy mutation rate to set, based on the desired genome-wide rate
				low = 0.5/size
				high = 2.0/size

				#Put some arguments into variables to make the command more readable
				startOrg = os.path.join(ancestorDir, fname)

				orgA = os.path.join(outputDir, "%s-A" %fname)
				orgB = os.path.join(outputDir, "%s-B" %fname)

				#Create a simple events file to fill the pop with the start org
				#and collect the dominant genotype after 1000 generations
				eventsFileA = open("events_%s_adapt.cfg" %fname, "w")
				eventsFileA.write("u begin InjectAll %s\n" %startOrg)
				eventsFileA.write("g 1000 PrintDominantGenotype\n")
				eventsFileA.write("g 1000 Exit\n")
				eventsFileA.close()

                                eventsFileB = open("events_%s_adapt.cfg" %fname, "w")
                                eventsFileB.write("u begin InjectAll %s\n" %startOrg)
                                eventsFileB.write("g 1000 PrintDominantGenotype\n")
                                eventsFileB.write("g 1000 Exit\n")
                                eventsFileB.close()


				#Run Avida with both the low and high mutation rate ~10 at a time
				runList.append("avida -v0 -c avida_adapt.cfg -set DATA_DIR %s -set COPY_MUT_PROB %s -set EVENT_FILE %s"
					%(orgA, low, eventsFileA.name))

				
 				runList.append("avida -v0 -c avida_adapt.cfg -set DATA_DIR %s -set COPY_MUT_PROB %s -set EVENT_FILE %s" 
					%(orgB, high, eventsFileB.name))


				#done with this file.
				break



#Now Create a job file for each run and submit it
for i in range(len(runList)):
	runFile = open("pairgen-%s.qsub" %i, "w")
	runFile.write("#!/bin/bash -login\n")
	runFile.write("#PBS -l walltime=01:00:00,nodes=1:ppn=1,mem=4gb\n")
	runFile.write("#PBS -j oe\n")
	runFile.write("#PBS -N pairgen-%s\n" %i)

	runFile.write("#Load the Avida module\n")
	runFile.write("module load avida\n")

	runFile.write("#Change to your working directory\n")
	runFile.write("cd %s\n" %(os.path.abspath(".")))

	runFile.write("#For each ancestor, run avida with mutation rate 0.5 and 2.0\n")
	runFile.write("%s\n" %runList[i])

	runFile.close();

	subprocess.call(["qsub", runFile.name])











