import sys
import json

fileX = "ax_array" + sys.argv[1] + ".txt"
fileY = "ay_array" + sys.argv[1] + ".txt"
fileZ = "az_array" + sys.argv[1] + ".txt"
fileT= "time_array" + sys.argv[1] + ".txt"

# print(fileX)
fx = open(fileX, 'r')
fy = open(fileY, 'r')
fz = open(fileZ, 'r')
ft = open(fileT, 'r')

ax = json.load(fx)
ay = json.load(fy)

az = json.load(fz)

at = json.load(ft)

# fx = json.load(fileX, 'r')

print(az)
total_array= []
for values in zip(ax,ay,az,at):
    total_array.append(values[0]+ values[1] + values[2])

    # total_array.append(str(values[3])+ ','+ str(values[0]+ values[1] + values[2]))
    print(values)

print(total_array)
with open('total_array'+str(sys.argv[1])+'.txt', 'w') as filehandle:
    json.dump(total_array,filehandle)
# fx= open()