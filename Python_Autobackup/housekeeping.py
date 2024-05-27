import os
import sys
import shutil
from datetime import datetime, timedelta

def move_old_backups(copyingto, archivedir, expiry_days):
    expiry_date = datetime.now() - timedelta(days=expiry_days)
    for root, dirs, files in os.walk(copyingto):
        for name in dirs + files:
            path = os.path.join(root, name)
            if os.path.getmtime(path) < expiry_date.timestamp() and 'Backups' not in path:
                shutil.move(path, os.path.join(archivedir, os.path.basename(path)))

if __name__ == "__main__":
    copyingto = sys.argv[1]
    archivedir = sys.argv[2]
    expiry_days = int(sys.argv[3])
    move_old_backups(copyingto, archivedir, expiry_days)
