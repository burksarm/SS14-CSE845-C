#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import scipy.stats

''' Plots the data from the mutation map on the competition organisms.
	Simply plots the total fraction of lethal, detrimental, neutral, and beneficial mutations.
'''

if not len(sys.argv) == 2:
	print "Usage: python mutAnalysis.py <OUTPUT_DIR>"
	quit()

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
		aData.append([float(d) * 100 for d in line.strip().split("\t")])

for line in open("../results/mutAnalysis/mutMap-B.dat"):
	if not line.startswith("#"):		
		bData.append([float(d) * 100 for d in line.strip().split("\t")])

#Calulate the means and stdevs (in case we want to plot error bars)
aMeans = []
aStdErrs = []

bMeans = []
bStdErrs = []

for i in range(4):
	#Get the data and convert to percentages
	aVals = [data[i] for data in aData]
	bVals = [data[i] for data in bData]

	#Calculate the means & stdevs
	aMeans.append(np.mean(aVals))
	aStdErrs.append(scipy.stats.sem(aVals))

	bMeans.append(np.mean(bVals))
	bStdErrs.append(scipy.stats.sem(bVals))

#Setup some needed vars for the plots
width = 0.25
index = np.arange(1)
errorConfig = {'ecolor': '0.3'}
labels = ["Percent Lethal mutations", "Percent Detrimental Mutations", "Percent Neutral Mutations", "Percent Beneficial Mutations"]

#Plot each metric in a separate figure
for i in range(4):
	plt.boxplot([[data[i] for data in aData], [data[i] for data in bData]], notch=True)

	#Set the labels/legend and save the figure
	plt.ylabel(labels[i])
	plt.xlabel("Ancestor Group")
	plt.xticks([1,2], ["A", "B"])
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	plt.savefig(os.path.join(outDir, getFigName(labels[i]) + ".png"))

	#Clear the plot for the next figure
	plt.clf()


