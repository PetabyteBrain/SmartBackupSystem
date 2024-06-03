#!/bin/bash
# ----------------
# housekeeping.sh
# ----------------
#
# this Script has the Task of Cleaning up the Backup Folder by checking if any of the Folders in it are Older than the Expiry Date amount of days
# ----------------
# The Value of the Variable can be changed so that the Expiry Date is higher / Lower

copyingto=$1
archivedir=$2
ExpiryDate=$3

find $copyingto/ -mtime +$ExpiryDate -not -path "*/Backups/" -exec  mv {} $archivedir \;