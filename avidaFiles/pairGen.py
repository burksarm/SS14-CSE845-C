#!/usr/bin/python
import os
import re
import subprocess

#Go through each dominant ancestor, figure out the genome-wide mutation rates for both 0.5 and 2.0
for dirname, dirs, files in os.walk("../complex/pool"):
	for fname in files:
		file = open(os.path.join("../complex/pool/", fname), "r")
		for line in file:
			#Find the Genome Size comment line in the file
			if re.match("# Genome Size.+[\d]+", line) != None:
				size = float(line.split()[-1])
				#print "%s -> %s" %(fname, size)
				
				#Calculate the copy mutation rate to set, based on the desired genome-wide rate
				low = 0.5/size
				high = 2.0/size

				#Put some arguments into variables to make the command more readable
				startOrg = "../complex/pool/%s" %fname

				#Run Avida with both the low and high mutation rate
				subprocess.Popen(["avida", "-c", "avida_flat.cfg", "-set", "DATA_DIR", "../flat/%s-A" %fname, 
					"-set", "COPY_MUT_PROB", "%s" %low, "-set", "START_ORGANISM", 
					startOrg])

                                subprocess.Popen(["avida", "-c", "avida_flat.cfg", "-set", "DATA_DIR", "../flat/%s-B" %fname,
                                        "-set", "COPY_MUT_PROB", "%s" %high, "-set", "START_ORGANISM",
                                        startOrg])

	
				#done with this file.
				break
		
