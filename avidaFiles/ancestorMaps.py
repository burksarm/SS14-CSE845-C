#!/usr/bin/python

#Simple script to get the mutation and task maps on all the complex ancestors
import os
import sys
import subprocess

if len(sys.argv) != 3:
	print "Usage: python ancestorMaps.py <COMPLEX_POOL_DIR> <OUTPUT_DIR>"
	quit()

complexPool = sys.argv[1]
outDir = sys.argv[2]

#Make sure the output path exists
if not os.path.exists(outDir):
	os.makedirs(outDir)

#Also make sure the mutation and task map directories exists
mutDir = os.path.join(outDir, "mutations")
taskDir = os.path.join(outDir, "tasks")

if not os.path.exists(mutDir):
	os.makedirs(mutDir)

if not os.path.exists(taskDir):
	os.makedirs(taskDir)

#Create an events file to put all the ancestors in a "population"
eventFile = open("events_ancestors.cfg", "w")
ancestors = None
for dirname, dirs, filenames in os.walk(complexPool):
	ancestors = filenames

#Inject each ancestor
cell = 0
for fileName in ancestors:
	eventFile.write("u begin Inject %s %s -1 %s\n" %(os.path.join(complexPool, fileName), cell, cell))
	cell += 1

#Save the "population"
eventFile.write("u begin SavePopulation\n")

#Done
eventFile.write("u begin Exit\n")
eventFile.close()


#Now go ahead and run avida to get the population
subprocess.call(("avida -c avida_comp.cfg -set EVENT_FILE events_ancestors.cfg -set DATA_DIR %s" %(outDir)).split())

#Rename the population to something obvious
os.rename("%s/detail--1.spop" %outDir, "%s/complexAncestors.spop" %outDir)

#Create the analyze file
analyzeFile = open("analyze_ancestors.cfg", "w")

#Load the population file 
analyzeFile.write("LOAD %s/complexAncestors.spop\n" %outDir)

#Run MAP_MUTATIONS on the ancestors
analyzeFile.write("MAP_MUTATIONS %s html\n" %mutDir)

#Run MAP_TASKS on the ancestors
analyzeFile.write("MAP_TASKS %s task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8 html\n" %taskDir)

#Done
analyzeFile.close()

#Fire up avida on the analyze file
subprocess.call(("avida -c avida_comp.cfg -set EVENT_FILE events.cfg -set ANALYZE_FILE analyze_ancestors.cfg -set DATA_DIR %s -a" %outDir).split())

#Finally, lets rename the files based on the ancestors so it's easier to keep up with
org = 1
for ancestor in ancestors:
	#Rename the mutations files
	oldName = os.path.join(mutDir, "mut_map.org-%s.html" %org)
	newName = os.path.join(mutDir, "mut_map_%s.html" %ancestor)

	os.rename(oldName, newName)

	#Rename the tasks files
	oldName = os.path.join(taskDir, "tasksites.org-%s.html" %org)
	newName = os.path.join(taskDir, "tasksites_%s.html" %ancestor)

	os.rename(oldName, newName)

	org += 1

	
