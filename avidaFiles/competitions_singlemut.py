#!/usr/bin/python
#Runs the competitions on all the pairs of organisms at all of the mutation rates.
import sys
import os
import re
import subprocess

#Calculates the mutation rate based on the genome length
#param fName the organism file
#param mutRate the genome-wide mutation rate with which to calculate the copy mutation rate
def calcMutRate(fName, mutRate):
	for line in open(fName):
			if line.startswith("# Genome Size"):
				genomeLength = float(line.split()[-1])
				return mutRate/genomeLength

def runComps(flatPoolDir, outputDir):
	#Make sure the output directory exists
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)

	#Use the environment file names to know which pair to compete.
	for dirname, dirs, files in os.walk("./"):
		for filename in files:
			m = re.match("environment_(dom-[\d]+)_comp", filename)
			if m != None:
				baseOrg = m.group(1)
			
				#Get the file names
				orgFiles = ("%s/%s.org-A" %(flatPoolDir, baseOrg), "%s/%s.org-B" %(flatPoolDir, baseOrg))
			
				#Now do the experiments for each mutation rate
				targetMutRate = 0.5
				while (targetMutRate <= 3.0):
					#Get the copy mutation rate (just use org A since they're the same length)
					copyMutRate = calcMutRate(orgFiles[0], targetMutRate)
					#parentMutRate = copyMutRate
				
					#Get the output directory name, based on the competition and the mutation rate
					outDir = "%s/%s-comp-%s" %(outputDir, baseOrg, targetMutRate)
				
					#Generate the run command, so we can print it (as a sanity check)
					runCommand = "avida -v0 -c avida_comp.cfg -set " +\
						"EVENT_FILE events_%s_comp.cfg -set ENVIRONMENT_FILE %s -set DATA_DIR %s -set COPY_MUT_PROB %.10f"\
						%(baseOrg, filename, outDir, copyMutRate)

					#Run the competition
					print runCommand
					subprocess.call(runCommand.split())
				
					targetMutRate += 0.5




if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "usage: python competitions.py <FLAT_ORGS_DIRECTORY> <OUTPUT_DIRECTORY>"
	else:
		runComps(sys.argv[1], sys.argv[2])
		subprocess.call(["python", "../scripts/renameCompPopulations.py", sys.argv[1]])		
			
