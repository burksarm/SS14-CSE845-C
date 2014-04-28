#!/usr/bin/python
import os
import sys
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import environments

MUT_RATES = [0.5, 3.0]
GENS = [gen for gen in range(0, 55, 5)]

#Convenience method to figure out the org's merit from the organism file
def getOrgMerit(org, ab):
	fName = "../organisms/flatPool/%s.org-%s" %(org,ab)

	for line in open(fName):
		if line.startswith("# Merit"):
			return float(line.strip().split()[-1])

#Convenience method to figure out the org's gestation time from the organism file
def getOrgGestTime(org, ab):
	fName = "../organisms/flatPool/%s.org-%s" %(org,ab)

	for line in open(fName):
		if line.startswith("# Gestation"):
			return float(line.strip().split()[-1])

#Convenience method to figure out the org's fitness time from the organism file
def getOrgFitness(org, ab):
	fName = "../organisms/flatPool/%s.org-%s" %(org,ab)

	for line in open(fName):
		if line.startswith("# Fitness"):
			return float(line.strip().split()[-1])

#Convenience method to figure out the org's num tasks time from the organism file
def getOrgTasks(org, ab):
	fName = "../organisms/flatPool/%s.org-%s" %(org,ab)

	return len(environments.getTasks(open(fName)))

#Generic convenience method to collect the average data from the specified column
def collectData(fName, collection, org, ab, column, isTasks=False): 
	gen = 0

	for line in open(fName):
			if not (line.startswith("#") or len(line.strip()) <= 1):
				items = line.split()

				#Initialize the collection the first time around
				if gen not in collection:
					collection[gen] = []

				#Now add the starting merit (if we're using merit)
				if gen == 0 and column == 1 and not isTasks:
					collection[0].append(getOrgMerit(org, ab))
	
				#Add the starting num tasks if we're using it
				elif gen == 0 and column == 1 and isTasks:
					collection[0].append(getOrgTasks(org, ab))

				#Same for the gestation time
				elif gen == 0 and column == 2:
					collection[0].append(getOrgGestTime(org, ab))

				#Same for fitness
				elif gen == 0 and column == 3:
					collection[0].append(getOrgFitness(org, ab))

				#Otherwise, add the merit we read in
				else:
					collection[gen].append(float(items[column]))

				gen += 5

	#Now fill the rest of the gens with 0's in the case that the org died
	while gen < 55:
		if gen not in collection:
			collection[gen] = []

		collection[gen].append(0.0)
		gen += 5

