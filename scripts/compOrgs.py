#!/usr/bin/python
import os
import re

#Simple module with a single method to get the list of ancestor names that were used for the competitions
#Import it into the script you'd like and use it. Just pass it the directory where the environment files
#are located, which should be the avidaFiles directory if you're using the generated environments.

#Gets a list of competition organism names, based on the generated environment files.
def getCompOrgs(environmentDir="../avidaFiles"):
	compOrgs = []
	#Use the environment file names to know which pair was run.
	for dirname, dirs, files in os.walk(environmentDir):
		for filename in files:
			#If it's one of the environment_dom*_comp files, we know it is a competiton environment.
			m = re.match("environment_(dom-[\d]+)_comp", filename)
			if m != None:
				baseOrg = m.group(1)
				compOrgs.append(baseOrg)
	
	#We got 'em all.
	return compOrgs