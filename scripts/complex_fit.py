import re
%pylab inline

fit_list= []

for i in range(1, 41):
    fitness = float(0)
    
    with open('pool/dom-%s.org' %i, 'r') as org:
    
        for line in org:
            if line.startswith('# Fitness'):
                fitness = float(line.split()[2])
                
                fit_list.append(fitness)
                
            
print fit_list

plot(fit_list)
