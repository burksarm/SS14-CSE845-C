#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt

argc = len(sys.argv)
if argc < 3:
	print "Usage analyzeTasks.py <TASK_ANALYSIS_RESULTS_DIRECTORY> <OUTPUT_DIRECTORY> <MUT_RATES (optional. ex. '0.5,3')>"
	quit()

MUT_RATES = [0.5, 3.0]

if argc == 4:
	MUT_RATES = sys.argv[3].split(",")

tasks = ["not", "nand", "and", "ornot", "or", "andnot", "nor", "xor", "equ"]

#Get the input and output directory
inDir = sys.argv[1]
outDir = sys.argv[2]

#Make sure the output path exists (and each competition directory)
if not os.path.exists(outDir):
	os.makedirs(outDir)

#First get the good competition organism names from file.
goodComps = []

inFile = open("../results/goodComps.txt", "r")

for line in inFile:
	goodComps.append(line.strip())



#Now collect all the data
for mutRate in MUT_RATES:
	allAData = {} #generation -> org-> [[total A descendants with each task 0-9]]
	allBData = {} #generation -> org-> [[total B descendants with each task 0-9]]

	for comp in range(1, 11):
		for org in goodComps:
			for gen in range(0, 55, 5):
					resultFile = open(os.path.join(inDir, "comp%s-tasks-%s-%s-%s" %(comp, org, mutRate, gen)), "r")

					#Init all nine tasks with 0
					if gen not in allAData:
						allAData[gen] = {}

					if org not in allAData[gen]:
						allAData[gen][org] = []

					if gen not in allBData:
						allBData[gen] = {}

					if org not in allBData[gen]:
						allBData[gen][org] = []

					allAData[gen][org].append([0.0] * 9 )
					allBData[gen][org].append([0.0] * 9 )

					#Parse the data
					for line in resultFile:	
						#Ignore comments and blanks
						if not line.startswith("#") and len(line.strip()) > 1: 
							items = line.split()
							label = items[0]
							numOrgs = float(items[1])
							taskInfo = [int(d) for d in items[2:]]

							#Update the counts for each task if it was done
							for i in range(9):
								if label == "0" and taskInfo[i] == 1:
									allAData[gen][org][comp-1][i] += numOrgs

								elif label == "1" and taskInfo[i] == 1:
									allBData[gen][org][comp-1][i] += numOrgs

							
	for org in goodComps:
		#Now plot the averages for each task for this mutation rate
		gens = [gen for gen in range(0, 55, 5)]

		#print "%s: %s" %(org, allAData[0][org])

		for task in range(9):
			lineStyle = "--" if task%2 == 0 else "-"

			#Calculate the averages
			taskInfo = [sum(taskData[task] for taskData in allAData[gen][org])/10 for gen in gens]
			#print taskInfo
			#allComps = [allAData[gen][org] for gen in gens]
			#print [sum([comp[task] for comp in allComps])/10.0]
			plt.plot(gens, taskInfo,
				label=tasks[task], ls=lineStyle)

		plt.xlabel("Generation")
		plt.ylabel("Organisms Performing Task")
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		plt.savefig(os.path.join(outDir, "tasks-%s-A-%s.png" %(org, mutRate)), bbox_inches="tight")
		plt.clf()

		#Redo it for B
		for task in range(9):
			lineStyle = "--" if task%2 == 0 else "-"

			#Calculate the averages
			taskInfo = [sum(taskData[task] for taskData in allBData[gen][org])/10 for gen in gens]
			plt.plot(gens, taskInfo,
				label=tasks[task], ls=lineStyle)

		plt.xlabel("Generation")
		plt.ylabel("Organisms Performing Task")
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		plt.savefig(os.path.join(outDir, "tasks-%s-B-%s.png" %(org, mutRate)), bbox_inches="tight")
		plt.clf()
		












