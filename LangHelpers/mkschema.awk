BEGIN {
  FS = ","
  type["int"] = "INTEGER"
  type["str"] = "STRING"
  type["float"] = "FLOAT"
  type["date"] = "DATETIME"
  empty = ""
  lines = 0
  includeDates = false
}

END {
	printf "\n"
}

/datetime/ {
  if (includeDates) {
    printBlock( type["date"], $1 )
  }
}

/int\(/ {
  printBlock( type["int"], $1 )
}

/float\(/ {
  printBlock( type["float"], $1 )
}

/char/ {
  printBlock( type["str"], $1 )
}

/mediumtext/ {
  printBlock( type["str"], $1 )
}

/blob/ {
  printBlock( type["str"], $1 )
}

function stripQuotes( str ) {
	s = gsub(/"/,"", str)
	return str	
}

function printBlock( type, name ) {
	
	if ( lines > 0 ) {
		printf ","
	}
	lines = lines + 1
    printf("%s:%s", stripQuotes(name), type)
}
