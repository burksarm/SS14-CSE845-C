#!/bin/bash

#Just submits 40 jobs. 
#The sleep is to try to get a separate output dir for each job to avoid conflicts. Not perfect.
for i in {1..40}
do
	qsub complex-pool.qsub
	sleep 30
done
