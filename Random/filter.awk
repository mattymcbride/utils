BEGIN {
  customer = ""
  hostName = ""
  custNo = 0
  hostNo = 0
  tableRow = 0
  tableName = ""
  inTable = 0
  colNum = 0
  tableCols[colNum] = ""
  fileNames[0] = ""
  tableNames[0] = ""
  fileCount = 0
  curTableNum = 0	
}

/^\([0-9]* row/ {
	tableDone()
}

// {
	if ( inTable == 1 ) {
		n = split( $0, a, "|" )
		outStr =  customer "," hostName 
		for (i=1; i<=n; i++ ) {
			outStr = outStr "," trim(a[i]) 
		}
		print outStr > fileNames[curTableNum]
	}
}

/^[ ]customer_name/ {
  # start of new customer 
  skiplines(2)
  customer = trim($0)
  custNo++ 
  hostNo = 0
  hostName = ""
}

/^[ ]*hostname/ {
  # start of new customer 
  skiplines(2)
  hostName = trim($0)
  hostNo++ 
}

/^[ ]*max_windows_count_5_min/ {
	tableStart("MaxWindow")
}

/^[ ]*windows_source_count/ {
	tableStart("WindowsSource")
}

/^[ ]*syslog_source_count/ {
	tableStart("SyslogSource")
}

/^[ ]*total_alerts/ {
	tableStart("TotalAlerts")
}

/^.*raw_windows_log_count/ {
	tableStart("RawWindowsLog")
}

/^.*triggered_control_count/ {
	tableStart("TriggeredControl")
}

END {

}
## functions ##

function getTable(nameStr) {
	for (i=0; i<fileCount; i++) {
		if ( tableNames[i] == nameStr ) {
			return i
		}
	}
	tableNames[++fileCount] = nameStr
	fileNames[fileCount] = "LS_DATA_" nameStr ".csv"
	columnStr = "customer,sensor"
	for (i=1;i<=colNum;i++) {
		columnStr = columnStr "," trim(tableCols[i])
	}
	print columnStr > fileNames[fileCount]
	return fileCount
}

function tableStart(name) {
	tableName = name
	colNum = split( $0, tableCols, "|" )
	curTableNum = getTable(name)
	tableRow = 0
	inTable = 1
	skiplines(1)
}

function tableDone() {
	if (inTable == 1 ) {
	 	tableName = ""
	 	tableRow = 0
	 	colNum = 0
		inTable = 0
		curTableNum = 0
	}
}

function skiplines(numLine) {
   while( numLine-- > 0) {
     if ((getline) == 0) {
          print "Error: EOF"
          tableDone()
          exit
     }
   }
}

function trim(str) {
	gsub(/^[ ]*/, "", str);
	gsub(/[ ]*$/, "", str);
	return str
}