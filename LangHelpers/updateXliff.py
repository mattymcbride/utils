# Import the os module, for the os.walk function
import sys, os, operator, shutil, re
import xml.etree.ElementTree as ET 
import MySQLdb, json
from os.path import basename

# DB Connection Info
debug = True

def dbgLog( str ) :
	if debug:
		print str

def updateXliffElement( root, id, newValue ) :

    xpath = ".//{" + xmlns +"}trans-unit/[@id='" + id + "']" 
    dbgLog("xpath::" + xpath)
    count = 0
    matchingUnits = root.findall(xpath)
    for unit in matchingUnits:
    	target = unit.find('{' + xmlns + '}target')
        if target is None:
        	dbgLog("No matching XML element")
        	continue
        print target	
        # update 
        oldText = target.text
        target.text = newTerm
        dbgLog("Upated '" + oldText + "' --> '" + newTerm + "'")
        count += 1

    return count
       
######  END DEF ###########################

# HACK THIS SHOULD COME FROM the XML DOC
xmlns = 'urn:oasis:names:tc:xliff:document:1.2'

# TODO
# 1 - make this a library
# 2 - pass in lists of values or a large dictionary
# 3 - write an app that reads from a DB table to update
# 4 - failure and logging
# 5 - external configuration for DB, files, settings

# test data
fileName = 'sample.xliff'
id = '8Ix-Z6-Cb2.text'
newTerm = 'Stato'
newFileName = 'newsample.xliff'

ET.register_namespace('', "urn:oasis:names:tc:xliff:document:1.2")
ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

if fileName.endswith('.xliff'):
    print "Importing " + fileName 

    tree = ET.parse(fileName)
    root = tree.getroot()
    matches = updateXliffElement(root, id, newTerm)
    
    dbgLog("Upated " + str(matches) + " translation units!" )
       
    tree.write(newFileName, encoding="utf-8", xml_declaration=True, default_namespace=None, method="xml") 
    dbgLog("Wrote " + newFileName)






