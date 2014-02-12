#!/usr/bin/python

#Plots the distributions of organism A and B for each of the competitions for an organism
#The plot is as in the "Survival of the Flattest" paper, Fig. 1.
import sys
import os
import matplotlib.pyplot as plt

#mutRates = ["0.5", "1.0", "1.5", "2.0", "2.5", "3.0"]

#TESTING use the above when finished developing.
mutRates = ["0.5"]

#Plots the results of all the competitions for the given org.
def plotCompetitions(org, resultsDir):
	for mutRate in mutRates:
		aProportions = {} #generation -> total number of A descendants
		bProportions = {} #generation -> total number of B descendants
		popSizes = {} #Holds the population size at each generation (we get this by counting the lines)
		
		#Files are saved by population snapshots from generation 5-50 in increments of 5
		generations = [gen for gen in range(5, 55, 5)]
		for gen in generations:
				resultFile = open(os.path.join(resultsDir, "%s-comp-%s-%s.dat" %(org, mutRate, gen)))
				
				popSize = 0.0
				for line in resultFile:
					if not(len(line.strip()) == 0 or line.startswith("#")):
						items = line.split()
						
						#A descendants have a label of 0, B descendants have a label of 1
						if items[0] == "0":
							popSize += 1.0
							
							if gen not in aProportions:
								aProportions[gen] = 0.0
							aProportions[gen] += 1.0
							
						elif items[0] == "1":
							popSize += 1.0
							
							if gen not in bProportions:
								bProportions[gen] = 0.0
							bProportions[gen] += 1.0
							
				popSizes[gen] = popSize
		
		#Get the population size, which could be slightly less than 3600
		
		#Sanity Check
		print aProportions
		print bProportions
		print popSizes
		
		#Now we have the proportions tallied up for the current mutation rate. Plot the data.
		plt.xlabel("Generation")
		plt.ylabel("Proportion")
		
		plt.plot(generations, [aProportions[gen]/popSizes[gen] for gen in generations], label="A")
		plt.plot(generations, [bProportions[gen]/popSizes[gen] for gen in generations], label="B")
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		
		#Save the plot to a png.
		plt.savefig(os.path.join(resultsDir, "%s-%s.png" %(org, mutRate)), bbox_inches = "tight")
		
		#Clear the plot for subsequent calls.
		plt.clf()
					
if __name__ == "__main__":
	plotCompetitions(sys.argv[1], sys.argv[2])