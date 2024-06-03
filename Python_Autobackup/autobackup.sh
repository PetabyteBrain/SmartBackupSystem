#!/bin/bash
# ----------------
# autobackup.sh
# ----------------
# 1.  The purpose of this File is to automatically create a copy of a chosen Folder (maybe of a Server)
#     and to Paste it into a Backup Folder. The Folder Name of the Backup should be: "'ServerName'_'DateofBackup'"
#
#     At the same time a Log file should be created to see and troubleshoot incase of problems
#
# 2.  The Second Part of the Script checks the Date of creation of the Scripts and if it's older than the chosen Archive
#     value it will be moved to the Archive Folder.
#
#     The Values: (copyingto, archivedir and ExpiryDate) int the Housekeeping file need to be changed if the Values in this File are changed.
#
#Change the Folowing Variables (BackupTitle, copyingfrom, copyingto and archivedir) to the correct Value for your Use Case.
# !!(Only change the Value for (today) if you want it to have another Name otherwise leave it)!!

BackupTitle="ServerXYZ"
copyingfrom="/home/vmadmin/Schreibtisch/TestEnvironment/TestServer"
copyingto="/home/vmadmin/Schreibtisch/TestEnvironment/Backups"
archivedir="/home/vmadmin/Schreibtisch/TestEnvironment/Archiv"
ExpiryDate=30
today=$(date '+%d-%m-%Y')

# 1.
if [[ -e $copyingfrom ]];then
    cp -r $"$copyingfrom" $"$copyingto"/$"$BackupTitle"_$"$today"
    if [[ -e $"$copyingto"/$"$BackupTitle"_$"$today" ]];then
        touch $"$copyingto"/log$"$today".txt && echo $"$today" "Successful Tranfer -- Backups should be found under" $"$copyingfrom" $"$copyingto"/$"$BackupTitle"_$"$today" >> $"$copyingto"/log$"$today".txt
    else
        echo $"$today" "Backup couldn't be Completed, if problem persists go find Server Admin to fix or contact Support." &>> $"$copyingto"/logfailed$"$today".txt
    fi
else
    echo $"$today" "Backup couldn't be Completed, if problem persists go find Server Admin to fix or contact Support." &>> $"$copyingto"/logfailed$"$today".txt
fi

# 2.
sudo ./housekeeping.sh $copyingto $archivedir $ExpiryDate;