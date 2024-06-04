# ----------------
# autobackup.ps1
# ----------------
# 1.  The purpose of this script is to automatically create a copy of a chosen folder
#     and paste it into a backup folder. The folder name of the backup should be: "'ServerName'_'DateofBackup'"
#
#     At the same time a log file should be created to see and troubleshoot in case of problems.
#
# 2.  The second part of the script checks the date of creation of the backups and if they're older than the chosen archive
#     value, it will move them to the archive folder.
#
# Change the following variables (BackupTitle, copyingfrom, copyingto, and archivedir) to the correct value for your use case.
# !!(Only change the value for $today if you want it to have another name, otherwise leave it)!!

$BackupTitle = "ServerXYZ"
$copyingfrom = "C:\Github\SmartBackupSystem\TestEnvironment"
$copyingto = "C:\Github\SmartBackupSystem\Backup"
$archivedir = "C:\Github\SmartBackupSystem\Archive"
$ExpiryDate = 30
$today = Get-Date -Format "dd-MM-yyyy"

# 1.
if (Test-Path $copyingfrom) {
    Copy-Item -Recurse -Path $copyingfrom -Destination $copyingto"\"$BackupTitle"_"$today
    if (Test-Path "$copyingto\$BackupTitle_$today") {
        "$today Successful Transfer -- Backups should be found under $copyingfrom $copyingto\$BackupTitle_$today" | Out-File -FilePath "$copyingto\log$today.txt"
    } else {
        "$today Backup couldn't be completed. If problem persists, find server admin to fix or contact support." | Out-File -FilePath "$copyingto\logfailed$today.txt" -Append
    }
} else {
    "$today Backup couldn't be completed. If problem persists, find server admin to fix or contact support." | Out-File -FilePath "$copyingto\logfailed$today.txt" -Append
}

# 2.
# Assuming you have a housekeeping PowerShell script named housekeeping.ps1
# and it accepts the same parameters.
.\winhousekeeping.ps1 -copyingto $copyingto -archivedir $archivedir -ExpiryDate $ExpiryDate
