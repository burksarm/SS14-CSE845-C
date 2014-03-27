#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
''' Analyzes the data from the mutation map on the competition organisms.
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

aData = []
bData = []

for line in open("../results/mutAnalysis/mutMap-A.dat"):
	if not line.startswith("#"):		
		aData.append([float(d) for d in line.strip().split("\t")])

for line in open("../results/mutAnalysis/mutMap-B.dat"):
	if not line.startswith("#"):		
		bData.append([float(d) for d in line.strip().split("\t")])


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

width = 0.25
index = np.arange(14)
errorConfig = {'ecolor': '0.3'}

labels = ["Fraction of Lethal mutations", "Fraction of Detrimental Mutations", "Fraction of Neutral Mutations", "Fraction of Beneficial Mutations"]

for i in range(4):
	aVals = [data[i] for data in aData]
	bVals = [data[i] for data in bData]

	plt.bar(index, aVals, width, color='b', label="A")#, yerr=[aStdvs[i] for aVal in aVals], error_kw=errorConfig)
	plt.bar(index+width, bVals, width, color='r', label="B")#yerr=[bStdvs[i] for bVal in bVals], error_kw=errorConfig

	plt.ylabel(labels[i])
	plt.xlabel("Ancestor Pair")
	plt.xticks(index + width, [group for group in range(1, 15)])
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	plt.savefig(os.path.join(outDir, getFigName(labels[i]) + ".png"), bbox_inches="tight")

	plt.clf()





