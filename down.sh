#!/bin/bash
mkdir Project_Files 
cd Project_Files/
for i in {A..Z}; do
  wget "https://www.mayoclinic.org/diseases-conditions/index?letter=$i"  
done

