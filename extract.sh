#!/bin/bash
mkdir Project_Files 
cd Project_Files/
for i in {A..Z}; do
  python3 extract.py $i  
done


