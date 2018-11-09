# hits.awk
BEGIN {
	paths["null"] = 0
}

// {
	hitCount = $2 + 0 # convert to number
	if ( index($1,".") > 0 )
	{
		paths[$1] = paths[$1] + hitCount
	}
	updatePaths( getPathFromURL($1), hitCount )
}

END {
	for ( path in paths ) 
	{
		print path "," paths[path]	
	}
}

function getPathFromURL(stringFullURL)
{
	str = ""
	n=split(stringFullURL, larray, "/" )
	for (i=1; i<=n; i++ ) 
	{
		if ( length(larray[i]) > 0 && index(larray[i],".") == 0 ) 
		{
			str = sprintf("%s/%s",str, larray[i]) 
		}
	}
	return str
}

function updatePaths(urlString, varCount) 
{
	str = ""
	n=split(urlString, larray, "/" )
	for (i=1; i<=n; i++ ) 
	{
		if ( length(larray[i]) > 0 && index(larray[i],".") == 0 ) 
		{
			str = sprintf("%s/%s",str, larray[i]) 
			paths[str] = paths[str] + varCount
		}
	}
}
