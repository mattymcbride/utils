import json, xml.etree.ElementTree as ET
import sys, os

def convertNessusToJSON(fileName, includeAllScans):
	
	tree = ET.parse(fileName)
	root = tree.getroot()

	outFileName = fileName.lower().replace("nessus","json")

	with open(outFileName, 'w') as outfile:  

		for reportHost in root.iter('ReportHost'):	

			host_ip = ''
			scan_end = ''

			hostProperties = reportHost.find('HostProperties')
			hostData = {}

			for tag in hostProperties.iter('tag'):
				hostData[tag.get('name')] = tag.text

				if (tag.get('name') == 'host-ip'):
					host_ip = tag.text
				elif (tag.get('name') == 'HOST_END'):
					scan_end = tag.text

			for reportItem in reportHost.iter('ReportItem'):		
				if (includeAllScans or reportItem.get('severity') <> '0'):

					# rewrite these
					reportData = {'src_ip': host_ip}
					reportData['timestamp'] = scan_end

					reportData.update(hostData)

					for item in reportItem.attrib:
						
						reportData[item] = reportItem.get(item)

						for reportDetails in reportItem.iter():
							reportData[reportDetails.tag] = reportDetails.text

					outfile.write('%s\n' % reportData)

def main(rootDir, includeAllScans):

	for dirName, subdirList, fileList in os.walk(rootDir):
		for fileName in fileList:
			if fileName.lower().endswith('.nessus'):
				print "Converting " + fileName + " to JSON"
				convertNessusToJSON(fileName, includeAllScans) 

if __name__ == "__main__":

	rootDir = '.'
	if len(sys.argv) > 1:
	    rootDir = sys.argv[1]

	print "Scanning " + rootDir + " for Nessus files"   
	main(rootDir, True)

