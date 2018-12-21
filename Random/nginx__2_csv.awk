# parse NGINX logs
BEGIN {
	print "time, sec, verb, url, return"
}

// {
	print $4 "," $5 "," stripquote($6) "," cleanurl($7) ","  $9 
}

function stripquote(str) {
	gsub(/"/, "", str)
	return str
}

function spliturl(url) {
	n = split(url,a,"?")
	r_url = a[1]

	return r_url
}

function cleanurl(url) {
	n = split(url,a,"?")
	r_url = a[1]
	curl = ""
	
	# remove segments that are just numerical	
	n = split(r_url,a,"/")
	for (i=2; i<=n; i = i + 1 ) {
		if ( match(a[i],/^[\-0-9]+$/) > 0 ) {
			curl = sprintf( "%s/[id]", curl )
		} else if ( match(a[i],/[0-9a-zA-Z]+\-[0-9a-z]+/) > 0 ) {
			curl = sprintf( "%s/[guid]", curl )
		} else if ( length(a[i]) > 12 && match(a[i],/^[0-9a-zA-Z]+$/) > 0 ) {
			curl = sprintf( "%s/[guid]", curl )
		} else {
			curl = sprintf( "%s/%s", curl, a[i] )
		}
	}

	return curl
}