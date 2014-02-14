#!/usr//bin/python

#Simply generates an analyze file for each competition then runs avida with it.
#This is probably more work than needed, but hey, it beats searching for a quicker way.
#Run this from the avidaFiles directory.
import sys
import os
import subprocess


def generateAndRun():
	#Top-level competition directory passed into the script
	compDir = sys.argv[1]

	#Make sure the resulting output directory exists for the competition
	outDir = sys.argv[2]
	if not os.path.exists(outDir):
		os.makedirs(outDir)


	#Html or dat format for results?
	format = sys.argv[3] if len(sys.argv) == 4 else "dat"

	for dirname, dirs, filenames in os.walk(compDir):
		#For each competition subdirectory, create an analyze file and run it
		for competitionDir in dirs:
			#Create the analyze file
			analyzeFile = open("../avidaFiles/analyze_%s.cfg" %competitionDir, "w")

			#Now write the commands to the analyze file
			analyzeFile.write("FORRANGE i 5 50 5\n")
			analyzeFile.write("\tPURGE_BATCH\n")
			analyzeFile.write("\tLOAD %s/detail-$i.spop\n" %os.path.abspath(os.path.join(compDir, competitionDir)))
			analyzeFile.write("\tRECALCULATE\n")
			analyzeFile.write("\tDETAIL %s/%s-$i.%s lineage num_cpus id fitness total_task_count total_task_performance_count viable\n" %(outDir, competitionDir, format))
			analyzeFile.write("END\n")
			analyzeFile.close()
			

			#Now run Avida in analyze mode with the file
			subprocess.call(["avida", "-c", "avida_flat.cfg", "-set", "ANALYZE_FILE", analyzeFile.name, "-a"])



if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: python analyze.py <COMPETITION_RESULTS_ORGANISMS_DIR (required)> <OUTPUT_DIR (required)> <FORMAT (optional. html or dat)"
	else:
		generateAndRun()


