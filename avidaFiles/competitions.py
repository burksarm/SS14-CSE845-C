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

def runComps(outputDir):
	#Use the environment file names to know which pair to run.
	for dirname, dirs, files in os.walk("./"):
		for filename in files:
			m = re.match("environment_(dom-[\d]+)_comp", filename)
			if m != None:
				baseOrg = m.group(1)
			
				#Get the file names
				orgFiles = ("../organisms/flatPool/%s.org-A" %baseOrg, "../organisms/flatPool/%s-B" %baseOrg)
			
				#Now do the experiments for each mutation rate
				targetMutRate = 0.5
				while (targetMutRate <= 3.0):
					#Get the copy mutation rate (just use org A since they're the same length)
					copyMutRate = calcMutRate(orgFiles[0], targetMutRate)
				
					#Get the output directory name, based on the competition and the mutation rate
					outDir = "%s/%s-comp-%s" %(outputDir, baseOrg, targetMutRate)
				
					#Run the competition
					subprocess.call(["avida", "-v0", "-c", "avida_flat.cfg", "-set", "EVENT_FILE", 
						"events_%s_comp.cfg" %baseOrg, "-set", "ENVIRONMENT_FILE", filename,
						"-set", "DATA_DIR", outDir, "-set", "COPY_MUT_PROB", "%s" %copyMutRate])
				
					targetMutRate += 0.5




if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "usage: python competitions.py <OUTPUT_DIRECTORY>"
	else:
		runComps(sys.argv[1])			
			
