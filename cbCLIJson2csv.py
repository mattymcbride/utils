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

	with open(filename+'.process.csv', 'wb') as csvfile1:
		reportwriter = csv.writer(csvfile1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

		for serverBlock in j:

			result = dict()

			try:

				server = serverBlock[0]

				result['current_sensor_count'] = server['current_sensor_count']
				result['is_license_valid'] = server['is_license_valid']
				result['license_end_date'] = server['license_end_date']
				result['licensed_sensors'] = server['licensed_sensors']
			
				result['server_url'] = serverBlock[1]
				result['server_url'] = re.sub('/api/concurrent_license_info.*$', '', result['server_url'])

				if ( resultCount == 0 ):
					reportwriter.writerow(list(result.keys()))
				reportwriter.writerow(list(result.values()))

				resultCount = resultCount + 1

			except:
				print "ERROR >>>"
				print	serverBlock



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


