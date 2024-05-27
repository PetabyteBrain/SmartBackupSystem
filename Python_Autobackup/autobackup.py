import os
import shutil
import datetime
import subprocess
import platform

def create_backup(copyingfrom, copyingto, backup_title):
    today = datetime.datetime.now().strftime('%d-%m-%Y')
    backup_path = os.path.join(copyingto, f"{backup_title}_{today}")
    log_success_path = os.path.join(copyingto, f"log{today}.txt")
    log_failed_path = os.path.join(copyingto, f"logfailed{today}.txt")
    
    if os.path.exists(copyingfrom):
        shutil.copytree(copyingfrom, backup_path)
        if os.path.exists(backup_path):
            with open(log_success_path, 'a') as log_file:
                log_file.write(f"{today} Successful Transfer -- Backups should be found under {copyingfrom} {backup_path}\n")
        else:
            with open(log_failed_path, 'a') as log_file:
                log_file.write(f"{today} Backup couldn't be Completed, if problem persists go find Server Admin to fix or contact Support.\n")
    else:
        with open(log_failed_path, 'a') as log_file:
            log_file.write(f"{today} Backup couldn't be Completed, if problem persists go find Server Admin to fix or contact Support.\n")

if __name__ == "__main__":
    BackupTitle = "ServerXYZ"
    copyingfrom = "C:\Users\Public\TestingGrounds\TestServer"
    copyingto = "C:\Users\Public\TestingGrounds\Backups"
    archivedir = "C:\Users\Public\TestingGrounds\Archive"
    ExpiryDate = 30

    if platform.system() == "Windows":
        copyingfrom = copyingfrom.replace("/", "\\")
        copyingto = copyingto.replace("/", "\\")
        archivedir = archivedir.replace("/", "\\")

    create_backup(copyingfrom, copyingto, BackupTitle)

    # Run the housekeeping script
    subprocess.run(["python", "housekeeping.py", copyingto, archivedir, str(ExpiryDate)])
