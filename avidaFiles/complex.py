#!/usr/bin/python
import os
import sys
from subprocess import call

#Figure out the directory name to save to
baseDir = "/mnt/home/burksarm/Documents/CSE845/20140201/complex/"

#Don't cause an endless loop if we mess with the dirs
if os.path.isdir(baseDir):

	i = 1
	while os.path.isdir(baseDir + "data-%s" %(i)):
		i += 1

	outDir = baseDir + "data-%s" %i


	#Run Avida i times, setting the output directory to data-i where i is the current run number
	call(["avida", "-c", "avida_complexityRobustness.cfg",  "-set", "DATA_DIR", outDir])



