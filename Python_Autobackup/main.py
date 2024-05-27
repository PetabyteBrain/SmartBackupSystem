import sqlite3
import os
from tkinter import *
from tkinter import messagebox

# Font Variable
Titlefont = 'Times New Roman'  # is for Title & smallTitle
SubTitlefont = 'Arial bold'  # is for smallTitle2
ButtonFont = 'Bold'  # is for all Buttons
TextFont = 'Arial bold'  # is for all Content and Texts

# Frame Variables
FrameTitle = 'Smart. B.S.'
FrameIcon = 'images/Icon.ico'
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

# Example function to insert a new backup record
def insert_backup(conn, backup_name, status, size, location, backup_type):
    with conn:
        sql = '''INSERT INTO backups(backup_name, status, size, location, type)
                 VALUES(?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, (backup_name, status, size, location, backup_type))
        return cur.lastrowid

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

# Main Window
win = Tk()
win.resizable(width=False, height=False)
win.title(FrameTitle)
win.iconbitmap(FrameIcon)
win.geometry(WindowSize)

conn = create_connection()
create_tables(conn)

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
SettingsBackup_Button = Button(home_frame, text="Settings", font=(ButtonFont, 10), command=Settings_Options)
SettingsBackup_Button.place(x=440, y=250)

# Screen 1 Frame --------------------------------------------------------------------- Check Archive
screen1_frame = Frame(win)

smallTitle = Label(screen1_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(screen1_frame, text="Check Archive", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)

# Example Button to go back to Home Screen
back_button = Button(screen1_frame, text="Back to Home", font=(ButtonFont, 10), command=lambda: (screen1_frame.pack_forget(), home_frame.pack(fill='both', expand=True)))
back_button.place(x=400, y=280)

screen1_frame.pack_forget()

# Screen 2 Frame --------------------------------------------------------------------- Create new Backup
screen2_frame = Frame(win)

smallTitle = Label(screen2_frame, text="Smart. Backup. System.", font=(Titlefont, 15))
smallTitle.place(x=10, y=0)
smallTitle2 = Label(screen2_frame, text="Create new Backup", font=(SubTitlefont, 15))
smallTitle2.place(x=50, y=40)

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

back_button = Button(screen6_frame, text="Back to Home", font=(ButtonFont, 10), command=lambda: (screen6_frame.pack_forget(), home_frame.pack(fill='both', expand=True)))
back_button.place(x=400, y=280)

screen6_frame.pack_forget()

win.mainloop()
