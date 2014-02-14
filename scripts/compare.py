#!/usr/bin/python
import environments 
#Handles generating environments for the competitions

#Compares each A/B pair to find pairs which A has a replication rate of at least 1.5 greater than B.
#A is from the low mutation rate, B is from the high mutation rate.
#For those pairs meeting the criteria, we'll generate an events and environment file for the competition

#Go through all the pairs and get their fitness
for i in range(1, 41):
	aFitness = float(0) #Will hold organism A's fitness
	bFitness = float(0) #Will hold organism B's fitness
	aViable = "0"       #Whether or not organism A is viable
	bViable = "0"       #Whether or not organism B is viable
	aMerit  =  None     #Holds organism A's merit
	bMeriit =  None     #Holds organism B's merit
	
	aFile = open("../organisms/flatPool/dom-%s.org-A" %i, "r")
	bFile = open("../organisms/flatPool/dom-%s.org-B" %i, "r")
	
	#Find the fitnesses and make sure they're both viable
	for line in aFile:
		if line.startswith("# Is Viable"):
			aViable = line.split()[-1]
		
		#Get the merit
		if line.startswith("# Merit"):
			aMerit = line.split()[-1]
		
		#Get the fitness
		if line.startswith("# Fitness"):
			aFitness = float(line.split()[2])
			break
	
	for line in bFile:
		if line.startswith("# Is Viable"):
			bViable = line.split()[-1]
			
		#Get the merit
		if line.startswith("# Merit"):
			bMerit = line.split()[-1]
		
		#Get the fitness
		if line.startswith("# Fitness"):
			bFitness = float(line.split()[2])
			break
		
	#Now compare them and if they meet the criteria, generate an events file for their competition
	if aViable == "1" and bViable == "1" and aFitness/bFitness > 1.5:
		#Create the events file
		eventsFile = open("../avidaFiles/events_dom-%s_comp.cfg" %i, "w")
		
		#Fill half the pop with organism A and give it a marker of 0
		eventsFile.write("#Fill half the pop with organism A and give it a marker of 0\n")

		for i in range(1800):
			eventsFile.write("u begin Inject %s %s %s 0\n\n" %(aFile.name, i, aMerit))
		
		#Fill half the pop with organism B and give it a marker of 1
		eventsFile.write("#Fill half the pop with organism B and give it a marker of 1\n")
		for i in range(1800, 3600):
			eventsFile.write("u begin Inject %s %s %s 1\n\n" %(bFile.name, i, bMerit))
		
		#Save the population every 5 generations
		eventsFile.write("#Save the population every 5 generations\n")
		eventsFile.write("g 5:5 SavePopulation\n\n")
		
		#Stop after 50 generations
		eventsFile.write("#Stop after 50 generations\n")
		eventsFile.write("g 50 Exit\n")
		
		#Now we need to generate an environment file to only reward tasks either A or B performs
		environments.generate(aFile.name, bFile.name)
	
