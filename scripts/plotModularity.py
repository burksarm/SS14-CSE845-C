#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt

#Plots the results from the AVERAGE_MODULARITY command on the competitions
if len(sys.argv) != 4:
	print "Usage plotModularity.py <INPUT_DIR> <OUTPUT_DIR> <COLUMN_TO_PLOT (0-based)>"
	quit()

inDir = sys.argv[1]
outDir = sys.argv[2]
column = int(sys.argv[3])

#Make sure the output path exists
if not os.path.exists(outDir):
	os.makedirs(outDir)

#Setup some needed vars
mutRates = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
gens = [gen for gen in range(0, 55, 5)]
labels = []

for line in open("avgModularityLegend.dat"):
	labels.append(line.strip())

#Get the organisms we used for the analysis
orgs = []
for line in open("../results/goodComps.txt"):
        orgs.append(line.strip())


#Plot the data for each org
for org in orgs:
	#Plot the data for each mutation rate separately
	for mutRate in mutRates:
		resultsA = {} #gen->data
		resultsB = {} #gen->data

		doLabel = True

		#Plot a line for each competition
		for comp in range(1, 11):
			#Collect the data from each generation
			for gen in gens:
				aFile = os.path.join(inDir, os.path.join("comp%s" %comp, "modularity-%s-comp-%s-%s-A.dat" %(org, mutRate, gen)))
				bFile = os.path.join(inDir, os.path.join("comp%s" %comp, "modularity-%s-comp-%s-%s-B.dat" %(org, mutRate, gen)))

				#Open the files and get the data (should just be a single line)
				resultsA[gen] = open(aFile, "r").readline().split()[column].strip()
				resultsB[gen] = open(bFile, "r").readline().split()[column].strip()

			
			#Now that we have the data, plot it!
			if (doLabel == True):
				plt.plot(gens, [resultsA[gen] for gen in gens], "b", label="A")
				plt.plot(gens, [resultsB[gen] for gen in gens], "r", label="B")
		
			else:
				plt.plot(gens, [resultsA[gen] for gen in gens], "b")
				plt.plot(gens, [resultsB[gen] for gen in gens], "r")

			doLabel = False
		
		#Save the plot
		plt.xlabel("Generation")
		plt.ylabel(labels[column])
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		plt.savefig(os.path.join(outDir, "%s-%s_modularity.png" %(org, mutRate)), bbox_inches="tight")

		#Clear the plot for the next mutatation rate/org
		plt.clf()








	
