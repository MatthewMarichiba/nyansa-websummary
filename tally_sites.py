# x You’re given an input file.
# x Each line consists of a timestamp (unix epoch in seconds) and a url separated by ‘|’ (pipe operator). 
# x The entries are not in any chronological order.
# x TODO: Account for mixed-case domains. Convert all to lower()
# x Your task is to produce a daily summarized report on url hit count, organized daily (mm/dd/yyyy GMT) 
# x the earliest date appearing first. TODO: Accommodate ordering by YEARS
# x For each day, you should display the number of times each url is visited 
# x in the order of highest hit count to lowest count. 
# x Your program should take in one command line argument: input file name. 
# x The output should be printed to stdout. 
# o You can assume that the cardinality (i.e. number of distinct values) of hit count values and the number of days are much smaller than the number of unique URLs. 
# o You may also assume that number of unique URLs can fit in memory, but not necessarily the entire file.

# Edge case handling
# x 1. What if bad line?
# x 2. What about end of file?
# x 3. Years out of order

# Big-O thoughts:
# Compute Complexity
# Assume N is the number of lines in the file (or perhaps the unique # of URLS).
# There are nested `for` loops; the outer loop iterates over dates, and the inner loop iterates over URLs
# Worst case, every line is a different URL.
# For the inner loop, we use python's sorted() function, which claims to have O(N log(N)) or better.
# 
# We expect the cardinality of dates to be low. Even though we loop over all dates, that loop will factor much lower than O(N).
# I would expect it to act more like a constant multiplier to the loop time, and so it is probably safe to eliminate it from the O(N).
#
# Memory complexity: Python's sorted() claims to require N/2 pointers. Hopefully, since storing all N website names in memory is OK, then storing N/2 pointers will also be fine.

import time
import sys

def timestampToTuple(ts):
    t = time.gmtime(ts)
    return tuple([t.tm_year, t.tm_mon, t.tm_mday])

# Handle command-line arguments
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <filename>")
    quit()
filename = sys.argv[1]

inputFile = open(filename, mode="r")
invalidLines = 0
urlTallies = {} # A 2D dictionary of hit tallies by date by url. Ex: { (2019, 8, 1): {"www.google.com": 23}, (2019, 8, 2): {"www.google.com": 20, "www.yahoo.com": 3} }

for line in inputFile:
    try: # if anything goes wrong processing a line, toss it out
        timestamp, url = line.split("|")
        timestamp = timestamp.strip()
        
        if timestamp:
            dateTuple = timestampToTuple(int(timestamp))
            url = url.strip().lower()
 
            if not dateTuple in urlTallies:
                urlTallies[dateTuple] = {}

            if not url in urlTallies[dateTuple]:
                urlTallies[dateTuple][url] = 1
            else:
                urlTallies[dateTuple][url] += 1
    except Exception as err:
        print(f'WARNING: {err} for line "{line.strip()}"')
        invalidLines += 1

inputFile.close()

# Prints a sorted list of url:hit key-value pairs. urlHits looks like: {"google.com": 4, "yahoo.com": 1 }
def printUrls(urlHits):
    tuplesSortedByHits = sorted(urlHits.items(), key=lambda kv: kv[1], reverse=True)
    for (key, value) in tuplesSortedByHits:
        print(f"{key} {value}")

# Iterate through all dates and print the URL hits for the day
sortedDates = sorted(urlTallies.keys())
for dateTuple in sortedDates:
    print(f"{dateTuple[1]}/{dateTuple[2]}/{dateTuple[0]} GMT")
    printUrls(urlTallies[dateTuple])

if invalidLines:
    print(f"{invalidLines} input lines were skipped due to invalid formatting")
