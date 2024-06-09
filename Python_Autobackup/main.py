import sqlite3
import os
import subprocess
import re
import platform
from tkinter import *
from tkinter import messagebox

# Script Variables
ExpiryDateD = None
ScheduleRepeatH = None
BackupTitleT = None
CopyPathP = None
PastePathP = None
ArchivePathP = None
OperatingSystem = None
ExpiryDateText = ExpiryDateD
regexnum = '^[0-9]+$'
regexletter = '^(?=.*[A-Za-z])[A-Za-z0-9_]+$'
regexdir = '^(?=.*[A-Za-z])[A-Za-z0-9_]+$'
regexlogfiles = '^' + 'log'


#Default Values Settings:
DefaultExpiryDate = 30
DefaultScheduleRepeat = 24
DefaultBackupTitle = 'ServerXYZ'
DefaultCopyPath = 'Default/Server/Path'
DefaultPastePath = 'Default/Server/Path'
DefaultArchivePath = 'Default/Server/Path'

# Font Variable
Titlefont = 'Times New Roman'  # is for Title & smallTitle
SubTitlefont = 'Arial bold'  # is for smallTitle2
ButtonFont = 'Bold'  # is for all Buttons
TextFont = 'Arial bold'  # is for all Content and Texts

# Frame Variables
FrameTitle = 'Smart. B.S.'
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
FrameIcon = os.path.join(script_dir, 'images', 'Icon.ico')
WindowSize = '700x350'

# SQLite Functions //////////////////////////////////////////////////////////////
def create_connection():
    # Define the path to the database file  
    db_directory = 'database'
    db_path = os.path.join(db_directory, 'Backups.db')
    
    # Create the directory if it does not exist
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
    
    # Connect to the database (it will be created if it does not exist)
    conn = sqlite3.connect(db_path)
    return conn

def create_tables(conn):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS backups (
                        backup_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        backup_name TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        status TEXT,
                        size INTEGER,
                        location TEXT,
                        type TEXT
                    )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS files (
                        file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        backup_id INTEGER,
                        file_path TEXT NOT NULL,
                        size INTEGER,
                        checksum TEXT,
                        modified_at DATETIME,
                        FOREIGN KEY (backup_id) REFERENCES backups(backup_id)
                    )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS settings (
                        setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        setting_name TEXT NOT NULL,
                        setting_value TEXT
                    )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS logs (
                        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        backup_id INTEGER,
                        log_message TEXT NOT NULL,
                        log_level TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (backup_id) REFERENCES backups(backup_id)
                    )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS schedules (
                        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        backup_id INTEGER,
                        schedule_time DATETIME NOT NULL,
                        frequency TEXT,
                        FOREIGN KEY (backup_id) REFERENCES backups(backup_id)
                    )''')
        # Recognised OS
        conn.execute('''INSERT INTO settings (setting_name, setting_value)
                        SELECT 'Recognised_OS', 'Unknown_OS'
                        WHERE NOT EXISTS (SELECT 1 FROM settings WHERE setting_name = 'Recognised_OS');''')
        # Expiry Date
        conn.execute('''INSERT INTO settings (setting_name, setting_value)
                        SELECT 'Expiry_Date', '30'
                        WHERE NOT EXISTS (SELECT 1 FROM settings WHERE setting_name = 'Expiry_Date');''')
        # Schedule Repeat
        conn.execute('''INSERT INTO settings (setting_name, setting_value)
                        SELECT 'Schedule_Repeat', '24'
                        WHERE NOT EXISTS (SELECT 1 FROM settings WHERE setting_name = 'Schedule_Repeat');''')
        # BACKUP TITLE
        conn.execute('''INSERT INTO settings (setting_name, setting_value)
                        SELECT 'Backup_Title', 'ServerXYZ'
                        WHERE NOT EXISTS (SELECT 1 FROM settings WHERE setting_name = 'Backup_Title');''')
        # Copying From
        conn.execute('''INSERT INTO settings (setting_name, setting_value)
                        SELECT 'Copying_From', 'Default'
                        WHERE NOT EXISTS (SELECT 1 FROM settings WHERE setting_name = 'Copying_From');''')
        # Copying To
        conn.execute('''INSERT INTO settings (setting_name, setting_value)
                        SELECT 'Copying_To', 'Backup'
                        WHERE NOT EXISTS (SELECT 1 FROM settings WHERE setting_name = 'Copying_To');''')
        # Archive Dir
        conn.execute('''INSERT INTO settings (setting_name, setting_value)
                        SELECT 'Archive_Dir', 'Default'
                        WHERE NOT EXISTS (SELECT 1 FROM settings WHERE setting_name = 'Archive_Dir');''')

# Example function to insert a new backup record
def insert_backup(conn, backup_name, status, size, location, backup_type):
    with conn:
        sql = '''INSERT INTO backups(backup_name, status, size, location, type)
                 VALUES(?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, (backup_name, status, size, location, backup_type))
        return cur.lastrowid

