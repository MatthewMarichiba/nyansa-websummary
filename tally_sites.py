# This script produces a daily summarized report on URL hit count for URLs in a given input file

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

# Prints a sorted list of key-value (url:hit) pairs. Ex: urlHits looks like: {"google.com": 4, "yahoo.com": 1 }
def printUrls(urlHits):
    tuplesSortedByHits = sorted(urlHits.items(), key=lambda kv: kv[1], reverse=True)
    for (key, value) in tuplesSortedByHits:
        print(f"{key} {value}")

# Iterate through all dates and print the URL hits for the day
sortedDates = sorted(urlTallies.keys())
for dateTuple in sortedDates:
    print(f"{str(dateTuple[1]).zfill(2)}/{str(dateTuple[2]).zfill(2)}/{dateTuple[0]} GMT") # Ex: "08/20/2012 GMT"
    printUrls(urlTallies[dateTuple])

if invalidLines:
    print(f"{invalidLines} input lines were skipped due to invalid formatting")
