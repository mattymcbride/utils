# Import the os module, for the os.walk function
import sys, os, operator, shutil, re
import xml.etree.ElementTree as ET 
import MySQLdb, json
from os.path import basename

def dbgLog( str ) :
	if debug:
		print str

def updateXliff( fileName, newFileName ):

    tree = ET.parse(fileName)
    root = tree.getroot()
    matches = updateTransUnitsAttr(root)
    
    dbgLog("Updated " + str(matches) + " translation units!" )
    tree.write(newFileName, encoding="utf-8", xml_declaration=True, default_namespace=None, method="xml") 
    return matches

def updateTransUnitsAttr( root ) :

    xpath = ".//{" + xmlns +"}trans-unit" 
    dbgLog("xpath::" + xpath)
    count = 0
    matchingUnits = root.findall(xpath)
   
    for unit in matchingUnits:

        hasSource = False
        text = None

        source = unit.find('{' + xmlns + '}source')
        if source is not None:
            hasSource = True
            text = source.text
            if text is None:
                hasSource = False
        
        # check verbotten words
        if hasSource and not shouldITranslate(text):
            hasSource = False

        if hasSource == False: 
            unit.set('translate', 'no')
            count += 1

    return count

def shouldITranslate(thisText):

    badlangs = [
        ('currency', '^\\$[0-9]+(\\.[0-9]+)*$'),
        ('just numbers', '^[0-9]+$'),
        ('just IP','^[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+$'),
        ('just time','^[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[AMPM].$'),
        ('just single non character','^[^a-zA-Z]$'),
        ('dashes','^[-]+$'),
        ('just weird','ZYXWVUTS'),
        ('placeholders','\${.*}'),
        ('IPv6 sorta','^([0-9]+\\.){3}[0-9],.*([a-fA-F0-9:])+$'),
        ('cents', '.*\xc2.*')
    ]

    for k,v in badlangs:
        m = re.match(v, thisText)
        if m is not None:
            dbgLog("Found instance of class '" + k + "' ==> \"" + thisText + "\"")
            return False
         
    return True
       
# END DEF #

xmlns = 'urn:oasis:names:tc:xliff:document:1.2'
xsi = 'http://www.w3.org/2001/XMLSchema-instance'
debug = False

rootDir = '.'
locale = ""

ET.register_namespace('', xmlns)
ET.register_namespace('xsi', xsi)

if len(sys.argv) > 1:
    rootDir = sys.argv[1]

print "Scanning " + rootDir + " for XLIFF"    

for dirName, subdirList, fileList in os.walk(rootDir):

    for fileName in fileList:

        fullname = os.path.join(dirName, fileName)
        if fileName.endswith('.xliff'):
            c = updateXliff( fullname, fullname )
            print "Updated " + str(c) + " attribute values in :: "+ fullname



    





