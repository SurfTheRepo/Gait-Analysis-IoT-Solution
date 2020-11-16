import matplotlib.pyplot as plt
import json
import sys
f = open(sys.argv[1])
arr = json.load(f)
plt.plot(arr)
plt.show()