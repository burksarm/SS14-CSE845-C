#!/usr/bin/python

#Simply renames the populations generated from the competitions so that they're in order, based on
#generation number so we can easily handle them in analyze mode. We know they were generated every
#Five generations, so we can keep track of which population we're using.
import sys
import os
import shutil

def rename():
	compDir = sys.argv[1]


	for dirname, dirs, filenames in os.walk(compDir):
		#Go Through all the competition directories
		for dir in dirs:
			#Get all the population files inside the competition directories
			for d, subdirs, popFiles in os.walk(os.path.join(compDir, dir)):
				pops = {} #Holds the update number extracted from the file name mapped to the filename

				for file in popFiles:
					update = int(file[file.find("-")+1:file.rfind(".")])
					pops[update] = file

				
				#Now rename the files, replacing the update number with the generation, by 5's
				generation = 5
				for update in sorted(pops.keys()):
					oldName = os.path.join(os.path.join(compDir, dir), "detail-%s.spop" %update)
					newName = os.path.join(os.path.join(compDir, dir), "detail-%s.spop" %generation)

					print oldName, "->", newName
					shutil.move(oldName, newName)

					generation += 5
				






if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage: python renameComPopulations.py <COMPETITION_RESULTS_DIRECTORY>"
		quit()
	rename()

