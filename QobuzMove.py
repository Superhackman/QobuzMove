# Import moduels
import os, sys, time, shutil, questionary, getpass
from pathlib import Path
from configparser import ConfigParser


# Define variables

# ConfigParser
parser = ConfigParser()
parser.read("config.ini")
config = parser["CONFIG"]
path = parser.get("CONFIG", "path")
setup = parser.get("CONFIG", "setup")

# "FORMAT (Bit depth, bitrate)" folder names
f_24_96 = "FLAC (24bit-96kHz)"
f_24_44 = "FLAC (24bit-44.1kHz)"
f_16_44 = "FLAC (16bit-44.1kHz)"
mp3 = "MP3"

# Misc
z = None
roaming = "C:/Users/" + getpass.getuser() + "/AppData/Roaming"


# Function to filter out files from os.listdir and return the resulting list of folders into a list
def getdirs():
    q = os.listdir(".")
    global z
    z = []
    for i in q:
        if os.path.isfile(i) == False:
            z.insert(0, i) # Returns list of folders in cwd into z array 
        else:
            continue # Skip to next item if current item is a file


# Create config.ini file
os.chdir(roaming) # Change directory to the current users roaming folder
if os.path.isdir("QobuzMove") == False:
    os.mkdir("QobuzMove") # If there is no QobuzMove directory already in roaming folder then create one
    os.chdir("QobuzMove")
else:
    os.chdir("QobuzMove")
if os.path.isfile("config.ini") == False:
    parser["CONFIG"] = {
        "path": "null",
        "setup": "1"
    } # If config.ini file dosen't exist inside QobuzMove directory then create one with default values
    with open("config.ini", "w") as conf:
        parser.write(conf)
else:
    pass


# Check if Qobuz downloader path has already been set in config and if not ask user to set it
notvalid = True
while notvalid:
    if setup == "1":
        QobuzPath = input("Enter the Qobuz donwloader path: ")
        if os.path.isdir(QobuzPath) == False:
            print("Path dosent exist, try agien") # Loop until user enters a valid path for QobuzDownloader
        else:
            config["path"] = QobuzPath
            config["setup"] = "0"
            with open("config.ini", "w") as conf:
                parser.write(conf) # When user enters a valid path for QobuzDownloader write it to config
            notvalid=False
            path = parser.get("CONFIG", "path")
            os.chdir(path)
    elif setup == "0":
        if os.path.isdir(path) == False:
            notvalid = True
            while notvalid:
                QobuzPath = input("Qobuz path no longer exists, please enter it agien: ")
                if os.path.isdir(QobuzPath) == False: # Check if the path in config is still valid
                    print("Path dosent exist, try agien") # If it isn't then loop until the user enters a new valid path
                else:
                    config["path"] = QobuzPath
                    config["setup"] = "0"
                    with open("config.ini", "w") as conf:
                        parser.write(conf)
                    notvalid=False
                    path = parser.get("CONFIG", "path")
                    os.chdir(path)
        else:
            QobuzPath = path
            config["path"] = QobuzPath
            config["setup"] = "0"
            with open("config.ini", "w") as conf:
                parser.write(conf)
            notvalid=False
            path = parser.get("CONFIG", "path")
            os.chdir(path)
    else:
        QobuzPath = path
        os.chdir(path)
        notvalid=False


# Get artist and album from user using questionary prompt
getdirs() # Call getdirs function
artist = questionary.select("Choose an artist: ", choices=z).ask(input) # Use z array from getdirs function to give a choice of folders
os.chdir(artist)

getdirs()
album = questionary.select("Choose an album: ", choices=z).ask(input)
os.chdir(album)


# Check if folder name variables defined earlier exist in album folder
if os.path.exists(f_24_96):
    correctdir = f_24_96 # When the correct directory name is found mark it for later using correctdir variable
elif os.path.exists(f_24_44):
    correctdir = f_24_44
elif os.path.exists(f_16_44):
    correctdir = f_16_44
elif os.path.exists(mp3):
    correctdir = mp3
else:
    print("Cannot find any music :( Exiting...")
    time.sleep(2.3)
    sys.exit() # If none of these folders can be found the program will exit.
               # If this happens it means either that the tool has already been run on this album or that it dosen't actually contain any QobuzDownloader music


# Delete artwork
os.chdir(correctdir)
if os.path.exists("Cover.jpg"):
    os.remove("Cover.jpg") # If album cover exists delete it.
else: print("Cannot remove artwork as none exists, continuing") # If it dosen't exist print a message and move on.


# Remove "FORMAT (Bit depth, bitrate)" folder
os.chdir("..") # Go back into album directory
albumdir = os.getcwd() + "/" + correctdir # Set albumdir to the current dir path + the name of the correctdir
os.chdir("..") # Go back into artist directory
movedir = os.getcwd() + "/" + correctdir # Set movedir to the current dir path + the name of the correctdir
shutil.move(albumdir, movedir) # Move the bitrate folder to the artist folder
os.rmdir(album) # Delete the album folder
os.rename(correctdir, album) # Rename the bitrate folder to the name of the album
print("Done!")
# I just wanted line 144 ヾ(•ω•`)o