# Take Last settings Values from DB ----------------------------------------------
def fetch_settings(conn):
    global ExpiryDateD, ScheduleRepeatH, BackupTitleT, CopyPathP, PastePathP, ArchivePathP, OperatingSystem
    with conn:
        sql = '''SELECT setting_name, setting_value FROM settings WHERE setting_name IN ('Expiry_Date', 'Schedule_Repeat', 'Backup_Title', 'Copying_From', 'Copying_To', 'Archive_Dir', 'Recognised_OS');'''
        cur = conn.cursor()
        cur.execute(sql)
        settings = cur.fetchall()
        for name, value in settings:
            if name == 'Expiry_Date':
                ExpiryDateD = value
            elif name == 'Schedule_Repeat':
                ScheduleRepeatH = value
            elif name == 'Backup_Title':
                BackupTitleT = value
            elif name == 'Copying_From':
                CopyPathP = value
            elif name == 'Copying_To':
                PastePathP = value
            elif name == 'Archive_Dir':
                ArchivePathP = value
            elif name == 'Recognised_OS':
                OperatingSystem = value
    UpdateDB(conn)
# Update DB values for Folders & Files ------------------------------------------
def UpdateDB(conn):
    os_name = platform.system()
    logfilename = 'log' + regexlogfiles
    if os.path.isfile(regexlogfiles):
        if OperatingSystem == 'Windows':
            os.listdir(PastePathP)
            with conn:
                conn.execute('''INSERT INTO logs (backup_id, log_message, log_level, Timestamp)
                            SELECT 'Archive_Dir', 'Default'
                            WHERE NOT EXISTS (SELECT 1 FROM settings WHERE setting_name = 'Archive_Dir');''')
        
        elif OperatingSystem in ['Linux', 'Darwin']:
            print()
        
        else:
            print()
    if os.path.isdir("data"):
        print()
# Update Settings Values ---------------------------------------------------------
def setOS(conn):
    os_name = platform.system()
    with conn:
        sql = '''UPDATE settings
                SET setting_value = ?
                WHERE setting_name = 'Recognised_OS';'''
        cur = conn.cursor()
        cur.execute(sql, (os_name,))
        return cur.lastrowid
def UpdateSettings_ExpiryDate(conn, ExpiryDateD):
    with conn:
        sql = '''UPDATE settings
                SET setting_value = ?
                WHERE setting_name = 'Expiry_Date';'''
        cur = conn.cursor()
        cur.execute(sql, (ExpiryDateD,))
        return cur.lastrowid
    
def UpdateSettings_ScheduleRepeat(conn, ScheduleRepeatH):
    with conn:
        sql = '''UPDATE settings
                SET setting_value = ?
                WHERE setting_name = 'Schedule_Repeat';'''
        cur = conn.cursor()
        cur.execute(sql, (ScheduleRepeatH,))
        return cur.lastrowid

def UpdateSettings_BackupTitle(conn, BackupTitleT):
    with conn:
        sql = '''UPDATE settings
                SET setting_value = ?
                WHERE setting_name = 'Backup_Title';'''
        cur = conn.cursor()
        cur.execute(sql, (BackupTitleT,))
        return cur.lastrowid

