#!/usr/bin/python

#Plots the proportions of organism A and B descendants for each of the 
#competitions for an organism
#The plot is like the "Survival of the Flattest" paper, Fig. 1.
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
	popSizes = {} #Holds the population size at each generation (we get this by counting the orgs)
	
	#Files are saved by population snapshots from generation 0-50 in increments of 5
	generations = [gen for gen in range(0, 55, 5)]
	for gen in generations:
		#Open the result file for this mutation rate, for the current generation
		resultFile = open(os.path.join(resultsDir, "%s-comp-%s-%s.dat" %(org, mutRate, gen)))
		
		#Initialize everything to zero, as some proportions will be zero
		popSize = 0.0
		aProportions[gen] = 0.0
		bProportions[gen] = 0.0

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
						aProportions[gen] += numCpus
						
					elif items[0] == "1":
						#We got a B descendant. Increment its count
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

#Plots a single competition (all mut rates) for a single ancestor organism
def plotSingleCompetition(org, resultsDir, outputDir):
	#Make sure the output directory exists
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)

	for mutRate in mutRates:
		#Plot each mutation rate for the org in a separate image
		plotCompetitions(org, resultsDir, mutRate, doLabel=True)

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
	if len(sys.argv) < 3:
		print "Usage: python plotProportions.py <COMPETITION_RESULTS_DIR> <OUTPUT_DIRECTORY> <ORG ex. dom-i (optional)>."
		quit()
	
	if len(sys.argv) == 3:
		#For all of the competitions, generate the plots.
		for compOrg in compOrgs.getCompOrgs():
			plotAllCompetitionLines(compOrg, sys.argv[1], sys.argv[2])

	#Plot the single competition if given a single org to plot
	elif len(sys.argv) == 4:
		plotSingleCompetition(sys.argv[3], sys.argv[1], sys.argv[2])

	
	
	
	
	
	
