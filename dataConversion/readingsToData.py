
import re
import sys
import pickle
import json

print(sys.argv[1])
# print("woo")
enc='cp437'
f = open(sys.argv[1], 'r', encoding=enc)


template = re.compile('readingNumber:(-?\d+)ax:(-?\d+):ay:(-?\d+)az:(-?\d+)gx:(-?\d+)gy:(-?\d+)gz:(-?\d+)')

rNum = re.compile('readingNumber:(-?\d+)')
rax = re.compile('ax:(-?\d+)')
ray = re.compile('ay:(-?\d+)')
raz = re.compile('az:(-?\d+)')
rgx = re.compile('gx:(-?\d+)')
rgy = re.compile('gy:(-?\d+)')
rgz = re.compile('gz:(-?\d+)')

# testData= "readingNumber:119ax:6:ay:6az:-106gx:-126gy:40gz:-71"
# index, ax, ay, az, gx, gy, gz = (template.match(testData)).group(1,2,3,4,5,6,7)

ax_array = []
ay_array = []
az_array = []
gx_array = []
gy_array = []
gz_array = []
time_array=[]

for line in f:
    lineMatching = template.match(line)
    if(lineMatching):
        time, ax, ay, az, gx, gy, gz = lineMatching.group(1,2,3,4,5,6,7)
        ax_array.append(int(ax))
        ay_array.append(int(ay))
        az_array.append(int(az))
        gx_array.append(int(gx))
        gy_array.append(int(gy))
        gz_array.append(int(gz))
        time_array.append(int(time))



        # ax_array[int(index)] = int(ax)
        # ay_array[int(index)] = int(ay)
        # az_array[int(index)] = int(az)
        # gx_array[int(index)] = int(gx)
        # gy_array[int(index)] = int(gy)
        # gz_array[int(index)] = int(gz)
        
print('ax_array'+str(sys.argv[2])+'.data', 'wb')

with open('ax_array'+str(sys.argv[2])+'.txt', 'w') as filehandle:
    json.dump(ax_array, filehandle)
with open('ay_array'+str(sys.argv[2])+'.txt', 'w') as filehandle:
    json.dump(ay_array, filehandle)
with open('az_array'+str(sys.argv[2])+'.txt', 'w') as filehandle:
    json.dump(az_array, filehandle)
with open('gx_array'+str(sys.argv[2])+'.txt', 'w') as filehandle:
    json.dump(gx_array, filehandle)
with open('gy_array'+str(sys.argv[2])+'.txt', 'w') as filehandle:
    json.dump(gy_array, filehandle)
with open('gz_array'+str(sys.argv[2])+'.txt', 'w') as filehandle:
    json.dump(gz_array, filehandle)
with open('time_array'+str(sys.argv[2])+'.txt', 'w') as filehandle:
    json.dump(time_array, filehandle)
# for index in range(len(time_array)):
#     print("time:",time_array[index])
#     print("ax:",ax_array[index])
#     print("ay:", ay_array[index])
#     print("az:", az_array[index])
#     print("gx:", gx_array[index])
#     print("gy:", gy_array[index])
#     print("gz:", gz_array[index])

# # print("reading 300" + "is ax" + str(ax_array[300])+ "ay" +str(ay_array[300]))
    # ay = re.match("ay:(-?\d+)",line).group()
    # ax = re.match("ax:(-?\d+)",line).group()
    # az = re.match("az:(-?\d+)",line).group()
    # gx = re.match("gx:(-?\d+)",line).group()
    # gy = re.match("gy:(-?\d+)",line).group()
    # gz = re.match("gz:(-?\d+)",line).group()    

    # print(readingNumber)
    # print(line)

# readingNumber:254ax:33:ay:38az:7gx:1375gy:-2903gz:-11405