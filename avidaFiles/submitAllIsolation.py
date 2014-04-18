#!/usr/bin/python

import os
import subprocess
import sys

if len(sys.argv) != 3:
	print "Usage: submitAllIsolation.py <OUTPUT_DIR> <NUM_GENS>"
	quit()

outDir  = sys.argv[1]
numGens = sys.argv[2]

for i in range(11):
	outPath = os.path.join(outDir, "run%s" %i)

	if not os.path.exists(outPath):
		os.makedirs(outPath)

	subprocess.call(("python analyzeTasks.py %s %s" %(outPath, numGens)).split())
	
