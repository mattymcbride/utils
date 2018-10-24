# JSON to CSV python
import json
import sys, os, operator, shutil, re
from os.path import basename
from datetime import datetime
import time

import csv

filename = ''
debug = False
testMode = True

def getTimeInSeconds(strTimeExpr):
	utc_time = datetime.strptime(strTimeExpr,
                             "%Y-%m-%dT%H:%M:%S.%fZ")
	return time.mktime(utc_time.timetuple())

def makeJSON2CSV( filepath, filename ) :

	input_file  = file(filepath, "r")
	j = json.loads(input_file.read().decode("utf-8-sig"))

	resultCount = 0
    
	try:
		results = j['results']
	except KeyError:
		print "Error: " + filename + " does not contain results[]"
		return

	with open(filename+'.process.csv', 'wb') as csvfile1:
		reportwriter = csv.writer(csvfile1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

		for result in results:
	
			if ( result['alert_type'] != "watchlist.hit.ingress.process" ):
				continue

			ioc_json = json.loads(result['ioc_value'])
			result['search_query'] = ioc_json['search_query']
			result['ioc_value'] = None

			result['resolved_time_sec'] = 0
			result['created_time_sec'] = 0

			# fill fields that may not exist in all 

			# make dates seconds
			try:
				result['resolved_time_sec'] = getTimeInSeconds(result['resolved_time'])
			except:
				result['resolved_time'] = ""
			
			try:
				result['created_time_sec'] = getTimeInSeconds(result['created_time'])
			except:
				result['created_time'] = ""
			
	

			if ( resultCount == 0 ):
				reportwriter.writerow(list(result.keys()))
			
			reportwriter.writerow(list(result.values()))

			resultCount = resultCount + 1

	resultCount = 0

	try:
		results = j['results']
	except KeyError:
		print "Error: " + filename + " does not contain results[]"
		return

	with open(filename+'.binary.csv', 'wb') as csvfile2:
		reportwriter = csv.writer(csvfile2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

		for result in results:
	
			
			if ( result['alert_type'] != "watchlist.hit.ingress.binary" ):
				continue
			
			ioc_json = json.loads(result['ioc_value'])
			result['search_query'] = ioc_json['search_query']
			result['ioc_value'] = None

			# make dates seconds
			result['resolved_time_sec'] = getTimeInSeconds(result['resolved_time'])
			result['created_time_sec'] = getTimeInSeconds(result['created_time'])
			
			if ( resultCount == 0 ):
				reportwriter.writerow(list(result.keys()))
			
			reportwriter.writerow(list(result.values()))

			resultCount = resultCount + 1

def main():
	rootDir = '.'

	if len(sys.argv) > 1:
		rootDir = sys.argv[1]

	for dirName, subdirList, fileList in os.walk(rootDir):
		for fileName in fileList:
			fullname = os.path.join(dirName, fileName)

			if fileName.endswith('.json'):
				print "Reading " + fullname
				makeJSON2CSV( fullname, fileName )


if __name__ == "__main__":
    main()


