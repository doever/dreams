#!/bin/bash

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                                 batch_exec_compare.sh                                       #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script Batch execution compare_file script.                                        #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/4/11 10:33                                                                #
# License    : Copyright (c) 2024 by cl                                                       #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


# Check if work_dt is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <work_dt>"
    exit 1
fi

# Set the work_dt variable
work_dt="$1"

# Define an array to store directory paths
declare -a directories=(
    "/path/to/directory1"
    "/path/to/directory2"
    "/path/to/directory3"
    # Add more directories as needed
)

# Loop through each directory
for directory in "${directories[@]}"; do
    # Check if the directory exists
    if [ -d "$directory" ]; then
        echo "Cleaning up directory: $directory"

        # Calculate the date range to delete files
        start_date=$(date -d "$work_dt -10 days" +%Y%m%d)
        end_date=$(date -d "$work_dt -3 days" +%Y%m%d)

        # Loop through date directories and delete files
        while [[ $start_date -le $end_date ]]; do
            date_dir="$directory/$start_date"
            if [ -d "$date_dir" ]; then
                echo "Removing files in $date_dir"
                rm -f "$date_dir"/*.dat  # Adjust file extension as needed
                rmdir "$date_dir" 2>/dev/null
            fi
            start_date=$(date -d "$start_date +1 day" +%Y%m%d)
        done
    else
        echo "Directory not found: $directory"
    fi
done
