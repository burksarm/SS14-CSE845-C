#!/usr/bin/python
import sys
import os
import re
from PIL import Image, ImageFont, ImageDraw

'''Creates simplified figures from the task sites map.
'''

if not len(sys.argv) == 3:
	print "Usage: python taskSites.py <INPUT_DIR> <OUTPUT_DIR>"
	quit()

#Setup some vars
inDir = sys.argv[1]
outDir = sys.argv[2]

#The colors to match in the html
NOT_PERFORMED = "#FF0000"
PERFORMED = "#00FF00"
NOT_USED = "#FFFFFF"

#Colors we'll use
colorMap = {NOT_PERFORMED: "#FF0000", PERFORMED: "#00FF00", NOT_USED: "#0000FF"}

#Make sure the output path exists
if not os.path.exists(outDir):
	os.makedirs(outDir)

#Load each html file and create a figure from it
for dirname, dirs, filenames in os.walk(inDir):
	for filename in filenames:
		if filename.endswith(".html"):
			genomeData = [] #holds all the task map data
			print filename
			doParse = False #whether or not to start collecting the data

			for line in open(os.path.join(inDir, filename)):
				#Don't start parsing until we get past the header row in the table
				firstRow = line.find("Base Creature") != -1
				if not doParse and firstRow and line.find("Totals") == -1:
					doParse = True

				#Parse all the rows in the table.
				if doParse and line.startswith("<tr>"):

					#Extract all the mutation rows
					cols = line.strip().split("<td ") if not firstRow else line.strip().split("<th ")
					colors = []
					for col in cols:
						#print col
						index = col.find("bgcolor")

						if index >= 0:
							color = col[index+9:index+16]
							colors.append(color)
	
					if len(colors) == 9:
						#print len(colors)
						genomeData.append(colors)

			#Create the figure now that we have the data

			xPos = 0 #starting x-coordinate to paint
			yPos = 0 #starting y-coordinate to paint

			GENE_WIDTH  = 5
			GENE_HEIGHT = 5

			img = Image.new('RGB', (GENE_WIDTH*9, GENE_HEIGHT*len(genomeData)))
			draw = ImageDraw.Draw(img)

			#Start at the bottom to make the image the same as the html
			for row in genomeData:
				for col in row:
					draw.rectangle(((xPos, yPos), (xPos+GENE_WIDTH, yPos+GENE_HEIGHT)), fill=colorMap[col], outline="black")
					xPos += GENE_WIDTH
				
				xPos = 0
				yPos += GENE_HEIGHT

			img.save(os.path.join(outDir, filename.replace("html", "png")))


