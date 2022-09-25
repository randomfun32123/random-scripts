import os
import sys
import mutagen
import subprocess
from mutagen.easyid3 import EasyID3

path = "/home/{YOUR USERNAME HERE}/Music/"

noDownload = False
if sys.argv[1] == "-n":
    noDownload = True
url = sys.argv[1]

artist = input("What Artist? ")
album = input("What Album? ")

if not os.path.exists(str(path + artist)):
    os.mkdir(str(path + artist))
newPath = str(path + artist + "/")

try:
    os.mkdir(str(newPath + album + "/"))
except:
    pass
newPath = str(newPath + album + "/")

if not noDownload:
    subprocess.call('youtube-dl -ciw --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" {url}'.format(url = url), shell = True, cwd = str(newPath))

fileList = []
for item in os.scandir(newPath):
    if item.is_file():
        fileList.append(newPath + str(item).replace("<DirEntry '", '').replace("'>", '').replace('<DirEntry "', '').replace('">', ''))
        print(str(item).replace("<DirEntry '", '').replace("'>", '').replace('<DirEntry "', '').replace('">', ''))


for i in range(0, len(fileList)):
    item = fileList[i]
    songName = fileList[i].split("/")[-1]
    songName = str(songName).replace(".mp3", '')

    if item.split(".")[-1] == "jpg" or item.split(".")[-1] == "png":
        continue

    # for i2 in range(-1, -1 * len(songNameTmp.split("-")), -1):
    #     if i2 >= -2:
    #         pass
    #     else:
    #         songName += songNameTmp.split("-")[i]


    file = EasyID3(item)
    file['title'] = songName
    file['artist'] = artist
    file['album'] = album
    file['tracknumber'] = str(i + 1)
    file.pprint()
    file.save()

    print("Metadata for", songName, "complete:", songName, "on", album, "track number", i + 1)
