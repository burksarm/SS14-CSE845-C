#!/usr/bin/python
import os

#task names to match in the organism file
tasks = ["not", "nand", "and", "orn", "or", "andn", "nor", "xor", "equ"]

#Gets the set of tasks performed in the given organism file
def getTasks(file):
	tasksPerformed = set()
	for line in file:
		#Get the tasks performed line
		items = line.split()

		if len(items) >= 4 and items[1] in tasks:
			#Gather the task if it was performed
			if int(items[2]) > 0:
				tasksPerformed.add(items[1])
	
	return tasksPerformed

#Generates the environment file that rewards the combined set of tasks A and B perform
def generate(aFile, bFile):
	#Will hold all the resource strings we'll write to file
	allResources = {} #format: task -> original line of text

	#Steal the resource strings from the regular environment.cfg file
	envFile = open("../avidaFiles/environment.cfg", "r")

	for line in envFile:
		if line.startswith("REACTION"):
			items = line.split()
			allResources[items[2]] = line.strip()


	#Get the set of tasks performed by both A and B
	allTasks = getTasks(open(aFile, "r"))
	allTasks.union(getTasks(open(bFile, "r")))
	
	#Get the dominant ancestor name that A and B are based on
	domName = aFile[aFile.rfind("/")+1:aFile.rfind(".")]
	
	#Now write the environment file
	outFile = open("../avidaFiles/environment_%s_comp.cfg" %domName, "w")
	for task in allTasks:
		outFile.write(allResources[task] + "\n")
	