def UpdateSettings_CopyingFrom(conn, CopyPathP):
    with conn:
        sql = '''UPDATE settings
                SET setting_value = ?
                WHERE setting_name = 'Copying_From';'''
        cur = conn.cursor()
        cur.execute(sql, (CopyPathP,))
        return cur.lastrowid

def UpdateSettings_CopyingTo(conn, PastePathP):
    with conn:
        sql = '''UPDATE settings
                SET setting_value = ?
                WHERE setting_name = 'Copying_To';'''
        cur = conn.cursor()
        cur.execute(sql, (PastePathP,))
        return cur.lastrowid

def UpdateSettings_ArchiveDir(conn, ArchivePathP):
    with conn:
        sql = '''UPDATE settings
                SET setting_value = ?
                WHERE setting_name = 'Archive_Dir';'''
        cur = conn.cursor()
        cur.execute(sql, (ArchivePathP,))
        return cur.lastrowid
# Button Fuctions -----------------------------------------------------------------
def CreateBackup():
    fetch_settings(conn)
    global ExpiryDateD, ScheduleRepeatH, BackupTitleT, CopyPathP, PastePathP, ArchivePathP, OperatingSystem
    if OperatingSystem == 'Windows':
        # Paths to the PowerShell scripts
        backup_script = 'Python_Autobackup/winautobackup.ps1'
        
        # Run the PowerShell scripts
        backup_result = subprocess.run(
            [
                'powershell', 
                '-ExecutionPolicy', 'Bypass', 
                '-File', backup_script, 
                '-BackupTitle', BackupTitleT, 
                '-CopyPath', CopyPathP, 
                '-PastePath', PastePathP, 
                '-ArchivePath', ArchivePathP, 
                '-ExpiryDate', str(ExpiryDateD)
            ], 
            shell=True
        )        
        print(backup_result)
        return "Running on Windows"
    
    elif OperatingSystem in ['Linux', 'Darwin']:  # Linux and macOS
        # Path to the Bash script
        script_path = 'Python_Autobackup/autobackup.sh'
        
        # Run the Bash script
        result = subprocess.run(['bash', script_path])
        
        print(result)
        return f"Running on {OperatingSystem}"
    
    else:
        print(OperatingSystem)
        return f"Running on {OperatingSystem}"
    
def CheckArchive():
    fetch_settings(conn)
    global ExpiryDateD, ScheduleRepeatH, BackupTitleT, CopyPathP, PastePathP, ArchivePathP, OperatingSystem
    if OperatingSystem == 'Windows':
        # Paths to the PowerShell scripts
        archive_script = 'Python_Autobackup/winhousekeeping.ps1'
        
        # Run the PowerShell scripts
        archive_result = subprocess.run(
            [
                'powershell', 
                '-ExecutionPolicy', 'Bypass', 
                '-File', archive_script, 
                '-copyingto', PastePathP, 
                '-archivedir', ArchivePathP, 
                '-ExpiryDate', ExpiryDateD
            ], 
            shell=True
        )        
        print(archive_result)
        return "Running on Windows"
    
    elif OperatingSystem in ['Linux', 'Darwin']:  # Linux and macOS
        # Path to the Bash script
        script_path = 'Python_Autobackup/housekeeping.sh'
        
        # Run the Bash script
        result = subprocess.run(['bash', script_path])
        
        print(result)
        return f"Running on {OperatingSystem}"
    
    else:
        print(OperatingSystem)
        return f"Running on {OperatingSystem}"
        

