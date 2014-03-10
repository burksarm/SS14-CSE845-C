#!/usr/bin/python
import os
import sys
from subprocess import call

#Figure out the directory name to save to
if len(sys.argv) != 2:
	print "Usage: python complex.py <OUTPUT_DIRECTORY>"
	quit()

outDir = sys.argv[1]

#Make sure the entire path exists, or else avida won't actually save
#even though it will create the inner-most dir if everything else exists
if not os.path.exists(outDir):
	os.makedirs(outDir)

#Run Avida i times, setting the output directory to data-i where i is the current run number
call(["avida", "-c", "avida_complexityRobustness.cfg",  "-set", "DATA_DIR", outDir])

