#!/usr/bin/python

#Simple script to show the lengths of organisms. Takes the path to the directory of organisms.
import sys
import os
import operator

if len(sys.argv) != 2:
	print "Usage: python orgLengths.py <ORGANISM_DIRECTORY>"
	quit()

orgDir = sys.argv[1]
orgLengths = {} #Format is org name -> length

#Go through each file and get the length
for dirname, dirs, filenames in os.walk(orgDir):
	for filename in filenames:
		for line in open(os.path.join(orgDir, filename)):
			if line.startswith("# Genome Size"):
				orgLengths[filename] = int(line.split()[-1])
				break


#Now sort the lengths and show them
sortedLengths = sorted(orgLengths.items(), key= operator.itemgetter(1))

for length in sortedLengths:
	print "%s\t%s" %(length[0], length[1])