#Collects all the data and plots it
def plotAvgData(column, yLabel, pngName, outDir, logScale, yRange, isTasks=False):
	aAverages = {} #Holds the averages over all the replicates: mutRate -> gen -> [avg col data]
	bAverages = {} #Holds the averages over all the replicates: mutRate -> gen -> [avg col data]

	#Go ahead and initialize the global collection so we don't have to later
	for mutRate in MUT_RATES:
		aAverages[mutRate] = {}
		bAverages[mutRate] = {}

		for gen in GENS:
			#Holds the average for each of the orgs across the 10 replicates
			aAverages[mutRate][gen] = [0.0]*len(goodComps)
			bAverages[mutRate][gen] = [0.0]*len(goodComps)

	#Collect the data
	for mutRate in MUT_RATES:
		for run in range(1, 11):
			allAData = {} #gen -> [avg col data] for each A org
			allBData = {} #gen -> [avg col data] for each B org

			for org in goodComps:
				if isTasks:
					collectData(os.path.join(inDir, 
						"run%s/%s-A-%s/ave_num_tasks.dat" %(run, org, mutRate)), 
						allAData, org, "A", column, True)

					collectData(os.path.join(inDir, 
						"run%s/%s-B-%s/ave_num_tasks.dat" %(run, org, mutRate)), 
						allBData, org, "B", column, True)
				else:
					collectData(os.path.join(inDir, "run%s/%s-A-%s/average.dat" 
						%(run, org, mutRate)), allAData, org, "A", column)
					collectData(os.path.join(inDir, "run%s/%s-B-%s/average.dat" 
						%(run, org, mutRate)), allBData, org, "B", column)

			#Now add all the data to the global collection
			for gen in GENS:
				#Add all the avg data for this gen (we'll average them at the end)
				for i in range(len(goodComps)):
					aAverages[mutRate][gen][i] += allAData[gen][i]
					bAverages[mutRate][gen][i] += allBData[gen][i]


	#Now we have the totals across all the runs, go through and divide by 10 to get the averages
	for mutRate in MUT_RATES:
		for gen in GENS:
			for i in range(len(goodComps)):
				aAverages[mutRate][gen][i] /= 10
				bAverages[mutRate][gen][i] /= 10

		#Calculate the std err or the mean among A and B for each gen
		aSems = [stats.sem(aAverages[mutRate][gen]) for gen in GENS]
		bSems = [stats.sem(bAverages[mutRate][gen]) for gen in GENS]


		#Now we're finally ready to plot
		if (logScale):
			plt.yscale('log')

		aLine = [sum(aAverages[mutRate][gen])/len(aAverages[mutRate][gen])
			for gen in GENS]

		bLine = [sum(bAverages[mutRate][gen])/len(bAverages[mutRate][gen]) 
			for gen in GENS]

		#Plot the lines for A and B
		plt.plot(GENS, aLine, color='b', label="fast replicator")
		plt.plot(GENS, bLine, color='r', label="slow replicator", ls="--")

		#Add the errorbars in on top of the line
		plt.errorbar(GENS, aLine, yerr=aSems, color="b", label=None)
		plt.errorbar(GENS, bLine, yerr=bSems, color="r", ls="--", label=None)

		#Set the x and y range to make comparing the mut rates easy
		plt.xlim(GENS[0]-1, GENS[-1]+1) #So we can see the 1st and last error bars
		plt.ylim(yRange[0], yRange[1])

		plt.xlabel("Generation")
		plt.ylabel(yLabel)
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		plt.savefig(os.path.join(outDir, "%s-%s.png" %(pngName, mutRate)), bbox_inches="tight")
		plt.clf()

		#Get the ending value for each A and B
		aEndValues = [aAverages[mutRate][GENS[-1]][i]
			for i in range(len(goodComps))]

		bEndValues = [bAverages[mutRate][GENS[-1]][i]
			for i in range(len(goodComps))]

		#Get the median and sem of the ending values for reporting
		aEndMedian = np.median(aEndValues)
		aEndSem = stats.sem(aEndValues)
		bEndMedian = np.median(bEndValues)
		bEndSem = stats.sem(bEndValues)
		

		#Perform the Mann-Whitney on the mean delta in the data across A vs B for each generation
		zStat, pVal = stats.ranksums(aEndValues, bEndValues)


		print "Final %s at mutation rate %s: Mann-Whitney p = %f, fast replicator median = %f, fast replicator SEM = %f slow replicator median = %f, slow replicator SEM = %f" %(yLabel, mutRate, pVal, aEndMedian, aEndSem, bEndMedian, bEndSem)

	print "-" * 50


#---------- Main----------------------------
#Check command line args
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: python taskAnalysis.py <INPUT_DIR> <OUTPUT_DIR>"
		quit()

	inDir = sys.argv[1]
	outDir = sys.argv[2]

	#Make sure the output path exists
	if not os.path.exists(outDir):
		os.makedirs(outDir)

	#First get the good competition organism names from file.
	goodComps = []

	inFile = open("../results/goodComps.txt", "r")

	for line in inFile:
		goodComps.append(line.strip())

	
	#Increase the font size since we're combining figures...
	font = {'size': '18'}
	matplotlib.rc('font', **font)
	
	plotAvgData(2, "Avg. Gestation Time", "avgGest_isolation", outDir, False, (200, 1000))
	plotAvgData(1, "Avg. Merit", "avgMerit_isolation", outDir, True,  (10000, pow(10, 10)))
	plotAvgData(3, "Avg. Fitness", "avgFitness_isolation", outDir, True, (10, pow(10, 7)))
	plotAvgData(1, "Avg. Tasks", "avgTasks_isolation", outDir, False, (0, 9), isTasks=True)
	















