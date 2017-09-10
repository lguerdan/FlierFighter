#!/bin/bash
i=0
for file in *.jpg
do
	mv "$file" "$i.jpg"
	i=$(($i+1))
done 
