
import re
import sys

print(sys.argv[1])
print("woo")
enc='cp437'
f = open(sys.argv[1], 'r', encoding=enc)


template = "readingNumber:(-?\d+)ax:(-?\d+):ay:(-?\d+)az:(-?\d+)gx:(-?\d+)gy:(-?\d+)gz:(-?\d+)"

for line in f:
    readingNumber = re.match("readingNumber:(-?\d+)")
    ax = re.match("ax:(-?\d+)")
    ay = re.match("ay:(-?\d+)")
    print(line)

# readingNumber:254ax:33:ay:38az:7gx:1375gy:-2903gz:-11405