# ----------------
# housekeeping.ps1
# ----------------
#
# This script has the task of cleaning up the backup folder by checking if any of the folders in it are older than the ExpiryDate amount of days.
# ----------------
# The value of the variable can be changed so that the ExpiryDate is higher or lower.

param (
    [string]$copyingto,
    [string]$archivedir,
    [int]$ExpiryDate
)

# Calculate the cutoff date
$cutoffDate = (Get-Date).AddDays(-$ExpiryDate)

# Get all directories in the backup folder older than the cutoff date
$oldBackups = Get-ChildItem -Path $copyingto | Where-Object { $_.LastWriteTime -lt $cutoffDate }

# Move old backups to the archive directory
foreach ($backup in $oldBackups) {
    Move-Item -Path $backup.FullName -Destination $archivedir
}
