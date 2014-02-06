#!/usr/bin/python
import re

#Compares each A/B pair to find pairs which A has a replication rate of at least 1.5 greater than B.
#A is from the low mutation rate, B is from the high mutation rate.

#Go through all the pairs and get their fitness
for i in range(1, 41):
	aFitness = float(0)
	bFitness = float(0)
	aViable = "0"
	bViable = "0"
	
	aFile = open("../organisms/flatPool/dom-%s.org-A" %i, "r")
	bFile = open("../organisms/flatPool/dom-%s.org-B" %i, "r")
	
	#Find the fitnesses and make sure they're both viable
	for line in aFile:
		if line.startswith("# Is Viable"):
			aViable = line.split()[-1]
		
		if line.startswith("# Fitness"):
			aFitness = float(line.split()[2])
			break
	
	for line in bFile:
		if line.startswith("# Is Viable"):
			bViable = line.split()[-1]
		
		if line.startswith("# Fitness"):
			bFitness = float(line.split()[2])
			break
		
	#Now compare them
	if aViable == "1" and bViable == "1" and aFitness/bFitness > 1.5:
		print aFile.name
		print bFile.name