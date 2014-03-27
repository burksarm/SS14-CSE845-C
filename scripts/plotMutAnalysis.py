#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
''' Plots the data from the mutation map on the competition organisms.
	Simply plots the total fraction of lethal, detrimental, neutral, and beneficial mutations.
'''

if not len(sys.argv) == 2:
	print "Usage: python mutAnalysis.py <OUTPUT_DIR>"

#Convenience method to generate a file name for the figure, based on the label
def getFigName(label):
	return ''.join(c for c in label.title() if not c.isspace())

#Setup some variables
outDir = sys.argv[1]



#Make sure output path exists
if not os.path.exists(outDir):
	os.makedirs(outDir)

#Load in the data from A and B
aData = []
bData = []

for line in open("../results/mutAnalysis/mutMap-A.dat"):
	if not line.startswith("#"):		
		aData.append([float(d) for d in line.strip().split("\t")])

for line in open("../results/mutAnalysis/mutMap-B.dat"):
	if not line.startswith("#"):		
		bData.append([float(d) for d in line.strip().split("\t")])

#Calulate the means and stdevs (in case we want to plot error bars)
aMeans = []
aStdvs = []

bMeans = []
bStdvs = []

for i in range(4):
	aVals = [data[i] for data in aData]
	bVals = [data[i] for data in bData]

	aMeans.append(np.mean(aVals))
	aStdvs.append(np.std(aVals))

	bMeans.append(np.mean(bVals))
	bStdvs.append(np.std(bVals))

#Setup some needed vars for the plots
width = 0.25
index = np.arange(14)
errorConfig = {'ecolor': '0.3'}
labels = ["Percent Lethal mutations", "Percent Detrimental Mutations", "Percent Neutral Mutations", "Percent Beneficial Mutations"]

#Plot each metric in a separate figure
for i in range(4):
	#Get all the data for A and B for the current column (and converto to percentages)
	aVals = [data[i] * 100 for data in aData]
	bVals = [data[i] * 100 for data in bData]

	plt.bar(index, aVals, width, color='b', label="A")#, yerr=[aStdvs[i] for aVal in aVals], error_kw=errorConfig)
	plt.bar(index+width, bVals, width, color='r', label="B")#yerr=[bStdvs[i] for bVal in bVals], error_kw=errorConfig)

	#Set the y scale to help compare figures
	#plt.ylim(0, 70)

	#Set the labels/legend and save the figure
	plt.ylabel(labels[i])
	plt.xlabel("Ancestor Pair")
	plt.xticks(index + width, [group for group in range(1, 15)])
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	plt.savefig(os.path.join(outDir, getFigName(labels[i]) + ".png"), bbox_inches="tight")

	#Clear the plot for the next figure
	plt.clf()


