#!/bin/bash

for ((i=$1; i <=$2; i++))
do
	cp -v data-$i/archive/*.org ancestorPool/dom-$i.org
done
