#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

#Simple script to plot ALL the data from the A and B clustered ancestors.
#Takes three arguments: 1 - the path to the AVERAGE_MODULARITY results
#					    2 - the output path
#Creates bar charts and box plots for each metric

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
barChartDir = os.path.join(outDir, "barCharts")
boxPlotDir  = os.path.join(outDir, "boxPlots")

#Make sure the output paths exist
if not os.path.exists(outDir):
	os.makedirs(outDir)

#Save bar charts and box plots
if not os.path.exists(barChartDir):
	os.makedirs(barChartDir)

if not os.path.exists(boxPlotDir):
	os.makedirs(boxPlotDir)

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

#Adjust the proportion of sites used in tasks based on the number of tasks done?
'''for i in range(len(aPoints)):
	aPoints[i][3] = (aPoints[i][3]/aPoints[i][1])
	bPoints[i][3] = (bPoints[i][3]/bPoints[i][1])'''

#Now get the Standard Error of the Mean for each point
aSems = []
bSems = []

for column in range(44):
	aSems.append(stats.sem([float(aPoints[i][column]) for i in range(len(aPoints))]))
	bSems.append(stats.sem([float(bPoints[i][column]) for i in range(len(bPoints))]))


#Plot the data for each cluster (A and B)
aFile = os.path.join(inDir, "modularity_cluster-A.dat")
bFile = os.path.join(inDir, "modularity_cluster-B.dat")

#Read all the data (should just be a single line)
aData = open(aFile, "r").readline().split()
bData = open(bFile, "r").readline().split()

#Go ahead and plot a figure for each column.
errorConfig = {'ecolor': '0.3'}

for column in range(44):
	print "plotting ", labels[column]
	results = []
	results.append([float(aData[column].strip())])
	results.append([float(bData[column].strip())])

	print "\tA: ", results[0], " B: ", results[1]

	#Plot the data in a bar chart.
	width = 0.25 #Width of each bar
	aPos = np.arange(1) #Position(s) for A bar(s)
	bPos = [pos + width/.75 for pos in aPos] #Position(s) for B bar(s)


	plt.bar(aPos, results[0], width, align="center", color="b", yerr=aSems[column], error_kw=errorConfig)
	plt.bar(bPos, results[1], width, align="center", color="r", yerr=bSems[column], error_kw=errorConfig)
	plt.xticks([aPos, bPos], ["A", "B"])

	plt.xlabel("Ancestor Group")
	plt.ylabel(labels[column])

	plt.savefig(os.path.join(barChartDir, getFigName(labels[column])), bbox_inches="tight")

	#Cleanup
	plt.clf()

	#Now plot the data in a box plot
	plt.boxplot([[data[column] for data in aPoints], [data[column] for data in bPoints]], notch=True, bootstrap=5000)
	plt.xlabel("Ancestor Group")
	plt.ylabel(labels[column])
	plt.xticks([1,2], ["A", "B"])
	plt.savefig(os.path.join(boxPlotDir, getFigName(labels[column])), bbox_inches="tight")
	plt.clf()









