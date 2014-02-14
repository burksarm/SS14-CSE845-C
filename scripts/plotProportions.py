#!/usr/bin/python

#Plots the distributions of organism A and B for each of the competitions for an organism
#The plot is as in the "Survival of the Flattest" paper, Fig. 1.
import sys
import os
import re
import matplotlib.pyplot as plt
import compOrgs

mutRates = ["0.5", "1.0", "1.5", "2.0", "2.5", "3.0"]

#Plots the results of all the mutation rates for the given org, for one competition.
def plotCompetitions(org, resultsDir, mutRate, doLabel, clearPlot=False):
	aProportions = {} #generation -> total number of A descendants
	bProportions = {} #generation -> total number of B descendants
	popSizes = {} #Holds the population size at each generation (we get this by counting the lines)
	
	#Add the initial generation 0 proportions that we seeded
	aProportions[0] = 1800.0
	bProportions[0] = 1800.0
	popSizes[0] = 3600.0
	
	#Files are saved by population snapshots from generation 5-50 in increments of 5
	generations = [gen for gen in range(0, 55, 5)]
	for gen in generations:
		if gen > 0: #Skip the initial. We already have those numbers
			#Open the result file for this mutation rate, for the current generation
			resultFile = open(os.path.join(resultsDir, "%s-comp-%s-%s.dat" %(org, mutRate, gen)))
			
			popSize = 0.0
			for line in resultFile:
				#Ignore comment lines and blank lines
				if not(len(line.strip()) == 0 or line.startswith("#")):
					#Get the space-delimited columns of data
					items = line.split()
					
					#How many organisms are there with this genotype?
					numCpus = float(items[1])
					
					#Only count genotypes that have num_cpus > 0
					if numCpus > 0.0:
						#Increment the population size
						popSize += numCpus
						
						#A descendants have a label of 0, B descendants have a label of 1
						if items[0] == "0":
							#We got an A descendant. Increment its count
							if gen not in aProportions:
								aProportions[gen] = 0.0
							aProportions[gen] += numCpus
							
						elif items[0] == "1":
							#We got a B descendant. Increment its count
							if gen not in bProportions:
								bProportions[gen] = 0.0
							bProportions[gen] += numCpus
			
			#Get the population size, which can be less than 3600				
			popSizes[gen] = popSize
	
	#Now we have the proportions tallied up for the current mutation rate. Plot the data.
	if doLabel == True: #Since we have 10 lines for each ancestor, only add the legend label once.
		plt.plot(generations, [aProportions[gen]/popSizes[gen] for gen in generations], "b-", label="A")
		plt.plot(generations, [bProportions[gen]/popSizes[gen] for gen in generations], "r-", label="B")
	else:
		plt.plot(generations, [aProportions[gen]/popSizes[gen] for gen in generations], "b-")
		plt.plot(generations, [bProportions[gen]/popSizes[gen] for gen in generations], "r-")
		
	#Clear the plot for subsequent calls.
	if (clearPlot == True):
		plt.clf()
		
#Plots all 10 competition lines for the given ancestor organism
def plotAllCompetitionLines(org, resultsDir, outputDir):
	#Make sure the output directory exists
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)
		
	for mutRate in mutRates:
		for i in range(1, 11):
			plotCompetitions(org, "%s/comp%s" %(resultsDir, i), mutRate, doLabel=True if i == 1 else False)
		
		#Save the plot to a png.
		plt.xlabel("Generation")
		plt.ylabel("Proportion")
		plt.ylim(0.0, 1.0)
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		plt.savefig(os.path.join(outputDir, "%s-%s.png" %(org, mutRate)), bbox_inches = "tight")
		
		#Clear the plot for the next mutation rate
		plt.clf()
	

#----------- MAIN ------------------------------		
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: python plotProportions.py <COMPETITION_RESULTS_DIR> <OUTPUT_DIRECTORY>."
		quit()
	
	#For all of the competitions, generate the plots.
	for compOrg in compOrgs.getCompOrgs():
		plotAllCompetitionLines(compOrg, sys.argv[1], sys.argv[2])

	
	
	
	
	
	