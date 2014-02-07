import re
import csv
from pandas import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%pylab inline

fit_list = []
for i in range(1, 41):
    fitness = float(0)
    
    with open('reproduction/pool/dom-%s.org' %i, 'r') as org:
    
        for line in org:
            if line.startswith('# Fitness'):
                fitness = float(line.split()[2])
                
                fit_list.append(fitness)

print fitness
fit_list.sort()
fit_list.reverse()


myfile = open('output.csv', 'wb')
wr = csv.writer(myfile)
wr.writerow("F")
for value in fit_list:
    wr.writerow([value])
    
# must specify that blank space " " is NaN  
experimentDF = read_csv("output.csv", na_values=[" "])  
print experimentDF

sns.set_color_palette("hls")
mpl.rc("figure", figsize=(16, 8))
sns.distplot(experimentDF)
