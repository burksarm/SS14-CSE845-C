#!/usr/bin/python
import sys

#Sanity check script to look at the A/B fitness ratios.

#Gets the good competitions from the manually-created list
def getGoodComps():
	goodComps = []
	for line in open("../results/goodComps.txt"):
		goodComps.append(line.strip())

	return goodComps

#Gets the A/B fitness ratios for each org in the flat pool
def getRatios(flatPoolDir):
	ratios = {} #base org -> A/B fitness ratio

	#Go through all the pairs and get their fitness ratios
	for i in range(1, 41):
		aFitness = float(0) #Will hold organism A's fitness
		bFitness = float(0) #Will hold organism B's fitness
		aViable = "0"       #Whether or not organism A is viable
		bViable = "0"       #Whether or not organism B is viable
		aMerit  =  None     #Holds organism A's merit
		bMeriit =  None     #Holds organism B's merit

		baseOrg = "dom-%s" %i
	
		aFile = open("%s/dom-%s.org-A" %(flatPoolDir, i), "r")
		bFile = open("%s/dom-%s.org-B" %(flatPoolDir, i), "r")
	
		#Find the fitnesses and make sure they're both viable
		for line in aFile:
			if line.startswith("# Is Viable"):
				aViable = line.split()[-1]

			#Get the fitness
			if line.startswith("# Fitness"):
				aFitness = float(line.split()[-1].strip())
				break
	
		for line in bFile:
			if line.startswith("# Is Viable"):
				bViable = line.split()[-1]
		
			#Get the fitness
			if line.startswith("# Fitness"):
				bFitness = float(line.split()[-1].strip())
				break
		
		#Collect the ratios for all orgs that meet the competition criteria
		abFitnessRatio = aFitness/bFitness
		if aViable == "1" and bViable == "1" and  abFitnessRatio > 1.5:
			ratios[baseOrg] = abFitnessRatio

	return ratios

#----------------- Main ------------------------
if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage python compare.py <FLAT_ORGS_DIR>"
		quit()

	#Get the A/B fitness ratios
	ratios = getRatios(sys.argv[1])
		
	#Get the good comps
	goodComps = getGoodComps()

	#Show the ratios for the good comps
	print "A/B fitness ratios for good competition pairs:"

	for org in sorted(ratios.keys()):
		if org in goodComps:
			print "%s:\t%f" %(org, ratios[org])

	#Show the ratios for the no-so-good comps
	print "-" * 50
	print "A/B fitness ratios for bad competition pairs:"

	for org in sorted(ratios.keys()):
		if org not in goodComps:
			print "%s:\t%f" %(org, ratios[org])

