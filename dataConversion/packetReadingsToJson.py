
import re
import sys
import pickle
import json

print(sys.argv[1])

with open(sys.argv[1]) as json_file:
    data = json.load(json_file)
print(data)

template = re.compile('ax(-?\d+)ay(-?\d+)az(-?\d+)gx(-?\d+)gy(-?\d+)gz(-?\d+)')


# testData= "readingNumber:119ax:6:ay:6az:-106gx:-126gy:40gz:-71"
# index, ax, ay, az, gx, gy, gz = (template.match(testData)).group(1,2,3,4,5,6,7)
readings = template.findall(data["data"])
print(readings)

ax_array = []
ay_array = []
az_array = []
gx_array = []
gy_array = []
gz_array = []
time_array=[]

for line in readings:
    ax, ay, az, gx, gy, gz = line
    ax_array.append(int(ax))
    ay_array.append(int(ay))
    az_array.append(int(az))
    gx_array.append(int(gx))
    gy_array.append(int(gy))
    gz_array.append(int(gz))

with open('ax_arrayPacket.txt', 'w') as filehandle:
    json.dump(ax_array, filehandle)
with open('ay_arrayPacket.txt', 'w') as filehandle:
    json.dump(ay_array, filehandle)
with open('az_arrayPacket.txt', 'w') as filehandle:
    json.dump(az_array, filehandle)
with open('gx_arrayPacket.txt', 'w') as filehandle:
    json.dump(gx_array, filehandle)
with open('gy_arrayPacket.txt', 'w') as filehandle:
    json.dump(gy_array, filehandle)
with open('gz_arrayPacket.txt', 'w') as filehandle:
    json.dump(gz_array, filehandle)
with open('time_arrayPacket.txt', 'w') as filehandle:
    json.dump(time_array, filehandle)
    
