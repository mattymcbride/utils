BEGIN { 
	FS="&" 
	mn = 0
}

// { 
	arr[0] = $1
	arr[1] = $2
	arr[2] = $3
	arr[3] = $4
	printPathFromArr( arr )
}

END {
}

# function
function printPathFromArr( arr ) {
	pathStr = ""
	for (s in arr) {
		tmp = getPathStr( arr[s] )
		if ( length(tmp) > 0 ) {
			pathStr = tmp
			break
		}
	}
	if ( length(pathStr) < 1 ) {
		pathStr = "<root folder>"
	}
	print pathStr
}

function getPathStr( str ) {
	where = match(str, /path\=/)
	if (where != 0) {
		n = split( str, a, "=" )
		return a[2]
	}
	return ""
}
