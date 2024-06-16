#!/bin/bash
# ----------------
# housekeeping.sh
# ----------------
#
# This script has the task of cleaning up the backup folder by checking if any of the folders in it are older than the ExpiryDate amount of days.
# ----------------
# The value of the variable can be changed so that the ExpiryDate is higher or lower.

copyingto=$1
archivedir=$2
ExpiryDate=$3

echo "copyingto: $copyingto"
echo "archivedir: $archivedir"
echo "ExpiryDate: $ExpiryDate"

# Ensure paths do not end with a slash
copyingto=${copyingto%/}
archivedir=${archivedir%/}

# Calculate the cutoff date
cutoffDate=$(date -d "-$ExpiryDate days" '+%Y-%m-%d')

echo "cutoffDate: $cutoffDate"

# Get all directories in the backup folder older than the cutoff date
find "$copyingto" -mindepth 1 -maxdepth 1 -type d -not -path "$copyingto" | while read -r dir; do
    dirDate=$(stat -c %Y "$dir")
    if [[ $(date -d "@$dirDate" +%Y-%m-%d) < "$cutoffDate" ]]; then
        echo "Moving $dir to $archivedir"
        mv "$dir" "$archivedir"
    fi
done