# -*- coding: utf-8 -*-
import sys, os, operator, shutil, re, io
from os.path import basename
import csv
import codecs, json
    
filename = ''
debug = False
testMode = False
locale = ""
logfile = None
ignoreExisting = False

# read the entire JSON, then read the CSV and update JSON where it's required

def logLine( message, row ):
    outStr = str(row) + ":" + message + "\n" 
    if (logfile is not None):
        logfile.write( outStr )
    else:
        print(outStr)

def updateTerm( j, key, value, newvalue, row ) :

    if (value == newvalue):
        logLine( "WARNING: " + key + " VALUE: \"" + value +"\" SAME AS SOURCE", row)
        return 

    # key could be dotted path
    # admin-registry.completeRegistryStepsFirst
    keys = key.split(".")
    ele = j
    for k in keys:
        ele = ele[k]

    for k,v in ele.items():
        if (k == value):

            if (ele[k] == newvalue and ignoreExisting ):
                logLine( "WARNING: " + key + " VALUE: \"" + value +"\" ALREADY TRANSLATED, MATCHES SOURCE", row)
                return
            
            ele[k] = unicode(newvalue, "utf-8", errors="ignore") 
            logLine( "UPDATE: " + key + " FROM: \"" + value +"\" TO: \"" + newvalue + "\"", row)
            return 

    logLine( "ERROR: Key " + key + "not in JSON", row)

def updateJSONFromCSV( jsonFileName, csvFileName ) :

    # read the JSON file entirely
    file_json  = file(jsonFileName, "r")
    j = json.loads(file_json.read().decode("utf-8-sig"))
    
    with open(csvFileName)  as csvfile:
        row_num = 1
        reader = csv.DictReader(csvfile)
        for row in reader:
            jsonKey = updateTerm(j, row['Key'], row['Original'], row['Modified'],row_num)
            row_num += 1
 
    # write the JSON back
    outfile = codecs.open(jsonFileName + ".updated.json", "w", "utf-8")
    json.dump(j, outfile, sort_keys = True, indent = 4, ensure_ascii = False, encoding="utf-8")
    outfile.close()


if __name__ == "__main__":

    rootDir = "."
    usage = "USAGE: updateJSON.py JSON_FILE_NAME CSV_FILE_NAME"
    if len(sys.argv) < 2:
        print usage
        exit()
    
    # could have just checked which ones have which extensions but meh ...
    jsonFileName = sys.argv[1]
    csvFileName = sys.argv[2]
    
    updateJSONFromCSV( jsonFileName, csvFileName )









