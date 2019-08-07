#!/bin/bash
if [ $# -ne 2 ] 
then
	python3 gridtomdp.py $1 1.0
else
	python3 gridtomdp.py $1 $2
fi