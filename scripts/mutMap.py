#!/usr/bin/python
import sys
import os
from PIL import Image, ImageFont, ImageDraw
import re
import matplotlib.pyplot as plt
import scipy.stats as stats

'''	Creates simplified figures from the genome mutations map. Also, analyzes the
	total number of completely neutral sites in the genome.
'''

#Convenience method to get the genome data from a file.
#param path - the path to the html mutation map file to parse
#Returns an array of color coded columns for each mutation along the genome (rows)
def getGenomeData(path):
	genomeData = [] #holds all the genome mutation data
	doParse = False #whether or not to start collecting the data

	for line in open(path):
		#Don't start parsing until we get past the header row in the table
		if not doParse and line.startswith("<tr><td align=right>"):
			doParse = True

		#Parse all the rows in the table.
		if doParse and line.startswith("<tr>"):

			#Extract all the mutation rows
			cols = line.strip().split("<th ")
			colors = []
			for col in cols:
				index = col.find("bgcolor")

				if index >= 0:
					color = col[index+9:index+16].replace("\"", "").replace("#", "")
					colors.append(color)

			if len(colors) > 0:
				genomeData.append(colors[0:28])

	return genomeData

#

#Convenience method to generate the mutation map figure based on the genome data
#param genomeData - the genome data generated from getGenomeData
#param outPath the path to save the figure to
def makeMutMap(genomeData, outPath):
	xPos = 0 #starting x-coordinate to paint
	yPos = 0 #starting y-coordinate to paint

	GENE_WIDTH  = 5
	GENE_HEIGHT = 5

	img = Image.new('RGB', (GENE_WIDTH*28, GENE_HEIGHT*len(genomeData)))
	draw = ImageDraw.Draw(img)

	for row in genomeData:
		for col in row:
			draw.rectangle(((xPos, yPos), (xPos+GENE_WIDTH, yPos+GENE_HEIGHT)), fill=colorMap[col], outline="black")
			xPos += GENE_WIDTH
		
		xPos = 0
		yPos += GENE_HEIGHT

	img.save(outPath)


#Convenience method to determine the percent of completely neutral sites
#in the genome, where completely neutral means all mutations are either neutral
#or beneficial (i.e. where they don't negatively affect fitness).
#param genomeData - the genome data generated from getGenomeData
#Returns the proportion of completely neutral sites in the genome
def calcNeutralSites(genomeData):
	totalNeutral = 0.0
	for siteData in genomeData:
		#Get the total set of different mutational effects
		mutTypes = set(siteData)

		#If they were all neutral or beneficial, increment the count
		if (len(mutTypes) == 1 and NEUTRAL in mutTypes):# or (len(mutTypes) == 2 and NEUTRAL in mutTypes and BENEFICIAL in mutTypes):
			totalNeutral += 1.0

	#Now calculate the percent of neutral sites in the entire genome
	percentNeutral = (totalNeutral/float(len(genomeData))) * 100

	return percentNeutral
		
#Convenience method to plot the percentages of completely neutral (or beneficial)
#sites in A vs B.
def plotPercentNeutral(aNeutralPercentages, bNeutralPercentages, outPath):
	#Calculate the Mann-Whitney U p-value
	zStat, pVal = stats.ranksums(aNeutralPercentages, bNeutralPercentages)

	#Now plot the percentages in a box plot
	plt.boxplot([aNeutralPercentages, bNeutralPercentages], notch=True)
	#plt.xlabel("Ancestor Group")
	plt.ylabel("Percent Neutral Sites")
	plt.xticks([1,2], ["fast replicator", "slow replicator"])
	plt.figtext(0.75, 0.8, " p=%.4f" %pVal)
	plt.savefig(outPath, bbox_inches="tight")


#Convenience method to get the base org name (i.e. dom-i) from the html file name
def getOrgName(filename):
	return filename[filename.find("dom-"):filename.rfind("-")]
		
#-------------------- main ----------------------------------
if not len(sys.argv) == 3:
	print "Usage: python mutMap.py <INPUT_DIR> <OUTPUT_DIR>"
	quit()

#Setup some vars
inDir = sys.argv[1]
outDir = sys.argv[2]

#Make sure the output path exists
if not os.path.exists(outDir):
	os.makedirs(outDir)

#The colors to match in the html
LETHAL = "FF0000"
DETRIMENTAL = "FFFF00"
NEUTRAL = "FFFFFF"
BENEFICIAL = "00FF00"

#Colors we'll use
colorMap = {LETHAL: "#FF0000", DETRIMENTAL: "#FFFF00", NEUTRAL: "#0000FF", BENEFICIAL: "#00FF00"}

#Load each html file and create a figure from it
neutralPercentages = {}	#Contains the neutral percentages for A/B ancestors

for dirname, dirs, filenames in os.walk(inDir):
	for filename in filenames:
		if filename.endswith(".html"):
			#Get the base org name
			baseOrg = getOrgName(filename)

			#Get the genome mutation data
			genomeData = getGenomeData(os.path.join(inDir, filename))

			#Create the figure now that we have the data
			makeMutMap(genomeData, os.path.join(outDir, filename.replace("html", "png")))

			#Figure out the percentage of completely neutral sites in the genome
			percentNeutral = calcNeutralSites(genomeData)

			#Collect neutral proportions for A and B so we can compare
			if filename.endswith("-A.html"):
				if not baseOrg in neutralPercentages:
					neutralPercentages[baseOrg] = [0, 0]

				neutralPercentages[baseOrg][0] = percentNeutral

			elif filename.endswith("-B.html"):
				if not baseOrg in neutralPercentages:
					neutralPercentages[baseOrg] = [0, 0]

				neutralPercentages[baseOrg][1] = percentNeutral

#Now plot the percentages neutral if we were analyzing A and B files
#Make sure A and B percentages are together for clarity
baseOrgs = neutralPercentages.keys()
aNeutralPercentages = [neutralPercentages[baseOrg][0] for baseOrg in baseOrgs]
bNeutralPercentages = [neutralPercentages[baseOrg][1] for baseOrg in baseOrgs]

#Sanity check
print "Base Ancestor,A,B"
for baseOrg in baseOrgs:
	print "%s,%s,%s" %(baseOrg,neutralPercentages[baseOrg][0], neutralPercentages[baseOrg][1])

plotPercentNeutral(aNeutralPercentages, bNeutralPercentages, os.path.join(outDir, "percentNeutralSites.png"))


				
