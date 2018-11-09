# Import the os module, for the os.walk function
import os
import operator
import shutil
 
# Set the directory you want to start from
rootDir = '.'

dirs = {}
level = 0

charToReplace = " "
replaceChar = "_"

#replace dir names
for dirName, subdirList, fileList in os.walk(rootDir):
    
    for sdir in subdirList:
        if sdir.find(" ") >= 0:
            fdir = os.path.join(dirName.replace(charToReplace, replaceChar), sdir)
            dirs[level] = [fdir, fdir.replace(charToReplace, replaceChar)]
            level = level + 1

for dl in dirs:
    shutil.move(dirs[dl][0], dirs[dl][1])
            
# then files
for dirName, subdirList, fileList in os.walk(rootDir):
    for fileName in fileList:
        if fileName.find(" ") >= 0:
            fname = os.path.join(dirName, fileName)
            nname = fname.replace(charToReplace, replaceChar)
            shutil.move(fname, nname)