def NewSettingValues():
    # Expiry Date Values # or ExpiryDateD == "0" 
    ExpiryDateD = entry_widget1.get()
    if entry_widget1.get() == None or ExpiryDateD == "" or ExpiryDateD == " " or not (re.search(regexnum, ExpiryDateD)):
        ExpiryDateD = DefaultExpiryDate
    else:
        ExpiryDateD = entry_widget1.get()
        text3.config(text=ExpiryDateD)
        UpdateSettings_ExpiryDate(conn, ExpiryDateD)
    # Schedule Repeat Date Values
    ScheduleRepeatH = entry_widget2.get()
    if entry_widget2.get() == None or ScheduleRepeatH == "0" or ScheduleRepeatH == "" or ScheduleRepeatH == " " or not (re.search(regexnum, ScheduleRepeatH)):
        ScheduleRepeatH = DefaultScheduleRepeat
    else:
        ScheduleRepeatH = entry_widget2.get()
        text5.config(text=ScheduleRepeatH)
        UpdateSettings_ScheduleRepeat(conn, ScheduleRepeatH)
    # Backup Title Values
    BackupTitleT = entry_widget3.get()
    if entry_widget3.get() == None or BackupTitleT == "0" or BackupTitleT == "" or BackupTitleT == " " or not (re.search(regexletter, BackupTitleT)):
        BackupTitleT = DefaultBackupTitle
    else:
        BackupTitleT = entry_widget3.get()
        text7.config(text=BackupTitleT)
        UpdateSettings_BackupTitle(conn, BackupTitleT)
    # Copying From Values
    CopyPathP = entry_widget4.get()
    if entry_widget4.get() == None or CopyPathP == "0" or CopyPathP == "" or CopyPathP == " " or not (re.search(regexdir, CopyPathP)):
        CopyPathP = DefaultCopyPath
    else:
        CopyPathP = entry_widget4.get()
        text9.config(text=CopyPathP)
        UpdateSettings_CopyingFrom(conn, CopyPathP)
    # Copying To Values
    PastePathP = entry_widget5.get()
    if entry_widget5.get() == None or PastePathP == "0" or PastePathP == "" or PastePathP == " " or not (re.search(regexdir, PastePathP)):
        PastePathP = DefaultPastePath
    else:
        PastePathP = entry_widget5.get()
        text11.config(text=PastePathP)
        UpdateSettings_CopyingTo(conn, PastePathP)
    # Archive Values
    ArchivePathP = entry_widget6.get()
    if entry_widget6.get() == None or ArchivePathP == "0" or ArchivePathP == "" or ArchivePathP == " " or not (re.search(regexdir, ArchivePathP)):
        ArchivePathP = DefaultArchivePath
    else:
        ArchivePathP = entry_widget6.get()
        text13.config(text=ArchivePathP)
        UpdateSettings_ArchiveDir(conn, ArchivePathP)
    messagebox.showinfo('Saving',  
                        "Settings saved successfully!") 
    entry_widget1.delete(0, END) 
    entry_widget2.delete(0, END)
    entry_widget3.delete(0, END)
    entry_widget4.delete(0, END)
    entry_widget5.delete(0, END)
    entry_widget6.delete(0, END)


# Tkinter Functions //////////////////////////////////////////////////////////////
def CheckArchive_Options():
    home_frame.pack_forget()
    screen1_frame.pack(fill='both', expand=True)

def CreateBackup_Options():
    home_frame.pack_forget()
    screen2_frame.pack(fill='both', expand=True)

def EditBackup_Options():
    home_frame.pack_forget()
    screen3_frame.pack(fill='both', expand=True)

def RetrieveBackup_Options():
    home_frame.pack_forget()
    screen4_frame.pack(fill='both', expand=True)

def ViewerBackup_Options():
    home_frame.pack_forget()
    screen5_frame.pack(fill='both', expand=True)

def Settings_Options():
    home_frame.pack_forget()
    screen6_frame.pack(fill='both', expand=True)

def Update_Options():
    text3.config(text=ExpiryDateD)
    text5.config(text=ScheduleRepeatH)

def Settings_ButtonPress():
    fetch_settings(conn)
    Update_Options()
    Settings_Options()
# Main Window
win = Tk()
win.resizable(width=False, height=False)
win.title(FrameTitle)
win.iconbitmap(FrameIcon)
win.geometry(WindowSize)

conn = create_connection()
create_tables(conn)
setOS(conn)
fetch_settings(conn)

# Home Screen Frame ---------------------------------------------------------------------
home_frame = Frame(win)
home_frame.pack(fill='both', expand=True)

