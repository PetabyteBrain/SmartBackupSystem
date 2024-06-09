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
# Change the following variables (BackupTitle, CopyPath, PastePath, and ArchivePath) to the correct value for your use case.
# !!(Only change the value for $today if you want it to have another name, otherwise leave it)!!
param (
    [string]$BackupTitle,
    [string]$CopyPath,
    [string]$PastePath,
    [string]$ArchivePath,
    [int]$ExpiryDate
)

$today = Get-Date -Format "dd-MM-yyyy"

# 1.
if (Test-Path $CopyPath) {
    $destinationPath = Join-Path -Path $PastePath -ChildPath "${BackupTitle}_$today"
    Copy-Item -Recurse -Path $CopyPath -Destination $destinationPath
    if (Test-Path $destinationPath) {
        "$today Successful Transfer -- Backups should be found under $CopyPath $destinationPath" | Out-File -FilePath (Join-Path -Path $PastePath -ChildPath "log$today.txt")
    } else {
        "$today Backup couldn't be completed. If problem persists, find server admin to fix or contact support." | Out-File -FilePath (Join-Path -Path $PastePath -ChildPath "logfailed$today.txt") -Append
    }
} else {
    "$today Backup couldn't be completed. If problem persists, find server admin to fix or contact support." | Out-File -FilePath (Join-Path -Path $PastePath -ChildPath "logfailed$today.txt") -Append
}

# 2.
# Ensure the housekeeping script path is correct
$housekeepingScript = Join-Path -Path $PSScriptRoot -ChildPath 'winhousekeeping.ps1'
& $housekeepingScript -copyingto $PastePath -archivedir $ArchivePath -ExpiryDate $ExpiryDate
