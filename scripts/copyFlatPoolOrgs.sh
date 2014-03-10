#!/bin/bash

for i in {1..40}
do
	cp -v $1/dom-$i.org-A/archive/*.org $2/dom-$i.org-A
	cp -v $1/dom-$i.org-B/archive/*.org $2/dom-$i.org-B
done
