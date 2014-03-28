#!/usr/bin/python
import sys
import os
from PIL import Image, ImageFont, ImageDraw
import re

'''Creates simplified figures from the genome mutations map.
'''

if not len(sys.argv) == 3:
	print "Usage: python mutMap.py <INPUT_DIR> <OUTPUT_DIR>"
	quit()

#Setup some vars
inDir = sys.argv[1]
outDir = sys.argv[2]

#The colors to match in the html
LETHAL = "FF0000"
DETRIMENTAL = "FFFF00"
NEUTRAL = "FFFFFF"
BENEFICIAL = "00FF00"

#Colors we'll use
colorMap = {LETHAL: "#FF0000", DETRIMENTAL: "#FFFF00", NEUTRAL: "#0000FF", BENEFICIAL: "#00FF00"}

#Make sure the output path exists
if not os.path.exists(outDir):
	os.makedirs(outDir)

#Load each html file and create a figure from it
for dirname, dirs, filenames in os.walk(inDir):
	for filename in filenames:
		if filename.endswith(".html"):
			genomeData = [] #holds all the genome mutation data
			doParse = False #whether or not to start collecting the data

			for line in open(os.path.join(inDir, filename)):
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

			#Create the figure now that we have the data

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

			img.save(os.path.join(outDir, filename.replace("html", "png")))
				
