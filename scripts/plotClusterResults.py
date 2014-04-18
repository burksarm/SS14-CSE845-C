#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

#Simple script to plot the data of interest from the A and B clustered ancestors.
#Takes three arguments: 1 - the path to the AVERAGE_MODULARITY results
#					    2 - the output path
#						3 - a list of column indices to plot. example: 0,1,3,10

#Convenience method to generate a file name for the figure, based on the label
def getFigName(label):
	return ''.join(c for c in label.title() if not c.isspace())

#Convenience method to make sure the output directories exist
#param dirs a list of output dirnames
def checkOutputPaths(dirNames):
	for dirName in dirNames:
		if not os.path.exists(dirName):
			os.makedirs(dirName)

#Check args
if len(sys.argv) < 3:
	print "Usage plotModularity.py <INPUT_DIR> <OUTPUT_DIR> <COLS TO PLOT (optional) example: 0,1,3,10"
	quit()

#Figure out the columns of interest to plot
COLS_TO_PLOT = [5, 6, 7]

if len(sys.argv) == 4:
	COLS_TO_PLOT = [int(col.strip()) for col in sys.argv[3].split(",")]

#Setup some needed vars
inDir = sys.argv[1]
outDir = sys.argv[2]
labels = []

#Make sure the output paths exist
checkOutputPaths([outDir])

for line in open("avgModularityLegend.dat"):
	labels.append(line.strip())

#Get the list of ancestors we used
ancestors = []
for line in open("../results/goodComps.txt", "r"):
	ancestors.append(line.strip())

#Collect all the individual A and B data points
aPoints = []
bPoints = []

for ancestor in ancestors:
	aPoints.append([float(d) for d in open(os.path.join(inDir, 
		"modularity_%s-A.dat" %ancestor)).readline().split()])

	bPoints.append([float(d) for d in open(os.path.join(inDir, 
		"modularity_%s-B.dat" %ancestor)).readline().split()])

#Adjust the proportion of sites used in tasks based on the number of tasks done
for i in range(len(aPoints)):
	aPoints[i][3] = (aPoints[i][3] / aPoints[i][1])
	bPoints[i][3] = (bPoints[i][3] / bPoints[i][1])

#Do a Mann-Whitney-Wilcox RankSum test on all the columns
pValues = []
for column in COLS_TO_PLOT:
	a = [aPoints[i][column] for i in range(len(aPoints))]
	b = [bPoints[i][column] for i in range(len(bPoints))]

	zStat, pVal = stats.ranksums(a, b)
	pValues.append(pVal)

#Plot the data for each cluster (A and B)
for i in range(len(COLS_TO_PLOT)):
	column = COLS_TO_PLOT[i]

	#Make the proportions from 0 to 1
	if (COLS_TO_PLOT[i] == 6 or COLS_TO_PLOT[i] == 7):
		plt.ylim(0, 1)

	plt.boxplot([[data[column] for data in aPoints], [data[column] for data in bPoints]], notch=True)
	plt.xlabel("Ancestor Group")
	plt.ylabel(labels[column])
	plt.figtext(0.75, 0.8, " p=%.4f" %pValues[i])
	plt.xticks([1,2], ["A", "B"])
	plt.savefig(os.path.join(outDir, getFigName(labels[column])), bbox_inches="tight")
	plt.clf()









