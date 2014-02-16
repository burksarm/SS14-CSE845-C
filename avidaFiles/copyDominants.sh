#!/bin/bash

for ((i=$1; i <=$40; i++))
do
	cp -v data-$i/archive/*.org ../organisms/complexPool/dom-$i.org
done
