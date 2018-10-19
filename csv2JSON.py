import json, csv
import sys, os
import os, time

def convertCSVToJSON(fileName, includeAllScans):
	
	outFileName = fileName.lower().replace("csv","json")

	(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fileName)
	timestamp = time.ctime(mtime)

	header=True
	rows = 0

	fields = []

	with open(fileName) as csvfile:
		with open(outFileName, 'w') as outfile:  
			fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in fileReader:
				rows = rows + 1
				if (header):
					for col in row:
						fields.append(col)
					header=False
				else:
					logLine = { 'timestamp': timestamp }
					colNum = 0
					
					try: 
						for col in row:
							logLine[fields[colNum]] = col
							colNum = colNum + 1
					except IndexError:
						print "#ERROR : Invalid CSV Line at row", rows, "ignoring record."

		 			outfile.write('%s\n' % logLine)

	print "Converted", rows, "rows from CSV to JSON."
					 				
def main(rootDir, includeAllScans):

	for dirName, subdirList, fileList in os.walk(rootDir):
		for fileName in fileList:
			if fileName.lower().endswith('.csv'):
				print "Converting " + fileName + " to JSON"
				convertCSVToJSON(fileName, includeAllScans) 

if __name__ == "__main__":

	rootDir = '.'
	if len(sys.argv) > 1:
	    rootDir = sys.argv[1]

	print "Scanning " + rootDir + " for CSV files"   
	main(rootDir, True)