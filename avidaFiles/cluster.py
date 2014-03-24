#!/usr/bin/python

#Simply creates an events file that injects all the A ancestors and
#all the B ancestors into an environment and saves the population.
#This also runs the AVERAGE_MODULARITY analysis on the organisms.
#Only uses the good competitions from results/goodComps.txt

import sys
import os
import subprocess

#Get the output directory
if not len(sys.argv) == 3:
	print "Usage: cluster.py <POP_OUTPUT_DIR> <RESULTS_OUTPUT_DIR>"
	quit()

popOutDir = sys.argv[1]
resultOutDir = sys.argv[2]

#Make sure the output paths exist
if not os.path.exists(popOutDir):
	os.makedirs(popOutDir)

if not os.path.exists(resultOutDir):
	os.makedirs(resultOutDir)

#Also make sure the mutation map directory exists
mutDir = os.path.join(resultOutDir, "mutations")

if not os.path.exists(mutDir):
	os.makedirs(mutDir)

#Get the list of ancestors we want to use
ancestors = []
for line in open("../results/goodComps.txt", "r"):
	ancestors.append(line.strip())

#Now create the event file
eventFile = open("events_cluster.cfg", "w")

#Inject each ancestor, A and B
cell = 0
for i in range(len(ancestors)):
	eventFile.write("u begin Inject ../organisms/flatPool/%s.org-A %s -1 0\n" %(ancestors[i], cell))
	eventFile.write("u begin Inject ../organisms/flatPool/%s.org-B %s -1 1\n" %(ancestors[i], cell+1))

	cell += 2

#Save the population
eventFile.write("u begin SavePopulation\n")

#Quit avida
eventFile.write("u begin Exit\n")
eventFile.close()

#Now go ahead and run avida to get the population
subprocess.call(("avida -c avida_comp.cfg -set EVENT_FILE events_cluster.cfg -set DATA_DIR %s" %(popOutDir)).split())

#Create the analyze file
analyzeFile = open("mod-analyze_cluster.cfg", "w")

#Load the population file to get all A organisms
analyzeFile.write("LOAD %s/detail--1.spop\n" %popOutDir)

#Filter to keep only A organisms
analyzeFile.write("FILTER lineage == 0\n")

#Run the average modularity on the A cluster
analyzeFile.write("AVERAGE_MODULARITY %s/modularity_cluster-A.dat task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8\n" %resultOutDir)

#Run MAP_MUTATIONS on the A cluster
analyzeFile.write("MAP_MUTATIONS %s html\n" %mutDir)

#Cleanup the results from A
analyzeFile.write("PURGE_BATCH\n")

#Re-load the population file to get all B organisms
analyzeFile.write("LOAD %s/detail--1.spop\n" %popOutDir)

#Now filter to keep only B organisms
analyzeFile.write("FILTER lineage == 1\n")

#Run the average modularity on the B cluster
analyzeFile.write("AVERAGE_MODULARITY %s/modularity_cluster-B.dat task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8\n" %resultOutDir)

#Run MAP_MUTATIONS on the B cluster
analyzeFile.write("MAP_MUTATIONS %s html\n" %mutDir)

#Done
analyzeFile.close()

#Fire up avida on the analyze file
subprocess.call(("avida -c avida_comp.cfg -set EVENT_FILE events.cfg -set ANALYZE_FILE mod-analyze_cluster.cfg -set DATA_DIR %s -a" %resultOutDir).split())

#Finally, lets rename the mutations files based on the pairs so it's easier to keep up with
org = 1
for ancestor in ancestors:
	oldA = os.path.join(mutDir, "mut_map.org-%s.html" %org)
	newA = os.path.join(mutDir, "mut_map_%s-A.html" %ancestor)

	oldB = os.path.join(mutDir, "mut_map.org-%s.html" %(org+1))
	newB = os.path.join(mutDir, "mut_map_%s-B.html" %ancestor)

	os.rename(oldA, newA)
	os.rename(oldB, newB)

	org += 2

 
