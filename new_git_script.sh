#!/bin/bash

# Array of branch names
branches=("release-1.0" "release-2.0" "release-3.0" "release-4.0" "release-5.0")

# Loop through each branch
for branch in "${branches[@]}"
do
    # Skip the main branch
    if [ "$branch" == "main" ]; then
        echo "Skipping main branch."
        continue
    fi
    
    # Checkout the branch
    git checkout $branch

    # Create a file with branch name
    touch "${branch}.txt"

    # Stage the new file
    git add "${branch}.txt"

    # Commit the file in the same branch
    git commit -m "Add file for branch ${branch}"
	  
    git push origin "${branch}"
done