#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

#Simple script to plot ALL the data from the A and B clustered ancestors.
#Takes three arguments: 1 - the path to the AVERAGE_MODULARITY results
#					    2 - the output path

#Convenience method to generate a file name for the figure, based on the label
def getFigName(label):
	return ''.join(c for c in label.title() if not c.isspace())

#Plots the results from the AVERAGE_MODULARITY command on the A-B clustered ancestors
if len(sys.argv) != 3:
	print "Usage plotModularity.py <INPUT_DIR> <OUTPUT_DIR>"
	quit()

#Setup some needed vars
inDir = sys.argv[1]
outDir = sys.argv[2]
labels = []

#Make sure the output path exists
if not os.path.exists(outDir):
	os.makedirs(outDir)

for line in open("avgModularityLegend.dat"):
	labels.append(line.strip())

#Plot the data for each cluster (A and B)
aFile = os.path.join(inDir, "modularity_cluster-A.dat")
bFile = os.path.join(inDir, "modularity_cluster-B.dat")

#Read all the data (should just be a single line)
aData = open(aFile, "r").readline().split()
bData = open(bFile, "r").readline().split()

#Go ahead and plot a figure for each column.
for column in range(44):
	print "plotting ", labels[column]
	results = []
	results.append([float(aData[column].strip())])
	results.append([float(bData[column].strip())])

	print "\tA: ", results[0], " B: ", results[1]

	#Plot the data.
	width = 0.25 #Width of each bar
	aPos = np.arange(1) #Position(s) for A bar(s)
	bPos = [pos + width/.75 for pos in aPos] #Position(s) for B bar(s)


	plt.bar(aPos, results[0], width, align="center", color="b")
	plt.bar(bPos, results[1], width, align="center", color="r")
	plt.xticks([aPos, bPos], ["A", "B"])

	plt.xlabel("Ancestor Group")
	plt.ylabel(labels[column])

	plt.savefig(os.path.join(outDir, getFigName(labels[column])), bbox_inches="tight")

	#Cleanup
	plt.clf()












