#!/bin/bash

while true; do
# Prompt the user for input and store it in a variable
	echo "Enter Medical Issue at current time:"
	read user_input
	if [[ "$user_input" == "exit" ]]; then
        	break  # Exit the loop if the user enters 'exit'
    	fi
	# Display the input for verification
	python3 gpt.py $user_input
	echo
	echo
	echo
	echo
done

