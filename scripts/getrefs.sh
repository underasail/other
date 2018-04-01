#! /bin/bash

# Search for and replace all space characters with "%20"
# Search_term: (.+)\t(\d*)\t(\d+)\t(\d+)
# Replace_term: "curl""http://www.crossref.org/openurl/?title=\1\&date=\2\&volume=\3\&spage=\4\&pid=mct30@miami.edu\&redirect=false\&format=unixref"
#JournalName	Year	Volume	StartPage
#American Naturalist     1880    14      617
curl "http://www.crossref.org/openurl/?title=American%20Naturalist&date=1880&volume=14&spage=617&pid=mct30@miami.edu&redirect=false&format=unixref"
curl "http://www.crossref.org/openurl/?title=Biol.%20Bull.&date=1928&volume=55&spage=69&pid=mct30@miami.edu&redirect=false&format=unixref"
curl "http://www.crossref.org/openurl/?title=PNAS&date=1965&volume=53&spage=187&pid=mct30@miami.edu&redirect=false&format=unixref"
curl "http://www.crossref.org/openurl/?title=Science&date=&volume=160&spage=1242&pid=mct30@miami.edu&redirect=false&format=unixref"
curl "http://www.crossref.org/openurl/?title=J%20Mar%20Biol%20Assoc%20UK&date=2005&volume=85&spage=695&pid=mct30@miami.edu&redirect=false&format=unixref"
curl "http://www.crossref.org/openurl/?title=Biochem.%20Biophys.%20Res.%20Comm.&date=1985&volume=126&spage=1259&pid=mct30@miami.edu&redirect=false&format=unixref"
curl "http://www.crossref.org/openurl/?title=Gene&date=1992&volume=111&spage=229&pid=mct30@miami.edu&redirect=false&format=unixref"
curl "http://www.crossref.org/openurl/?title=Nature%20Biotechnology&date=&volume=17&spage=969&pid=mct30@miami.edu&redirect=false&format=unixref"
curl "http://www.crossref.org/openurl/?title=Phil%20Trans%20Roy%20Soc%20B&date=1992&volume=335&spage=281&pid=mct30@miami.edu&redirect=false&format=unixref"