smallTitle = Label(home_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(home_frame, text="Home", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)

CleanupBackup_Button = Button(home_frame, text="Check date for Archive", font=('bold', 10), command=CheckArchive_Options)
CleanupBackup_Button.place(x=400, y=100)
NewBackup_Button = Button(home_frame, text="Create New Backup", font=('bold', 10), command=CreateBackup_Options)
NewBackup_Button.place(x=400, y=130)
Editor_Button = Button(home_frame, text="Edit Backups", font=(ButtonFont, 10), command=EditBackup_Options)
Editor_Button.place(x=400, y=160)
RetrieveBackup_Button = Button(home_frame, text="Retrieve Backup", font=(ButtonFont, 10), command=RetrieveBackup_Options)
RetrieveBackup_Button.place(x=400, y=190)
ViewerBackup_Button = Button(home_frame, text="View Backups", font=(ButtonFont, 10), command=ViewerBackup_Options)
ViewerBackup_Button.place(x=400, y=220)
Quit = Button(home_frame, text="Quit", font=(ButtonFont, 10), command=win.quit)
Quit.place(x=400, y=250)
SettingsBackup_Button = Button(home_frame, text="Settings", font=(ButtonFont, 10), command=Settings_ButtonPress)
SettingsBackup_Button.place(x=440, y=250)

# Screen 1 Frame --------------------------------------------------------------------- Check Archive
screen1_frame = Frame(win)

smallTitle = Label(screen1_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(screen1_frame, text="Check Archive", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)

CheckArchive_button = Button(screen1_frame, text="Check Dates for Archive", font=(ButtonFont, 10), command=CheckArchive)
CheckArchive_button.place(x=400, y=200)

back_button = Button(screen1_frame, text="Back to Home", font=(ButtonFont, 10), command=lambda: (screen1_frame.pack_forget(), home_frame.pack(fill='both', expand=True)))
back_button.place(x=400, y=280)

screen1_frame.pack_forget()

# Screen 2 Frame --------------------------------------------------------------------- Create new Backup
screen2_frame = Frame(win)

smallTitle = Label(screen2_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(screen2_frame, text="Create new Backup", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)

PlanBackup_button = Button(screen2_frame, text="PlanBackup", font=(ButtonFont, 10), command=CreateBackup)
PlanBackup_button.place(x=400, y=200)
create_button = Button(screen2_frame, text="New Backup", font=(ButtonFont, 10), command=CreateBackup)
create_button.place(x=400, y=240)
back_button = Button(screen2_frame, text="Back to Home", font=(ButtonFont, 10), command=lambda: (screen2_frame.pack_forget(), home_frame.pack(fill='both', expand=True)))
back_button.place(x=400, y=280)

screen2_frame.pack_forget()

# Screen 3 Frame --------------------------------------------------------------------- Edit Backups
screen3_frame = Frame(win)

smallTitle = Label(screen3_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(screen3_frame, text="Edit Backup", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)

back_button = Button(screen3_frame, text="Back to Home", font=(ButtonFont, 10), command=lambda: (screen3_frame.pack_forget(), home_frame.pack(fill='both', expand=True)))
back_button.place(x=400, y=280)

screen3_frame.pack_forget()

# Screen 4 Frame --------------------------------------------------------------------- Retrieve Backups
screen4_frame = Frame(win)

smallTitle = Label(screen4_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(screen4_frame, text="Retrieve Backups", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)

back_button = Button(screen4_frame, text="Back to Home", font=(ButtonFont, 10), command=lambda: (screen4_frame.pack_forget(), home_frame.pack(fill='both', expand=True)))
back_button.place(x=400, y=280)

screen4_frame.pack_forget()

# Screen 5 Frame --------------------------------------------------------------------- Viewer Backups
screen5_frame = Frame(win)

smallTitle = Label(screen5_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(screen5_frame, text="View Backups", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)

back_button = Button(screen5_frame, text="Back to Home", font=(ButtonFont, 10), command=lambda: (screen5_frame.pack_forget(), home_frame.pack(fill='both', expand=True)))
back_button.place(x=400, y=280)

screen5_frame.pack_forget()

# Screen 6 Frame --------------------------------------------------------------------- Settings
screen6_frame = Frame(win)

smallTitle = Label(screen6_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(screen6_frame, text="Settings", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)
# Expiry Date
text2 = Label(screen6_frame, text="Expiry Date:", font=(SubTitlefont, 10))
text2.place(x=80, y=70)
text3 = Label(screen6_frame, text=ExpiryDateD, font=(SubTitlefont, 10))
text3.place(x=190, y=70)
# Schedule Repeat
text4 = Label(screen6_frame, text="Schedule Repeat:", font=(SubTitlefont, 10))
text4.place(x=80, y=100)
text5 = Label(screen6_frame, text=ScheduleRepeatH, font=(SubTitlefont, 10))
text5.place(x=190, y=100)
# Backup Title
text6 = Label(screen6_frame, text="Backup Title:", font=(SubTitlefont, 10))
text6.place(x=80, y=130)
text7 = Label(screen6_frame, text=BackupTitleT, font=(SubTitlefont, 10))
text7.place(x=190, y=130)
# Copying from
text8 = Label(screen6_frame, text="Copying from:", font=(SubTitlefont, 10))
text8.place(x=80, y=160)
text9 = Label(screen6_frame, text=CopyPathP, font=(SubTitlefont, 10))
text9.place(x=190, y=160)
# Copying to
text10 = Label(screen6_frame, text="Copying to:", font=(SubTitlefont, 10))
text10.place(x=80, y=190)
text11 = Label(screen6_frame, text=PastePathP, font=(SubTitlefont, 10))
text11.place(x=190, y=190)
# Archive Directory
text12 = Label(screen6_frame, text="Archive Directory:", font=(SubTitlefont, 10))
text12.place(x=80, y=220)
text13 = Label(screen6_frame, text=ArchivePathP, font=(SubTitlefont, 10))
text13.place(x=190, y=220)
# Recognised OS
text14 = Label(screen6_frame, text="Recognised OS:", font=(SubTitlefont, 10))
text14.place(x=80, y=280)
text15 = Label(screen6_frame, text=OperatingSystem, font=(SubTitlefont, 10))
text15.place(x=190, y=280)
# Input v
canvas_widget = Canvas(screen6_frame, width=200, height=300) 
canvas_widget.place(x=280, y=-40) 
  
# Create and place the label in canvas 
# for user to enter his name 
label_widget1 = Label(screen6_frame, text="Expiry Date (in Days)") 
canvas_widget.create_window(100, 120, window=label_widget1)

label_widget2 = Label(screen6_frame, text="Scheduled Repeat (in Hours)") 
canvas_widget.create_window(100, 150, window=label_widget2) 

label_widget3 = Label(screen6_frame, text="Backup Title (No Spaces)") 
canvas_widget.create_window(100, 180, window=label_widget3)

label_widget4 = Label(screen6_frame, text="copying from (No Spaces)") 
canvas_widget.create_window(100, 210, window=label_widget4) 

label_widget5 = Label(screen6_frame, text="copying to (No Spaces)") 
canvas_widget.create_window(100, 240, window=label_widget5)

label_widget6 = Label(screen6_frame, text="Archive Directory (No Spaces)") 
canvas_widget.create_window(100, 270, window=label_widget6)
# Create an input name on canvas 
# for inputting user name using widget Entry 
entry_widget1 = Entry(screen6_frame) 
canvas_widget.create_window(250, 120, window=entry_widget1) 

entry_widget2 = Entry(screen6_frame) 
canvas_widget.create_window(250, 150, window=entry_widget2) 

entry_widget3 = Entry(screen6_frame) 
canvas_widget.create_window(250, 180, window=entry_widget3)

entry_widget4 = Entry(screen6_frame) 
canvas_widget.create_window(250, 210, window=entry_widget4)

entry_widget5 = Entry(screen6_frame) 
canvas_widget.create_window(250, 240, window=entry_widget5)

entry_widget6 = Entry(screen6_frame) 
canvas_widget.create_window(250, 270, window=entry_widget6)
  
# Creating and placing the button on canvas to submit data 
button_widget = Button(text='Submit', command=NewSettingValues) 
canvas_widget.create_window(220, 300, window=button_widget)

button_widget1 = Button(text='Back to Home', command=lambda: (screen6_frame.pack_forget(), home_frame.pack(fill='both', expand=True))) 
canvas_widget.create_window(140, 300, window=button_widget1)
# Input ^

screen6_frame.pack_forget()

win.mainloop()
