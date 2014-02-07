import re
import csv
from pandas import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%pylab inline

fit_comp = []
for i in range(1, 41):
    fitness = float(0)
    
    with open('reproduction/pool/dom-%s.org' %i, 'r') as org:
    
        for line in org:
            if line.startswith('# Fitness'):
                fitness = float(line.split()[2])
                
                fit_comp.append(fitness)

fit_comp.sort()
fit_comp.reverse()

fit_low = []
for i in range(1, 41):
    fitness = float(0)
    
    with open('reproduction/pairs/dom-%s.org-A' %i, 'r') as org:
    
        for line in org:
            if line.startswith('# Fitness'):
                fitness = float(line.split()[2])
                
                fit_low.append(fitness)

fit_low.sort()
fit_low.reverse()

fit_high = []
for i in range(1, 41):
    fitness = float(0)
    
    with open('reproduction/pairs/dom-%s.org-B' %i, 'r') as org:
    
        for line in org:
            if line.startswith('# Fitness'):
                fitness = float(line.split()[2])
                
                fit_high.append(fitness)

fit_high.sort()
fit_high.reverse()


with open('fitness.csv', 'wb') as f:
    w = csv.writer(f,delimiter=',', quoting = csv.QUOTE_ALL)
    w.writerow('CLH')
    for row in zip(fit_comp, fit_low, fit_high):
        w.writerow(row)
    
# must specify that blank space " " is NaN  
experimentDF = read_csv("fitness.csv", na_values=[" "])  
print experimentDF

sns.set_color_palette("hls")
mpl.rc("figure", figsize=(16, 8))
experimentDF.dropna().plot(kind='kde')
