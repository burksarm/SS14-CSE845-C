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

#Also make sure the mutation and task map directories exists
mutDir = os.path.join(resultOutDir, "mutations")
taskDir = os.path.join(resultOutDir, "tasks")

if not os.path.exists(mutDir):
	os.makedirs(mutDir)

if not os.path.exists(taskDir):
	os.makedirs(taskDir)

#Get the list of ancestors we want to use
ancestors = []
for line in open("../results/goodComps.txt", "r"):
	ancestors.append(line.strip())

#Now create the event files
eventFile1 = open("events_cluster1.cfg", "w")
eventFile2 = open("events_cluster2.cfg", "w")

#Inject each ancestor, A and B
cell = 0
for i in range(len(ancestors)):
	#Cluster1 actually clusters into A and B
	eventFile1.write("u begin Inject ../organisms/flatPool/%s.org-A %s -1 0\n" %(ancestors[i], cell))
	eventFile1.write("u begin Inject ../organisms/flatPool/%s.org-B %s -1 1\n" %(ancestors[i], cell+1))

	#Cluster2 gives each org a different tag so we can get them one-by-one later
	eventFile2.write("u begin Inject ../organisms/flatPool/%s.org-A %s -1 %s\n" %(ancestors[i], cell, cell))
	eventFile2.write("u begin Inject ../organisms/flatPool/%s.org-B %s -1 %s\n" %(ancestors[i], cell+1, cell+1))
	cell += 2

#Save the populations
eventFile1.write("u begin SavePopulation\n")
eventFile2.write("u begin SavePopulation\n")

#Quit avida
eventFile1.write("u begin Exit\n")
eventFile2.write("u begin Exit\n")
eventFile1.close()
eventFile2.close()

#Now go ahead and run avida to get the cluster
subprocess.call(("avida -c avida_comp.cfg -set EVENT_FILE events_cluster1.cfg -set DATA_DIR %s" %(popOutDir)).split())

#Rename the first population
os.rename("%s/detail--1.spop" %popOutDir, "%s/cluster.spop" %popOutDir)

#Run avida again to get the labeled population
subprocess.call(("avida -c avida_comp.cfg -set EVENT_FILE events_cluster2.cfg -set DATA_DIR %s" %(popOutDir)).split())

#Rename the second population for completness' sake
os.rename("%s/detail--1.spop" %popOutDir, "%s/labeled.spop" %popOutDir)

#Create the analyze file
analyzeFile = open("mod-analyze_cluster.cfg", "w")

#Load the population file to get all A organisms
analyzeFile.write("LOAD %s/cluster.spop\n" %popOutDir)

#Filter to keep only A organisms
analyzeFile.write("FILTER lineage == 0\n")

#Run the average modularity on the A cluster
analyzeFile.write("AVERAGE_MODULARITY %s/modularity_cluster-A.dat task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8\n" %resultOutDir)

#Run MAP_MUTATIONS on the A cluster
analyzeFile.write("MAP_MUTATIONS %s html\n" %mutDir)

#Run MAP_TASKS on the A cluster
analyzeFile.write("MAP_TASKS %s task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8 html\n" %taskDir)

#Cleanup the results from A
analyzeFile.write("PURGE_BATCH\n")

#Re-load the population file to get all B organisms
analyzeFile.write("LOAD %s/cluster.spop\n" %popOutDir)

#Now filter to keep only B organisms
analyzeFile.write("FILTER lineage == 1\n")

#Run the average modularity on the B cluster
analyzeFile.write("AVERAGE_MODULARITY %s/modularity_cluster-B.dat task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8\n" %resultOutDir)

#Run MAP_MUTATIONS on the B cluster
analyzeFile.write("MAP_MUTATIONS %s html\n" %mutDir)

#Run MAP_TASKS on the B cluster
analyzeFile.write("MAP_TASKS %s task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8 html\n\n" %taskDir)

#Now we have to run AVERAGE_MODULARITY on each organism to get the data points
analyzeFile.write("#===================\n")

#Go through the population and run AVERAGE_MODULARITY on each org separately
analyzeFile.write("FORRANGE i 0 %s\n" %(len(ancestors) * 2 - 1)) #x2 because of pairs

analyzeFile.write("\tLOAD %s/labeled.spop\n" %popOutDir)

#Get that org
analyzeFile.write("\tFILTER lineage == $i\n")

#Finally, run AVERAGE_MODULARITY
analyzeFile.write("\tAVERAGE_MODULARITY %s/modularity_$i.dat task.0 task.1 task.2 task.3 task.4 task.5 task.6 task.7 task.8\n" %resultOutDir)
analyzeFile.write("END")

#Done
analyzeFile.close()

#Fire up avida on the analyze file
subprocess.call(("avida -c avida_comp.cfg -set EVENT_FILE events.cfg -set ANALYZE_FILE mod-analyze_cluster.cfg -set DATA_DIR %s -a" %resultOutDir).split())

#Finally, lets rename the files based on the pairs so it's easier to keep up with
org = 1
for ancestor in ancestors:
	#Rename the mutations files
	oldA = os.path.join(mutDir, "mut_map.org-%s.html" %org)
	newA = os.path.join(mutDir, "mut_map_%s-A.html" %ancestor)

	oldB = os.path.join(mutDir, "mut_map.org-%s.html" %(org+1))
	newB = os.path.join(mutDir, "mut_map_%s-B.html" %ancestor)

	os.rename(oldA, newA)
	os.rename(oldB, newB)

	#Rename the tasks files
	oldA = os.path.join(taskDir, "tasksites.org-%s.html" %org)
	newA = os.path.join(taskDir, "tasksites_%s-A.html" %ancestor)

	oldB = os.path.join(taskDir, "tasksites.org-%s.html" %(org+1))
	newB = os.path.join(taskDir, "tasksites_%s-B.html" %ancestor)

	os.rename(oldA, newA)
	os.rename(oldB, newB)

	#Rename the modularity files
	oldA = os.path.join(resultOutDir, "modularity_%s.dat" %(org-1))
	newA = os.path.join(resultOutDir, "modularity_%s-A.dat" %ancestor)

	oldB = os.path.join(resultOutDir, "modularity_%s.dat" %(org))
	newB = os.path.join(resultOutDir, "modularity_%s-B.dat" %ancestor)

	os.rename(oldA, newA)
	os.rename(oldB, newB)

	org += 2

 
