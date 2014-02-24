#!/usr/bin/python
import os

#Gets the set of task names from the environment-all-logic file.
def getAllTasks():
	#task names to match in the organism file
	tasks = set() #["not", "nand", "and", "orn", "or", "andn", "nor", "xor", "equ"]

	#The task name we'll use to match in the organisms is item 3 in the env file
	for line in open("../avidaFiles/environment.cfg", "r"):
		if line.startswith("REACTION"):
			items = line.split()
			tasks.add(items[2])

	#Return it (we'll make it a set just to be extra safe)
	return tasks

#Gets the set of tasks performed in the given organism file
def getTasks(file):
	tasksPerformed = set()
	for line in file:
		#Get the tasks performed line
		items = line.split()

		if len(items) >= 4 and items[1] in getAllTasks():
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
	
	#Get the dominant ancestor name that A and B are based on
	domName = aFile[aFile.rfind("/")+1:aFile.rfind(".")]

	#Get the set of tasks performed by the common ancestor
	ancestorTasks = getTasks(open("../organisms/complexPoolAllLogic/%s.org" %domName, "r"))
	
	#Now write the environment file
	outFile = open("../avidaFiles/environment_%s_comp.cfg" %domName, "w")
	for task in ancestorTasks:
		outFile.write(allResources[task] + "\n")
	

