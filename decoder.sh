#!/bin/bash
if [ $# -ne 3 ] 
then
	python3 pydecoder.py $1 $2 1.0
else
	python3 pydecoder.py $1 $2 $3
fi