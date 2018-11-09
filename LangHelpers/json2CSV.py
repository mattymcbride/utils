# Import the os module, for the os.walk function
import sys, os, operator, shutil, re
from os.path import basename
import json
import codecs

filename = ''
debug = False
testMode = False
locale = ""

def printStringVal( outfile, parentKey, stringVal ):
    stringVal = stringVal.replace( "\"", "\"\"" )  
    outStr = parentKey + ",\"" + stringVal + "\"\n" 
    outfile.write( outStr )

def readValues( outfile, p, d ) :
    
    for k,v in d.items():
        if isinstance(v, dict):
            p2 = p + "." + k
            readValues( outfile, p2, v )
        else:
            printStringVal( outfile, p, k )

def JSONToCSV( filepath, filename ) :

    input_file  = file(filepath, "r")
    outFileName = filepath + ".csv"
    outfile = codecs.open(outFileName, "w", "utf-8")
    printStringVal( outfile, "Key", "EN_Default")

    j = json.loads(input_file.read().decode("utf-8-sig"))

    for ele in j:
        if isinstance(j[ele], dict):
            readValues( outfile, ele, j[ele] )
        else:
            printStringVal( outfile, ele, j[ele] )

    outfile.close()

if __name__ == "__main__":

    rootDir = "."
    if len(sys.argv) > 1:
        rootDir = sys.argv[1]

    for dirName, subdirList, fileList in os.walk(rootDir):
        for fileName in fileList:
            fullname = os.path.join(dirName, fileName)
            if fileName.endswith('.json'):
                print "Converting " + fullname + "::" + locale
                JSONToCSV( fullname, fileName )









