#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pylab import *
import scipy.stats

''' Plots the data from the mutation map on the competition organisms.
	Simply plots the total fraction of lethal, detrimental, neutral, and beneficial mutations.
'''

if not len(sys.argv) == 2:
	print "Usage: python mutAnalysis.py <OUTPUT_DIR>"
	quit()

labels = ["(%) Lethal", "(%) Detrimental", "(%) Neutral", "(%) Beneficial"]

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
aMedians = []
aStdErrs = []

bMeans = []
bMedians = []
bStdErrs = []
pVals = []

for i in range(4):
	#Get the data and convert to percentages
	aVals = [data[i] for data in aData]
	bVals = [data[i] for data in bData]

	#Calculate the medians, means & sems for reporting
	aMeans.append(np.mean(aVals))
	aMedians.append(np.median(aVals))
	aStdErrs.append(scipy.stats.sem(aVals))

	bMeans.append(np.mean(bVals))
	bMedians.append(np.median(bVals))
	bStdErrs.append(scipy.stats.sem(bVals))

	#Get the Mann-Whitney p-value
	zStat, pVal = scipy.stats.ranksums(aVals, bVals)
	pVals.append(pVal)

	print "%s Mann-Whitney p=%f, fast replicator median = %f, SEM = %f, slow replicator median = %f, SEM = %f" %(labels[i], pVal, aMedians[i], aStdErrs[i], bMedians[i], bStdErrs[i])

#Setup some needed vars for the plots
width = 0.25
index = np.arange(1)
errorConfig = {'ecolor': '0.3'}

#Set font size (larger since we're combining figures...)
font = {'size': '18'}
matplotlib.rc('font', **font)

#Setup some layout stuff for the figure
fig, axes = plt.subplots(nrows=2, ncols=2)
fig.tight_layout()
plt.subplots_adjust(right=1.25)

#x and y starting point for the p-value text
pXStart = 0.40
pYStart = 0.85

#subplot labels...
subPlots = ["(a)", "(b)", "(c)", "(d)"]
subXStart = 0.115
subYStart = 0.88

#Plot each metric in the multi-plot...
for i in range(4):
	plt.subplot(2, 2, i+1)
	plt.boxplot([[data[i] for data in aData], [data[i] for data in bData]], notch=True)
	
	#Make a p-value text label
	pText = pText = (" p=%.4f" %pVals[i]) if pVals[i] >= .0001 else "p < 0.0001"
	
	#Set the labels/legend and save the figure
	plt.ylabel(labels[i])

	plt.ylim(0, 100)
	
	#Only put the x-axis labels at the bottom
	#if (i >= 2):
	plt.xticks([1,2], ["fast replicator", "slow replicator"])
	#else:
	#	plt.xticks([1,2], ['', ''])
	
	#Show the p-values
	plt.figtext(pXStart, pYStart, pText)
	
	#Add a sub-plot label
	plt.figtext(subXStart, subYStart, subPlots[i])
	
	pXStart += 0.65
	subXStart += 0.65
	
	if (i == 1):
		pXStart = 0.40
		pYStart -= 0.48
		
		subXStart = 0.115
		subYStart -= 0.48
		

	#Clear the plot for the next figure
	#plt.clf()
	



plt.savefig(os.path.join(outDir, "mutatitonTypes.png"), bbox_inches="tight")	


